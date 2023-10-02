"""constants for iron cardio session parameters."""

from pathlib import Path

WARNING = "red"
SUGGESTION = "yellow"

KETTLEBELLS_HOME = Path().home() / ".kettlebells"
KETTLEBELLS_DB = KETTLEBELLS_HOME / "kettlebells_db.json"

DATE_FORMAT = "%Y-%m-%d"


IRON_CARDIO_PARAMS = {
    "bells": {"Single Bell": 4 / 6, "Double Bells": 2 / 6},
    "doublebell variations": {
        "Double Classic": 3 / 6,
        "Double Traveling 2s": 1 / 6,
        "Double Classic + Pullup": 1 / 6,
    },
    "singlebell variations": {
        "Classic": 3 / 10,
        "Classic + Pullup": 1 / 10,
        "Classic + Snatch": 1 / 10,
        "Traveling 2s": 1 / 10,
        "Traveling 2s + Snatch": 1 / 10,
        "Traveling 2s + Pullup": 1 / 10,
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
    "rep schemes": {
        "Classic": 3,
        "Classic + Pullup": 3,
        "Double Classic": 3,
        "Double Classic + Pullup": 3,
        "Classic + Snatch": 4,
        "Traveling 2s": 4,
        "Traveling 2s + Pullup": 4,
        "Double Traveling 2s": 4,
        "Traveling 2s + Snatch": 5,
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
    "rep schemes": {
        "Armor Building Complex 2.0": 6,
        "Armor Building Complex": 6,
    },
}
