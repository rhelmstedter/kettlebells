from iron_cardio.iron_cardio import Session

TEST_SESSION = Session(
    **{
        "bells": "Double Bells",
        "variation": "Double Classic + Pullup",
        "time": 30,
        "load": 28,
        "units": "kilograms",
        "swings": 60,
        "sets": 20,
    }
)

TEST_SESSION_NO_SWINGS = Session(
    **{
        "bells": "Single Bell",
        "variation": "Traveling 2s + Snatch",
        "time": 20,
        "load": 24,
        "units": "kilograms",
        "swings": 0,
        "sets": 16,
    },
)

TEST_SESSION_SINGLE_BELL_PULLUPS = Session(
    **{
        "bells": "Single Bell",
        "variation": "Classic + Pullup",
        "time": 10,
        "load": 20,
        "units": "kilograms",
        "swings": 100,
        "sets": 10,
    },
)

TEST_CACHE_SESSION = Session(
    **{
        "bells": "Double Bells",
        "variation": "Double Classic",
        "time": 20,
        "load": 20,
        "units": "kilograms",
        "swings": 0,
        "sets": 0,
    }
)

TEST_DATA = {
    "loads": {
        "units": "kilograms",
        "bodyweight": 90,
        "light load": 20,
        "medium load": 24,
        "heavy load": 28,
    },
    "saved_sessions": [
        {
            "date": "2023-09-14",
            "session": {
                "bells": "Double Bells",
                "variation": "Double Classic",
                "time": 20,
                "load": 20,
                "units": "kilograms",
                "swings": 0,
                "sets": 29,
            },
        },
    ],
    "cached_sessions": [
        {
            "bells": "Single Bell",
            "variation": "Classic",
            "time": 10,
            "load": 28,
            "units": "kilograms",
            "swings": 0,
            "sets": 0,
        },
    ],
}

TEST_DATA_FULL_CACHE = {
    "loads": {
        "units": "kilograms",
        "bodyweight": 90,
        "light load": 20,
        "medium load": 24,
        "heavy load": 28,
    },
    "saved_sessions": [
        {
            "date": "2023-09-14",
            "session": {
                "bells": "Double Bells",
                "variation": "Double Classic",
                "time": 20,
                "load": 20,
                "units": "kilograms",
                "swings": 0,
                "sets": 29,
            },
        },
    ],
    "cached_sessions": [
        {
            "bells": "Single Bell",
            "variation": "Classic",
            "time": 10,
            "load": 28,
            "units": "kilograms",
            "swings": 0,
            "sets": 0,
        },
        {
            "bells": "Double Bells",
            "variation": "Double Classic",
            "time": 10,
            "load": 24,
            "units": "kilograms",
            "swings": 0,
            "sets": 0,
        },
        {
            "bells": "Single Bell",
            "variation": "Traveling 2s + Snatch",
            "time": 20,
            "load": 24,
            "units": "kilograms",
            "swings": 70,
            "sets": 0,
        },
        {
            "bells": "Double Bells",
            "variation": "Double Classic",
            "time": 10,
            "load": 28,
            "units": "kilograms",
            "swings": 0,
            "sets": 0,
        },
        {
            "bells": "Single Bell",
            "variation": "Traveling 2s + Snatch",
            "time": 20,
            "load": 24,
            "units": "kilograms",
            "swings": 0,
            "sets": 0,
        },
        {
            "bells": "Single Bell",
            "variation": "Traveling 2s",
            "time": 20,
            "load": 24,
            "units": "kilograms",
            "swings": 120,
            "sets": 0,
        },
        {
            "bells": "Double Bells",
            "variation": "Double Traveling 2s",
            "time": 30,
            "load": 28,
            "units": "kilograms",
            "swings": 120,
            "sets": 0,
        },
        {
            "bells": "Single Bell",
            "variation": "Traveling 2s + Pullup",
            "time": 30,
            "load": 20,
            "units": "kilograms",
            "swings": 0,
            "sets": 0,
        },
        {
            "bells": "Double Bells",
            "variation": "Double Traveling 2s",
            "time": 10,
            "load": 24,
            "units": "kilograms",
            "swings": 0,
            "sets": 0,
        },
        {
            "bells": "Double Bells",
            "variation": "Double Classic + Pullup",
            "time": 30,
            "load": 28,
            "units": "kilograms",
            "swings": 60,
            "sets": 0,
        },
    ],
}
