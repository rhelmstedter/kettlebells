import sys
from datetime import datetime
from os import environ
from pathlib import Path
from random import choice, choices

from iterfzf import iterfzf
from pydantic import BaseModel
from rich.prompt import Confirm, IntPrompt, Prompt

from .console import console
from .constants import (
    ABC_PARAMS,
    ABF_PARAMS,
    ABFB_PARAMS,
    BODYWEIGHT_FACTORS,
    BTB_PARAMS,
    DATE_FORMAT,
    DFW_PARAMS,
    FZF_DEFAULT_OPTS,
    HUMAN_MOVEMENTS,
    IRON_CARDIO_PARAMS,
    POUNDS_TO_KILOS_RATE,
    PW_PARAMS,
    ROP_PARAMS,
    SUGGESTION,
    THE_GIANT_PARAMS,
    THE_WOLF_PARAMS,
    WARNING,
    WORKOUT_GENERATOR_PARAMS,
)
from .database import bodyweight_share, read_database, write_database
from .entry import EntryError, format_spec, parse_spec
from .names import bump_variation, normalize_workout_type, resolve_workout_type


class Exercise(BaseModel):
    """Exercise object.

    Attributes:
        name: str
        load: int, for bodyweight exercises (see BODYWEIGHT_FACTORS) the added weight
        sets: int
        reps: int
    """

    name: str
    load: int
    sets: int
    reps: int

    @property
    def is_bodyweight(self) -> bool:
        return self.name in BODYWEIGHT_FACTORS

    def total_load(self, bodyweight: int) -> int:
        """The load moved per rep, including the bodyweight share if any."""
        return self.load + bodyweight_share(self.name, bodyweight)

    def describe_load(self, units: str) -> str:
        if self.is_bodyweight:
            return f"BW + {self.load} {units}" if self.load else "BW"
        return f"{self.load} {units}"


class Workout(BaseModel):
    """Workout object.

    Attributes:
        workout_type: str
        variation: str
        time: int
        units: str
        bodyweight: int
        exercises: list[Exercise]
        notes: str
    """

    workout_type: str
    variation: str
    time: int
    units: str
    bodyweight: int
    exercises: list[Exercise]
    notes: str = ""

    def display_workout(self) -> None:
        """Print a workout to the console."""
        console.print(self.workout_type.upper())
        console.print("=" * len(self.workout_type), style="green")
        display_params = [("Variation", self.variation), ("Time", f"{self.time} mins")]
        if self.workout_type in ["iron cardio", "armor building complex"]:
            display_params.append(("Load", f"{self.exercises[0].load} {self.units}"))
            swings = [e for e in self.exercises if "Swing" in e.name]
            if swings:
                display_params.append(("Kettlebell Swing", swings[0].reps))
        elif self.workout_type == "back to basics":
            second_block = self.exercises[-1]
            display_params.append(
                ("Clean and Press Load", f"{self.exercises[0].load} {self.units}")
            )
            display_params.append(
                (f"{second_block.name} Load", f"{second_block.load} {self.units}")
            )
        else:
            exercises = []
            for exercise in self.exercises:
                exercises.append(
                    (
                        exercise.name,
                        f"{exercise.sets} X {exercise.reps} with {exercise.describe_load(self.units)}",
                    )
                )
            _print_helper(display_params)
            console.print("Exercises")
            console.print("---------", style="green")
            _print_helper(exercises)
            self._display_notes()
            return
        _print_helper(display_params)
        self._display_notes()

    def _display_notes(self) -> None:
        if self.notes:
            console.print(f"Notes: {self.notes}", style="italic")
            console.print()

    def calc_workout_stats(self) -> dict:
        """Calculate the stats for a given workout.

        Returns:
            A dict containing total weight moved, reps, weight density and rep density.
        """
        total_reps = 0
        weight_moved = 0
        for exercise in self.exercises:
            load = exercise.total_load(self.bodyweight)
            if "double" in exercise.name.lower():
                load *= 2
            if "clean and press" in exercise.name.lower():
                reps = 2 * exercise.reps * exercise.sets
            else:
                reps = exercise.reps * exercise.sets
            total_reps += reps
            weight_moved += reps * load
        stats = {
            "weight moved": weight_moved,
            "reps": total_reps,
            "weight density": round(weight_moved / self.time, 1),
            "rep density": round(total_reps / self.time, 1),
        }
        return stats

    def display_workout_stats(self) -> None:
        """Prints the stats for a given workout.

        Returns:
            None
        """
        stats = self.calc_workout_stats()
        console.print("Workout Stats")
        console.print("=============", style="green")
        stats_to_print = [
            ("Weight Moved", f"{stats.get('weight moved'):,} {self.units}"),
            ("Total Reps", f"{stats.get('reps')}"),
            ("Weight Density", f"{stats.get('weight density')} kg/min"),
            ("Rep Density", f"{stats.get('rep density')} reps/min"),
        ]
        _print_helper(stats_to_print)


