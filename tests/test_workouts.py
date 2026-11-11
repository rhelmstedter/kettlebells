from pathlib import Path
from unittest import mock

import pytest

from kettlebells.constants import IRON_CARDIO_PARAMS
from kettlebells.workouts import (
    Workout,
    _get_options,
    _get_units,
    create_abf_barbell_workout,
    create_abf_workout,
    create_btb_workout,
    create_custom_workout,
    create_ic_or_abc,
    create_perfect_workout,
    create_rite_of_passage_workout,
    create_set_based_workout,
    create_time_based_workout,
    create_workout_generator_workout,
    random_ic_or_abc,
    set_loads,
    set_program_loads,
)

from .test_constants import (
    TEST_ABF_ABC_WORKOUT,
    TEST_ABF_PRESS_WORKOUT,
    TEST_ABFB,
    TEST_BTB_WORKOUT,
    TEST_CUSTOM_WORKOUT,
    TEST_DOUBLE_TRAVELING_2S_WORKOUT,
    TEST_GIANT_WORKOUT,
    TEST_IC_WORKOUT,
    TEST_PERFECT_WORKOUT,
    TEST_ROP_WORKOUT,
    TEST_SINGLE_TRAVELING_2S_WORKOUT,
    TEST_WOLF_WORKOUT,
    TEST_WORKOUT_GENERATOR_WORKOUT,
    TEST_WORKOUT_NO_SWINGS,
    TEST_WORKOUT_SINGLE_BELL_PULLUPS,
)

POSSIBLE_SWINGS = [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]


def test_create_random_workout(database):
    """Test when a workout is created, the parameters are appropriate based on the
    database and within the ranges defined in the constants module.
    """
    actual = random_ic_or_abc(Path(database.name), "ic")
    assert isinstance(actual, Workout)
    assert (
        actual.variation in IRON_CARDIO_PARAMS["doublebell variations"].keys()
        or actual.variation in IRON_CARDIO_PARAMS["singlebell variations"].keys()
    )
    assert actual.time in IRON_CARDIO_PARAMS["times"].keys()


@pytest.mark.parametrize("workout", [TEST_IC_WORKOUT, TEST_BTB_WORKOUT])
def test_display_workout(workout, capfd):
    """Test a workout is displayed correctly in the console."""
    workout.display_workout()
    output = capfd.readouterr()[0]
    assert workout.workout_type.upper() in output
    assert "=" * len(workout.workout_type) in output
    assert "Variation: " in output
    assert "Time: " in output
    assert "Load: " in output


def test_display_custom_workout(capfd):
    """Test a custom workout is displayed correctly in the console."""
    TEST_CUSTOM_WORKOUT.display_workout()
    output = capfd.readouterr()[0]
    assert TEST_CUSTOM_WORKOUT.workout_type.upper() in output
    assert "=" * len(TEST_CUSTOM_WORKOUT.workout_type) in output
    assert "Variation: " in output
    assert "Time: " in output
    assert "Exercises" in output


def test_display_workout_no_swings(capfd):
    """Test a workout is displayed correctly in the console with no swings."""
    TEST_WORKOUT_NO_SWINGS.display_workout()
    output = capfd.readouterr()[0]
    assert TEST_WORKOUT_NO_SWINGS.workout_type.upper() in output
    assert "=" * len(TEST_WORKOUT_NO_SWINGS.workout_type) in output
    assert "Variation: " in output
    assert "Time: " in output
    assert "Load: " in output
    assert "Swing: " not in output


@pytest.mark.parametrize(
    "workout, stats",
    [
        (
            TEST_IC_WORKOUT,
            {
                "weight moved": 6760,
                "reps": 140,
                "weight density": 225.3,
                "rep density": 4.7,
            },
        ),
        (
            TEST_WORKOUT_NO_SWINGS,
            {
                "weight moved": 1536,
                "reps": 64,
                "weight density": 76.8,
                "rep density": 3.2,
            },
        ),
    ],
)
def test_calc_workout_stats(workout, stats):
    """Test workout stats are calculated correctly."""
    actual = workout.calc_workout_stats()
    expected = stats
    assert actual == expected


