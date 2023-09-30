from pathlib import Path

import pytest

from iron_cardio.iron_cardio_database import read_database
from iron_cardio.iron_cardio_stats import (
    calc_session_stats,
    display_session_stats,
    get_all_time_stats,
)

from .test_constants import (
    TEST_SESSION,
    TEST_SESSION_NO_SWINGS,
    TEST_SESSION_SINGLE_BELL_PULLUPS,
)


@pytest.mark.parametrize(
    "session, stats",
    [
        (TEST_SESSION, {"weight moved": 6840, "reps": 80, "pace": 22.5}),
        (
            TEST_SESSION_NO_SWINGS,
            {"weight moved": 1920, "reps": 80, "pace": 15.0},
        ),
    ],
)
def test_calc_session_stats(session, stats):
    """Test session stats are calculated correctly."""
    actual = calc_session_stats(session, 90)
    expected = stats
    assert actual == expected


def test_display_session_stats_single_bell_pullups(capfd):
    """Test session stats are displayed correctly."""
    display_session_stats(TEST_SESSION_SINGLE_BELL_PULLUPS, 90)
    output = capfd.readouterr()[0]
    expected = """Session Stats
=============
Weight Moved: 3,050 kilograms
  Total Reps: 35
        Pace: 17.1 sec/rep
"""
    assert expected in output


def test_get_all_time_stats(database, capfd):
    """Test that get_all_time_stats returns the dates and stats from the test database."""
    expected = (["2023-09-14"], [3480])
    data = read_database(Path(database.name))
    actual = get_all_time_stats(data)
    output = capfd.readouterr()[0]
    expected_output = """\nAll Time Stats
==============
    Total Sessions: 1
        Total Time: 20 mins
Total Weight Moved: 3,480 kilograms
        Total Reps: 87
      Average Pace: 13.8 sec/rep"""
    assert actual == expected
    assert expected_output in output