def random_ic_or_abc(db_path: Path, workout_type: str) -> Workout:
    """Create a random workout based on workout_type.

    Args:
        db_path:  The Path to the database.
        workout_type:  Either ic or abc.
    Returns:
        A Workout object with randomly generated parameters.
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
            name="Kettlebell Swing",
            load=load,
            sets=1,
            reps=choice(range(50, 160, 10)),
        )
        exercises.append(swings)
    return Workout(
        workout_type=workout_type,
        variation=variation,
        time=time,
        units=units,
        bodyweight=data["loads"]["bodyweight"],
        exercises=exercises,
    )


def create_ic_or_abc(db_path: Path, workout_type: str) -> Workout:
    """Create an ic or abc Workout.

    Args:
        db_path: The Path object to the database.
        workout_type: The workout type either 'ic' or 'abc'

    Returns:
        A Workout object created by the user.
    """
    data = read_database(db_path)
    bodyweight = data["loads"]["bodyweight"]
    units = data["loads"]["units"]
    workout_type, workout_params = _get_workout_params(workout_type)
    bells = _get_options(workout_params["bells"])
    if bells == "Double Bells":
        variation = _get_options(workout_params["doublebell variations"])
    elif bells == "Single Bell":
        variation = _get_options(workout_params["singlebell variations"])
    time = IntPrompt.ask("How long was your workout (mins)")
    load = IntPrompt.ask(f"What weight did you use ({units})")
    sets = IntPrompt.ask("How many sets did you complete?")
    exercises = []
    if "Traveling 2s" in variation:
        sets = sets + sets // 3
    for exercise, reps in workout_params["exercises"][variation]:
        if bells == "Single Bell" and exercise == "Pullup":
            sets = sets // 2
        exercises.append(
            Exercise(
                name=exercise,
                load=0 if exercise in BODYWEIGHT_FACTORS else load,
                sets=sets,
                reps=reps,
            )
        )
    if Confirm.ask("Did you swing"):
        swings = IntPrompt.ask("How many swings")
        load = IntPrompt.ask(f"What weight did you use ({units})")
        exercises.append(
            Exercise(
                name="Kettlebell Swing",
                load=load,
                sets=1,
                reps=swings,
            )
        )
    return Workout(
        workout_type=workout_type,
        variation=variation,
        time=time,
        units=units,
        bodyweight=bodyweight,
        exercises=exercises,
    )


def set_loads() -> dict:
    """Creates a dictionary containing the units and kettlebell weights and body weight
    of the user.

    Returns:
        A dict of the loads set by the user.

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
            return loads


def set_program_loads(loads: dict) -> dict:
    """Adds a program and load to the loads dictionary.

    Returns:
        The loads dictionary with an added item of the program and load.

    """
    program = Prompt.ask("Enter the name of the program").lower()
    program_load = IntPrompt.ask(f"Enter the weight for the {program.title()}")
    loads[program] = program_load
    return loads


