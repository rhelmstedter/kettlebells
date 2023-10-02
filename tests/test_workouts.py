import json
from pathlib import Path
from unittest import mock

import pytest

from kettlebells.constants import IRON_CARDIO_PARAMS
from kettlebells.workouts import (
    Workout,
    _get_options,
    _get_units,
    create_custom_ic_session,
    random_workout,
    set_loads,
)

from .test_constants import TEST_SESSION, TEST_SESSION_NO_SWINGS

POSSIBLE_SWINGS = [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]


def test_create_random_workout(database):
    """Test when a session is created, the parameters are appropriate based on the
    database and within the ranges defined in the constants module.
    """
    loads = json.load(open(database.name))["ic_loads"]
    actual = random_workout(Path(database.name), 'iron-cardio')
    assert isinstance(actual, Workout)
    assert actual.bells in IRON_CARDIO_PARAMS["bells"].keys()
    assert (
        actual.variation in IRON_CARDIO_PARAMS["doublebell variations"].keys()
        or actual.variation in IRON_CARDIO_PARAMS["singlebell variations"].keys()
    )
    assert actual.time in IRON_CARDIO_PARAMS["times"].keys()
    assert actual.load in loads.values()
    assert actual.units == loads["units"]
    assert actual.swings == 0 or actual.swings in POSSIBLE_SWINGS


def test_display_ic_session(capfd):
    """Test a session is displayed correctly in the console."""
    TEST_SESSION.display_workout()
    output = capfd.readouterr()[0]
    assert TEST_SESSION.workout_type.upper() in output
    assert "===================" in output
    assert "Bells: " in output
    assert "Variation: " in output
    assert "Time: " in output
    assert "Load: " in output
    assert "Swings: " in output


def test_display_session_no_swings(capfd):
    """Test a session is displayed correctly in the console with no swings."""
    TEST_SESSION_NO_SWINGS.display_workout()
    output = capfd.readouterr()[0]
    assert TEST_SESSION.workout_type.upper() in output
    assert "===================" in output
    assert "Bells: " in output
    assert "Variation: " in output
    assert "Time: " in output
    assert "Load: " in output
    assert "Swings: " not in output


@mock.patch("kettlebells.workouts.IntPrompt.ask")
@mock.patch("kettlebells.workouts.Confirm")
@mock.patch("kettlebells.workouts._get_units")
def test_set_loads(units_mock, confirm_mock, int_mock):
    """Test that setting the loads in the database works."""
    expected = {
        "units": "pounds",
        "bodyweight": 190,
        "light load": 1,
        "medium load": 2,
        "heavy load": 3,
    }
    int_mock.side_effect = [190, 1, 2, 3]  # [body_weight, light, med, heavy]
    confirm_mock.side_effect = ["y"]
    units_mock.side_effect = ["pounds"]
    actual = set_loads()
    assert actual == expected


@pytest.mark.parametrize("response, units", [("p", "pounds"), ("k", "kilograms")])
@mock.patch("kettlebells.workouts.Prompt.ask")
def test_get_units_good_input(ask_mock, response, units):
    """Test that units are set correctly."""
    expected = units
    ask_mock.side_effect = [response]
    actual = _get_units()
    assert actual == expected


@pytest.mark.parametrize(
    "workout_param, response, option",
    [
        (IRON_CARDIO_PARAMS["bells"], 1, "Single Bell"),
        (IRON_CARDIO_PARAMS["singlebell variations"], 3, "Classic + Snatch"),
    ],
)
@mock.patch("kettlebells.workouts.IntPrompt.ask")
def test_get_options(ask_mock, workout_param, response, option):
    """Test the options for session parameters are valid."""
    expected = option
    ask_mock.side_effect = [response]
    actual = _get_options(workout_param)
    assert actual == expected


@pytest.mark.parametrize(
    "session, bells, variation, int_responses, sets",
    [
        (TEST_SESSION, "Double Bells", "Double Classic + Pullup", [30, 28, 60], 20),
        (
            TEST_SESSION_NO_SWINGS,
            "Single Bell",
            "Traveling 2s + Snatch",
            [20, 24, 0],
            16,
        ),
    ],
)
@mock.patch("kettlebells.workouts.IntPrompt.ask")
@mock.patch("kettlebells.workouts.Confirm")
@mock.patch("kettlebells.workouts._get_units")
@mock.patch("kettlebells.workouts._get_options")
def test_custom_session(
    options_mock,
    units_mock,
    confirm_mock,
    int_mock,
    session,
    bells,
    variation,
    int_responses,
    sets,
):
    """Test creating a custom session works as intended."""
    expected = session
    options_mock.side_effect = [bells, variation]
    int_mock.side_effect = int_responses
    confirm_mock.side_effect = ["y"]
    units_mock.side_effect = ["kilograms"]
    actual = create_custom_ic_session()
    actual.sets = sets
    assert isinstance(actual, Workout)
    assert actual == expected
