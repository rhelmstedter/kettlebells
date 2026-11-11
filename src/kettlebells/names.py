"""Normalize and resolve workout type and exercise names."""

import re
from collections import Counter

from .constants import (
    DEFAULT_EXERCISE_ALIASES,
    EXERCISE_NAME_FIXES,
    EXERCISES,
    WORKOUT_TYPE_FIXES,
    WORKOUT_TYPE_NAMES,
)


def _clean(name: str) -> str:
    return re.sub(r"\s+", " ", name).strip()


def normalize_exercise_name(name: str) -> str:
    """Fix spacing, known misspellings and the casing of "TRX" in an exercise name."""
    name = _clean(name)
    name = EXERCISE_NAME_FIXES.get(name.lower(), name)
    return re.sub(r"\btrx\b", "TRX", name, flags=re.IGNORECASE)


def normalize_workout_type(name: str, data: dict | None = None) -> str:
    """Return the canonical spelling of a workout type.

    Built-in program names win, then the most common existing spelling in the
    database (compared case-insensitively), then the name as typed.
    """
    name = _clean(name)
    name = WORKOUT_TYPE_FIXES.get(name.lower(), name)
    key = name.casefold()
    for builtin in WORKOUT_TYPE_NAMES.values():
        if builtin.casefold() == key:
            return builtin
    if data:
        existing = Counter(
            w["workout"]["workout_type"]
            for w in data.get("saved_workouts", [])
            if w["workout"]["workout_type"].casefold() == key
        )
        if existing:
            return existing.most_common(1)[0][0]
    return name


def known_exercises(data: dict) -> dict[str, str]:
    """Map the casefolded name of every known exercise to its spelling."""
    names = list(EXERCISES) + list(data.get("exercises", {}))
    for workout in data.get("saved_workouts", []):
        names.extend(e["name"] for e in workout["workout"]["exercises"])
    return {n.casefold(): n for n in names if n not in ("Done", "Other")}


def exercise_aliases(data: dict) -> dict[str, str]:
    """Default exercise aliases merged with the user's own (which win)."""
    user = {k.casefold(): v for k, v in data.get("aliases", {}).get("exercises", {}).items()}
    return DEFAULT_EXERCISE_ALIASES | user


def workout_type_aliases(data: dict) -> dict[str, str]:
    """Built-in workout type codes merged with the user's own (which win)."""
    user = {k.casefold(): v for k, v in data.get("aliases", {}).get("workout_types", {}).items()}
    return WORKOUT_TYPE_NAMES | user


def resolve_exercise(name: str, data: dict) -> str:
    """Turn a short or loosely typed exercise name into the stored name.

    Raises:
        ValueError: If the name is not an alias or a known exercise.
    """
    cleaned = _clean(name)
    aliases = exercise_aliases(data)
    if cleaned.casefold() in aliases:
        return aliases[cleaned.casefold()]
    known = known_exercises(data)
    normalized = normalize_exercise_name(cleaned)
    for candidate in (cleaned, normalized):
        if candidate.casefold() in known:
            return normalize_exercise_name(known[candidate.casefold()])
    raise ValueError(
        f"Unknown exercise '{cleaned}'. Use the full name, or add a short name with "
        f'kettlebells alias {cleaned} "Full Exercise Name".'
    )


def resolve_workout_type(name: str, data: dict) -> str:
    """Turn a workout type code (es, ic, ...) or name into the stored name."""
    aliases = workout_type_aliases(data)
    cleaned = _clean(name)
    if cleaned.casefold() in aliases:
        return aliases[cleaned.casefold()]
    return normalize_workout_type(cleaned, data)


def bump_variation(variation: str) -> str:
    """Increase the last number in a variation, keeping its zero padding.

    Examples: "D10" -> "D11", "09" -> "10", "W2D3" -> "W2D4". A variation with no
    number is returned unchanged.
    """
    matches = list(re.finditer(r"\d+", variation))
    if not matches:
        return variation
    last = matches[-1]
    number = str(int(last.group()) + 1).zfill(len(last.group()))
    return variation[: last.start()] + number + variation[last.end() :]
