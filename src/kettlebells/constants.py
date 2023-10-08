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
