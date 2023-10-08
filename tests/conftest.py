import json
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory

import pytest

from .test_constants import TEST_DATA


@pytest.fixture(scope="function")
def database_home():
    with TemporaryDirectory() as db_dir:
        db_home = Path(db_dir)
        db_path = db_home / "test_db.json"
        return db_path


@pytest.fixture(scope="function")
def database():
    database = NamedTemporaryFile()
    with open(database.name, "w") as db:
        json.dump(TEST_DATA, db)
    return database
