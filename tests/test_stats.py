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


PLOT_DATES = ["2023-02-01", "2023-02-15", "2023-03-10", "2023-11-20"]
PLOT_WEIGHTS = [2300, 12500, 4100, 8000]


@pytest.mark.parametrize(
    "plot_type, title, expected_text",
    [
        ("event", "Workouts Across the Year", ["Jan", "Dec", "Months"]),
        ("line", "Weight Moved Per Workout", ["10,000", "15,000", "Date"]),
        ("bar", "Weight Moved by Month", ["Feb-23", "Nov-23", "15,000"]),
    ],
)
def test_plot_workouts_renders(plot_type, title, expected_text, capfd):
    """Render each plot with the real plotext, so an API change fails the test."""
    plot_workouts(PLOT_DATES, PLOT_WEIGHTS, plot_type, False, False)
    output = capfd.readouterr()[0]
    assert title in output
    for text in expected_text:
        assert text in output
    assert "e4" not in output  # no scientific-notation tick labels


@pytest.mark.parametrize(
    "plot_type, median, average, orientation, value",
    [
        ("line", True, False, "h", 6050),
        ("line", False, True, "h", 6725),
        ("bar", True, False, "v", 8000),
        ("bar", False, True, "v", 26900 / 3),
    ],
)
def test_plot_reference_lines(plot_type, median, average, orientation, value, capfd):
    import plotext as plt

    with mock.patch.object(plt.figure, "line", wraps=plt.figure.line) as line_mock:
        plot_workouts(PLOT_DATES, PLOT_WEIGHTS, plot_type, median, average)
    line_mock.assert_called_once()
    assert line_mock.call_args.args[0] == pytest.approx(value)
    assert line_mock.call_args.kwargs["orientation"] == orientation


@pytest.mark.parametrize("year, expected", [(None, "2026"), (2025, "2025")])
def test_event_plot_year(year, expected):
    """The event plot spans the given year, or the year of the last workout."""
    import plotext as plt

    with mock.patch.object(plt.figure, "ruler") as ruler_mock, mock.patch.object(plt.figure, "show"):
        plot_workouts(["2025-12-30", "2026-01-02"], [1, 2], "event", False, False, year=year)
    ruler_mock.return_value.lim.assert_any_call(f"{expected}-01-01", f"{expected}-12-31")


@pytest.mark.parametrize("plot_type, dates, message", [("pie", PLOT_DATES, "pie not a valid plot"), ("line", [], "No workouts")])
def test_plot_workouts_nothing_to_draw(plot_type, dates, message, capfd):
    plot_workouts(dates, PLOT_WEIGHTS[: len(dates)], plot_type, False, False)
    assert message in capfd.readouterr()[0]


def test_dates_in_cal(database, capfd):
    data = read_database(Path(database.name))
    actual = _get_dates(data)
    expected = [(12, 9, 2023), (14, 9, 2023)]
    assert actual == expected


def test_get_exercises_by_movement(database, capfd):
    from kettlebells.stats import get_exercises_by_movement

    data = read_database(Path(database.name))
    table = get_exercises_by_movement(data, "2023-09-01", "2023-12-31")
    assert table.title == "Fundamental Human Movements"
    assert table.row_count > 2


def test_print_calendar(database, capfd):
    from kettlebells.stats import print_calendar

    print_calendar(read_database(Path(database.name)), 2023)
    output = capfd.readouterr()[0]
    assert "September 2023" in output


@pytest.mark.parametrize(
    "maximum, positions",
    [
        (8286, [0, 2000, 4000, 6000, 8000, 10000]),
        (75346, [0, 20000, 40000, 60000, 80000]),
        (14800, [0, 5000, 10000, 15000]),
        (0, [0]),
    ],
)
def test_number_ticks(maximum, positions):
    from kettlebells.stats import _number_ticks

    actual_positions, labels = _number_ticks(maximum)
    assert actual_positions == positions
    assert labels == [f"{p:,}" for p in positions]
