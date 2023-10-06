import json
from dataclasses import asdict
from pathlib import Path

import pytest

import kettlebells.database as db

from .test_constants import (
    TEST_CACHE_SESSION,
    TEST_DATA,
    TEST_DATA_FULL_CACHE,
    TEST_SESSION,
)


def test_initialize_database(database_home):
    expected = {"loads": dict(), "saved_workouts": [], "cached_workouts": []}
    db.initialize_database(database_home.parents[0], database_home, False)
    assert database_home.is_file()
    assert json.load(open(database_home)) == expected


def test_initialize_database_already_existes(database, capfd):
    db.initialize_database(
        Path(database.name).parents[0], Path(database.name), False
    )
    output = capfd.readouterr()[0]
    assert "Database base already exits." in output


def test_initialize_database_force(database):
    expected = {"loads": dict(), "saved_workouts": [], "cached_workouts": []}
    db.initialize_database(Path(database.name).parents[0], Path(database.name), True)
    assert Path(database.name).is_file()
    assert json.load(open(database.name)) == expected


def test_read_no_database(database_home, capfd):
    with pytest.raises(SystemExit):
        db.read_database(database_home)
    output = capfd.readouterr()[0]
    assert "Could not find kettlebells database." in output


def test_confirm_loads(database_home, capfd):
    db.initialize_database(database_home.parents[0], database_home, False)
    with pytest.raises(SystemExit):
        db.confirm_loads(database_home)
    output = capfd.readouterr()[0]
    assert "Could not find loads in database." in output


def test_write_database(database):
    db.write_database(database.name, TEST_DATA)
    actual = json.load(open(database.name))
    assert actual == TEST_DATA


def test_read_database(database):
    data = db.read_database(Path(database.name))
    assert data == TEST_DATA_FULL_CACHE


def test_save_session(database):
    db.save_workout(Path(database.name), "2023-09-14", TEST_SESSION)
    data = json.load(open(database.name))
    assert data["saved_workouts"][-1] == {
        "date": "2023-09-14",
        "session": {
            "bodyweight": 90,
            "bells": "Double Bells",
            "variation": "Double Classic + Pullup",
            "time": 30,
            "load": 28,
            "units": "kilograms",
            "swings": 60,
            "sets": 20,
            "reps": 3,
            "workout_type": "iron cardio",
        },
    }


def test_cache_session(database):
    db.cache_workout(Path(database.name), TEST_CACHE_SESSION)
    data = json.load(open(database.name))
    assert len(data["cached_workouts"]) == 10
    assert data["cached_workouts"][-1] == asdict(TEST_CACHE_SESSION)
