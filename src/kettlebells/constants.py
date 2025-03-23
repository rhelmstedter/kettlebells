"""constants for kettlebells."""

from pathlib import Path

WARNING = "red"
SUGGESTION = "yellow"
FZF_DEFAULT_OPTS = "--height 13 --layout=reverse --border rounded --margin=2%,5%,10%,2%"
KETTLEBELLS_HOME = Path().home() / ".kettlebells"
KETTLEBELLS_DB = KETTLEBELLS_HOME / "kettlebells_db.json"
DATE_FORMAT = "%Y-%m-%d"
POUNDS_TO_KILOS_RATE = 0.45359237

IRON_CARDIO_PARAMS = {
    "bells": {"Single Bell": 4 / 6, "Double Bells": 2 / 6},
    "doublebell variations": {
        "Double Classic": 3 / 6,
        "Double Classic + Pullup": 2 / 6,
        "Double Traveling 2s": 1 / 6,
    },
    "singlebell variations": {
        "Classic": 6 / 12,
        "Classic + Pullup": 3 / 12,
        "Classic + Snatch": 2 / 12,
        "Traveling 2s": 1 / 12,
    },
    "times": {
        30: 1 / 6,
        20: 4 / 6,
        10: 1 / 6,
    },
    "loads": {
        "heavy load": 2 / 6,
        "medium load": 3 / 6,
        "light load": 1 / 6,
    },
    "swings": {True: 2 / 6, False: 4 / 6},
    "exercises": {
        "Classic": [
            ("Kettlebell Clean", 1),
            ("Kettlebell Press", 1),
            ("Kettlebell Front Squat", 1),
        ],
        "Classic + Pullup": [
            ("Kettlebell Clean", 1),
            ("Kettlebell Press", 1),
            ("Kettlebell Front Squat", 1),
            ("Pullup", 1),
        ],
        "Classic + Snatch": [
            ("Kettlebell Clean", 1),
            ("Kettlebell Press", 1),
            ("Kettlebell Front Squat", 1),
            ("Kettlebell Snatch", 1),
        ],
        "Traveling 2s": [
            ("Kettlebell Clean", 1),
            ("Kettlebell Press", 1),
            ("Kettlebell Front Squat", 1),
        ],
        "Double Classic": [
            ("Double Kettlebell Clean", 1),
            ("Double Kettlebell Press", 1),
            ("Double Kettlebell Front Squat", 1),
        ],
        "Double Classic + Pullup": [
            ("Double Kettlebell Clean", 1),
            ("Double Kettlebell Press", 1),
            ("Double Kettlebell Front Squat", 1),
            ("Pullup", 1),
        ],
        "Double Traveling 2s": [
            ("Double Kettlebell Clean", 1),
            ("Double Kettlebell Press", 1),
            ("Double Kettlebell Front Squat", 1),
        ],
    },
}

ABC_PARAMS = {
    "bells": {"Single Bell": 2 / 6, "Double Bells": 4 / 6},
    "doublebell variations": {"Armor Building Complex": 1},
    "singlebell variations": {"Armor Building Complex 2.0": 1},
    "times": {
        30: 1 / 10,
        25: 3 / 10,
        20: 3 / 10,
        15: 2 / 10,
        10: 1 / 10,
    },
    "loads": {
        "heavy load": 2 / 6,
        "medium load": 3 / 6,
        "light load": 1 / 6,
    },
    "swings": {True: 1 / 6, False: 5 / 6},
    "exercises": {
        "Armor Building Complex 2.0": [
            ("Kettlebell Clean", 2),
            ("Kettlebell Press", 2),
            ("Kettlebell Front Squat", 2),
        ],
        "Armor Building Complex": [
            ("Double Kettlebell Clean", 2),
            ("Double Kettlebell Press", 1),
            ("Double Kettlebell Front Squat", 3),
        ],
    },
}

