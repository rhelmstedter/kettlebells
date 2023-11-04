from kettlebells.workouts import Exercise, Workout

TEST_IC_WORKOUT = Workout(
    **{
        "bodyweight": 90,
        "units": "kg",
        "variation": "Double Classic + Pullup",
        "time": 30,
        "exercises": [
            Exercise(
                **{
                    "name": "Double Clean",
                    "load": 28,
                    "sets": 20,
                    "reps": 1,
                },
            ),
            Exercise(
                **{
                    "name": "Double Press",
                    "load": 28,
                    "sets": 20,
                    "reps": 1,
                },
            ),
            Exercise(
                **{
                    "name": "Double Front Squat",
                    "load": 28,
                    "sets": 20,
                    "reps": 1,
                },
            ),
            Exercise(
                **{
                    "name": "Pullup",
                    "load": 86,
                    "sets": 20,
                    "reps": 1,
                },
            ),
            Exercise(
                **{
                    "name": "Swings",
                    "load": 28,
                    "sets": 1,
                    "reps": 60,
                },
            ),
        ],
        "workout_type": "iron cardio",
    }
)

TEST_SINGLE_TRAVELING_2S_WORKOUT = Workout(
    **{
        "bodyweight": 90,
        "units": "kg",
        "variation": "Traveling 2s",
        "time": 10,
        "exercises": [
            Exercise(
                **{
                    "name": "Clean",
                    "load": 20,
                    "sets": 13,
                    "reps": 1,
                },
            ),
            Exercise(
                **{
                    "name": "Press",
                    "load": 20,
                    "sets": 13,
                    "reps": 1,
                },
            ),
            Exercise(
                **{
                    "name": "Front Squat",
                    "load": 20,
                    "sets": 13,
                    "reps": 1,
                },
            ),
            Exercise(
                **{
                    "name": "Swings",
                    "load": 20,
                    "sets": 1,
                    "reps": 100,
                },
            ),
        ],
        "workout_type": "iron cardio",
    }
)
TEST_DOUBLE_TRAVELING_2S_WORKOUT = Workout(
    **{
        "bodyweight": 90,
        "units": "kg",
        "variation": "Double Traveling 2s",
        "time": 29,
        "exercises": [
            Exercise(
                **{
                    "name": "Double Clean",
                    "load": 28,
                    "sets": 16,
                    "reps": 1,
                },
            ),
            Exercise(
                **{
                    "name": "Double Press",
                    "load": 28,
                    "sets": 16,
                    "reps": 1,
                },
            ),
            Exercise(
                **{
                    "name": "Double Front Squat",
                    "load": 28,
                    "sets": 16,
                    "reps": 1,
                },
            ),
            Exercise(
                **{
                    "name": "Swings",
                    "load": 28,
                    "sets": 1,
                    "reps": 50,
                },
            ),
        ],
        "workout_type": "iron cardio",
    }
)

TEST_BTB_WORKOUT = Workout(
    **{
        "bodyweight": 90,
        "units": "kg",
        "variation": "2 C&P Ladders + Snatch",
        "time": 30,
        "exercises": [
            Exercise(**{"name": "Clean and Press", "load": 24, "sets": 2, "reps": 20}),
            Exercise(**{"name": "Snatch", "load": 20, "sets": 1, "reps": 100}),
        ],
        "workout_type": "back to basics",
    },
)
TEST_PERFECT_WORKOUT = Workout(
    **{
        "bodyweight": 90,
        "units": "kg",
        "variation": "The Bull",
        "time": 10,
        "exercises": [
            Exercise(
                **{
                    "name": "Half-kneeling Press",
                    "load": 20,
                    "sets": 3,
                    "reps": 16,
                },
            ),
            Exercise(
                **{
                    "name": "Hanging Leg Raise",
                    "load": 0,
                    "sets": 3,
                    "reps": 8,
                },
            ),
            Exercise(
                **{
                    "name": "Bulgarian Goat Bag Swing",
                    "load": 24,
                    "sets": 3,
                    "reps": 8,
                },
            ),
            Exercise(
                **{
                    "name": "Bent Over Row",
                    "load": 20,
                    "sets": 3,
                    "reps": 16,
                },
            ),
            Exercise(
                **{
                    "name": "Goblet Squat",
                    "load": 20,
                    "sets": 1,
                    "reps": 8,
                },
            ),
            Exercise(
                **{
                    "name": "Broomstick Overhead Sqaut",
                    "load": 0,
                    "sets": 1,
                    "reps": 8,
                },
            ),
        ],
        "workout_type": "perfect workout",
    },
)
TEST_CUSTOM_WORKOUT = Workout(
    **{
        "bodyweight": 90,
        "units": "kg",
        "variation": "custom",
        "time": 30,
        "exercises": [
            Exercise(**{"name": "Turkish Get-up", "load": 24, "sets": 1, "reps": 6}),
            Exercise(**{"name": "TRX T", "load": 0, "sets": 3, "reps": 8}),
        ],
        "workout_type": "custom",
    },
)
TEST_GIANT_WORKOUT = Workout(
    **{
        "bodyweight": 90,
        "units": "kg",
        "variation": "W1D1",
        "workout_type": "The Giant 1.0",
        "time": 30,
        "exercises": [
            Exercise(**{"name": "Double Clean and Press", "load": 24, "sets": 10, "reps": 5}),
        ],
    },
)