def create_btb_workout(db_path: Path) -> Workout:
    """Create a back to basics kettelbell workout.

    Args:
        db_path: The Path to the database.

    Returns:
        A workout object.

    """
    data = read_database(db_path)
    bodyweight = data["loads"]["bodyweight"]
    units = data["loads"]["units"]
    workout_type, workout_params = _get_workout_params("btb")
    variation = _get_options(workout_params)
    if "Squat" in variation:
        second_block = "double kettlebell front squats"
    else:
        second_block = "kettlebell snatch"
    time = IntPrompt.ask("Workout duration (mins)")
    console.print("Enter the weight used for the...")
    c_and_p_load = IntPrompt.ask(f"clean and press ({units})")
    second_block_load = IntPrompt.ask(f"{second_block} ({units})")
    c_and_p = workout_params[variation]["exercises"][0]
    second_block_exercise = workout_params[variation]["exercises"][1]
    exercises = [
        Exercise(
            name=c_and_p["name"],
            load=c_and_p_load,
            sets=c_and_p["sets"],
            reps=c_and_p["reps"],
        ),
        Exercise(
            name=second_block_exercise["name"],
            load=second_block_load,
            sets=second_block_exercise["sets"],
            reps=second_block_exercise["reps"],
        ),
    ]
    return Workout(
        workout_type=workout_type,
        variation=variation,
        time=time,
        units=units,
        bodyweight=bodyweight,
        exercises=exercises,
    )


def create_perfect_workout(db_path: Path) -> Workout:
    """Create a Dan John perfect workout.

    Args:
        db_path: The Path to the database.

    Returns:
        A workout object.

    """
    data = read_database(db_path)
    bodyweight = data["loads"]["bodyweight"]
    units = data["loads"]["units"]
    workout_type, workout_params = _get_workout_params("pw")
    variation = _get_options(workout_params)
    time = IntPrompt.ask("Workout duration (mins)")
    console.print("Enter the weight for the...")
    exercises = []
    no_load_exercises = ["Broomstick", "Hanging"]
    for exercise in workout_params[variation]["exercises"]:
        if not any(x in exercise["name"] for x in no_load_exercises):
            exercise["load"] = IntPrompt.ask(f"  {exercise['name']}")
        exercises.append(Exercise(**exercise))
    return Workout(
        workout_type=workout_type,
        variation=variation,
        time=time,
        units=units,
        bodyweight=bodyweight,
        exercises=exercises,
    )


def create_easy_strength_workout(db_path: Path) -> Workout | None:
    """Create an Easy Strength workout from one of the easy strength templates."""
    return create_from_template(db_path, "easy strength")


def create_time_based_workout(db_path: Path, workout_type: str) -> Workout:
    """Create a workout based on a given amount of time. E.g., The Giant.

    Args:
        db_path: The path to the database.
        workout_type: The name of the program.

    Returns:
        The workout object for a given day of a program.
    """
    data = read_database(db_path)
    bodyweight = data["loads"]["bodyweight"]
    units = data["loads"]["units"]
    workout_type, workout_params = _get_workout_params(workout_type)
    program = _get_options(workout_params)
    try:
        load = data["loads"][workout_type]
    except KeyError:
        console.print(
            f"Could not find load for {workout_type} in the database.", WARNING
        )
        console.print(
            "Try running [underline]kettlebells setloads -p[/underline]", SUGGESTION
        )
    week = Prompt.ask("Enter the week")
    day = Prompt.ask("Enter the day")
    variation = f"W{week}D{day}"
    time = IntPrompt.ask("Workout duration (mins)")
    sets = IntPrompt.ask("Number of sets")
    exercises = []
    for exercise in workout_params[program][variation]:
        if isinstance(exercise["reps"], list):
            exercise["reps"] = sum(exercise["reps"])
        exercise["sets"] = sets
        exercise["load"] = load
        exercises.append(Exercise(**exercise))
    if Confirm.ask("Did you do any auxiliary exercises"):
        auxiliary_exercises = add_exercises(db_path, bodyweight, units)
        exercises.extend(auxiliary_exercises)

    return Workout(
        workout_type=program,
        variation=variation,
        time=time,
        units=units,
        bodyweight=bodyweight,
        exercises=exercises,
    )


