from dataclasses import dataclass

from pathlib import Path
from random import choice, choices

from rich.prompt import Confirm, IntPrompt, Prompt

from .console import console
from .constants import (
    ABC_PARAMS,
    IRON_CARDIO_PARAMS,
    SUGGESTION,
    WARNING,
)
from .database import read_database


@dataclass
class Exercise:
    name: str
    load: int
    sets: int
    reps: int


@dataclass
class Workout:
    bodyweight: int
    units: str
    variation: str
    time: int
    exercises: list[Exercise]
    workout_type: str

    def display_workout(self) -> None:
        """Print an a workout to the console.
        :returns: None.
        """
        console.print(self.workout_type.upper())
        console.print("=" * len(self.workout_type), style="green")
        console.print(f"Variation: {self.variation}")
        console.print(f"     Time: {self.time} mins")
        if self.workout_type in ["iron cardio", "armor building complex"]:
            swings = [e for e in self.exercises if "Swings" in e.name]
            console.print(
                f"     Load: {self.exercises[0].load} {self.units}"
            )
            if swings and "Swings" in swings:
                console.print("   Swings:", swings[0].reps)
        else:
            for exercise in self.exercises:
                console.print(exercise.name.title())
                console.print(f"\tLoad: {exercise.load}")
                console.print(f"\t{exercise.sets} sets of {exercise.reps} reps")

    def calc_workout_stats(self) -> dict:
        """Calculate the stats for a given workout.
        :returns: A dict containing total weight moved, number of reps, and the pace.
        """
        total_reps = 0
        weight_moved = 0
        for exercise in self.exercises:
            total_reps += exercise.reps * exercise.sets
            if "double" in exercise.name.lower():
                weight_moved += exercise.reps * exercise.sets * exercise.load * 2
            else:
                weight_moved += exercise.reps * exercise.sets * exercise.load

        stats = {
            "weight moved": weight_moved,
            "reps": total_reps,
            "pace": round((self.time * 60) / total_reps, 1),
        }
        return stats

    def display_workout_stats(self) -> None:
        """Prints the stats for a given workout.
        :returns: None"""
        stats = self.calc_workout_stats()
        console.print("Workout Stats")
        console.print("=============", style="green")
        console.print(f"Weight Moved: {stats.get('weight moved'):,} {self.units}")
        console.print(f"  Total Reps: {stats.get('reps')}")
        console.print(f"        Pace: {stats.get('pace')} sec/rep")


def random_workout(db_path: Path, workout_type: str) -> Workout:
    """Create a random workout based on workout_type.
    :param db_path: The Path to the database.
    :returns: A Workout object with randomly generated parameters.
    """
    data = read_database(db_path)
    loads = data["loads"]
    workout_type, workout_params = _get_workout_params(workout_type)
    bells = choices(
        population=tuple(workout_params["bells"].keys()),
        weights=tuple(workout_params["bells"].values()),
    )[0]
    if bells == "Double Bells":
        variation = choices(
            population=tuple(workout_params["doublebell variations"].keys()),
            weights=tuple(workout_params["doublebell variations"].values()),
        )[0]
    elif bells == "Single Bell":
        variation = choices(
            population=tuple(workout_params["singlebell variations"].keys()),
            weights=tuple(workout_params["singlebell variations"].values()),
        )[0]
    time = choices(
        population=tuple(workout_params["times"].keys()),
        weights=tuple(workout_params["times"].values()),
    )[0]
    load = choices(
        population=tuple(workout_params["loads"].keys()),
        weights=tuple(workout_params["loads"].values()),
    )[0]
    swings = choices(
        population=tuple(workout_params["swings"].keys()),
        weights=tuple(workout_params["swings"].values()),
    )[0]
    load = loads[load]
    units = loads["units"]
    exercises = []
    for exercise in workout_params["exercises"][variation]:
        exercises.append(
            Exercise(name=exercise[0], load=load, sets=0, reps=exercise[1])
        )

    if swings:
        swings = Exercise(
            name="Swings",
            load=load,
            sets=1,
            reps=choice(range(50, 160, 10)),
        )
        exercises.append(swings)
    return Workout(
        bodyweight=data["loads"]["bodyweight"],
        units=units,
        variation=variation,
        time=time,
        exercises=exercises,
        workout_type=workout_type,
    )