def test_display_workout_stats_single_bell_pullups(capfd):
    """Test workout stats are displayed correctly."""
    TEST_WORKOUT_SINGLE_BELL_PULLUPS.display_workout_stats()
    output = capfd.readouterr()[0]
    expected = """Workout Stats
=============
  Weight Moved: 1,050 kg
    Total Reps: 35
Weight Density: 105.0 kg/min
   Rep Density: 3.5 reps/min
"""
    assert expected in output


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


@pytest.mark.parametrize("response, units", [("p", "lbs"), ("k", "kg")])
def test_get_units_good_input(response, units, prompt_mock):
    """Test that units are set correctly."""
    expected = units
    prompt_mock.side_effect = [response]
    actual = _get_units()
    assert actual == expected


@pytest.mark.parametrize(
    "workout_param, response, option",
    [
        (IRON_CARDIO_PARAMS["bells"], 1, "Single Bell"),
        (IRON_CARDIO_PARAMS["singlebell variations"], 3, "Classic + Snatch"),
    ],
)
def test_get_options(workout_param, response, option, int_mock):
    """Test the options for workout parameters are valid."""
    expected = option
    int_mock.side_effect = [response]
    actual = _get_options(workout_param)
    assert actual == expected


def test_get_options_bad_input(int_mock):
    """Test bad index results in infinite loop."""
    try:
        int_mock.side_effect = [10, 20, "k"]
        _get_options(IRON_CARDIO_PARAMS["bells"])
    except StopIteration:
        pass


@pytest.mark.parametrize(
    "test_workout, bells, variation, confirm, int_responses",
    [
        # int responses are time, load, sets, swings count, swing load
        (
            TEST_IC_WORKOUT,
            "Double Bells",
            "Double Classic + Pullup",
            True,
            [30, 28, 20, 60, 28],
        ),
        (
            TEST_DOUBLE_TRAVELING_2S_WORKOUT,
            "Double Bells",
            "Double Traveling 2s",
            True,
            [29, 28, 12, 50, 28],
        ),
        (
            TEST_SINGLE_TRAVELING_2S_WORKOUT,
            "Single Bell",
            "Traveling 2s",
            True,
            [10, 20, 10, 100, 20],
        ),
    ],
)
def test_custom_ic_workout(
    test_workout,
    bells,
    variation,
    confirm,
    int_responses,
    options_mock,
    units_mock,
    confirm_mock,
    int_mock,
    database,
):
    """Test creating a custom iron cardio or abc workout works as intended."""
    expected = test_workout
    options_mock.side_effect = [bells, variation]
    int_mock.side_effect = int_responses
    units_mock.side_effect = ["kg"]
    confirm_mock.return_value = "y"
    actual = create_ic_or_abc(Path(database.name), "ic")
    assert actual == expected


# def test_easy_strength_workout(
#     options_mock,
#     units_mock,
#     confirm_mock,
#     int_mock,
#     database,
# ):
#     """Test creating an easy strength workout."""
#     expected = TEST_EASY_STRENGTH_WORKOUT
#     options_mock.side_effect = ["regular"]
#     int_mock.side_effect = [30, 24, 20, 24, 20, 24, 20, 24, 20, 24, 20, 24]
#     units_mock.side_effect = ["kg"]
#     actual = create_easy_strength_workout(Path(database.name), "es")
#     assert isinstance(actual, Workout)
#     assert actual == expected


