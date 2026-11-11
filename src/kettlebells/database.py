import json
import shutil
import sys
from collections import deque
from datetime import datetime
from pathlib import Path

from rich.console import Console

from .console import console
from .constants import (
    BODYWEIGHT_FACTORS,
    DATE_FORMAT,
    EXERCISES,
    SCHEMA_VERSION,
    SUGGESTION,
    WARNING,
)
from .names import normalize_exercise_name, normalize_workout_type

err_console = Console(stderr=True)


def initialize_database(kettlebells_home: Path, db_path: Path, force: bool) -> None:
    """Creates the home directory and the JSON database.

    Args:
        kettlebells_home: The home directory for the kettlebells database.
        db_path: The Path to the database.
        force: If True, overwrites the existing database with a blank one.

    """
    if kettlebells_home.is_dir() and force:
        pass
    elif db_path.is_file():
        console.print(":warning: Database base already exits.", style=WARNING)
        console.print(
            "Run [underline]kettlebells init --force[/underline] to overwrite database.",
            style=SUGGESTION,
        )
        return
    try:
        kettlebells_home.mkdir()
    except FileExistsError:
        pass
    data: dict = {
        "schema_version": SCHEMA_VERSION,
        "loads": dict(),
        "templates": dict(),
        "aliases": {"exercises": {}, "workout_types": {}},
        "exercises": EXERCISES,
        "saved_workouts": [],
        "cached_workouts": [],
    }
    write_database(db_path, data)


def update_database(db_path: Path) -> None:
    """Update the database with new exercises.

    Args:
        db_path: The Path to the database.
        data: The new version of the database to write.

    """
    data = read_database(db_path)
    exercises = data.get("exercises")
    if exercises:
        data["exercises"] = exercises | EXERCISES
    else:
        data["exercises"] = EXERCISES
    write_database(db_path, data)


def read_database(db_path: Path) -> dict:
    """Read from the data base.

    Args:
        db_path: The Path to the database.

    Returns:
        A json object of the data.

    """
    if not db_path.is_file():
        console.print(":warning: Could not find kettlebells database.", style=WARNING)
        console.print(
            "Try running [underline]kettlebells init[/underline] first.",
            style=SUGGESTION,
        )
        sys.exit()
    with open(db_path) as db:
        data = json.load(db)
    if data.get("schema_version", 1) < SCHEMA_VERSION:
        data = _upgrade_database(db_path, data)
    return data


def write_database(db_path: Path, data: dict) -> None:
    """Write data to database.
    :param db_path: The Path to the database.
    :param data: The new version of the database to write.
    :returns: None
    """
    with open(db_path, "w") as db:
        json.dump(data, db, indent=4)


def confirm_loads(db_path: Path) -> None:
    """Checks if the loads have been set in the database.

    Args:
        db_path: The Path to the database.

    """
    data = read_database(db_path)
    if not data["loads"]:
        console.print("[red]:warning: Could not find loads in database.", style=WARNING)
        console.print(
            "Try running [underline]iron-cardio setloads[/underline] first.",
            style=SUGGESTION,
        )
        sys.exit()


def cache_workout(db_path: Path, workout) -> None:
    """Cache last 10 generated workout.

    Args:
        db_path: The Path to the database.
        workout: Workout object to be stored in the cache.

    """
    data = read_database(db_path)
    cache = deque(data["cached_workouts"], maxlen=1)
    cache.append(workout.model_dump())
    data["cached_workouts"] = list(cache)
    write_database(db_path, data)


def save_workout(db_path: Path, workout_date: str, workout) -> None:
    """Save a workout in the database.

    Args:
        db_path: The Path to the database.
        workout_date: The date of the workout.
        workout: Workout object to be stored in the database.

    """
    save_workouts(db_path, [(workout_date, workout)])


def save_workouts(db_path: Path, workouts: list[tuple[str, object]]) -> None:
    """Save several (date, workout) pairs in one write, normalizing their names."""
    data = read_database(db_path)
    for workout_date, workout in workouts:
        data["saved_workouts"].append(
            {"date": workout_date, "workout": normalize_workout(workout.model_dump(), data)}
        )
    _sort_saved(data)
    write_database(db_path, data)


def replace_workout(db_path: Path, index: int, workout_date: str, workout) -> None:
    """Replace the saved workout at index."""
    data = read_database(db_path)
    data["saved_workouts"][index] = {
        "date": workout_date,
        "workout": normalize_workout(workout.model_dump(), data),
    }
    _sort_saved(data)
    write_database(db_path, data)


def delete_workout(db_path: Path, index: int) -> dict:
    """Delete the saved workout at index, after backing up the database.

    Returns:
        The deleted entry.
    """
    data = read_database(db_path)
    backup_database(db_path, "pre-delete")
    removed = data["saved_workouts"].pop(index)
    write_database(db_path, data)
    return removed


def _sort_saved(data: dict) -> None:
    data["saved_workouts"] = sorted(
        data["saved_workouts"], key=lambda x: datetime.strptime(x["date"], DATE_FORMAT)
    )


def backup_database(db_path: Path, label: str) -> Path:
    """Copy the database next to itself with a timestamped name."""
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = db_path.with_name(f"{db_path.name}.{label}-{stamp}.bak")
    shutil.copy2(db_path, backup)
    return backup


