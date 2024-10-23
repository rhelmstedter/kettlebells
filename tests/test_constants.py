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
        "variation": "Custom",
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
            Exercise(
                **{"name": "Double Clean and Press", "load": 24, "sets": 10, "reps": 5}
            ),
        ],
    },
)

TEST_WOLF_WORKOUT = Workout(
    **{
        "bodyweight": 90,
        "units": "kg",
        "variation": "W1D1",
        "workout_type": "The Wolf",
        "time": 12,
        "exercises": [
            Exercise(
                **{
                    "name": "Snatch",
                    "load": 16,
                    "sets": 3,
                    "reps": 10,
                }
            ),
            Exercise(
                **{
                    "name": "Double Front Squat",
                    "load": 16,
                    "sets": 3,
                    "reps": 5,
                }
            ),
            Exercise(
                **{
                    "name": "Double Press",
                    "load": 16,
                    "sets": 3,
                    "reps": 5,
                }
            ),
            Exercise(
                **{
                    "name": "Double Front Squat",
                    "load": 16,
                    "sets": 3,
                    "reps": 5,
                }
            ),
            Exercise(
                **{
                    "name": "Double Clean",
                    "load": 16,
                    "sets": 3,
                    "reps": 5,
                }
            ),
            Exercise(
                **{
                    "name": "Double Front Squat",
                    "load": 16,
                    "sets": 3,
                    "reps": 5,
                }
            ),
        ],
    },
)


TEST_ABFB = Workout(
    **{
        "bodyweight": 90,
        "units": "kg",
        "variation": "Program Three",
        "time": 32,
        "exercises": [
            Exercise(
                **{
                    "name": "Clean and Press",
                    "load": 20,
                    "sets": 1,
                    "reps": 8,
                },
            ),
            Exercise(
                **{
                    "name": "Front Squat",
                    "load": 20,
                    "sets": 1,
                    "reps": 1,
                },
            ),
            Exercise(
                **{
                    "name": "Clean and Press",
                    "load": 29,
                    "sets": 1,
                    "reps": 8,
                },
            ),
            Exercise(
                **{
                    "name": "Front Squat",
                    "load": 29,
                    "sets": 1,
                    "reps": 1,
                },
            ),
            Exercise(
                **{
                    "name": "Clean and Press",
                    "load": 43,
                    "sets": 3,
                    "reps": 8,
                },
            ),
            Exercise(
                **{
                    "name": "Front Squat",
                    "load": 43,
                    "sets": 3,
                    "reps": 1,
                },
            ),
            Exercise(
                **{
                    "name": "Curl",
                    "load": 20,
                    "sets": 2,
                    "reps": 8,
                },
            ),
            Exercise(
                **{
                    "name": "Curl",
                    "load": 25,
                    "sets": 3,
                    "reps": 8,
                },
            ),
        ],
        "workout_type": "armor building formula barbell",
    }
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

TEST_WORKOUT_GENERATOR_WORKOUT = Workout(
    **{
        "bodyweight": 90,
        "units": "kg",
        "variation": "3 X 10",
        "time": 40,
        "exercises": [
            Exercise(
                **{
                    "name": "Deadlift",
                    "sets": 3,
                    "reps": 10,
                    "load": 100,
                },
            ),
            Exercise(
                **{
                    "name": "Bench Press",
                    "sets": 3,
                    "reps": 10,
                    "load": 80,
                },
            ),
        ],
        "workout_type": "workout generator",
    }
)
TEST_EASY_STRENGTH_WORKOUT = Workout(
    **{
        "bodyweight": 90,
        "units": "kg",
        "variation": "24",
        "time": 30,
        "exercises": [
            Exercise(
                **{
                    "name": "Goblet Squat",
                    "sets": 1,
                    "reps": 10,
                    "load": 32,
                },
            ),
            Exercise(
                **{
                    "name": "Swing",
                    "sets": 5,
                    "reps": 15,
                    "load": 32,
                },
            ),
            Exercise(
                **{
                    "name": "Dip",
                    "sets": 2,
                    "reps": 5,
                    "load": 98,
                },
            ),
            Exercise(
                **{
                    "name": "Double Front Squat",
                    "sets": 2,
                    "reps": 5,
                    "load": 28,
                },
            ),
            Exercise(
                **{
                    "name": "Bent Over Row",
                    "sets": 2,
                    "reps": 10,
                    "load": 32,
                },
            ),
            Exercise(
                **{
                    "name": "Ab Wheel",
                    "sets": 1,
                    "reps": 10,
                    "load": 0,
                },
            ),
        ],
        "workout_type": "easy strength",
    }
)

TEST_ABF_PRESS_WORKOUT = Workout(
    **{
        "bodyweight": 90,
        "units": "kg",
        "variation": "Double Press",
        "time": 30,
        "exercises": [
            Exercise(
                **{
                    "name": "Double Press",
                    "sets": 5,
                    "reps": 2,
                    "load": 20,
                },
            ),
            Exercise(
                **{
                    "name": "Double Press",
                    "sets": 5,
                    "reps": 3,
                    "load": 20,
                },
            ),
            Exercise(
                **{
                    "name": "Double Press",
                    "sets": 5,
                    "reps": 5,
                    "load": 20,
                },
            ),
            Exercise(
                **{
                    "name": "Double Press",
                    "sets": 5,
                    "reps": 10,
                    "load": 20,
                },
            ),
        ],
        "workout_type": "armor building formula",
    }
)
TEST_ABF_ABC_WORKOUT = Workout(
    **{
        "bodyweight": 90,
        "units": "kg",
        "variation": "Armor Building Complex",
        "time": 30,
        "exercises": [
            Exercise(
                **{
                    "name": "Double Clean",
                    "sets": 30,
                    "reps": 2,
                    "load": 20,
                },
            ),
            Exercise(
                **{
                    "name": "Double Press",
                    "sets": 30,
                    "reps": 1,
                    "load": 20,
                },
            ),
            Exercise(
                **{
                    "name": "Double Front Squat",
                    "sets": 30,
                    "reps": 3,
                    "load": 20,
                },
            ),
        ],
        "workout_type": "armor building formula",
    }
)
TEST_ROP_WORKOUT = Workout(
    **{
        "bodyweight": 90,
        "units": "kg",
        "variation": "Medium",
        "time": 45,
        "exercises": [
            Exercise(
                **{
                    "name": "Clean and Press",
                    "sets": 5,
                    "reps": 12,
                    "load": 28,
                },
            ),
            Exercise(
                **{
                    "name": "Pullup",
                    "sets": 5,
                    "reps": 6,
                    "load": 86,
                },
            ),
            Exercise(
                **{
                    "name": "Swing",
                    "sets": 5,
                    "reps": 10,
                    "load": 28,
                },
            ),
        ],
        "workout_type": "rite of passage",
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
        "the wolf": 16,
    },
    "saved_workouts": [
        {
            "date": "2023-09-12",
            "workout": {
                "bodyweight": 90,
                "units": "kg",
                "variation": "W1D1",
                "time": 20,
                "exercises": [
                    {
                        "name": "Double Clean and Press",
                        "load": 24,
                        "sets": 8,
                        "reps": 3,
                    },
                    {
                        "name": "Double Front Squat",
                        "load": 24,
                        "sets": 8,
                        "reps": 3,
                    },
                ],
                "workout_type": "Dry Fighting Weight",
            },
        },
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
