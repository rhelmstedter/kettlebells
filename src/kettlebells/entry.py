"""Parse the quick-entry text format.

One workout per entry, segments separated by semicolons:

    ES D11 16min; SGD 2x5@185lb; Chin 2x5+25lb; Dip 3x3+45lb (elbow hurts); AW 1x10; note: HARD!

* The first segment is the header: a workout type (a code such as ``es`` or a name),
  an optional variation (``D11``, ``W2D3``, ``07``, ...) and the duration (``16min``).
  If the variation is left out, the last variation of that workout type is bumped.
* Each exercise segment is ``<name> <sets>x<reps>``, optionally followed by a load:
  ``@32``, ``@185lb``, ``@24kg`` or ``+25lb``. A load without a unit uses the
  database units. For bodyweight exercises (chinups, dips, ...) the load is the added
  weight, so ``@25lb`` and ``+25lb`` mean the same thing.
* Text in parentheses after an exercise, and segments starting with ``note:`` or ``#``,
  are kept as the workout notes.

A file holds one ``YYYY-MM-DD <entry>`` per line. Blank lines and lines starting with
``#`` are ignored.
"""

import re
from datetime import datetime

from .constants import BODYWEIGHT_FACTORS, DATE_FORMAT, POUNDS_TO_KILOS_RATE
from .names import bump_variation, resolve_exercise, resolve_workout_type

SPEC_RE = re.compile(
    r"^(?P<sets>\d+)\s*[x×]\s*(?P<reps>\d+)"
    r"(?:\s*(?:(?P<sign>[@+])\s*(?P<load>\d+(?:\.\d+)?)\s*(?P<unit>kgs?|lbs?)?|@\s*bw))?$",
    re.IGNORECASE,
)
EXERCISE_RE = re.compile(
    r"^(?P<name>.+?)\s+(?P<spec>\d+\s*[x×]\s*\d+.*?)\s*(?:\((?P<note>[^)]*)\))?$",
    re.IGNORECASE,
)
TIME_RE = re.compile(r"\b(\d+)\s*(?:min|mins|minutes|m)\b", re.IGNORECASE)
VARIATION_RE = re.compile(r"^(?:(?:[wd]\d+)+|\d+)$", re.IGNORECASE)


class EntryError(ValueError):
    """A quick-entry string could not be parsed."""


def convert_load(load: float, unit: str | None, units: str) -> int:
    """Convert a load to the database units and round it to a whole number."""
    unit = (unit or units).lower().rstrip("s")
    target = units.lower().rstrip("s")
    if unit == "lb" and target == "kg":
        load *= POUNDS_TO_KILOS_RATE
    elif unit == "kg" and target == "lb":
        load /= POUNDS_TO_KILOS_RATE
    return int(round(load))


def parse_spec(text: str, units: str) -> tuple[int, int, int]:
    """Parse ``3x5``, ``3x5@24``, ``2x5@185lb`` or ``3x3+20`` into (sets, reps, load)."""
    match = SPEC_RE.match(text.strip())
    if not match:
        raise EntryError(f"'{text}' should look like 3x5, 3x5@24, 2x5@185lb or 3x3+20.")
    load = 0
    if match["load"]:
        load = convert_load(float(match["load"]), match["unit"], units)
    return int(match["sets"]), int(match["reps"]), load


def format_spec(name: str, sets: int, reps: int, load: int) -> str:
    """The inverse of parse_spec, in database units."""
    spec = f"{sets}x{reps}"
    if load:
        spec += f"+{load}" if name in BODYWEIGHT_FACTORS else f"@{load}"
    return spec


def _parse_header(header: str, data: dict) -> tuple[str, str, int]:
    time_match = TIME_RE.search(header)
    if not time_match:
        raise EntryError(f"'{header}' needs a duration, e.g. '16min'.")
    time = int(time_match.group(1))
    words = (header[: time_match.start()] + header[time_match.end() :]).split()
    variation = ""
    if len(words) > 1 and VARIATION_RE.match(words[-1]):
        variation = words.pop().upper()
    if not words:
        raise EntryError(f"'{header}' needs a workout type, e.g. 'ES' or 'iron cardio'.")
    workout_type = resolve_workout_type(" ".join(words), data)
    if not variation:
        previous = [
            w["workout"]["variation"]
            for w in data.get("saved_workouts", [])
            if w["workout"]["workout_type"].casefold() == workout_type.casefold()
        ]
        variation = bump_variation(previous[-1]) if previous else "Custom"
    return workout_type, variation, time


def parse_entry(text: str, data: dict) -> dict:
    """Parse one quick-entry string into the fields of a Workout.

    Raises:
        EntryError: If any part of the entry can't be understood.
    """
    segments = [s.strip() for s in text.split(";") if s.strip()]
    if not segments:
        raise EntryError("The entry is empty.")
    units = data["loads"]["units"]
    workout_type, variation, time = _parse_header(segments[0], data)
    exercises = []
    notes = []
    for segment in segments[1:]:
        note = re.match(r"^(?:notes?:|#)\s*(.*)$", segment, re.IGNORECASE)
        if note:
            notes.append(note.group(1))
            continue
        match = EXERCISE_RE.match(segment)
        if not match:
            raise EntryError(f"'{segment}' should look like 'SGD 2x5@185lb'.")
        try:
            name = resolve_exercise(match["name"], data)
        except ValueError as error:
            raise EntryError(str(error)) from error
        sets, reps, load = parse_spec(match["spec"], units)
        exercises.append({"name": name, "sets": sets, "reps": reps, "load": load})
        if match["note"]:
            notes.append(f"{name}: {match['note'].strip()}")
    if not exercises:
        raise EntryError("The entry has no exercises.")
    return {
        "workout_type": workout_type,
        "variation": variation,
        "time": time,
        "units": units,
        "bodyweight": data["loads"]["bodyweight"],
        "exercises": exercises,
        "notes": "; ".join(notes),
    }


def parse_lines(lines: list[str], data: dict) -> list[tuple[str, dict]]:
    """Parse ``YYYY-MM-DD <entry>`` lines.

    Each workout is added to a copy of the saved workouts as it's parsed, so a file of
    consecutive days without variations counts D11, D12, D13...

    Raises:
        EntryError: Naming the line that failed.
    """
    data = dict(data, saved_workouts=list(data.get("saved_workouts", [])))
    parsed = []
    for number, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        date, _, entry = line.partition(" ")
        try:
            datetime.strptime(date, DATE_FORMAT)
        except ValueError:
            raise EntryError(f"Line {number}: '{date}' is not a YYYY-MM-DD date.") from None
        try:
            workout = parse_entry(entry, data)
        except EntryError as error:
            raise EntryError(f"Line {number}: {error}") from None
        parsed.append((date, workout))
        data["saved_workouts"].append({"date": date, "workout": workout})
    return parsed
