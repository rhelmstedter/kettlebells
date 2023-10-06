from unittest import mock
from pathlib import Path

from typer.testing import CliRunner

from kettlebells.__init__ import __version__

from kettlebells.__main__ import cli
import kettlebells.__main__

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
@mock.patch("kettlebells.__main__.IntPrompt.ask")
def test_done_with_save(int_mock, prompt_mock, confirm_mock, database):
    """Test the done command prints out renders the last workout generated and the stats."""
    confirm_mock.return_value = True
    prompt_mock.side_effect = ["2023-09-12"]
    int_mock.side_effect = [10]

    with mock.patch.object(kettlebells.__main__, "KETTLEBELLS_DB", Path(database.name)):
        result = runner.invoke(cli, ["done"])
        assert "Last workout generated:" in result.stdout
        assert "Workout Stats" in result.stdout


def test_last(database):
    """Test the last command reads the last saved workout and displays the date and stats."""
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
    runner.invoke(cli, ["init"])
    init_mock.assert_called_once()


@mock.patch("kettlebells.__main__.read_database")
@mock.patch("kettlebells.__main__.top_ten_workouts")
def test_best(best_mock, read_mock):
    "Test best command calls read_database and top_ten_workouts."""
    runner.invoke(cli, ["best"])
    best_mock.assert_called_once()
    read_mock.assert_called_once()


@mock.patch("kettlebells.__main__.read_database")
@mock.patch("kettlebells.__main__.get_all_time_stats")
def test_stats(stats_mock, read_mock):
    """Test getting the stats"""
    runner.invoke(cli, ["stats"])
    read_mock.assert_called_once()
    stats_mock.assert_called_once()
