from pathlib import Path

from kettlebells.database import read_database
from kettlebells.stats import get_all_time_stats, top_ten_workouts


def test_get_all_time_stats(database, capfd):
    """Test that get_all_time_stats returns the dates and stats from the test database."""
    expected = (["2023-09-14"], [3480])
    data = read_database(Path(database.name))
    actual = get_all_time_stats(data)
    output = capfd.readouterr()[0]
    expected_output = """\nAll Time Stats
==============
     Total Workouts: 1
         Total Time: 0 days 00 hours 20 mins
 Total Weight Moved: 3,480 kg
         Total Reps: 87
Mean Weight Density: 174.0 kg/min
   Mean Rep Density: 4.3 reps/min"""
    assert actual == expected
    assert expected_output in output


def test_top_ten_workouts(database):
    """Test the table object created by top_ten_workouts."""
    data = read_database(Path(database.name))
    table = top_ten_workouts(data, "weight-moved")
    assert table.title == "Top Ten Workouts by Weight Moved"
    assert len(table.rows) == 1
    assert len(table.columns) == 8