BTB_PARAMS = {
    "2 C&P Ladders + Snatch": {
        "exercises": [
            {
                "name": "Kettlebell Clean and Press",
                "sets": 2,
                "reps": 20,
            },
            {
                "name": "Kettlebell Snatch",
                "sets": 1,
                "reps": 100,
            },
        ],
    },
    "3 C&P Ladders + Snatch": {
        "exercises": [
            {
                "name": "Kettlebell Clean and Press",
                "sets": 3,
                "reps": 20,
            },
            {
                "name": "Kettlebell Snatch",
                "sets": 1,
                "reps": 80,
            },
        ],
    },
    "5 C&P Ladders + Snatch": {
        "exercises": [
            {
                "name": "Kettlebell Clean and Press",
                "sets": 5,
                "reps": 20,
            },
            {
                "name": "Kettlebell Snatch",
                "sets": 1,
                "reps": 60,
            },
        ],
    },
    "2 C&P Ladders + Squats": {
        "exercises": [
            {
                "name": "Kettlebell Clean and Press",
                "sets": 2,
                "reps": 20,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "sets": 2,
                "reps": 10,
            },
        ],
    },
    "3 C&P Ladders + Squats": {
        "exercises": [
            {
                "name": "Kettlebell Clean and Press",
                "sets": 3,
                "reps": 20,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "sets": 3,
                "reps": 10,
            },
        ],
    },
    "5 C&P Ladders + Squats": {
        "exercises": [
            {
                "name": "Kettlebell Clean and Press",
                "sets": 5,
                "reps": 20,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "sets": 5,
                "reps": 10,
            },
        ],
    },
}

PW_PARAMS = {
    "Original": {
        "exercises": [
            {
                "name": "Half-kneeling Kettlebell Press",
                "sets": 3,
                "reps": 16,
            },
            {
                "name": "Hanging Leg Raise",
                "sets": 3,
                "reps": 8,
                "load": 0,
            },
            {
                "name": "Banded Hip Thrust",
                "sets": 3,
                "reps": 15,
            },
            {
                "name": "Bulgarian Goat Bag Swing",
                "sets": 3,
                "reps": 8,
            },
            {
                "name": "Goblet Squat",
                "sets": 1,
                "reps": 8,
            },
            {
                "name": "Broomstick Overhead Squat",
                "sets": 1,
                "reps": 8,
                "load": 0,
            },
        ],
    },
    "Indoor": {
        "exercises": [
            {
                "name": "Half-kneeling Kettlebell Press",
                "sets": 3,
                "reps": 16,
            },
            {
                "name": "Hanging Leg Raise",
                "sets": 3,
                "reps": 8,
                "load": 0,
            },
            {
                "name": "Hip Thrust",
                "sets": 1,
                "reps": 120,
            },
            {
                "name": "Clam Shell",
                "sets": 1,
                "reps": 120,
            },
            {
                "name": "Goblet Squat",
                "sets": 1,
                "reps": 8,
            },
            {
                "name": "Broomstick Overhead Squat",
                "sets": 1,
                "reps": 8,
                "load": 0,
            },
        ],
    },
    "The Bull": {
        "exercises": [
            {
                "name": "Half-kneeling Kettlebell Press",
                "sets": 3,
                "reps": 16,
            },
            {
                "name": "Hanging Leg Raise",
                "sets": 3,
                "reps": 8,
                "load": 0,
            },
            {
                "name": "Bulgarian Goat Bag Swing",
                "sets": 3,
                "reps": 8,
            },
            {
                "name": "Kettlebell Bent Over Row",
                "sets": 3,
                "reps": 16,
            },
            {
                "name": "Goblet Squat",
                "sets": 1,
                "reps": 8,
            },
            {
                "name": "Broomstick Overhead Squat",
                "sets": 1,
                "reps": 8,
                "load": 0,
            },
        ],
    },
}

THE_GIANT_PARAMS = {
    "The Giant 1.0": {
        "W1D1": [
            {
                "name": "Double Kettlebell Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 5,
            },
        ],
        "W1D2": [
            {
                "name": "Double Kettlebell Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 6,
            },
        ],
        "W1D3": [
            {
                "name": "Double Kettlebell Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 4,
            },
        ],
        "W2D1": [
            {
                "name": "Double Kettlebell Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 5,
            },
        ],
        "W2D2": [
            {
                "name": "Double Kettlebell Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 6,
            },
        ],
        "W2D3": [
            {
                "name": "Double Kettlebell Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 4,
            },
        ],
        "W3D1": [
            {
                "name": "Double Kettlebell Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 5,
            },
        ],
        "W3D2": [
            {
                "name": "Double Kettlebell Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 6,
            },
        ],
        "W3D3": [
            {
                "name": "Double Kettlebell Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 4,
            },
        ],
        "W4D1": [
            {
                "name": "Double Kettlebell Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 5,
            },
        ],
        "W4D2": [
            {
                "name": "Double Kettlebell Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 6,
            },
        ],
        "W4D3": [
            {
                "name": "Double Kettlebell Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 4,
            },
        ],
    },
}