def create_custom_workout(db_path: Path, workout_type: str) -> Workout:
    """Create a custom Workout Object.
    :returns: An Workout object created by the user.
    """
    data = read_database(db_path)
    bodyweight = data["loads"]["bodyweight"]
    workout_type, workout_params = _get_workout_params(workout_type)
    bells = _get_options(workout_params["bells"])
    if bells == "Double Bells":
        variation = _get_options(workout_params["doublebell variations"])
    elif bells == "Single Bell":
        variation = _get_options(workout_params["singlebell variations"])
    time = IntPrompt.ask("How long was your workout (in minutes)")
    units = _get_units()
    load = IntPrompt.ask(f"What weight did you use (in {units})")
    sets = IntPrompt.ask("How many sets did you complete?")
    exercises = []
    for exercise in workout_params["exercises"][variation]:
        if bells == "Single Bell" and exercise[0] == "Pullup":
            exercises.append(
                Exercise(
                    name=exercise[0],
                    load=bodyweight,
                    sets=sets // 2,
                    reps=exercise[1],
                )
            )
        elif bells == "Double Bells" and exercise[0] == "Pullup":
            exercises.append(
                Exercise(
                    name=exercise[0],
                    load=bodyweight,
                    sets=sets,
                    reps=exercise[1],
                )
            )
        else:
            exercises.append(
                Exercise(
                    name=exercise[0],
                    load=load,
                    sets=sets,
                    reps=exercise[1],
                )
            )
    if Confirm.ask("Did you swing"):
        swings = IntPrompt.ask("How many swings")
        exercises.append(
            Exercise(
                name="Swings",
                load=load,
                sets=1,
                reps=swings,
            )
        )
    return Workout(
        bodyweight=bodyweight,
        units=units,
        variation=variation,
        time=time,
        exercises=exercises,
        workout_type=workout_type,
    )


def set_loads() -> dict:
    """Creates a dictionary containing the units and kettlebell weights and body weight
    of the user.
    :returns: A dict of the loads set by the user.
    """
    while True:
        units = _get_units()
        bodyweight = IntPrompt.ask("Bodyweight")
        console.print("Enter the weight for the...")
        light_load = IntPrompt.ask("Light kettlebell")
        medium_load = IntPrompt.ask("Medium kettlebell")
        heavy_load = IntPrompt.ask("Heavy kettlebell")
        loads = {
            "units": units,
            "bodyweight": bodyweight,
            "light load": light_load,
            "medium load": medium_load,
            "heavy load": heavy_load,
        }
        console.clear()
        for label, value in loads.items():
            console.print(f"{label.title()}: {value}")
        if Confirm.ask(
            "Are these loads correct? If you confirm, they will be used to generate workouts."
        ):
            break
    return loads


def _get_options(workout_param: dict) -> str:
    """Select options for a given workout parameter.
    :param workout_param: The dictionary containing options for a Workout parameter.
    :returns: A string consisting of the workout parameter choosen by the user.
    """
    options = list(workout_param.keys())
    for i, option in enumerate(options, 1):
        print(f"    [{i}] {option}")
    while True:
        try:
            selection = IntPrompt.ask("Choose your option")
            return options[selection - 1]
        except IndexError:
            print(":warning: Not a valid option.", style=WARNING)
            print("Enter a number between 1 and {max(options) + 1}.", style=SUGGESTION)
            continue


def _get_units() -> str:
    """A helper function to get the units.
    :returns: A string, either 'pounds' or 'kilograms'.
    """
    while True:
        units = Prompt.ask("[P]ounds or [K]ilograms").lower()
        if units.startswith("p"):
            units = "pounds"
        elif units.startswith("k"):
            units = "kilograms"
        else:
            console.print(":warning: Invalid option", style=WARNING)
            console.print("Please enter P or K", style=SUGGESTION)
            continue
        break
    return units


def _get_workout_params(workout_type: str) -> dict:
    match workout_type:
        case "iron-cardio" | "iron cardio":
            return "iron cardio", IRON_CARDIO_PARAMS
        case "abc" | "Armor Building Complex":
            return "armor building complex", ABC_PARAMS
