import json
from dataclasses import asdict
from pathlib import Path

import pytest

import iron_cardio.iron_cardio_database as ic_db

from .test_constants import (
    TEST_CACHE_SESSION,
    TEST_DATA,
    TEST_DATA_FULL_CACHE,
    TEST_SESSION,
)


def test_initialize_database(database_home):
    expected = {"loads": dict(), "saved_sessions": [], "cached_sessions": []}
    ic_db.initialize_database(database_home.parents[0], database_home, False)
    assert database_home.is_file()
    assert json.load(open(database_home)) == expected


def test_initialize_database_already_existes(database, capfd):
    ic_db.initialize_database(
        Path(database.name).parents[0], Path(database.name), False
    )
    output = capfd.readouterr()[0]
    assert "Database base already exits." in output


def test_initialize_database_force(database):
    expected = {"loads": dict(), "saved_sessions": [], "cached_sessions": []}
    ic_db.initialize_database(Path(database.name).parents[0], Path(database.name), True)
    assert Path(database.name).is_file()
    assert json.load(open(database.name)) == expected


def test_read_no_database(database_home, capfd):
    with pytest.raises(SystemExit):
        ic_db.read_database(database_home)
    output = capfd.readouterr()[0]
    assert "Could not find Iron Cardio database." in output


def test_confirm_loads(database_home, capfd):
    ic_db.initialize_database(database_home.parents[0], database_home, False)
    with pytest.raises(SystemExit):
        ic_db.confirm_loads(database_home)
    output = capfd.readouterr()[0]
    assert "Could not find loads in database." in output


def test_write_database(database):
    ic_db.write_database(database.name, TEST_DATA)
    actual = json.load(open(database.name))
    assert actual == TEST_DATA


def test_read_database(database):
    data = ic_db.read_database(Path(database.name))
    assert data == TEST_DATA_FULL_CACHE


def test_save_session(database):
    ic_db.save_session(Path(database.name), "2023-09-14", TEST_SESSION)
    data = json.load(open(database.name))
    assert data["saved_sessions"][-1] == {
        "date": "2023-09-14",
        "session": {
            "bells": "Double Bells",
            "variation": "Double Classic + Pullup",
            "time": 30,
            "load": 28,
            "units": "kilograms",
            "swings": 60,
            "sets": 20,
        },
    }


def test_cache_session(database):
    ic_db.cache_session(Path(database.name), TEST_CACHE_SESSION)
    data = json.load(open(database.name))
    assert len(data["cached_sessions"]) == 10
    assert data["cached_sessions"][-1] == asdict(TEST_CACHE_SESSION)