@mock.patch("kettlebells.workouts.iterfzf")
def test_workout_generator_workout(
    fzf_mock,
    options_mock,
    units_mock,
    confirm_mock,
    int_mock,
    database,
):
    """Test creating a workout generator workout."""
    expected = TEST_WORKOUT_GENERATOR_WORKOUT
    int_mock.side_effect = [40, 100, 10, 80, 10]
    options_mock.side_effect = ["3 X 10"]
    fzf_mock.side_effect = ["Deadlift", "Bench Press", "Done"]
    units_mock.side_effect = ["kg"]
    actual = create_workout_generator_workout(Path(database.name))
    assert actual == expected


def test_rop_workout(
    options_mock,
    units_mock,
    int_mock,
    database,
):
    """Test creating a rite of passage workout."""
    expected = TEST_ROP_WORKOUT
    options_mock.side_effect = [
        "Medium",
        "Kettlebell Clean and Press",
        "Pullup",
        "Kettlebell Swing",
        "Done",
    ]
    int_mock.side_effect = [45, 28, 5, 3, 0, 5, 3, 28, 5, 10]
    units_mock.side_effect = ["kg"]
    actual = create_rite_of_passage_workout(Path(database.name))
    assert actual == expected


@pytest.mark.parametrize(
    "test_workout, variation, int_responses",
    [
        (
            TEST_ABF_ABC_WORKOUT,
            "Armor Building Complex",
            [30, 20, 30],
        ),
        (
            TEST_ABF_PRESS_WORKOUT,
            "Double Kettlebell Press",
            [30, 20, 5, 5, 5, 5],
        ),
    ],
)
def test_abf_workout(
    test_workout,
    variation,
    int_responses,
    options_mock,
    units_mock,
    int_mock,
    database,
):
    """Test creating a armor building formula workout."""
    expected = test_workout
    options_mock.side_effect = [variation]
    int_mock.side_effect = int_responses
    units_mock.side_effect = ["kg"]
    actual = create_abf_workout(Path(database.name))
    assert actual == expected


@mock.patch("kettlebells.workouts.iterfzf")
def test_abfb(
    fzf_mock,
    options_mock,
    units_mock,
    confirm_mock,
    int_mock,
    database,
):
    """Test creating a armor building formula barbell workout."""
    expected = TEST_ABFB
    options_mock.side_effect = ["Program Three"]
    int_mock.side_effect = [
        32,  # time
        1,  # squat reps
        45,  # load
        1,  # sets at ^ load
        65,  # load
        1,  # sets at ^ load
        95,  # load
        3,  # sets at ^ load
        5,  # sets of curls
        45,  # load
        2,  # sets at ^ load
        55,  # load
        3,  # sets at ^ load
    ]
    units_mock.side_effect = ["kg"]
    confirm_mock.return_value = "n"
    fzf_mock.return_value = None
    actual = create_abf_barbell_workout(Path(database.name))
    assert isinstance(actual, Workout)
    assert actual == expected


def test_btb_workout(
    options_mock,
    units_mock,
    confirm_mock,
    int_mock,
    database,
):
    """Test creating a back to basics workout works as intended."""
    expected = TEST_BTB_WORKOUT
    options_mock.side_effect = ["2 C&P Ladders + Snatch"]
    int_mock.side_effect = [30, 24, 20]  # time, load, sets
    units_mock.return_value = "kg"
    actual = create_btb_workout(Path(database.name))
    assert isinstance(actual, Workout)
    assert actual == expected


def test_perfect_workout(
    options_mock,
    units_mock,
    int_mock,
    database,
):
    """Test creating a perfect."""
    expected = TEST_PERFECT_WORKOUT
    options_mock.side_effect = ["The Bull"]
    int_mock.side_effect = [10, 20, 24, 20, 20]  # time, press, BGBS, Row, GS
    units_mock.return_value = "kg"
    actual = create_perfect_workout(Path(database.name))
    assert isinstance(actual, Workout)
    assert actual == expected