def create_set_based_workout(db_path: Path, workout_type: str) -> Workout:
    """Create a workout based on a given number of sets.

    Args:
        db_path: The path to the database.
        workout_type: The name of the program.

    Returns:
        The workout object for a given day of a program.
    """
    data = read_database(db_path)
    bodyweight = data["loads"]["bodyweight"]
    units = data["loads"]["units"]
    workout_type, workout_params = _get_workout_params(workout_type)
    program = _get_options(workout_params)
    try:
        load = data["loads"][workout_type]
    except KeyError:
        console.print(
            f"Could not find load for {workout_type} in the database.", style=WARNING
        )
        console.print(
            "Try running [underline]kettlebells setloads -p[/underline]",
            style=SUGGESTION,
        )
        sys.exit()
    week = Prompt.ask("Enter the week")
    day = Prompt.ask("Enter the day")
    variation = f"W{week}D{day}"
    time = IntPrompt.ask("How long was your workout (mins)")
    exercises = []
    for exercise in workout_params[program][variation]:
        exercise["load"] = load
        exercises.append(Exercise(**exercise))
    return Workout(
        workout_type=program,
        variation=variation,
        time=time,
        units=units,
        bodyweight=bodyweight,
        exercises=exercises,
    )


def create_workout_generator_workout(db_path: Path) -> Workout:
    """Create a workout based on the Dan John Workout Generator.

    Args:
        db_path: The path to the database.

    Returns:
        A custom workout object built by the user.
    """
    data = read_database(db_path)
    bodyweight = data["loads"]["bodyweight"]
    units = data["loads"]["units"]
    workout_type, workout_params = _get_workout_params("wg")
    variation = _get_options(workout_params)
    if workout_params[variation].get("time"):
        time = workout_params[variation]["time"]
    else:
        time = IntPrompt.ask("Duration (mins)")
    exercises = []
    while True:
        name = _get_exercise(db_path)
        if not name:
            break
        console.print(name)
        load = IntPrompt.ask(_load_label(name, units))
        sets = workout_params[variation]["sets"]
        reps = IntPrompt.ask("  (Average) Reps per set")
        exercises.append(Exercise(name=name, load=load, sets=sets, reps=reps))
    return Workout(
        workout_type=workout_type,
        variation=variation.title(),
        time=time,
        units=units,
        bodyweight=bodyweight,
        exercises=exercises,
    )


def create_rite_of_passage_workout(db_path: Path) -> Workout:
    """Create a Rite of Passage workout.

    Args:
        db_path: The Path to the database.

    Returns:
        A workout object.
    """
    data = read_database(db_path)
    bodyweight = data["loads"]["bodyweight"]
    units = data["loads"]["units"]
    workout_type, workout_params = _get_workout_params("rop")
    variation = _get_options(workout_params)
    time = IntPrompt.ask("Workout duration (mins)")
    exercises = []
    while True:
        name = _get_options(workout_params[variation]["exercises"])
        if name.lower() == "done":
            break
        load = IntPrompt.ask(_load_label(name, units))
        if name in ["Kettlebell Swing", "Kettlebell Snatch"]:
            sets = IntPrompt.ask("  Number of sets")
            reps = IntPrompt.ask("  Number of reps")
        else:
            sets = IntPrompt.ask("  Number of ladders")
            rungs = IntPrompt.ask("  Number of rungs")
            reps = rungs * (rungs + 1) // 2
        if name.lower() == "kettlebell clean and press":
            reps *= 2
        exercises.append(Exercise(name=name, load=load, sets=sets, reps=reps))
    return Workout(
        workout_type=workout_type,
        variation=f"{variation:0>2}",
        time=time,
        units=units,
        bodyweight=bodyweight,
        exercises=exercises,
    )


