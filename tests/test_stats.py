from pathlib import Path
from unittest import mock

import plotext as plt
import pytest

from kettlebells.database import read_database
from kettlebells.stats import get_all_time_stats, plot_workouts, top_ten_workouts


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


@pytest.mark.parametrize(
    "title, x_label, plot_size, plot_type, median, average",
    [
        ("Workouts Across the Year", "Months", (130, 20), "event", False, False),
        ("Weight Moved Per Workout", "Date", (90, 30), "line", True, False),
        ("Weight Moved by Month", "Weight Moved", (90, 30), "bar", False, True),
    ],
)
@mock.patch("kettlebells.stats.plt")
def test_event_plot(plt_mock, title, x_label, plot_size, plot_type, median, average):
    plot_workouts(["2023-02-01"], [2300], plot_type, median, average)
    plt_mock.title.assert_called_once_with(title)
    plt_mock.xlabel.assert_called_once_with(x_label)
    plt_mock.plotsize.assert_called_once_with(*plot_size)
    if median:
        plt_mock.hline.assert_called_once()
    if average:
        plt_mock.vline.assert_called_once()
