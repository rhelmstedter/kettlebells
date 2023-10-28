"""constants for kettlebells."""

from pathlib import Path

WARNING = "red"
SUGGESTION = "yellow"

KETTLEBELLS_HOME = Path().home() / ".kettlebells"
KETTLEBELLS_DB = KETTLEBELLS_HOME / "kettlebells_db.json"

DATE_FORMAT = "%Y-%m-%d"

IRON_CARDIO_PARAMS = {
    "bells": {"Single Bell": 4 / 6, "Double Bells": 2 / 6},
    "doublebell variations": {
        "Double Classic": 4 / 6,
        "Double Classic + Pullup": 2 / 6,
    },
    "singlebell variations": {
        "Classic": 3 / 6,
        "Classic + Pullup": 2 / 6,
        "Classic + Snatch": 1 / 6,
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
    },
}

ABC_PARAMS = {
    "bells": {"Single Bell": 2 / 6, "Double Bells": 4 / 6},
    "doublebell variations": {"Armor Building Complex": 1},
    "singlebell variations": {"Armor Building Complex 2.0": 1},
    "times": {
        25: 1 / 6,
        20: 2 / 6,
        15: 2 / 6,
        10: 1 / 6,
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
                "name": "Banded Hip Thrust",
                "sets": 3,
                "reps": 15,
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

EXERCISES = [
    "Ab Wheel",
    "Banded Hip Thrust",
    "Bent Over Row",
    "Bent Press",
    "Bodyweight Row",
    "Bodyweight Squat",
    "Broomstick Overhead Squat",
    "Bulgarian Goat Bag Swing",
    "Clean and Press",
    "Clean",
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
    "Jerk",
    "Other",
    "Pistol Squat",
    "Press",
    "Pull-up",
    "Push Press",
    "Push-up",
    "Renegade Row",
    "Snatch",
    "Split Squat",
    "Swing",
    "TRX Advanced Row",
    "TRX I",
    "TRX Row",
    "TRX Single Arm Row",
    "TRX T",
    "TRX Y",
    "Thruster",
    "Toes to Bar",
    "Turkish Get-up",
    "Weighted Dip",
    "Weighted Pull-up",
    "Windmill",
]
