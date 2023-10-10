import json
from pathlib import Path
from unittest import mock

import pytest

from kettlebells.constants import IRON_CARDIO_PARAMS
from kettlebells.workouts import (
    Workout,
    _get_options,
    _get_units,
    create_custom_workout,
    random_workout,
    set_loads,
)

from .test_constants import TEST_WORKOUT, TEST_WORKOUT_NO_SWINGS

POSSIBLE_SWINGS = [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]


def test_create_random_workout(database):
    """Test when a workout is created, the parameters are appropriate based on the
    database and within the ranges defined in the constants module.
    """
    loads = json.load(open(database.name))["loads"]
    actual = random_workout(Path(database.name), "iron-cardio")
    assert isinstance(actual, Workout)
    assert (
        actual.variation in IRON_CARDIO_PARAMS["doublebell variations"].keys()
        or actual.variation in IRON_CARDIO_PARAMS["singlebell variations"].keys()
    )
    assert actual.time in IRON_CARDIO_PARAMS["times"].keys()


def test_display_workout(capfd):
    """Test a workout is displayed correctly in the console."""
    TEST_WORKOUT.display_workout()
    output = capfd.readouterr()[0]
    assert TEST_WORKOUT.workout_type.upper() in output
    assert "=" * len(TEST_WORKOUT.workout_type) in output
    assert "Variation: " in output
    assert "Time: " in output
    assert "Load: " in output


def test_display_workout_no_swings(capfd):
    """Test a workout is displayed correctly in the console with no swings."""
    TEST_WORKOUT_NO_SWINGS.display_workout()
    output = capfd.readouterr()[0]
    assert TEST_WORKOUT_NO_SWINGS.workout_type.upper() in output
    assert "=" * len(TEST_WORKOUT_NO_SWINGS.workout_type) in output
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
    """Test the options for workout parameters are valid."""
    expected = option
    ask_mock.side_effect = [response]
    actual = _get_options(workout_param)
    assert actual == expected


@pytest.mark.parametrize(
    "workout, bells, variation, confirm, int_responses",
    [
        # int responses are time, load, sets, swings
        (
            TEST_WORKOUT,
            "Double Bells",
            "Double Classic + Pullup",
            True,
            [30, 28, 20, 60],
        ),
    ],
)
@mock.patch("kettlebells.workouts.IntPrompt.ask")
@mock.patch("kettlebells.workouts.Confirm")
@mock.patch("kettlebells.workouts._get_units")
@mock.patch("kettlebells.workouts._get_options")
def test_custom_workout(
    options_mock,
    units_mock,
    confirm_mock,
    int_mock,
    workout,
    bells,
    variation,
    confirm,
    int_responses,
    database,
):
    """Test creating a custom workout works as intended."""
    expected = workout
    options_mock.side_effect = [bells, variation]
    int_mock.side_effect = int_responses
    confirm_mock.return_value = "y"
    units_mock.side_effect = ["kilograms"]
    actual = create_custom_workout(Path(database.name), "iron-cardio")
    assert isinstance(actual, Workout)
    assert actual == expected