def _load_label(name: str, units: str) -> str:
    if name in BODYWEIGHT_FACTORS:
        return f"  Added weight in {units} (0 for bodyweight only)"
    return f"  Load in {units}"


def add_exercises(db_path: Path, bodyweight, units) -> list[Exercise]:
    exercises = []
    while True:
        name = _get_exercise(db_path)
        if not name:
            break
        console.print(name)
        load = IntPrompt.ask(_load_label(name, units))
        sets = IntPrompt.ask("  Number of sets")
        reps = IntPrompt.ask("  Reps per set")
        exercises.append(Exercise(name=name, load=load, sets=sets, reps=reps))
    return exercises


def create_custom_workout(db_path: Path) -> Workout:
    """Create a custom workout.

    Args:
        db_path: The path to the database.

    Returns:
        A custom workout object built by the user.
    """
    data = read_database(db_path)
    bodyweight = data["loads"]["bodyweight"]
    units = data["loads"]["units"]
    workout_type = Prompt.ask("Type of workout")
    if not workout_type:
        workout_type = "custom"
    variation = Prompt.ask("Variation")
    if not variation:
        variation = "Custom"
    time = IntPrompt.ask("Duration (mins)")
    exercises = add_exercises(db_path, bodyweight, units)

    return Workout(
        workout_type=workout_type,
        variation=variation.title(),
        time=time,
        units=units,
        bodyweight=bodyweight,
        exercises=exercises,
    )


def create_abf_barbell_workout(db_path: Path) -> Workout:
    """Create an Amor Building Formula Barbell workout.

    Args:
        db_path: The path to the database.

    Returns:
        A workout object built by the user.
    """
    data = read_database(db_path)
    bodyweight = data["loads"]["bodyweight"]
    units = data["loads"]["units"]
    workout_type, workout_param = _get_workout_params("abfb")
    variation = _get_options(workout_param["variations"])
    time = IntPrompt.ask("Duration (mins)")
    exercises = []
    if variation == "Program Three":
        squat_reps = IntPrompt.ask("Reps per set for front squat")
    for exercise in workout_param["exercises"]:
        print()
        print(exercise)
        if exercise == "Curl":
            sets_left = IntPrompt.ask(f"Number of total sets in the {exercise}")
        else:
            sets_left = workout_param["exercises"][exercise]["sets"]
        while sets_left > 0:
            load = IntPrompt.ask("  Load in lbs")
            sets = IntPrompt.ask("  Number of sets at this load")
            reps = workout_param["exercises"][exercise]["reps"]
            sets_left -= sets
            load = convert_pounds_to_kilos(load)
            exercises.append(Exercise(name=exercise, load=load, sets=sets, reps=reps))
            if variation == "Program Three" and exercise == "Clean and Press":
                exercises.append(
                    Exercise(name="Front Squat", load=load, sets=sets, reps=squat_reps)
                )
    if Confirm.ask("Did you do any auxiliary exercises"):
        auxiliary_exercises = add_exercises(db_path, bodyweight, units)
        exercises.extend(auxiliary_exercises)
    print()
    return Workout(
        workout_type=workout_type,
        variation=variation.title(),
        time=time,
        units=units,
        bodyweight=bodyweight,
        exercises=exercises,
    )


