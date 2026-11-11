import json
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory

import pytest

from .test_constants import TEST_DATA


@pytest.fixture(autouse=True)
def isolate_real_database(monkeypatch, tmp_path):
    """Never let a test read or write ~/.kettlebells.

    Reading an old database upgrades it in place, so a test that forgets to patch
    KETTLEBELLS_DB would otherwise rewrite the user's real data.
    """
    db_path = tmp_path / "isolated_db.json"
    db_path.write_text(json.dumps(TEST_DATA))
    monkeypatch.setattr("kettlebells.__main__.KETTLEBELLS_DB", db_path)
    monkeypatch.setattr("kettlebells.constants.KETTLEBELLS_DB", db_path)
    monkeypatch.setattr("kettlebells.constants.KETTLEBELLS_HOME", tmp_path)


@pytest.fixture(scope="function")
def database_home():
    with TemporaryDirectory() as db_dir:
        db_home = Path(db_dir)
        db_path = db_home / "test_db.json"
        return db_path


@pytest.fixture(scope="function")
def database():
    database = NamedTemporaryFile(delete=False)
    with open(database.name, "w") as db:
        json.dump(TEST_DATA, db)
    return database


@pytest.fixture()
def prompt_mock(mocker):
    yield mocker.patch("kettlebells.workouts.Prompt.ask")


@pytest.fixture()
def int_mock(mocker):
    yield mocker.patch("kettlebells.workouts.IntPrompt.ask")


@pytest.fixture()
def confirm_mock(mocker):
    yield mocker.patch("kettlebells.workouts.Confirm")


@pytest.fixture()
def units_mock(mocker):
    yield mocker.patch("kettlebells.workouts._get_units")


@pytest.fixture()
def options_mock(mocker):
    yield mocker.patch("kettlebells.workouts._get_options")
