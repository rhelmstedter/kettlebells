import json
from pathlib import Path
from unittest import mock

import pytest

import kettlebells.database as db
from kettlebells.constants import EXERCISES

from .test_constants import TEST_DATA, TEST_IC_WORKOUT, TEST_NEW_EXERCISES


def test_initialize_database(database_home):
    expected = {
        "schema_version": 2,
        "loads": dict(),
        "templates": dict(),
        "aliases": {"exercises": {}, "workout_types": {}},
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
        "schema_version": 2,
        "loads": dict(),
        "templates": dict(),
        "aliases": {"exercises": {}, "workout_types": {}},
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
                    "load": 0,
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
            "notes": "",
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


V1_DATA = {
    "loads": {"units": "kg", "bodyweight": 85},
    "templates": {
        "easy strength": {
            "regular": {"exercises": [{"name": "Dip", "sets": 3, "reps": 3, "load": 20}]},
            # Made by the old `kettlebells template`, with the bodyweight share included.
            "cli": [{"name": "Chinup", "sets": 3, "reps": 3, "load": 92}],
        }
    },
    "exercises": {"Overhead Tricep Extention": ["upper body isolation"]},
    "saved_workouts": [
        {
            "date": "2026-01-01",
            "workout": {
                "workout_type": "Easy Strength",
                "variation": "D1",
                "time": 20,
                "units": "kg",
                "bodyweight": 86,
                "exercises": [
                    {"name": "Chinup", "load": 93, "sets": 3, "reps": 3},
                    {"name": "Dip", "load": 82, "sets": 3, "reps": 3},
                    {"name": "Trx Tricep Extension", "load": 0, "sets": 2, "reps": 10},
                ],
            },
        },
        {
            "date": "2026-01-02",
            "workout": {
                "workout_type": "easy strength",
                "variation": "D2",
                "time": 20,
                "units": "kg",
                "bodyweight": 86,
                "exercises": [{"name": "TRX Row", "load": 0, "sets": 1, "reps": 5}],
            },
        },
    ],
    "cached_workouts": [],
}


def test_migrate_data_keeps_totals():
    from kettlebells.workouts import Workout

    data, report = db.migrate_data(json.loads(json.dumps(V1_DATA)))
    first = data["saved_workouts"][0]["workout"]
    assert [e["load"] for e in first["exercises"]] == [11, 0, 0]
    # The total load is what it was before: 93 = 11 + int(0.96 * 86).
    assert Workout(**first).exercises[0].total_load(86) == 93
    assert first["workout_type"] == "easy strength"
    assert first["exercises"][2]["name"] == "TRX Tricep Extension"
    # TRX Row was saved without bodyweight; it now counts it.
    assert data["saved_workouts"][1]["workout"]["exercises"][0]["load"] == 0
    assert len(report["clamped"]) == 1
    assert data["templates"]["easy strength"]["cli"] == {
        "exercises": [{"name": "Chinup", "sets": 3, "reps": 3, "load": 11}]
    }
    assert data["templates"]["easy strength"]["regular"]["exercises"][0]["load"] == 20
    assert "Overhead Tricep Extension" in data["exercises"]
    assert "Overhead Tricep Extention" not in data["exercises"]
    assert data["schema_version"] == 2
    # Running it again changes nothing.
    again, _ = db.migrate_data(json.loads(json.dumps(data)))
    assert again == data


def test_read_database_upgrades_and_backs_up(tmp_path):
    path = tmp_path / "db.json"
    path.write_text(json.dumps(V1_DATA))
    data = db.read_database(path)
    assert data["schema_version"] == 2
    assert json.load(open(path))["schema_version"] == 2
    backups = list(tmp_path.glob("db.json.pre-v2-*.bak"))
    assert len(backups) == 1
    assert json.load(open(backups[0])) == V1_DATA


def test_save_workout_normalizes_names(database):
    from kettlebells.workouts import Exercise, Workout

    workout = Workout(
        workout_type="Easy Strength",
        variation="D3",
        time=10,
        units="kg",
        bodyweight=90,
        exercises=[Exercise(name="Trx Tricep Extension", load=0, sets=1, reps=10)],
    )
    db.save_workout(Path(database.name), "2023-09-15", workout)
    saved = json.load(open(database.name))["saved_workouts"][-1]["workout"]
    assert saved["workout_type"] == "easy strength"
    assert saved["exercises"][0]["name"] == "TRX Tricep Extension"


def test_delete_and_replace_workout(database):
    from kettlebells.workouts import Workout

    path = Path(database.name)
    first = json.load(open(path))["saved_workouts"][0]
    db.replace_workout(path, 0, "2023-09-20", Workout(**first["workout"]))
    data = json.load(open(path))
    assert [w["date"] for w in data["saved_workouts"]] == ["2023-09-14", "2023-09-20"]
    removed = db.delete_workout(path, 1)
    assert removed["date"] == "2023-09-20"
    assert len(json.load(open(path))["saved_workouts"]) == 1
    assert list(path.parent.glob(path.name + ".pre-delete-*.bak"))
