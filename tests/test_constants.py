from kettlebells.workouts import Workout
from kettlebells.constants import IC_REP_SCHEMES

TEST_SESSION = Workout(
    **{
        "bells": "Double Bells",
        "variation": "Double Classic + Pullup",
        "time": 30,
        "load": 28,
        "units": "kilograms",
        "swings": 60,
        "sets": 20,
        "reps": IC_REP_SCHEMES["Double Classic + Pullup"],
        "workout_type": "iron cardio",
    }
)

TEST_SESSION_NO_SWINGS = Workout(
    **{
        "bells": "Single Bell",
        "variation": "Traveling 2s + Snatch",
        "time": 20,
        "load": 24,
        "units": "kilograms",
        "swings": 0,
        "sets": 16,
        "reps": IC_REP_SCHEMES["Traveling 2s + Snatch"],
        "workout_type": "iron cardio",
    },
)

TEST_SESSION_SINGLE_BELL_PULLUPS = Workout(
    **{
        "bells": "Single Bell",
        "variation": "Classic + Pullup",
        "time": 10,
        "load": 20,
        "units": "kilograms",
        "swings": 100,
        "sets": 10,
        "reps": IC_REP_SCHEMES["Classic + Pullup"],
        "workout_type": "iron cardio",
    },
)

TEST_CACHE_SESSION = Workout(
    **{
        "bells": "Double Bells",
        "variation": "Double Classic",
        "time": 20,
        "load": 20,
        "units": "kilograms",
        "swings": 0,
        "sets": 0,
        "reps": IC_REP_SCHEMES["Double Classic"],
        "workout_type": "iron cardio",
    }
)

TEST_DATA = {
    "ic_loads": {
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
                "reps": IC_REP_SCHEMES["Double Classic"],
                "workout_type": "iron cardio",
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
            "reps": IC_REP_SCHEMES["Classic"],
            "workout_type": "iron cardio",
        },
    ],
}

TEST_DATA_FULL_CACHE = {
    "ic_loads": {
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
                "reps": IC_REP_SCHEMES["Double Classic"],
                "workout_type": "iron cardio",
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
            "reps": IC_REP_SCHEMES["Classic"],
            "workout_type": "iron cardio",
        },
        {
            "bells": "Double Bells",
            "variation": "Double Classic",
            "time": 10,
            "load": 24,
            "units": "kilograms",
            "swings": 0,
            "sets": 0,
            "reps": IC_REP_SCHEMES["Double Classic"],
            "workout_type": "iron cardio",
        },
        {
            "bells": "Single Bell",
            "variation": "Traveling 2s + Snatch",
            "time": 20,
            "load": 24,
            "units": "kilograms",
            "swings": 70,
            "sets": 0,
            "reps": IC_REP_SCHEMES["Traveling 2s + Snatch"],
            "workout_type": "iron cardio",
        },
        {
            "bells": "Double Bells",
            "variation": "Double Classic",
            "time": 10,
            "load": 28,
            "units": "kilograms",
            "swings": 0,
            "sets": 0,
            "reps": IC_REP_SCHEMES["Double Classic"],
            "workout_type": "iron cardio",
        },
        {
            "bells": "Single Bell",
            "variation": "Traveling 2s + Snatch",
            "time": 20,
            "load": 24,
            "units": "kilograms",
            "swings": 0,
            "sets": 0,
            "reps": IC_REP_SCHEMES["Traveling 2s + Snatch"],
            "workout_type": "iron cardio",
        },
        {
            "bells": "Single Bell",
            "variation": "Traveling 2s",
            "time": 20,
            "load": 24,
            "units": "kilograms",
            "swings": 120,
            "sets": 0,
            "reps": IC_REP_SCHEMES["Traveling 2s"],
            "workout_type": "iron cardio",
        },
        {
            "bells": "Double Bells",
            "variation": "Double Traveling 2s",
            "time": 30,
            "load": 28,
            "units": "kilograms",
            "swings": 120,
            "sets": 0,
            "reps": IC_REP_SCHEMES["Double Traveling 2s"],
            "workout_type": "iron cardio",
        },
        {
            "bells": "Single Bell",
            "variation": "Traveling 2s + Pullup",
            "time": 30,
            "load": 20,
            "units": "kilograms",
            "swings": 0,
            "sets": 0,
            "reps": IC_REP_SCHEMES["Traveling 2s + Pullup"],
            "workout_type": "iron cardio",
        },
        {
            "bells": "Double Bells",
            "variation": "Double Traveling 2s",
            "time": 10,
            "load": 24,
            "units": "kilograms",
            "swings": 0,
            "sets": 0,
            "reps": IC_REP_SCHEMES["Double Traveling 2s"],
            "workout_type": "iron cardio",
        },
        {
            "bells": "Double Bells",
            "variation": "Double Classic + Pullup",
            "time": 30,
            "load": 28,
            "units": "kilograms",
            "swings": 60,
            "sets": 0,
            "reps": IC_REP_SCHEMES["Double Classic + Pullup"],
            "workout_type": "iron cardio",
        },
    ],
}
