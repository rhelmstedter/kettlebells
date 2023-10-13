from kettlebells.workouts import Exercise, Workout

TEST_WORKOUT = Workout(
    **{
        "bodyweight": 90,
        "units": "kilograms",
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
                    "load": 90,
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

TEST_WORKOUT_NO_SWINGS = Workout(
    **{
        "bodyweight": 90,
        "units": "kilograms",
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
        "units": "kilograms",
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
        "units": "kilograms",
        "bodyweight": 90,
        "light load": 20,
        "medium load": 24,
        "heavy load": 28,
    },
    "saved_workouts": [
        {
            "date": "2023-09-14",
            "workout": {
                "bodyweight": 90,
                "units": "kilograms",
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
            "units": "kilograms",
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
