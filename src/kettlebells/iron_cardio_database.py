import json
import sys
from collections import deque
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from .console import console
from .constants import DATE_FORMAT


def initialize_database(iron_cardio_home: Path, db_path: Path, force: bool) -> None:
    """Creates the home directory and the JSON database.
    :param iron_cardio_home: The home directory for the Iron Cardio database.
    :param db_path: The Path to the database.
    :param force: If True, overwrites the existing database with a blank one.
    :returns: None
    """
    if iron_cardio_home.is_dir() and force:
        pass
    elif db_path.is_file():
        console.print(
            "[yellow] Database base already exits. Run 'iron-cardio init --force' to overwrite database."
        )
        return
    try:
        iron_cardio_home.mkdir()
    except FileExistsError:
        pass
    data = {"loads": dict(), "saved_sessions": [], "cached_sessions": []}
    write_database(db_path, data)


def read_database(db_path: Path) -> json:
    """Read from the data base.
    :param db_path: The Path to the database.
    :returns: A json object of the data.
    """
    if not db_path.is_file():
        console.print("[red]:warning: Could not find Iron Cardio database.")
        console.print(
            "[yellow] Try running [underline]iron-cardio init[/underline] first."
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
        console.print("[red]:warning: Could not find loads in database.")
        console.print(
            "[yellow] Try running [underline]iron-cardio setloads[/underline] first."
        )
        sys.exit()


def cache_session(db_path: Path, session) -> None:
    """Cache last 10 generated sessions.
    :param db_path: The Path to the database.
    :param session: Session object to be stored in the cache.
    :returns: None
    """
    data = read_database(db_path)
    cache = deque(data["cached_sessions"], maxlen=10)
    cache.append(asdict(session))
    data["cached_sessions"] = list(cache)
    write_database(db_path, data)


def save_session(db_path: Path, session_date: str, session) -> None:
    """Save a session in the database.
    :param db_path: The Path to the database.
    :param session_date: The date of the workout.
    :param session: Session object to be stored in the database.
    :returns: None
    """
    data = read_database(db_path)
    data["saved_sessions"].append({"date": session_date, "session": asdict(session)})
    data["saved_sessions"] = sorted(
        data["saved_sessions"], key=lambda x: datetime.strptime(x["date"], DATE_FORMAT)
    )
    write_database(db_path, data)
