import json
import re
from unittest import mock

import plotext as plt
import pytest

from kettlebells.plots import (
    _number_ticks,
    aggregate,
    bar_chart,
    plot_workouts,
    write_html_report,
)
from kettlebells.workouts import Exercise, Workout

PLOT_DATES = ["2023-02-01", "2023-02-15", "2023-03-10", "2023-11-20"]
PLOT_WEIGHTS = [2300, 12500, 4100, 8000]


def _plain(text: str) -> str:
    return re.sub(r"\x1b\[[0-9;]*m", "", text)


@pytest.mark.parametrize(
    "plot_type, expected_text",
    [
        ("event", ["Workouts Across 2023", "Jan", "Dec"]),
        ("line", ["Weight Moved Per Workout (kg)", "10,000", "15,000"]),
        ("bar", ["Weight Moved by Month (kg)", "Feb-23", "Nov-23", "14,800"]),
    ],
)
def test_plot_workouts_renders(plot_type, expected_text, capfd):
    """Render each plot for real, so a plotext API change fails the test."""
    plot_workouts(PLOT_DATES, PLOT_WEIGHTS, plot_type, False, False)
    output = capfd.readouterr()[0]
    for text in expected_text:
        assert text in output
    assert "e4" not in output  # no scientific-notation tick labels
    # plotext 6 paints white (color 15) behind figure.line()/event(); they must not be used.
    assert "48;5;15" not in output


def test_line_plot_by_month(capfd):
    plot_workouts(PLOT_DATES, PLOT_WEIGHTS, "line", True, False, by="month")
    output = capfd.readouterr()[0]
    assert "Weight Moved Per Month (kg)" in output
    assert "48;5;15" not in output


def test_line_plot_reference_line():
    with mock.patch.object(plt.figure, "signal", wraps=plt.figure.signal) as signal_mock:
        with mock.patch.object(plt.figure, "show"):
            plot_workouts(PLOT_DATES, PLOT_WEIGHTS, "line", True, False)
    reference = signal_mock.call_args_list[-1]
    assert reference.args == (["2023-02-01", "2023-11-20"], [6050, 6050])


@pytest.mark.parametrize("year, expected", [(None, "2026"), (2025, "2025")])
def test_event_plot_year(year, expected):
    """The event plot spans the given year, or the year of the last workout."""
    with mock.patch.object(plt.figure, "ruler") as ruler_mock, mock.patch.object(plt.figure, "show"):
        plot_workouts(["2025-12-30", "2026-01-02"], [1, 2], "event", False, False, year=year)
    ruler_mock.return_value.lim.assert_any_call(f"{expected}-01-01", f"{expected}-12-31")


@pytest.mark.parametrize(
    "plot_type, dates, by, message",
    [
        ("pie", PLOT_DATES, "workout", "pie not a valid plot"),
        ("line", [], "workout", "No workouts"),
        ("line", PLOT_DATES, "year", "year is not one of workout, week, month"),
    ],
)
def test_plot_workouts_nothing_to_draw(plot_type, dates, by, message, capfd):
    plot_workouts(dates, PLOT_WEIGHTS[: len(dates)], plot_type, False, False, by=by)
    assert message in capfd.readouterr()[0]


@pytest.mark.parametrize(
    "by, expected",
    [
        ("workout", (PLOT_DATES, PLOT_WEIGHTS)),
        # 2023-02-01 is a Wednesday, so its week starts on Monday 2023-01-30.
        ("week", (["2023-01-30", "2023-02-13", "2023-03-06", "2023-11-20"], PLOT_WEIGHTS)),
        ("month", (["2023-02-01", "2023-03-01", "2023-11-01"], [14800, 4100, 8000])),
    ],
)
def test_aggregate(by, expected):
    assert aggregate(PLOT_DATES, PLOT_WEIGHTS, by) == expected


def test_aggregate_same_week():
    assert aggregate(["2026-11-09", "2026-11-11", "2026-11-16"], [1, 2, 4], "week") == (
        ["2026-11-09", "2026-11-16"],
        [3, 4],
    )


def _render(renderable, width=100) -> str:
    from rich.console import Console

    console = Console(width=width, record=True, file=open("/dev/null", "w"), color_system=None)
    console.print(renderable)
    return console.export_text()


def test_bar_chart_lengths_match_values():
    """Every bar is exactly proportional to its value, to an eighth of a character."""
    labels = [f"M{i:02}" for i in range(14)]
    values = [5000 * (i + 1) for i in range(14)]
    text = _render(bar_chart("Weight", labels, values, "kg", width=40))
    eighths = {b: i for i, b in enumerate(" ▏▎▍▌▋▊▉█")}
    for label, value in zip(labels, values):
        line = next(line for line in text.splitlines() if line.lstrip().startswith(label))
        bar = line.split(label, 1)[1].rsplit(f"{value:,}", 1)[0]
        length = sum(8 if c == "█" else eighths.get(c, 0) for c in bar if c not in "│")
        assert length == round(value / values[-1] * 40 * 8), label
        assert line.rstrip().endswith(f"{value:,}")


def test_bar_chart_reference():
    text = _render(bar_chart("Weight", ["A", "B", "C"], [10, 20, 40], "kg", show_median=True, width=40))
    assert "│ Median: 20 kg" in text
    a_row = next(line for line in text.splitlines() if line.lstrip().startswith("A "))
    assert "│" in a_row  # the median mark sits past the end of A's short bar


def test_number_ticks_values():
    assert _number_ticks(8286) == ([0, 2000, 4000, 6000, 8000, 10000], ["0", "2,000", "4,000", "6,000", "8,000", "10,000"])
    assert _number_ticks(0) == ([0], ["0"])


def test_write_html_report(tmp_path):
    workout = Workout(
        workout_type="easy strength",
        variation="D11",
        time=16,
        units="kg",
        bodyweight=85,
        notes="felt </script> fine",
        exercises=[Exercise(name="Dip", load=20, sets=3, reps=3)],
    )
    path = write_html_report(tmp_path / "stats.html", [("2026-11-09", workout)], "kg", "All Time Stats")
    html = path.read_text()
    assert "<title>Kettlebells Stats</title>" in html
    assert "plotly.js/3.0.1/plotly.min.js" in html
    # The notes can't close the data <script> early.
    assert html.count("</script>") == 3
    payload = re.search(r'<script id="data" type="application/json">(.*?)</script>', html, re.S).group(1)
    data = json.loads(payload)
    assert data["units"] == "kg"
    assert data["rows"] == [
        {
            "date": "2026-11-09",
            "type": "Easy Strength",
            "variation": "D11",
            "time": 16,
            "weight": 909,
            "reps": 9,
            "notes": "felt </script> fine",
        }
    ]
    assert "909 kg" in html


def test_write_html_report_empty(tmp_path):
    html = write_html_report(tmp_path / "s.html", [], "kg", "Stats").read_text()
    assert "No workouts" in html
