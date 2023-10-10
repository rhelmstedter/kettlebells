from pathlib import Path

import pytest

from kettlebells.database import read_database
from kettlebells.stats import (
    get_all_time_stats,
)

from .test_constants import (
    TEST_WORKOUT,
    TEST_WORKOUT_NO_SWINGS,
    TEST_WORKOUT_SINGLE_BELL_PULLUPS,
)


@pytest.mark.parametrize(
    "workout, stats",
    [
        (TEST_WORKOUT, {"weight moved": 6840, "reps": 140, "pace": 12.9}),
        (
            TEST_WORKOUT_NO_SWINGS,
            {"weight moved": 1536, "reps": 64, "pace": 18.8},
        ),
    ],
)
def test_calc_workout_stats(workout, stats):
    """Test workout stats are calculated correctly."""
    actual = workout.calc_workout_stats()
    expected = stats
    assert actual == expected


def test_display_workout_stats_single_bell_pullups(capfd):
    """Test workout stats are displayed correctly."""
    TEST_WORKOUT_SINGLE_BELL_PULLUPS.display_workout_stats()
    output = capfd.readouterr()[0]
    expected = """Workout Stats
=============
Weight Moved: 1,050 kilograms
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
    Total Workouts: 1
        Total Time: 20 mins
Total Weight Moved: 3,480 kilograms
        Total Reps: 87
      Average Pace: 13.8 sec/rep"""
    assert actual == expected
    assert expected_output in output
