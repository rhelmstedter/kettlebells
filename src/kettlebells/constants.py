"""constants for iron cardio session parameters."""

from pathlib import Path

KETTLEBELLS_HOME = Path().home() / ".kettlebells"
KETTLEBELLS_DB = KETTLEBELLS_HOME / "kettlebells_db.json"

IC_BELLS = {"Single Bell": 4 / 6, "Double Bells": 2 / 6}
IC_DOUBLEBELL_VARIATIONS = {
    "Double Classic": 3 / 6,
    "Double Traveling 2s": 1 / 6,
    "Double Classic + Pullup": 1 / 6,
    "Armor Building Complex": 1 / 6,
}
IC_SINGLEBELL_VARIATIONS = {
    "Classic": 3 / 10,
    "Classic + Pullup": 1 / 10,
    "Classic + Snatch": 1 / 10,
    "Traveling 2s": 1 / 10,
    "Traveling 2s + Snatch": 1 / 10,
    "Traveling 2s + Pullup": 1 / 10,
    "Armor Building Complex 2.0": 2 / 10,
}
IC_TIMES = {
    30: 1 / 6,
    20: 4 / 6,
    10: 1 / 6,
}
IC_LOADS = {
    "heavy load": 2 / 6,
    "medium load": 3 / 6,
    "light load": 1 / 6,
}
IC_SWINGS = {True: 2 / 6, False: 4 / 6}
DATE_FORMAT = "%Y-%m-%d"
IC_REP_SCHEMES = {
    "Classic": 3,
    "Classic + Pullup": 3,
    "Double Classic": 3,
    "Double Classic + Pullup": 3,
    "Classic + Snatch": 4,
    "Traveling 2s": 4,
    "Traveling 2s + Pullup": 4,
    "Double Traveling 2s": 4,
    "Traveling 2s + Snatch": 5,
    "Armor Building Complex 2.0": 6,
    "Armor Building Complex": 6,
}