def normalize_workout(workout: dict, data: dict) -> dict:
    """Normalize the workout type and exercise names of a workout dict."""
    workout["workout_type"] = normalize_workout_type(workout["workout_type"], data)
    for exercise in workout["exercises"]:
        exercise["name"] = normalize_exercise_name(exercise["name"])
    return workout


def bodyweight_share(name: str, bodyweight: int | float) -> int:
    """The part of a bodyweight exercise's load that comes from bodyweight."""
    return int(BODYWEIGHT_FACTORS.get(name, 0) * bodyweight)


def migrate_data(data: dict) -> tuple[dict, dict]:
    """Bring a database dict up to SCHEMA_VERSION.

    Version 1 -> 2:
      * Bodyweight exercises store only the added weight. The bodyweight share is
        int(factor * bodyweight), which is what earlier versions added, so the total
        load of every past workout is unchanged. Loads that were saved without the
        bodyweight share (they come out negative) are set to 0 added weight.
      * Workout types and exercise names are normalized, so near-duplicates
        ("easy strength" / "Easy Strength") are grouped together.
      * Templates use the {"exercises": [...]} layout with added weight only.

    Returns:
        The migrated data and a report of what changed.
    """
    report = {"bodyweight loads": 0, "clamped": [], "workout types": {}, "exercise names": {}}
    if data.get("schema_version", 1) >= 2:
        return data, report

    def to_added(exercise: dict, bodyweight: int, where: str) -> None:
        if exercise["name"] not in BODYWEIGHT_FACTORS:
            return
        added = exercise["load"] - bodyweight_share(exercise["name"], bodyweight)
        if added < 0:
            report["clamped"].append(f"{where} {exercise['name']} (was {exercise['load']})")
            added = 0
        exercise["load"] = added
        report["bodyweight loads"] += 1

    for entry in data.get("saved_workouts", []):
        workout = entry["workout"]
        for exercise in workout["exercises"]:
            to_added(exercise, workout["bodyweight"], entry["date"])
    for workout in data.get("cached_workouts", []):
        for exercise in workout["exercises"]:
            to_added(exercise, workout["bodyweight"], "cached workout")

    # Templates created by `kettlebells template` were saved as a bare list with the
    # bodyweight share included; hand-written ones use {"exercises": [...]} without it.
    bodyweight = data.get("loads", {}).get("bodyweight", 0)
    for workout_type, variations in data.get("templates", {}).items():
        for variation, template in variations.items():
            if isinstance(template, list):
                for exercise in template:
                    to_added(exercise, bodyweight, f"template {workout_type}/{variation}")
                variations[variation] = {"exercises": template}

    # Workout types: build one canonical spelling per case-insensitive group first, so
    # the choice doesn't depend on the order workouts are rewritten in.
    canonical = {
        old: normalize_workout_type(old, data)
        for old in {e["workout"]["workout_type"] for e in data.get("saved_workouts", [])}
    }
    for entry in data.get("saved_workouts", []):
        old = entry["workout"]["workout_type"]
        if canonical[old] != old:
            report["workout types"][old] = canonical[old]
            entry["workout"]["workout_type"] = canonical[old]
    for workout in [e["workout"] for e in data.get("saved_workouts", [])] + data.get(
        "cached_workouts", []
    ):
        for exercise in workout["exercises"]:
            new = normalize_exercise_name(exercise["name"])
            if new != exercise["name"]:
                report["exercise names"][exercise["name"]] = new
                exercise["name"] = new
    for variations in data.get("templates", {}).values():
        for template in variations.values():
            for exercise in template["exercises"]:
                exercise["name"] = normalize_exercise_name(exercise["name"])

    exercises: dict = {}
    for name, movements in (data.get("exercises") or {}).items():
        merged = exercises.setdefault(normalize_exercise_name(name), [])
        merged.extend(m for m in movements if m not in merged)
    data["exercises"] = exercises | {k: v for k, v in EXERCISES.items() if k not in exercises}

    data.setdefault("templates", {})
    data.setdefault("aliases", {})
    data["aliases"].setdefault("exercises", {})
    data["aliases"].setdefault("workout_types", {})
    data["schema_version"] = 2
    return data, report


def _upgrade_database(db_path: Path, data: dict) -> dict:
    """Back up and migrate an old database, then tell the user what changed."""
    backup = backup_database(db_path, "pre-v2")
    data, report = migrate_data(data)
    write_database(db_path, data)
    err_console.print(f"Upgraded the kettlebells database. Backup: {backup}", style=SUGGESTION)
    err_console.print(
        f"  {report['bodyweight loads']} bodyweight exercise loads now store added weight only.",
        style=SUGGESTION,
    )
    if report["clamped"]:
        err_console.print(
            f"  {len(report['clamped'])} were saved without bodyweight and now count it: "
            + ", ".join(report["clamped"]),
            style=SUGGESTION,
        )
    for old, new in sorted(report["workout types"].items()):
        err_console.print(f"  Workout type '{old}' -> '{new}'", style=SUGGESTION)
    for old, new in sorted(report["exercise names"].items()):
        err_console.print(f"  Exercise '{old}' -> '{new}'", style=SUGGESTION)
    return data