def create_abf_workout(db_path: Path) -> Workout:
    """Create an armor building formula Workout.

    Args:
        db_path: The Path object to the database.

    Returns:
        A Workout object created by the user.
    """
    data = read_database(db_path)
    bodyweight = data["loads"]["bodyweight"]
    units = data["loads"]["units"]
    workout_type, workout_params = _get_workout_params("abf")
    variation = _get_options(workout_params)
    time = IntPrompt.ask("How long was your workout (mins)")
    load = IntPrompt.ask(f"What weight did you use ({units})")
    exercises = []
    if variation in ("Armor Building Complex", "Intro"):
        sets = IntPrompt.ask("How many rounds of ABC did you complete?")
        for exercise, reps in workout_params["Armor Building Complex"]:
            exercises.append(
                Exercise(
                    name=exercise,
                    load=load,
                    sets=sets,
                    reps=reps,
                )
            )
    if variation in ("Double Kettlebell Press", "Intro"):
        for exercise, reps in workout_params["Double Kettlebell Press"]:
            sets = IntPrompt.ask(f"How many sets of {reps} reps did you complete")
            exercises.append(
                Exercise(
                    name=exercise,
                    load=load,
                    sets=sets,
                    reps=reps,
                )
            )
    return Workout(
        workout_type=workout_type,
        variation=variation,
        time=time,
        units=units,
        bodyweight=bodyweight,
        exercises=exercises,
    )


def prompt_exercises(db_path: Path, exercises: list[Exercise], units: str) -> list[Exercise]:
    """Go through exercises with their current values as defaults.

    Enter keeps an exercise as is, a new value such as 3x5@24, 2x5@185lb or 3x3+20
    replaces it, and - drops it. More exercises can be added at the end.
    """
    console.print(
        f"Press Enter to keep, type a new value (3x5@24, 2x5@185lb, 3x3+20; loads in {units} "
        "unless given), or - to drop an exercise.",
        style=SUGGESTION,
    )
    result = []
    for exercise in exercises:
        default = format_spec(exercise.name, exercise.sets, exercise.reps, exercise.load)
        while True:
            answer = Prompt.ask(f"  {exercise.name}", default=default).strip()
            if answer in ("-", "skip"):
                break
            try:
                sets, reps, load = parse_spec(answer, units)
            except EntryError as error:
                console.print(f":warning: {error}", style=WARNING)
                continue
            result.append(Exercise(name=exercise.name, load=load, sets=sets, reps=reps))
            break
    if Confirm.ask("Add more exercises?", default=False):
        result.extend(add_exercises(db_path, 0, units))
    return result


def last_workout_of_type(data: dict, workout_type: str) -> tuple[str, Workout] | None:
    """The date and workout of the most recent saved workout of a type."""
    key = workout_type.casefold()
    for entry in reversed(data.get("saved_workouts", [])):
        if entry["workout"]["workout_type"].casefold() == key:
            return entry["date"], Workout(**entry["workout"])
    return None


def _recent_workout_types(data: dict, limit: int = 10) -> list[str]:
    types: list[str] = []
    for entry in reversed(data.get("saved_workouts", [])):
        workout_type = entry["workout"]["workout_type"]
        if workout_type not in types:
            types.append(workout_type)
        if len(types) == limit:
            break
    return types


def _find_key(options, name: str) -> str | None:
    return next((key for key in options if key.casefold() == name.casefold()), None)


def create_template(db_path: Path) -> None:
    """Create a template for a program, or update an existing one."""
    data = read_database(db_path)
    units = data["loads"]["units"]
    bodyweight = data["loads"]["bodyweight"]
    templates = data.setdefault("templates", {})
    if templates:
        console.print("Existing templates:")
        for workout_type, variations in templates.items():
            console.print(f"    {workout_type.title()}: {', '.join(variations)}")
    workout_type = resolve_workout_type(Prompt.ask("Type of workout (a code such as es, or a name)"), data)
    workout_type = _find_key(templates, workout_type) or workout_type
    variation = Prompt.ask("Template name (e.g. regular, light, The Bull)")
    variation = _find_key(templates.get(workout_type, {}), variation) or variation
    existing = templates.get(workout_type, {}).get(variation)
    if existing:
        console.print(f"Updating the {workout_type.title()} {variation} template.")
        exercises = prompt_exercises(db_path, [Exercise(**e) for e in existing["exercises"]], units)
    else:
        last = last_workout_of_type(data, workout_type)
        if last and Confirm.ask(f"Start from your last {workout_type.title()} workout ({last[0]})?"):
            exercises = prompt_exercises(db_path, last[1].exercises, units)
        else:
            exercises = add_exercises(db_path, bodyweight, units)
    # Re-read: adding a new exercise above writes it to the database.
    data = read_database(db_path)
    data.setdefault("templates", {}).setdefault(workout_type, {})[variation] = {
        "exercises": [e.model_dump() for e in exercises]
    }
    write_database(db_path, data)
    console.print(f"Saved the {workout_type.title()} {variation} template.")


