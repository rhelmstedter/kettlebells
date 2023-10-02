from dataclasses import dataclass

from pathlib import Path
from random import choice, choices

from rich import print
from rich.prompt import Confirm, IntPrompt, Prompt

from .console import console
from .constants import (
    IRON_CARDIO_PARAMS,
    SUGGESTION,
    WARNING,
)
from .database import read_database


@dataclass
class Workout:
    bells: str
    variation: str
    time: int
    load: int
    units: str
    swings: int
    sets: int
    reps: int
    workout_type: str

    def display_workout(self) -> None:
        """Print an a workout to the console.
        :returns: None.
        """
        if self.swings:
            swings = f"   Swings: {self.swings} reps"
        else:
            swings = ""
        print(
            f"""{self.workout_type.upper()}\n[green]===================[/green]
    Bells: {self.bells.title()}
Variation: {self.variation}
     Time: {self.time} mins
     Load: {self.load} {self.units}
{swings}
"""
        )


def random_ic_session(db_path: Path) -> Workout:
    """Create a random Iron Cardio Session.
    :param db_path: The Path to the database.
    :returns: A Session object with randomly generated parameters.
    """
    data = read_database(db_path)
    loads = data["ic_loads"]
    bells = choices(
        population=tuple(IRON_CARDIO_PARAMS["bells"].keys()),
        weights=tuple(IRON_CARDIO_PARAMS["bells"].values()),
    )[0]
    if bells == "Double Bells":
        variation = choices(
            population=tuple(IRON_CARDIO_PARAMS["doublebell variations"].keys()),
            weights=tuple(IRON_CARDIO_PARAMS["doublebell variations"].values()),
        )[0]
    elif bells == "Single Bell":
        variation = choices(
            population=tuple(IRON_CARDIO_PARAMS["singlebell variations"].keys()),
            weights=tuple(IRON_CARDIO_PARAMS["singlebell variations"].values()),
        )[0]
    time = choices(
        population=tuple(IRON_CARDIO_PARAMS["times"].keys()),
        weights=tuple(IRON_CARDIO_PARAMS["times"].values()),
    )[0]
    load = choices(
        population=tuple(IRON_CARDIO_PARAMS["loads"].keys()),
        weights=tuple(IRON_CARDIO_PARAMS["loads"].values()),
    )[0]
    swings = choices(
        population=tuple(IRON_CARDIO_PARAMS["swings"].keys()),
        weights=tuple(IRON_CARDIO_PARAMS["swings"].values()),
    )[0]
    load = loads[load]
    units = loads["units"]
    if swings:
        swings = choice(range(50, 160, 10))
    else:
        swings = 0
    return Workout(
        bells=bells,
        variation=variation,
        time=time,
        load=load,
        units=units,
        swings=swings,
        sets=0,
        reps=IRON_CARDIO_PARAMS["rep schemes"][variation],
        workout_type="iron cardio",
    )


def _get_options(session_param: dict) -> str:
    """Select options for a given Session parameter.
    :param session_param: The dictionary containing options for a Session parameter.
    :returns: A string consisting of the Session parameter choosen by the user.
    """
    options = list(session_param.keys())
    for i, option in enumerate(options, 1):
        print(f"    [{i}] {option}")
    while True:
        try:
            selection = IntPrompt.ask("Choose your option")
            return options[selection - 1]
        except IndexError:
            print(':warning: Not a valid option.', style=WARNING)
            print('Enter a number between 1 and {max(options) + 1}.', style=SUGGESTION)
            continue


def create_custom_ic_session() -> Workout:
    """Create a custom Iron Cardio session.
    :returns: An Workout object created by the user.
    """
    bells = _get_options(IRON_CARDIO_PARAMS["bells"])
    if bells == "Double Bells":
        variation = _get_options(IRON_CARDIO_PARAMS["doublebell variations"])
    elif bells == "Single Bell":
        variation = _get_options(IRON_CARDIO_PARAMS["singlebell variations"])
    time = IntPrompt.ask("How long was your session (in minutes)")
    units = _get_units()
    load = IntPrompt.ask(f"What weight did you use (in {units})")
    if Confirm.ask("Did you swing"):
        swings = IntPrompt.ask("How many swings")
    else:
        swings = 0
    return Workout(
        bells,
        variation,
        time,
        load,
        units,
        swings,
        0,
        IRON_CARDIO_PARAMS["rep schemes"][variation],
        "iron cardio",
    )


def _get_units():
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


def set_ic_loads() -> dict:
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
            "Are these loads correct? If you confirm, they will be used to generate Iron Cardio sessions."
        ):
            break
    return loads
