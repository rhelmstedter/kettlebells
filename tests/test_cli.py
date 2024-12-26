from pathlib import Path
from unittest import mock

import kettlebells.__main__
import pytest
from kettlebells.__init__ import __version__
from kettlebells.__main__ import cli
from typer.testing import CliRunner

from .test_constants import TEST_IC_WORKOUT

runner = CliRunner()


def test_version():
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert f"{__version__}\n" in result.stdout


@mock.patch("kettlebells.__main__.Confirm.ask")
def test_save_without_save(confirm_mock, database):
    """Test workout not saved renders correctly."""
    confirm_mock.return_value = ""
    with mock.patch.object(kettlebells.__main__, "KETTLEBELLS_DB", Path(database.name)):
        result = runner.invoke(cli, ["save"])
        assert "Last workout generated:" in result.stdout
        assert "Workout not saved." in result.stdout


@pytest.mark.parametrize(
    "func, option",
    [
        ("create_ic_or_abc", "ic"),
        ("create_btb_workout", "btb"),
        ("create_custom_workout", "custom"),
        ("create_perfect_workout", "pw"),
        ("create_time_based_workout", "giant"),
        # ("from_dict", None),
    ],
)
def test_matching(func, option):
    with mock.patch("kettlebells.__main__." + func) as save_mock:
        runner.invoke(cli, ["save", "--workout-type", option])
        save_mock.assert_called_once()


def test_save_bad_input(database):
    """Test workout not saved renders correctly."""
    with mock.patch.object(kettlebells.__main__, "KETTLEBELLS_DB", Path(database.name)):
        result = runner.invoke(cli, ["save", "-w asdf"])
        assert "'asdf' is not an option" in result.stdout


@mock.patch("kettlebells.__main__.Confirm.ask")
@mock.patch("kettlebells.__main__.Prompt.ask")
@mock.patch("kettlebells.__main__.save_workout")
def test_save(save_mock, prompt_mock, confirm_mock, database):
    """Test the save command prints out renders the last workout generated and the stats."""
    confirm_mock.return_value = True
    prompt_mock.side_effect = ["2023-09-12"]

    with mock.patch.object(kettlebells.__main__, "KETTLEBELLS_DB", Path(database.name)):
        result = runner.invoke(cli, ["save"])
        assert "Workout Stats" in result.stdout
        save_mock.assert_called_once()


def test_last(database):
    """Test the last command reads the last saved session and displays the date and stats."""
    with mock.patch.object(kettlebells.__main__, "KETTLEBELLS_DB", Path(database.name)):
        result = runner.invoke(cli, ["last"])
        assert "Date: Sep 14, 2023" in result.stdout


@mock.patch("kettlebells.stats.iterfzf")
def test_view(iterfzf_mock, database):
    """Test the view command."""
    iterfzf_mock.return_value = "2023-09-14"
    with mock.patch.object(kettlebells.__main__, "KETTLEBELLS_DB", Path(database.name)):
        result = runner.invoke(cli, ["view"])
        assert "Date: Sep 14, 2023" in result.stdout


@mock.patch("kettlebells.__main__.filter_by_program")
def test_view_program(filter_mock, database):
    """Test the view -program command."""
    filter_mock.return_value = "2023-09-14"
    with mock.patch.object(kettlebells.__main__, "KETTLEBELLS_DB", Path(database.name)):
        runner.invoke(cli, ["view", "-P"])
        filter_mock.assert_called_once()


@mock.patch("kettlebells.__main__.set_loads")
@mock.patch("kettlebells.__main__.read_database")
@mock.patch("kettlebells.__main__.write_database")
def test_setloads(write_mock, read_mock, loads_mock):
    """Test setloads command calls set_loads, read_database, and write_database."""
    runner.invoke(cli, ["setloads"])
    loads_mock.assert_called_once()
    read_mock.assert_called_once()
    write_mock.assert_called_once()


@mock.patch("kettlebells.__main__.initialize_database")
def test_init(init_mock):
    """Test init command calls initialize_database."""
    result = runner.invoke(cli, ["init"])
    assert result.exit_code == 0
    init_mock.assert_called_once()


@mock.patch("kettlebells.__main__.top_ten_workouts")
def test_stats_best(best_mock, database):
    """Test stats command with best flag calls read_database and top_ten_workouts."""
    with mock.patch.object(kettlebells.__main__, "KETTLEBELLS_DB", Path(database.name)):
        result = runner.invoke(cli, ["stats", "-b"])
        assert result.exit_code == 0
        best_mock.assert_called_once()


@mock.patch("kettlebells.__main__.plot_workouts")
def test_stats_plot(plot_mock, database):
    """Test stats command with plot flag."""
    with mock.patch.object(kettlebells.__main__, "KETTLEBELLS_DB", Path(database.name)):
        result = runner.invoke(cli, ["stats", "-p", "line"])
        assert result.exit_code == 0
        plot_mock.assert_called_once()


@mock.patch("kettlebells.__main__.print_calendar")
def test_stats_calendar(cal_mock, database):
    """Test stats command with calendar flag."""
    with mock.patch.object(kettlebells.__main__, "KETTLEBELLS_DB", Path(database.name)):
        result = runner.invoke(cli, ["stats", "-c", "-y", "2023"])
        assert result.exit_code == 0
        cal_mock.assert_called_once()


@mock.patch("kettlebells.__main__.read_database")
@mock.patch("kettlebells.__main__.get_all_stats")
def test_stats(stats_mock, read_mock):
    """Test getting the stats"""
    runner.invoke(cli, ["stats"])
    read_mock.assert_called_once()
    stats_mock.assert_called_once()


@mock.patch("kettlebells.__main__.confirm_loads")
@mock.patch("kettlebells.__main__.random_ic_or_abc")
@mock.patch("kettlebells.__main__.cache_workout")
def test_random(cache_mock, workout_mock, confirm_mock):
    """Test getting the stats"""
    workout_mock.return_value = TEST_IC_WORKOUT
    runner.invoke(cli, ["random", "-w ic"])
    workout_mock.assert_called_once()
    cache_mock.assert_called_once()
    confirm_mock.assert_called_once()