THE_WOLF_PARAMS = {
    "The Wolf": {
        "W1D1": [
            {
                "name": "Kettlebell Snatch",
                "load": 0,
                "sets": 3,
                "reps": 10,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Press",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Clean",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
        ],
        "W1D2": [
            {
                "name": "Double Kettlebell Clean",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Press",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Clean",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
        ],
        "W1D3": [
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Press",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Clean",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
        ],
        "W2D1": [
            {
                "name": "Kettlebell Snatch",
                "load": 0,
                "sets": 4,
                "reps": 10,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Press",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Clean",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
        ],
        "W2D2": [
            {
                "name": "Double Kettlebell Clean",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Press",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Clean",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
        ],
        "W2D3": [
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Press",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Clean",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
        ],
        "W3D1": [
            {
                "name": "Kettlebell Snatch",
                "load": 0,
                "sets": 5,
                "reps": 10,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Press",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Clean",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
        ],
        "W3D2": [
            {
                "name": "Double Kettlebell Clean",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Press",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Clean",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
        ],
        "W3D3": [
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Press",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Clean",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
        ],
        "W4D1": [
            {
                "name": "Kettlebell Snatch",
                "load": 0,
                "sets": 3,
                "reps": 10,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Press",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Clean",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
        ],
        "W4D2": [
            {
                "name": "Double Kettlebell Clean",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Press",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Clean",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
        ],
        "W4D3": [
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Press",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Clean",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
        ],
        "W5D1": [
            {
                "name": "Kettlebell Snatch",
                "load": 0,
                "sets": 4,
                "reps": 10,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Press",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Clean",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
        ],
        "W5D2": [
            {
                "name": "Double Kettlebell Clean",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Press",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Clean",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
        ],
        "W5D3": [
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Press",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Clean",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
        ],
        "W6D1": [
            {
                "name": "Kettlebell Snatch",
                "load": 0,
                "sets": 5,
                "reps": 10,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Press",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Clean",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
        ],
        "W6D2": [
            {
                "name": "Double Kettlebell Clean",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Press",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Clean",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
        ],
        "W6D3": [
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Press",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Clean",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
        ],
    },
}

WORKOUT_GENERATOR_PARAMS = {
    "3 X 8": {
        "sets": 3,
    },
    "3 X 10": {
        "sets": 3,
    },
    "3 X 12": {
        "sets": 3,
    },
    "30/30 For 30": {
        "time": 30,
        "sets": 6,
    },
}

ABFB_PARAMS = {
    "variations": ["Program One", "Program Two", "Program Three"],
    "exercises": {
        "Clean and Press": {
            "reps": 8,
            "sets": 5,
        },
        "Curl": {
            "reps": 8,
            "sets": 5,
        },
    },
}

ABF_PARAMS = {
    "Armor Building Complex": ABC_PARAMS["exercises"]["Armor Building Complex"],
    "Double Kettlebell Press": [
        ("Double Kettlebell Press", 2),
        ("Double Kettlebell Press", 3),
        ("Double Kettlebell Press", 5),
        ("Double Kettlebell Press", 10),
    ],
}


EASY_STRENGTH_PARAMS = {
    "regular": {
        "exercises": [
            {
                "name": "Deadlift",
                "sets": 3,
                "reps": 3,
                "load": 102,
            },
            {
                "name": "Double Kettlebell Press",
                "sets": 5,
                "reps": 2,
                "load": 32,
            },
            {
                "name": "Chinup",
                "sets": 3,
                "reps": 3,
                "load": 0,
            },
            {
                "name": "Ab Wheel",
                "sets": 1,
                "reps": 10,
                "load": 0,
            },
        ],
    },
    "light": {
        "exercises": [
            {
                "name": "Deadlift",
                "sets": 1,
                "reps": 10,
                "load": 86,
            },
            {
                "name": "Double Kettlebell Press",
                "sets": 1,
                "reps": 10,
                "load": 24,
            },
            {
                "name": "TRX I",
                "sets": 1,
                "reps": 5,
                "load": 0,
            },
            {
                "name": "TRX Y",
                "sets": 1,
                "reps": 5,
                "load": 0,
            },
            {
                "name": "TRX T",
                "sets": 1,
                "reps": 5,
                "load": 0,
            },
            {
                "name": "TRX High Pull",
                "sets": 1,
                "reps": 5,
                "load": 0,
            },
            {
                "name": "TRX Row",
                "sets": 1,
                "reps": 5,
                "load": 0,
            },
            {
                "name": "Ab Wheel",
                "sets": 1,
                "reps": 5,
                "load": 0,
            },
            {
                "name": "Hanging Leg Raise",
                "sets": 1,
                "reps": 5,
                "load": 0,
            },
        ],
    },
}

ROP_PARAMS = {
    "Heavy": {
        "exercises": [
            "Kettlebell Clean and Press",
            "Pullup",
            "Kettlebell Swing",
            "Done",
        ],
    },
    "Medium": {
        "exercises": [
            "Kettlebell Clean and Press",
            "Pullup",
            "Kettlebell Swing",
            "Done",
        ],
    },
    "Light": {
        "exercises": [
            "Kettlebell Clean and Press",
            "Pullup",
            "Kettlebell Snatch",
            "Done",
        ],
    },
}

DFW_PARAMS = {
    "dry fighting weight": {
        "W1D1": [
            {
                "name": "Double Kettlebell Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": [1, 2, 3],
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 0,
                "reps": [1, 2, 3],
            },
        ],
        "W1D2": [
            {
                "name": "Double Kettlebell Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 1,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 0,
                "reps": 1,
            },
        ],
        "W1D3": [
            {
                "name": "Double Kettlebell Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 2,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 0,
                "reps": 2,
            },
        ],
        "W2D1": [
            {
                "name": "Double Kettlebell Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": [1, 2, 3],
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 0,
                "reps": [1, 2, 3],
            },
        ],
        "W2D2": [
            {
                "name": "Double Kettlebell Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 1,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 0,
                "reps": 1,
            },
        ],
        "W2D3": [
            {
                "name": "Double Kettlebell Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 3,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 0,
                "reps": 3,
            },
        ],
        "W3D1": [
            {
                "name": "Double Kettlebell Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": [1, 2, 3, 4],
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 0,
                "reps": [1, 2, 3, 4],
            },
        ],
        "W3D2": [
            {
                "name": "Double Kettlebell Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 2,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 0,
                "reps": 2,
            },
        ],
        "W3D3": [
            {
                "name": "Double Kettlebell Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 3,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 0,
                "reps": 3,
            },
        ],
        "W4D1": [
            {
                "name": "Double Kettlebell Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": [1, 2, 3, 4, 5],
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 0,
                "reps": [1, 2, 3, 4, 5],
            },
        ],
        "W4D2": [
            {
                "name": "Double Kettlebell Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 2,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 0,
                "reps": 2,
            },
        ],
        "W4D3": [
            {
                "name": "Double Kettlebell Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 2,
            },
            {
                "name": "Double Kettlebell Front Squat",
                "load": 0,
                "sets": 0,
                "reps": 2,
            },
        ],
    },
}

EXERCISES = {
    "Kettlebell Press": ["push"],
    "Kettlebell Clean and Press": ["hinge", "push", "pull"],
    "Kettlebell Clean": ["hinge", "pull"],
    "Goblet Squat": ["squat"],
    "Swing": ["hinge"],
    "Kettlebell Swing": ["hinge"],
    "Ab Wheel": ["core"],
    "Arch Body Leglift": ["core"],
    "Plank Shoulder Tap": ["core"],
    "Banded Hip Thrust": ["hinge"],
    "Bent Over Row": ["pull"],
    "Kettlebell Bent Over Row": ["pull"],
    "Hands Elevated Pike Pushup": ["push"],
    "Arch Body Leg Lift": ["core"],
    "Side Plank Lift": ["core"],
    "Bent Press": ["hinge", "push"],
    "Bird Dog": ["core"],
    "Bodyweight Row": ["pull"],
    "Bodyweight Squat": ["squat"],
    "Broomstick Overhead Squat": ["squat"],
    "Bulgarian Goat Bag Swing": ["hinge"],
    "Chinup": ["pull"],
    "Clean and Press": ["hinge", "push", "pull"],
    "Clean": ["hinge", "pull"],
    "Curl": ["upper body isolation"],
    "Lateral Raise": ["upper body isolation"],
    "Shrimp Squat": ["squat"],
    "Overhead Squat": ["squat"],
    "Overhead Box Squat": ["squat"],
    "TRX Shrimp Squat": ["squat"],
    "TRX Jump Squat": ["squat"],
    "One Arm Swing": ["hinge"],
    "Deadlift": ["hinge"],
    "Dip": ["push"],
    "Anchor Squat": ["squat"],
    "Done": [None],
    "Double Clean and Press": ["hinge", "push", "pull"],
    "Double Bent Over Row": ["pull"],
    "Double Clean": ["hinge", "pull"],
    "Double Deadlift": ["hinge"],
    "Double Front Squat": ["squat"],
    "Double Jerk": ["push"],
    "Double Press": ["push"],
    "Double Push Press": ["push"],
    "Double Split Squat": ["squat"],
    "Double Swing": ["hinge"],
    "Double Kettlebell Clean and Press": ["hinge", "push", "pull"],
    "Double Kettlebell Bent Over Row": ["pull"],
    "Double Kettlebell Clean": ["hinge"],
    "Double Kettlebell Deadlift": ["hinge"],
    "Double Kettlebell Front Squat": ["squat"],
    "Double Kettlebell Jerk": ["push"],
    "Double Kettlebell Press": ["push"],
    "Double Kettlebell Push Press": ["push"],
    "Double Kettlebell Split Squat": ["squat"],
    "Double Kettlebell Swing": ["hinge"],
    "Racked Kettlebell Squat": ["squat"],
    "Front Squat": ["squat"],
    "Half-kneeling Kettlebell Press": ["push"],
    "Half-kneeling Press": ["push"],
    "Hanging Leg Raise": ["core"],
    "Hip Thrust": ["hinge"],
    "Hollow Body Rock": ["core"],
    "Jerk": ["push"],
    "Lateral Squat": ["squat"],
    "Other": [None],
    "Pike Pushup": ["push"],
    "Pistol Squat": ["squat"],
    "Pullup": ["pull"],
    "Press": ["push"],
    "Push Press": ["push"],
    "Pushup Position Plank": ["core"],
    "Pushup": ["push"],
    "Renegade Row": ["pull"],
    "Scapular Push Up": ["core"],
    "Side Plank Hip Lift": ["core"],
    "Side Plank": ["core"],
    "Side Lift": ["core"],
    "Single Leg Deadlift": ["hinge"],
    "Kettlebell Snatch": ["hinge", "pull"],
    "Snatch": ["hinge", "pull"],
    "Split Squat": ["squat"],
    "TRX Advanced Row": ["pull"],
    "TRX Bicep Curl": ["upper body isolation"],
    "TRX I": ["pull"],
    "TRX Pushup": ["push"],
    "TRX Row": ["pull"],
    "TRX Single Arm Row": ["pull"],
    "TRX T": ["pull"],
    "TRX Y": ["pull"],
    "TRX Fly": ["upper body isolation"],
    "Thruster": ["squat", "push"],
    "Toes to Bar": ["core"],
    "Turkish Get-up": ["squat", "core"],
    "Windmill": ["core"],
    "Leg Press": ["squat"],
}

HUMAN_MOVEMENTS = [
    "push",
    "pull",
    "squat",
    "hinge",
    "core",
    "upper body isolation",
    "lower body isolation",
    "done",
]

BODYWEIGHT_FACTORS = {
    "Bodyweight Row": 0.5,
    "Chinup": 0.96,
    "Dip": 0.96,
    "Pike Pushup": 0.64,
    "Pullup": 0.96,
    "Pushup": 0.64,
    "TRX Advanced Row": 0.64,
    "TRX Pushup": 0.5,
    "TRX Row": 0.3,
}
