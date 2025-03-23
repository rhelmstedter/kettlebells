import json
from pathlib import Path
from unittest import mock

import pytest

import kettlebells.database as db
from kettlebells.constants import EXERCISES

from .test_constants import TEST_DATA, TEST_IC_WORKOUT, TEST_NEW_EXERCISES


def test_initialize_database(database_home):
    expected = {
        "loads": dict(),
        "templates": dict(),
        "exercises": EXERCISES,
        "saved_workouts": [],
        "cached_workouts": [],
    }
    db.initialize_database(database_home.parents[0], database_home, False)
    assert database_home.is_file()
    assert json.load(open(database_home)) == expected


def test_initialize_database_already_existes(database, capfd):
    db.initialize_database(Path(database.name).parents[0], Path(database.name), False)
    output = capfd.readouterr()[0]
    assert "Database base already exits." in output


def test_initialize_database_force(database):
    expected = {
        "loads": dict(),
        "templates": dict(),
        "exercises": EXERCISES,
        "saved_workouts": [],
        "cached_workouts": [],
    }
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
    assert data == TEST_DATA


def test_save_workout(database):
    db.save_workout(Path(database.name), "2023-09-14", TEST_IC_WORKOUT)
    data = json.load(open(database.name))
    assert data["saved_workouts"][-1] == {
        "date": "2023-09-14",
        "workout": {
            "bodyweight": 90,
            "units": "kg",
            "variation": "Double Classic + Pullup",
            "time": 30,
            "exercises": [
                {
                    "name": "Double Kettlebell Clean",
                    "load": 28,
                    "sets": 20,
                    "reps": 1,
                },
                {
                    "name": "Double Kettlebell Press",
                    "load": 28,
                    "sets": 20,
                    "reps": 1,
                },
                {
                    "name": "Double Kettlebell Front Squat",
                    "load": 28,
                    "sets": 20,
                    "reps": 1,
                },
                {
                    "name": "Pullup",
                    "load": 86,
                    "sets": 20,
                    "reps": 1,
                },
                {
                    "name": "Kettlebell Swing",
                    "load": 28,
                    "sets": 1,
                    "reps": 60,
                },
            ],
            "workout_type": "iron cardio",
        },
    }


def test_cache_workout(database):
    db.cache_workout(Path(database.name), TEST_IC_WORKOUT)
    data = json.load(open(database.name))
    assert len(data["cached_workouts"]) == 1
    assert data["cached_workouts"][-1] == TEST_IC_WORKOUT.model_dump()


@mock.patch("kettlebells.database.EXERCISES", TEST_NEW_EXERCISES)
def test_update_database(database):
    db.update_database(Path(database.name))
    data = json.load(open(database.name))
    expected = {
        "Kettlebell Press": ["push"],
        "Goblet Squat": ["squat"],
    } | TEST_NEW_EXERCISES
    assert data["exercises"] == expected
