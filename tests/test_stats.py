from pathlib import Path
from unittest import mock

import pytest
from kettlebells.database import read_database
from kettlebells.stats import (
    _get_dates,
    filter_by_program,
    get_all_stats,
    plot_workouts,
    retrieve_workout,
    top_ten_workouts,
    view_program,
)
from kettlebells.workouts import Workout


def test_get_all_time_stats(database, capfd):
    """Test that get_all_time_stats returns the dates and stats from the test database."""
    expected = (["2023-09-12", "2023-09-14"], [3456, 3480])
    data = read_database(Path(database.name))
    actual = get_all_stats(data)
    output = capfd.readouterr()[0]
    expected_output = """\nAll Time Stats
==============
     Total Workouts: 2
         Total Time: 0 days 00 hours 40 mins
 Total Weight Moved: 6,936 kg
         Total Reps: 159
Mean Weight Density: 173.4 kg/min
   Mean Rep Density: 4.0 reps/min"""
    assert actual == expected
    assert expected_output in output


def test_top_ten_workouts(database):
    """Test the table object created by top_ten_workouts."""
    data = read_database(Path(database.name))
    table = top_ten_workouts(data, "weight-moved")
    assert table.title == "Top Ten Workouts by Weight Moved"
    assert len(table.rows) == 2
    assert len(table.columns) == 8


@mock.patch("kettlebells.stats.iterfzf")
def test_filter_by_program(fzf_mock, database):
    """Test the table object created by filter_by_program."""
    data = read_database(Path(database.name))
    data["saved_workouts"].pop(0)
    fzf_mock.return_value = "Dry Fighting Weight"

    filtered_data, program = filter_by_program(data)
    assert program == "Dry Fighting Weight"
    assert filtered_data == data


def test_view_program(database):
    """Test the table object created by filter_by_program."""
    data = read_database(Path(database.name))
    data["saved_workouts"].pop(0)
    table = view_program(data, "Dry Fighting Weight", False)
    assert table.title == "Dry Fighting Weight"
    assert len(table.rows) == 1
    assert len(table.columns) == 9


@mock.patch("kettlebells.stats.iterfzf")
def test_retrieve_workout(fzf_mock, database):
    """Test the table object created by filter_by_program."""
    data = read_database(Path(database.name))
    expected = Workout(**data["saved_workouts"][1]["workout"])
    fzf_mock.return_value = "2023-09-14"
    date, actual = retrieve_workout(data, False)
    assert actual == expected
    assert date == "2023-09-14"


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


def test_dates_in_cal(database, capfd):
    data = read_database(Path(database.name))
    actual = _get_dates(data)
    expected = [(12, 9, 2023), (14, 9, 2023)]
    assert actual == expected