@pytest.mark.parametrize(
    "workout_type, variation", [("custom", "custom"), (None, None)]
)
@mock.patch("kettlebells.workouts.iterfzf")
def test_create_custom_workout(
    fzf_mock,
    workout_type,
    variation,
    int_mock,
    prompt_mock,
    database,
):
    """Test creating a custom workout works as intended."""
    expected = TEST_CUSTOM_WORKOUT
    prompt_mock.side_effect = [workout_type, variation]
    fzf_mock.side_effect = ["Turkish Get-up", "TRX T", "Done"]
    # int_mocks = [time, load1, sets1, reps1, load2, sets2, reps3]
    int_mock.side_effect = [30, 24, 1, 6, 0, 3, 8]
    actual = create_custom_workout(Path(database.name))
    assert isinstance(actual, Workout)
    assert actual == expected


def test_set_progam_loads(int_mock, prompt_mock):
    """Test if setting program loads addes to loads dict."""
    prompt_mock.side_effect = ["the giant"]
    int_mock.side_effect = [24]
    loads = {
        "units": "kg",
        "bodyweight": 90,
        "light load": 20,
        "medium load": 24,
        "heavy load": 28,
    }
    expected = {
        "units": "kg",
        "bodyweight": 90,
        "light load": 20,
        "medium load": 24,
        "heavy load": 28,
        "the giant": 24,
    }
    actual = set_program_loads(loads)
    assert actual == expected


@mock.patch("kettlebells.workouts.iterfzf")
def test_create_giant_workout(
    iterfzf_mock, int_mock, prompt_mock, confirm_mock, database
):
    """Test creating a giant workout."""
    iterfzf_mock.return_value = None
    prompt_mock.side_effect = ["1", "1"]
    int_mock.side_effect = [1, 30, 10]
    confirm_mock.side_effect = "n"
    actual = create_time_based_workout(Path(database.name), "giant")
    assert actual == TEST_GIANT_WORKOUT


def test_create_wolf_workout(int_mock, prompt_mock, database):
    """Test creating a wolf workout."""
    prompt_mock.side_effect = ["1", "1"]
    int_mock.side_effect = [1, 12]
    actual = create_set_based_workout(Path(database.name), "wolf")
    assert actual == TEST_WOLF_WORKOUT


# def test_add_exercise_to_database(options_mock, database):
#     """Test adding an exercise to the database."""
#     options_mock.side_effect = ["squat", "Done"]
#     add_exercise_to_database(Path(database.name), "leg press")
#     db = json.load(open(database.name))
#     assert db["exercises"]["leg curl"] == ["lower body isolation"]


def _es_database(path):
    import json

    data = json.load(open(path))
    data["loads"]["bodyweight"] = 85
    data["templates"] = {
        "easy strength": {
            "regular": {
                "exercises": [
                    {"name": "Snatch Grip Deadlift", "load": 84, "sets": 2, "reps": 5},
                    {"name": "Dip", "load": 20, "sets": 3, "reps": 3},
                    {"name": "Ab Wheel", "load": 0, "sets": 1, "reps": 10},
                ]
            }
        }
    }
    data["saved_workouts"].append(
        {
            "date": "2026-11-09",
            "workout": {
                "workout_type": "easy strength",
                "variation": "D11",
                "time": 16,
                "units": "kg",
                "bodyweight": 85,
                "exercises": [
                    {"name": "Snatch Grip Deadlift", "load": 84, "sets": 2, "reps": 5},
                    {"name": "Chinup", "load": 11, "sets": 2, "reps": 5},
                    {"name": "Dip", "load": 20, "sets": 3, "reps": 3},
                ],
            },
        }
    )
    json.dump(data, open(path, "w"))


