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
        "Classic": [("Clean", 1), ("Press", 1), ("Front Squat", 1)],
        "Classic + Pullup": [
            ("Clean", 1),
            ("Press", 1),
            ("Front Squat", 1),
            ("Pullup", 1),
        ],
        "Classic + Snatch": [
            ("Clean", 1),
            ("Press", 1),
            ("Front Squat", 1),
            ("Snatch", 1),
        ],
        "Traveling 2s": [("Clean", 1), ("Press", 1), ("Front Squat", 1)],
        "Double Classic": [
            ("Double Clean", 1),
            ("Double Press", 1),
            ("Double Front Squat", 1),
        ],
        "Double Classic + Pullup": [
            ("Double Clean", 1),
            ("Double Press", 1),
            ("Double Front Squat", 1),
            ("Pullup", 1),
        ],
        "Double Traveling 2s": [
            ("Double Clean", 1),
            ("Double Press", 1),
            ("Double Front Squat", 1),
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
        "Armor Building Complex 2.0": [("Clean", 2), ("Press", 2), ("Front Squat", 2)],
        "Armor Building Complex": [
            ("Double Clean", 2),
            ("Double Press", 1),
            ("Double Front Squat", 3),
        ],
    },
}

BTB_PARAMS = {
    "2 C&P Ladders + Snatch": {
        "exercises": [
            {
                "name": "Clean and Press",
                "sets": 2,
                "reps": 20,
            },
            {
                "name": "Snatch",
                "sets": 1,
                "reps": 100,
            },
        ],
    },
    "3 C&P Ladders + Snatch": {
        "exercises": [
            {
                "name": "Clean and Press",
                "sets": 3,
                "reps": 20,
            },
            {
                "name": "Snatch",
                "sets": 1,
                "reps": 80,
            },
        ],
    },
    "5 C&P Ladders + Snatch": {
        "exercises": [
            {
                "name": "Clean and Press",
                "sets": 5,
                "reps": 20,
            },
            {
                "name": "Snatch",
                "sets": 1,
                "reps": 60,
            },
        ],
    },
    "2 C&P Ladders + Squats": {
        "exercises": [
            {
                "name": "Clean and Press",
                "sets": 2,
                "reps": 20,
            },
            {
                "name": "Double Front Squat",
                "sets": 2,
                "reps": 10,
            },
        ],
    },
    "3 C&P Ladders + Squats": {
        "exercises": [
            {
                "name": "Clean and Press",
                "sets": 3,
                "reps": 20,
            },
            {
                "name": "Double Front Squat",
                "sets": 3,
                "reps": 10,
            },
        ],
    },
    "5 C&P Ladders + Squats": {
        "exercises": [
            {
                "name": "Clean and Press",
                "sets": 5,
                "reps": 20,
            },
            {
                "name": "Double Front Squat",
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
                "name": "Half-kneeling Press",
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
                "name": "Broomstick Overhead Sqaut",
                "sets": 1,
                "reps": 8,
                "load": 0,
            },
        ],
    },
    "Indoor": {
        "exercises": [
            {
                "name": "Half-kneeling Press",
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
                "name": "Broomstick Overhead Sqaut",
                "sets": 1,
                "reps": 8,
                "load": 0,
            },
        ],
    },
    "The Bull": {
        "exercises": [
            {
                "name": "Half-kneeling Press",
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
                "name": "Bent Over Row",
                "sets": 3,
                "reps": 16,
            },
            {
                "name": "Goblet Squat",
                "sets": 1,
                "reps": 8,
            },
            {
                "name": "Broomstick Overhead Sqaut",
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
                "name": "Double Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 5,
            },
        ],
        "W1D2": [
            {
                "name": "Double Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 6,
            },
        ],
        "W1D3": [
            {
                "name": "Double Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 4,
            },
        ],
        "W2D1": [
            {
                "name": "Double Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 5,
            },
        ],
        "W2D2": [
            {
                "name": "Double Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 6,
            },
        ],
        "W2D3": [
            {
                "name": "Double Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 4,
            },
        ],
        "W3D1": [
            {
                "name": "Double Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 5,
            },
        ],
        "W3D2": [
            {
                "name": "Double Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 6,
            },
        ],
        "W3D3": [
            {
                "name": "Double Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 4,
            },
        ],
        "W4D1": [
            {
                "name": "Double Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 5,
            },
        ],
        "W4D2": [
            {
                "name": "Double Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 6,
            },
        ],
        "W4D3": [
            {
                "name": "Double Clean and Press",
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
                "name": "Snatch",
                "load": 0,
                "sets": 3,
                "reps": 10,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Press",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Clean",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
        ],
        "W1D2": [
            {
                "name": "Double Clean",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Press",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Clean",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
        ],
        "W1D3": [
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Press",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Clean",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
        ],
        "W2D1": [
            {
                "name": "Snatch",
                "load": 0,
                "sets": 4,
                "reps": 10,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Press",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Clean",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
        ],
        "W2D2": [
            {
                "name": "Double Clean",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Press",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Clean",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
        ],
        "W2D3": [
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Press",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Clean",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
        ],
        "W3D1": [
            {
                "name": "Snatch",
                "load": 0,
                "sets": 5,
                "reps": 10,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Press",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Clean",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
        ],
        "W3D2": [
            {
                "name": "Double Clean",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Press",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Clean",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
        ],
        "W3D3": [
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Press",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Clean",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
        ],
        "W4D1": [
            {
                "name": "Snatch",
                "load": 0,
                "sets": 3,
                "reps": 10,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Press",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Clean",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
        ],
        "W4D2": [
            {
                "name": "Double Clean",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Press",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Clean",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
        ],
        "W4D3": [
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Press",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Clean",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 3,
                "reps": 5,
            },
        ],
        "W5D1": [
            {
                "name": "Snatch",
                "load": 0,
                "sets": 4,
                "reps": 10,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Press",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Clean",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
        ],
        "W5D2": [
            {
                "name": "Double Clean",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Press",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Clean",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
        ],
        "W5D3": [
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Press",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Clean",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 4,
                "reps": 5,
            },
        ],
        "W6D1": [
            {
                "name": "Snatch",
                "load": 0,
                "sets": 5,
                "reps": 10,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Press",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Clean",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
        ],
        "W6D2": [
            {
                "name": "Double Clean",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Press",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Clean",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
        ],
        "W6D3": [
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Press",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Clean",
                "load": 0,
                "sets": 5,
                "reps": 5,
            },
            {
                "name": "Double Front Squat",
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
    "Double Press": [
        ("Double Press", 2),
        ("Double Press", 3),
        ("Double Press", 5),
        ("Double Press", 10),
    ],
}


EASY_STRENGTH_PARAMS = {
    "regular": {
        "exercises": [
            {
                "name": "Goblet Squat",
                "sets": 1,
                "reps": 10,
                "load": 32,
            },
            {
                "name": "Swing",
                "sets": 5,
                "reps": 15,
                "load": 32,
            },
            {
                "name": "Dip",
                "sets": 2,
                "reps": 5,
                "load": 12,
            },
            {
                "name": "Double Front Squat",
                "sets": 2,
                "reps": 5,
                "load": 28,
            },
            {
                "name": "Bent Over Row",
                "sets": 2,
                "reps": 10,
                "load": 32,
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
                "name": "Goblet Squat",
                "sets": 1,
                "reps": 10,
                "load": 24,
            },
            {
                "name": "Swing",
                "sets": 3,
                "reps": 15,
                "load": 24,
            },
            {
                "name": "Dip",
                "sets": 1,
                "reps": 10,
                "load": 0,
            },
            {
                "name": "Double Front Squat",
                "sets": 1,
                "reps": 10,
                "load": 24,
            },
            {
                "name": "Bent Over Row",
                "sets": 1,
                "reps": 20,
                "load": 24,
            },
            {
                "name": "Ab Wheel",
                "sets": 1,
                "reps": 10,
                "load": 0,
            },
        ],
    },
}

ROP_PARAMS = {
    "Heavy": {
        "exercises": [
            "Clean and Press",
            "Pullup",
            "Swing",
            "Done",
        ],
    },
    "Medium": {
        "exercises": [
            "Clean and Press",
            "Pullup",
            "Swing",
            "Done",
        ],
    },
    "Light": {
        "exercises": [
            "Clean and Press",
            "Pullup",
            "Snatch",
            "Done",
        ],
    },
}

DFW_PARAMS = {
    "dry fighting weight": {
        "W1D1": [
            {
                "name": "Double Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": [1, 2, 3],
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 0,
                "reps": [1, 2, 3],
            },
        ],
        "W1D2": [
            {
                "name": "Double Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 1,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 0,
                "reps": 1,
            },
        ],
        "W1D3": [
            {
                "name": "Double Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 2,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 0,
                "reps": 2,
            },
        ],
        "W2D1": [
            {
                "name": "Double Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": [1, 2, 3],
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 0,
                "reps": [1, 2, 3],
            },
        ],
        "W2D2": [
            {
                "name": "Double Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 1,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 0,
                "reps": 1,
            },
        ],
        "W2D3": [
            {
                "name": "Double Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 3,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 0,
                "reps": 3,
            },
        ],
        "W3D1": [
            {
                "name": "Double Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": [1, 2, 3, 4],
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 0,
                "reps": [1, 2, 3, 4],
            },
        ],
        "W3D2": [
            {
                "name": "Double Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 2,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 0,
                "reps": 2,
            },
        ],
        "W3D3": [
            {
                "name": "Double Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 3,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 0,
                "reps": 3,
            },
        ],
        "W4D1": [
            {
                "name": "Double Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": [1, 2, 3, 4, 5],
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 0,
                "reps": [1, 2, 3, 4, 5],
            },
        ],
        "W4D2": [
            {
                "name": "Double Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 2,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 0,
                "reps": 2,
            },
        ],
        "W4D3": [
            {
                "name": "Double Clean and Press",
                "load": 0,
                "sets": 0,
                "reps": 2,
            },
            {
                "name": "Double Front Squat",
                "load": 0,
                "sets": 0,
                "reps": 2,
            },
        ],
    },
}

EXERCISES = [
    "Ab Wheel",
    "Arch Body Leg Lift",
    "Banded Hip Thrust",
    "Bent Over Row",
    "Bent Press",
    "Bird Dog",
    "Bodyweight Row",
    "Bodyweight Squat",
    "Broomstick Overhead Squat",
    "Bulgarian Goat Bag Swing",
    "Chinup",
    "Clean and Press",
    "Clean",
    "Curl",
    "Deadlift",
    "Dip",
    "Done",
    "Double Bent Over Row",
    "Double Clean and Press",
    "Double Clean",
    "Double Deadlift",
    "Double Front Squat",
    "Double Jerk",
    "Double Press",
    "Double Push Press",
    "Double Split Squat",
    "Double Swing",
    "Front Squat",
    "Goblet Squat",
    "Half-kneeling Press",
    "Hanging Leg Raise",
    "Hip Thrust",
    "Hollow Body Rock",
    "Jerk",
    "Lateral Squat",
    "Other",
    "Pike Pushup",
    "Pistol Squat",
    "Press",
    "Pullup",
    "Push Press",
    "Pushup Position Plank",
    "Pushup",
    "Renegade Row",
    "Scapular Push Up",
    "Side Plank Hip Lift",
    "Side Plank",
    "Single Leg Deadlift",
    "Snatch",
    "Split Squat",
    "Swing",
    "TRX Advanced Row",
    "TRX Bicep Curl",
    "TRX I",
    "TRX Pushup",
    "TRX Row",
    "TRX Single Arm Row",
    "TRX T",
    "TRX Y",
    "Thruster",
    "Toes to Bar",
    "Turkish Get-up",
    "Windmill",
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
