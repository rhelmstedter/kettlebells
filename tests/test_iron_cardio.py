import json
from pathlib import Path
from unittest import mock

import pytest

from iron_cardio.constants import (
    BELLS,
    DOUBLEBELL_VARIATIONS,
    SINGLEBELL_VARIATIONS,
    TIMES,
)
from iron_cardio.iron_cardio import (
    Session,
    _get_options,
    _get_units,
    create_custom_session,
    create_session,
    display_session,
    set_loads,
)

from .test_constants import TEST_SESSION, TEST_SESSION_NO_SWINGS

POSSIBLE_SWINGS = [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]


def test_create_session(database):
    """Test when a session is created, the parameters are appropriate based on the
    database and within the ranges defined in the constants module.
    """
    loads = json.load(open(database.name))["loads"]
    actual = create_session(Path(database.name))
    assert isinstance(actual, Session)
    assert actual.bells in BELLS.keys()
    assert (
        actual.variation in DOUBLEBELL_VARIATIONS.keys()
        or actual.variation in SINGLEBELL_VARIATIONS.keys()
    )
    assert actual.time in TIMES.keys()
    assert actual.load in loads.values()
    assert actual.units == loads["units"]
    assert actual.swings == 0 or actual.swings in POSSIBLE_SWINGS


def test_display_session(capfd):
    """Test a session is displayed correctly in the console."""
    display_session(TEST_SESSION)
    output = capfd.readouterr()[0]
    assert "Iron Cardio Session" in output
    assert "===================" in output
    assert "Bells: " in output
    assert "Variation: " in output
    assert "Time: " in output
    assert "Load: " in output
    assert "Swings: " in output


def test_display_session_no_swings(capfd):
    """Test a session is displayed correctly in the console with no swings."""
    display_session(TEST_SESSION_NO_SWINGS)
    output = capfd.readouterr()[0]
    assert "Iron Cardio Session" in output
    assert "===================" in output
    assert "Bells: " in output
    assert "Variation: " in output
    assert "Time: " in output
    assert "Load: " in output
    assert "Swings: " not in output


@mock.patch("iron_cardio.iron_cardio.IntPrompt.ask")
@mock.patch("iron_cardio.iron_cardio.Confirm")
@mock.patch("iron_cardio.iron_cardio._get_units")
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
@mock.patch("iron_cardio.iron_cardio.Prompt.ask")
def test_get_units_good_input(ask_mock, response, units):
    """Test that units are set correctly."""
    expected = units
    ask_mock.side_effect = [response]
    actual = _get_units()
    assert actual == expected


@pytest.mark.parametrize(
    "session_param, response, option",
    [
        (BELLS, 1, "Single Bell"),
        (SINGLEBELL_VARIATIONS, 3, "Classic + Snatch"),
        (DOUBLEBELL_VARIATIONS, 4, "Armor Building Complex"),
    ],
)
@mock.patch("iron_cardio.iron_cardio.IntPrompt.ask")
def test_get_options(ask_mock, session_param, response, option):
    """Test the options for session parameters are valid."""
    expected = option
    ask_mock.side_effect = [response]
    actual = _get_options(session_param)
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
@mock.patch("iron_cardio.iron_cardio.IntPrompt.ask")
@mock.patch("iron_cardio.iron_cardio.Confirm")
@mock.patch("iron_cardio.iron_cardio._get_units")
@mock.patch("iron_cardio.iron_cardio._get_options")
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
    actual = create_custom_session()
    actual.sets = sets
    assert isinstance(actual, Session)
    assert actual == expected
