from pathlib import Path
from unittest import mock

import pytest
from typer.testing import CliRunner

import kettlebells.__main__
from kettlebells.__init__ import __version__
from kettlebells.__main__ import cli

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
    prompt_mock.side_effect = ["2023-09-12", ""]

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


def test_add_single_entry(database):
    import json

    with mock.patch.object(kettlebells.__main__, "KETTLEBELLS_DB", Path(database.name)):
        result = runner.invoke(
            cli, ["add", "2026-11-09", "ES D11 16min; DFS 2x5@24; Dip 3x3+45lb (HARD!)", "--yes"]
        )
    assert result.exit_code == 0, result.stdout
    assert "BW + 20 kg" in result.stdout
    saved = json.load(open(database.name))["saved_workouts"][-1]
    assert saved["date"] == "2026-11-09"
    assert saved["workout"]["notes"] == "Dip: HARD!"


def test_add_file(database, tmp_path):
    import json

    notes = tmp_path / "notes.txt"
    notes.write_text("2026-11-09 ES D11 16min; AW 1x10\n\n2026-11-11 ES 20min; AW 1x12\n")
    with mock.patch.object(kettlebells.__main__, "KETTLEBELLS_DB", Path(database.name)):
        result = runner.invoke(cli, ["add", "--file", str(notes)], input="y\n")
    assert result.exit_code == 0, result.stdout
    saved = json.load(open(database.name))["saved_workouts"]
    assert [w["workout"]["variation"] for w in saved[-2:]] == ["D11", "D12"]


def test_add_error(database):
    with mock.patch.object(kettlebells.__main__, "KETTLEBELLS_DB", Path(database.name)):
        result = runner.invoke(cli, ["add", "2026-11-09", "ES 16min; Nope 1x1", "--yes"])
    assert result.exit_code == 1
    assert "Unknown exercise 'Nope'" in result.stdout


def test_alias(database):
    import json

    with mock.patch.object(kettlebells.__main__, "KETTLEBELLS_DB", Path(database.name)):
        runner.invoke(cli, ["alias", "GSQ", "Goblet Squat"])
        listing = runner.invoke(cli, ["alias"])
        assert "GSQ: Goblet Squat" in listing.stdout
        assert "SGD: Snatch Grip Deadlift" in listing.stdout
        runner.invoke(cli, ["alias", "gsq", "--remove"])
    assert json.load(open(database.name))["aliases"]["exercises"] == {}


def test_delete(database):
    import json

    with mock.patch.object(kettlebells.__main__, "KETTLEBELLS_DB", Path(database.name)):
        result = runner.invoke(cli, ["delete", "2023-09-14"], input="y\n")
    assert "Workout deleted." in result.stdout
    assert [w["date"] for w in json.load(open(database.name))["saved_workouts"]] == ["2023-09-12"]


def test_delete_declined(database):
    import json

    with mock.patch.object(kettlebells.__main__, "KETTLEBELLS_DB", Path(database.name)):
        result = runner.invoke(cli, ["delete", "2023-09-14"], input="\n")
    assert "Workout not deleted." in result.stdout
    assert len(json.load(open(database.name))["saved_workouts"]) == 2


def test_save_repeat(database):
    with mock.patch.object(kettlebells.__main__, "KETTLEBELLS_DB", Path(database.name)):
        with mock.patch("kettlebells.__main__.repeat_last_workout") as repeat_mock:
            repeat_mock.return_value = None
            runner.invoke(cli, ["save", "--repeat", "-w", "es"])
    repeat_mock.assert_called_once_with(Path(database.name), "easy strength")


def test_edit(database):
    import json

    from kettlebells.workouts import Exercise, Workout

    edited = Workout(
        workout_type="iron cardio",
        variation="Double Classic",
        time=25,
        units="kg",
        bodyweight=90,
        exercises=[Exercise(name="Double Kettlebell Clean", load=20, sets=29, reps=1)],
        notes="felt good",
    )
    with mock.patch.object(kettlebells.__main__, "KETTLEBELLS_DB", Path(database.name)):
        with mock.patch("kettlebells.__main__.edit_workout", return_value=("2023-09-14", edited)):
            result = runner.invoke(cli, ["edit", "2023-09-14"], input="y\n")
    assert "Workout updated." in result.stdout
    saved = json.load(open(database.name))["saved_workouts"][-1]["workout"]
    assert (saved["time"], saved["notes"]) == (25, "felt good")


@mock.patch("kettlebells.__main__.iterfzf")
def test_edit_pick_cancelled(fzf_mock, database):
    fzf_mock.return_value = None
    with mock.patch.object(kettlebells.__main__, "KETTLEBELLS_DB", Path(database.name)):
        result = runner.invoke(cli, ["edit"])
    assert result.exit_code == 0
    labels = list(fzf_mock.call_args.args[0])
    assert labels[0].startswith("2023-09-14  Iron Cardio")


def test_delete_no_match(database):
    with mock.patch.object(kettlebells.__main__, "KETTLEBELLS_DB", Path(database.name)):
        result = runner.invoke(cli, ["delete", "2020-01-01"])
    assert "No saved workouts on 2020-01-01" in result.stdout


def test_save_template(database):
    with mock.patch.object(kettlebells.__main__, "KETTLEBELLS_DB", Path(database.name)):
        with mock.patch("kettlebells.__main__.create_from_template") as template_mock:
            template_mock.return_value = None
            runner.invoke(cli, ["save", "-t"])
    template_mock.assert_called_once_with(Path(database.name), None)


def test_add_needs_arguments(database):
    with mock.patch.object(kettlebells.__main__, "KETTLEBELLS_DB", Path(database.name)):
        result = runner.invoke(cli, ["add"])
    assert result.exit_code == 1
    assert "Give a date and a workout" in result.stdout


def test_stats_by_movement(database):
    with mock.patch.object(kettlebells.__main__, "KETTLEBELLS_DB", Path(database.name)):
        result = runner.invoke(cli, ["stats", "-M", "-y", "2023"])
    assert result.exit_code == 0
    assert "Fundamental Human Movements" in result.stdout


def test_stats_html(database, tmp_path):
    with mock.patch.object(kettlebells.__main__, "KETTLEBELLS_DB", Path(database.name)), mock.patch.object(
        kettlebells.__main__, "KETTLEBELLS_HOME", tmp_path
    ), mock.patch("kettlebells.__main__.webbrowser.open") as open_mock:
        result = runner.invoke(cli, ["stats", "--html", "-y", "2023"])
    assert result.exit_code == 0, result.stdout
    page = tmp_path / "stats.html"
    assert "Stats from 2023" in page.read_text()
    open_mock.assert_called_once_with(page.as_uri())


def test_stats_plot_options(database):
    with mock.patch.object(kettlebells.__main__, "KETTLEBELLS_DB", Path(database.name)):
        with mock.patch("kettlebells.__main__.plot_workouts") as plot_mock:
            runner.invoke(cli, ["stats", "-p", "line", "--by", "week"])
    assert plot_mock.call_args.kwargs == {"by": "week", "units": "kg"}
