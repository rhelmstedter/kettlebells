import copy

import pytest

from kettlebells.entry import EntryError, format_spec, parse_entry, parse_lines, parse_spec
from kettlebells.names import bump_variation, normalize_exercise_name, normalize_workout_type, resolve_exercise

from .test_constants import TEST_DATA


@pytest.fixture
def data():
    data = copy.deepcopy(TEST_DATA)
    data["loads"]["bodyweight"] = 85
    data["saved_workouts"].append(
        {
            "date": "2026-11-05",
            "workout": {
                "workout_type": "easy strength",
                "variation": "D10",
                "time": 37,
                "units": "kg",
                "bodyweight": 85,
                "exercises": [{"name": "Snatch Grip Deadlift", "load": 84, "sets": 3, "reps": 3}],
            },
        }
    )
    return data


@pytest.mark.parametrize(
    "text, expected",
    [
        ("3x5", (3, 5, 0)),
        ("3x5@24", (3, 5, 24)),
        ("3 x 5 @ 24kg", (3, 5, 24)),
        ("2x5@185lb", (2, 5, 84)),
        ("2x5+25lb", (2, 5, 11)),
        ("3x3+45lbs", (3, 3, 20)),
        ("1x10@bw", (1, 10, 0)),
    ],
)
def test_parse_spec(text, expected):
    assert parse_spec(text, "kg") == expected


def test_parse_spec_kg_to_lb():
    assert parse_spec("1x5@32kg", "lbs") == (1, 5, 71)


def test_parse_spec_bad():
    with pytest.raises(EntryError):
        parse_spec("five by five", "kg")


def test_format_spec_round_trips():
    assert format_spec("Dip", 3, 3, 20) == "3x3+20"
    assert format_spec("Deadlift", 2, 5, 84) == "2x5@84"
    assert format_spec("Ab Wheel", 1, 10, 0) == "1x10"
    assert parse_spec(format_spec("Dip", 3, 3, 20), "kg") == (3, 3, 20)


def test_parse_entry(data):
    workout = parse_entry(
        "ES D11 16min; SGD 2x5@185lb; Chin 2x5+25lb; Dip 3x3+45lb (elbow hurts); AW 1x10; note: HARD!",
        data,
    )
    assert workout["workout_type"] == "easy strength"
    assert workout["variation"] == "D11"
    assert workout["time"] == 16
    assert workout["bodyweight"] == 85
    assert workout["exercises"] == [
        {"name": "Snatch Grip Deadlift", "sets": 2, "reps": 5, "load": 84},
        {"name": "Chinup", "sets": 2, "reps": 5, "load": 11},
        {"name": "Dip", "sets": 3, "reps": 3, "load": 20},
        {"name": "Ab Wheel", "sets": 1, "reps": 10, "load": 0},
    ]
    assert workout["notes"] == "Dip: elbow hurts; HARD!"


def test_parse_entry_bumps_missing_variation(data):
    assert parse_entry("es 20 min; AW 1x10", data)["variation"] == "D11"


def test_parse_entry_user_alias(data):
    data["aliases"]["exercises"]["zz"] = "Goblet Squat"
    assert parse_entry("Custom 10min; ZZ 3x5@24", data)["exercises"][0]["name"] == "Goblet Squat"


@pytest.mark.parametrize(
    "text, message",
    [
        ("ES D11; AW 1x10", "duration"),
        ("ES 10min", "no exercises"),
        ("ES 10min; Mystery Lift 3x5", "Unknown exercise"),
        ("ES 10min; AW lots", "should look like"),
    ],
)
def test_parse_entry_errors(text, message, data):
    with pytest.raises(EntryError, match=message):
        parse_entry(text, data)


def test_parse_lines_counts_days(data):
    lines = [
        "# my notes",
        "",
        "2026-11-09 ES 16min; AW 1x10",
        "2026-11-11 ES 18min; AW 1x10",
    ]
    parsed = parse_lines(lines, data)
    assert [(d, w["variation"]) for d, w in parsed] == [("2026-11-09", "D11"), ("2026-11-11", "D12")]
    assert len(data["saved_workouts"]) == 3  # the caller's data is untouched


def test_parse_lines_bad_date(data):
    with pytest.raises(EntryError, match="Line 1"):
        parse_lines(["11/09/2026 ES 16min; AW 1x10"], data)


@pytest.mark.parametrize(
    "variation, expected",
    [("D10", "D11"), ("09", "10"), ("W2D3", "W2D4"), ("The Bull", "The Bull"), ("D9", "D10")],
)
def test_bump_variation(variation, expected):
    assert bump_variation(variation) == expected


@pytest.mark.parametrize(
    "name, expected",
    [
        ("Trx Tricep Extension", "TRX Tricep Extension"),
        ("Overhead Tricep Extention", "Overhead Tricep Extension"),
        ("  Arch  Body Leglift ", "Arch Body Leg Lift"),
        ("Deadlift", "Deadlift"),
    ],
)
def test_normalize_exercise_name(name, expected):
    assert normalize_exercise_name(name) == expected


def test_normalize_workout_type():
    data = {
        "saved_workouts": [
            {"workout": {"workout_type": "Strong On", "exercises": []}},
            {"workout": {"workout_type": "Strong On", "exercises": []}},
            {"workout": {"workout_type": "strong on", "exercises": []}},
        ]
    }
    assert normalize_workout_type("Easy Strength", data) == "easy strength"
    assert normalize_workout_type("Strong On!", data) == "Strong On"
    assert normalize_workout_type("STRONG ON", data) == "Strong On"
    assert normalize_workout_type("55x5", data) == "5x5"
    assert normalize_workout_type("Brand New", data) == "Brand New"


def test_resolve_exercise_case_insensitive(data):
    assert resolve_exercise("goblet squat", data) == "Goblet Squat"
    assert resolve_exercise("sgd", data) == "Snatch Grip Deadlift"