def create_from_template(db_path: Path, workout_type: str | None = None) -> Workout | None:
    """Create a workout from a saved template, with each exercise editable."""
    data = read_database(db_path)
    templates = data.get("templates", {})
    if workout_type is None and templates:
        workout_type = _get_options(list(templates))
    key = _find_key(templates, workout_type or "")
    if key is None:
        console.print(f":warning: No templates for {workout_type or 'any workout'}.", style=WARNING)
        console.print(
            "Create one with [underline]kettlebells template[/underline].", style=SUGGESTION
        )
        return None
    variations = templates[key]
    if len(variations) > 1:
        template_name = _get_options(list(variations))
    else:
        template_name = next(iter(variations))
    units = data["loads"]["units"]
    last = last_workout_of_type(data, key)
    if last and any(c.isdigit() for c in last[1].variation):
        default_variation = bump_variation(last[1].variation)
    else:
        default_variation = template_name.title()
    variation = Prompt.ask("Variation (e.g. the day)", default=default_variation)
    time = IntPrompt.ask("Workout duration (mins)")
    exercises = [Exercise(**e) for e in variations[template_name]["exercises"]]
    exercises = prompt_exercises(db_path, exercises, units)
    return Workout(
        workout_type=key,
        variation=variation,
        time=time,
        units=units,
        bodyweight=data["loads"]["bodyweight"],
        exercises=exercises,
    )


def repeat_last_workout(db_path: Path, workout_type: str | None = None) -> Workout | None:
    """Copy the last workout of a type, bumping the day, with each exercise editable."""
    data = read_database(db_path)
    if not data.get("saved_workouts"):
        console.print(":warning: There are no saved workouts to repeat.", style=WARNING)
        return None
    if workout_type:
        workout_type = resolve_workout_type(workout_type, data)
    else:
        workout_type = _get_options(_recent_workout_types(data))
    found = last_workout_of_type(data, workout_type)
    if found is None:
        console.print(f":warning: No saved {workout_type} workouts.", style=WARNING)
        return None
    date, last = found
    console.print(f"Repeating your {last.workout_type.title()} {last.variation} workout from {date}.")
    variation = Prompt.ask("Variation (e.g. the day)", default=bump_variation(last.variation))
    time = IntPrompt.ask("Workout duration (mins)", default=last.time)
    exercises = prompt_exercises(db_path, last.exercises, data["loads"]["units"])
    return Workout(
        workout_type=last.workout_type,
        variation=variation,
        time=time,
        units=data["loads"]["units"],
        bodyweight=data["loads"]["bodyweight"],
        exercises=exercises,
    )


def edit_workout(db_path: Path, date: str, workout: Workout) -> tuple[str, Workout]:
    """Edit every field of a saved workout, with the current values as defaults."""
    data = read_database(db_path)
    while True:
        new_date = Prompt.ask("Date (YYYY-MM-DD)", default=date)
        try:
            datetime.strptime(new_date, DATE_FORMAT)
            break
        except ValueError:
            console.print(f":warning: {new_date} not a valid date.", style=WARNING)
    workout_type = normalize_workout_type(Prompt.ask("Type of workout", default=workout.workout_type), data)
    variation = Prompt.ask("Variation", default=workout.variation)
    time = IntPrompt.ask("Workout duration (mins)", default=workout.time)
    bodyweight = IntPrompt.ask(f"Bodyweight ({workout.units})", default=workout.bodyweight)
    exercises = prompt_exercises(db_path, workout.exercises, workout.units)
    notes = Prompt.ask("Notes (- to clear)", default=workout.notes or None, show_default=bool(workout.notes)) or ""
    return new_date, Workout(
        workout_type=workout_type,
        variation=variation,
        time=time,
        units=workout.units,
        bodyweight=bodyweight,
        exercises=exercises,
        notes="" if notes.strip() == "-" else notes.strip(),
    )


