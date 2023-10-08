import json
import sys
from collections import deque
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from .console import console
from .constants import DATE_FORMAT, SUGGESTION, WARNING


def initialize_database(kettlebells_home: Path, db_path: Path, force: bool) -> None:
    """Creates the home directory and the JSON database.
    :param kettlebells_home: The home directory for the kettlebells database.
    :param db_path: The Path to the database.
    :param force: If True, overwrites the existing database with a blank one.
    :returns: None
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
    data = {"loads": dict(), "saved_workouts": [], "cached_workouts": []}
    write_database(db_path, data)


def read_database(db_path: Path) -> json:
    """Read from the data base.
    :param db_path: The Path to the database.
    :returns: A json object of the data.
    """
    if not db_path.is_file():
        console.print(":warning: Could not find kettlebells database.", style=WARNING)
        console.print(
            "Try running [underline]kettlebells init[/underline] first.",
            style=SUGGESTION,
        )
        sys.exit()
    with open(db_path) as db:
        return json.load(db)


def write_database(db_path: Path, data: dict) -> None:
    """Write data to database.
    :param db_path: The Path to the database.
    :param data: The new version of the database to write.
    :returns: None
    """
    with open(db_path, "w") as db:
        json.dump(data, db)


def confirm_loads(db_path: Path) -> None:
    """Checks if the loads have been set in the database.
    :param db_path: The Path to the database.
    :returns: None
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
    :param db_path: The Path to the database.
    :param workout: Workout object to be stored in the cache.
    :returns: None
    """
    data = read_database(db_path)
    cache = deque(data["cached_workouts"], maxlen=1)
    cache.append(asdict(workout))
    data["cached_workouts"] = list(cache)
    write_database(db_path, data)


def save_workout(db_path: Path, workout_date: str, workout) -> None:
    """Save a workout in the database.
    :param db_path: The Path to the database.
    :param workout_date: The date of the workout.
     n:param workout: Workout object to be stored in the database.
    :returns: None
    """
    data = read_database(db_path)
    data["saved_workouts"].append({"date": workout_date, "workout": asdict(workout)})
    data["saved_workouts"] = sorted(
        data["saved_workouts"], key=lambda x: datetime.strptime(x["date"], DATE_FORMAT)
    )
    write_database(db_path, data)