TEST_WORKOUT_NO_SWINGS = Workout(
    **{
        "bodyweight": 90,
        "units": "kg",
        "variation": "Classic + Snatch",
        "time": 20,
        "exercises": [
            Exercise(
                **{
                    "name": "Clean",
                    "load": 24,
                    "sets": 16,
                    "reps": 1,
                },
            ),
            Exercise(
                **{
                    "name": "Press",
                    "load": 24,
                    "sets": 16,
                    "reps": 1,
                },
            ),
            Exercise(
                **{
                    "name": "Front Squat",
                    "load": 24,
                    "sets": 16,
                    "reps": 1,
                },
            ),
            Exercise(
                **{
                    "name": "Snatch",
                    "load": 24,
                    "sets": 16,
                    "reps": 1,
                },
            ),
        ],
        "workout_type": "iron cardio",
    }
)

TEST_WORKOUT_SINGLE_BELL_PULLUPS = Workout(
    **{
        "bodyweight": 90,
        "units": "kg",
        "variation": "Classic + Pullup",
        "time": 10,
        "exercises": [
            Exercise(
                **{
                    "name": "Clean",
                    "load": 20,
                    "sets": 10,
                    "reps": 1,
                },
            ),
            Exercise(
                **{
                    "name": "Press",
                    "load": 20,
                    "sets": 10,
                    "reps": 1,
                },
            ),
            Exercise(
                **{
                    "name": "Front Squat",
                    "load": 20,
                    "sets": 10,
                    "reps": 1,
                },
            ),
            Exercise(
                **{
                    "name": "Pullup",
                    "load": 90,
                    "sets": 5,
                    "reps": 1,
                },
            ),
        ],
        "workout_type": "iron cardio",
    }
)

TEST_DATA = {
    "loads": {
        "units": "kg",
        "bodyweight": 90,
        "light load": 20,
        "medium load": 24,
        "heavy load": 28,
        "the giant": 24,
    },
    "saved_workouts": [
        {
            "date": "2023-09-14",
            "workout": {
                "bodyweight": 90,
                "units": "kg",
                "variation": "Double Classic",
                "time": 20,
                "exercises": [
                    {
                        "name": "Double Clean",
                        "load": 20,
                        "sets": 29,
                        "reps": 1,
                    },
                    {
                        "name": "Double Press",
                        "load": 20,
                        "sets": 29,
                        "reps": 1,
                    },
                    {
                        "name": "Double Front Squat",
                        "load": 20,
                        "sets": 29,
                        "reps": 1,
                    },
                ],
                "workout_type": "iron cardio",
            },
        },
    ],
    "cached_workouts": [
        {
            "bodyweight": 90,
            "units": "kg",
            "variation": "Double Classic + Pullup",
            "time": 30,
            "exercises": [
                {
                    "name": "Double Clean",
                    "load": 28,
                    "sets": 20,
                    "reps": 1,
                },
                {
                    "name": "Double Press",
                    "load": 28,
                    "sets": 20,
                    "reps": 1,
                },
                {
                    "name": "Double Front Squat",
                    "load": 28,
                    "sets": 20,
                    "reps": 1,
                },
                {
                    "name": "Pullup",
                    "load": 90,
                    "sets": 20,
                    "reps": 1,
                },
                {
                    "name": "Swings",
                    "load": 28,
                    "sets": 6,
                    "reps": 10,
                },
            ],
            "workout_type": "iron cardio",
        }
    ],
}
