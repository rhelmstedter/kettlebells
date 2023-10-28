from pathlib import Path
from unittest import mock

from typer.testing import CliRunner

import kettlebells.__main__
from kettlebells.__init__ import __version__
from kettlebells.__main__ import cli

runner = CliRunner()


def test_version():
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert f"{__version__}\n" in result.stdout


@mock.patch("kettlebells.__main__.Confirm.ask")
def test_done_without_save(confirm_mock, database):
    """Test workout not saved renders correctly."""
    confirm_mock.return_value = ""
    with mock.patch.object(kettlebells.__main__, "KETTLEBELLS_DB", Path(database.name)):
        result = runner.invoke(cli, ["done"])
        assert "Last workout generated:" in result.stdout
        assert "Workout not saved." in result.stdout


@mock.patch("kettlebells.__main__.Confirm.ask")
@mock.patch("kettlebells.__main__.Prompt.ask")
@mock.patch("kettlebells.__main__.save_workout")
def test_done_with_save(save_mock, prompt_mock, confirm_mock, database):
    """Test the done command prints out renders the last workout generated and the stats."""
    confirm_mock.return_value = True
    prompt_mock.side_effect = ["2023-09-12"]

    with mock.patch.object(kettlebells.__main__, "KETTLEBELLS_DB", Path(database.name)):
        result = runner.invoke(cli, ["done"])
        assert "Workout Stats" in result.stdout
        save_mock.assert_called_once()


def test_last(database):
    """Test the last command reads the last saved session and displays the date and stats."""
    with mock.patch.object(kettlebells.__main__, "KETTLEBELLS_DB", Path(database.name)):
        result = runner.invoke(cli, ["last"])
        assert "Date: Sep 14, 2023" in result.stdout


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
def test_stats_best(best_mock):
    """Test stats command with best flag calls read_database and top_ten_workouts."""
    result = runner.invoke(cli, ["stats", "-b"])
    assert result.exit_code == 0
    best_mock.assert_called_once()


@mock.patch("kettlebells.__main__.plot_workouts")
def test_stats_plot(plot_mock):
    """Test stats command with plot flag."""
    result = runner.invoke(cli, ["stats", "-p", "line"])
    assert result.exit_code == 0
    plot_mock.assert_called_once()


@mock.patch("kettlebells.__main__.print_calendar")
def test_stats_calendar(cal_mock):
    """Test stats command with calendar flag."""
    result = runner.invoke(cli, ["stats", "-c", 2023])
    assert result.exit_code == 0
    cal_mock.assert_called_once()


@mock.patch("kettlebells.__main__.read_database")
@mock.patch("kettlebells.__main__.get_all_time_stats")
def test_stats(stats_mock, read_mock):
    """Test getting the stats"""
    runner.invoke(cli, ["stats"])
    read_mock.assert_called_once()
    stats_mock.assert_called_once()