def _get_options(options: dict | list) -> str:
    """Select options for a given workout parameter.
    Args:
        workout_param: options for a given workout parameter.
    Returns:
        A string consisting of the workout parameter choosen by the user.
    """
    if isinstance(options, dict):
        options = list(options.keys())
    for i, option in enumerate(options, 1):
        console.print(f"    [{i}] {option.title()}")
    while True:
        try:
            selection = IntPrompt.ask("Choose your option")
            return options[selection - 1]
        except (IndexError, TypeError):
            console.print(":warning: Not a valid option.", style=WARNING)
            console.print(
                "Enter a number between 1 and {max(options) + 1}.", style=SUGGESTION
            )
            continue


def _get_units() -> str:
    """A helper function to get the units.

    Returns:
        A string, either 'lbs' or 'kg'.
    """
    while True:
        units = Prompt.ask("[P]ounds or [K]ilograms").lower()
        if units.startswith("p"):
            units = "lbs"
        elif units.startswith("k"):
            units = "kg"
        else:
            console.print(":warning: Invalid option", style=WARNING)
            console.print("Please enter P or K", style=SUGGESTION)
            continue
        break
    return units


def _get_workout_params(workout_type: str) -> tuple[str, dict]:
    """Gets the workout parameters from the constants file.

    Args:
        workout_type: The workout type: ic, abc, btb, or pw.

    Returns:
        A tuple of the long name, and the dict of parameters.
    """
    match workout_type:
        case "ic":
            return "iron cardio", IRON_CARDIO_PARAMS
        case "abc":
            return "armor building complex", ABC_PARAMS
        case "btb":
            return "back to basics", BTB_PARAMS
        case "pw":
            return "perfect workout", PW_PARAMS
        case "giant":
            return "the giant", THE_GIANT_PARAMS
        case "wolf":
            return "the wolf", THE_WOLF_PARAMS
        case "wg":
            return "workout generator", WORKOUT_GENERATOR_PARAMS
        case "rop":
            return "rite of passage", ROP_PARAMS
        case "abfb":
            return "armor building formula barbell", ABFB_PARAMS
        case "abf":
            return "armor building formula", ABF_PARAMS
        case "dfw":
            return "dry fighting weight", DFW_PARAMS


def convert_pounds_to_kilos(load: int) -> int:
    """Convert a load in pounds to kilograms."""
    return round(load * POUNDS_TO_KILOS_RATE, 0)


def add_exercise_to_database(db_path: Path, exercise: str) -> None:
    """Add an exercise to the database."""
    data = read_database(db_path)
    movements = []
    while True:
        movement = _get_options(HUMAN_MOVEMENTS)
        if movement == "done":
            break
        else:
            movements.append(movement)
    data["exercises"][exercise] = movements
    write_database(db_path, data)


def _print_helper(to_print: list) -> None:
    """Print out various workout parameters formatted based on longest label.

    Args:
        to_print: A list of workout parameters.
    """
    longest_label = len(max(to_print, key=lambda x: len(x[0]))[0])
    for label, value in to_print:
        console.print(f"{label: >{longest_label}}: {value}")
    console.print()


def _get_exercise(db_path: Path) -> str | None:
    environ["FZF_DEFAULT_OPTS"] = FZF_DEFAULT_OPTS
    exercises = read_database(db_path)["exercises"]
    exercise = iterfzf(exercises, multi=False)
    match exercise:
        case "Other":
            exercise = Prompt.ask("Name of exercise").title()
            add_exercise_to_database(db_path, exercise)
            return exercise
        case "Done" | None:
            return None
        case _:
            return exercise