def test_repeat_last_workout(prompt_mock, int_mock, confirm_mock, database):
    """Enter keeps each value, typing replaces it, and - drops an exercise."""
    from kettlebells.workouts import repeat_last_workout

    _es_database(database.name)
    # variation, then one answer per exercise
    prompt_mock.side_effect = ["D12", "3x3@84", "-", "3x3+45lb"]
    int_mock.side_effect = [18]
    confirm_mock.ask.return_value = False
    workout = repeat_last_workout(Path(database.name), "es")
    assert prompt_mock.call_args_list[0].kwargs["default"] == "D12"
    assert [c.kwargs["default"] for c in prompt_mock.call_args_list[1:]] == ["2x5@84", "2x5+11", "3x3+20"]
    assert int_mock.call_args.kwargs["default"] == 16
    assert workout.workout_type == "easy strength"
    assert workout.variation == "D12"
    assert workout.time == 18
    assert [(e.name, e.sets, e.reps, e.load) for e in workout.exercises] == [
        ("Snatch Grip Deadlift", 3, 3, 84),
        ("Dip", 3, 3, 20),
    ]


def test_create_easy_strength_from_template(prompt_mock, int_mock, confirm_mock, database):
    """The template is applied as stored: no extra bodyweight on the dip."""
    from kettlebells.workouts import create_easy_strength_workout

    _es_database(database.name)
    prompt_mock.side_effect = lambda *args, default=None, **kwargs: default
    int_mock.side_effect = [30]
    confirm_mock.ask.return_value = False
    workout = create_easy_strength_workout(Path(database.name))
    assert workout.variation == "D12"
    dip = workout.exercises[1]
    assert (dip.name, dip.load, dip.total_load(85)) == ("Dip", 20, 101)


def test_create_from_template_missing(database, capfd):
    from kettlebells.workouts import create_from_template

    assert create_from_template(Path(database.name), "the bull") is None
    assert "No templates for the bull" in capfd.readouterr()[0]


def test_create_template_updates_existing(prompt_mock, confirm_mock, database):
    import json

    from kettlebells.workouts import create_template

    _es_database(database.name)
    prompt_mock.side_effect = ["es", "Regular", "2x5@90", "3x3+20", "1x10"]
    confirm_mock.ask.return_value = False
    create_template(Path(database.name))
    template = json.load(open(database.name))["templates"]["easy strength"]
    assert list(template) == ["regular"]
    assert template["regular"]["exercises"][0] == {
        "name": "Snatch Grip Deadlift",
        "load": 90,
        "sets": 2,
        "reps": 5,
    }


def test_display_bodyweight_and_notes(capfd):
    from kettlebells.workouts import Exercise

    workout = Workout(
        workout_type="easy strength",
        variation="D1",
        time=10,
        units="kg",
        bodyweight=85,
        notes="too light",
        exercises=[
            Exercise(name="Dip", load=20, sets=3, reps=3),
            Exercise(name="Chinup", load=0, sets=3, reps=3),
        ],
    )
    workout.display_workout()
    output = capfd.readouterr()[0]
    assert "3 X 3 with BW + 20 kg" in output
    assert "3 X 3 with BW\n" in output
    assert "Notes: too light" in output
    assert workout.calc_workout_stats()["weight moved"] == 9 * 101 + 9 * 81


def test_edit_workout(prompt_mock, int_mock, confirm_mock, database):
    from kettlebells.workouts import Exercise, edit_workout

    workout = Workout(
        workout_type="easy strength",
        variation="D1",
        time=10,
        units="kg",
        bodyweight=86,
        exercises=[Exercise(name="Dip", load=20, sets=3, reps=3)],
    )
    prompt_mock.side_effect = ["bad date", "2026-11-08", "Easy Strength", "D2", "3x5+20", "elbow hurts"]
    int_mock.side_effect = [12, 85]
    confirm_mock.ask.return_value = False
    date, edited = edit_workout(Path(database.name), "2026-11-09", workout)
    assert date == "2026-11-08"
    assert edited.workout_type == "easy strength"
    assert (edited.variation, edited.time, edited.bodyweight) == ("D2", 12, 85)
    assert edited.exercises[0].reps == 5
    assert edited.notes == "elbow hurts"
