from dataclasses import dataclass
from pathlib import Path
from random import choice, choices

from rich import print
from rich.prompt import Confirm, IntPrompt, Prompt

from .console import console
from .constants import (
    BELLS,
    DOUBLEBELL_VARIATIONS,
    LOADS,
    SINGLEBELL_VARIATIONS,
    SWINGS,
    TIMES,
)
from .iron_cardio_database import read_database


@dataclass
class Session:
    bells: str
    variation: str
    time: int
    load: int
    units: str
    swings: int
    sets: int = 0


def create_session(db_path: Path) -> Session:
    """Create a random Iron Cardio Session.
    :param db_path: The Path to the database.
    :returns: A Session object with randomly generated parameters.
    """
    data = read_database(db_path)
    loads = data["loads"]
    bells = choices(
        population=tuple(BELLS.keys()),
        weights=tuple(BELLS.values()),
    )[0]
    if bells == "Double Bells":
        variation = choices(
            population=tuple(DOUBLEBELL_VARIATIONS.keys()),
            weights=tuple(DOUBLEBELL_VARIATIONS.values()),
        )[0]
    elif bells == "Single Bell":
        variation = choices(
            population=tuple(SINGLEBELL_VARIATIONS.keys()),
            weights=tuple(SINGLEBELL_VARIATIONS.values()),
        )[0]
    time = choices(
        population=tuple(TIMES.keys()),
        weights=tuple(TIMES.values()),
    )[0]
    load = choices(
        population=tuple(LOADS.keys()),
        weights=tuple(LOADS.values()),
    )[0]
    swings = choices(
        population=tuple(SWINGS.keys()),
        weights=tuple(SWINGS.values()),
    )[0]
    load = loads[load]
    units = loads["units"]
    if swings:
        swings = choice(range(50, 160, 10))
    else:
        swings = 0
    return Session(bells, variation, time, load, units, swings)


def _get_options(session_param: dict) -> str:
    """Select options for a given Session parameter.
    :param session_param: The dictionary containing options for a Session parameter.
    :returns: A string consisting of the Session parameter choosen by the user.
    """
    options = list(session_param.keys())
    for i, option in enumerate(options, 1):
        print(f"    [{i}] {option}")
    selection = IntPrompt.ask("Choose your option")
    return options[selection - 1]


def create_custom_session() -> Session:
    """Create a custom Iron Cardio session.
    :returns: A Session object created by the user.
    """
    bells = _get_options(BELLS)
    if bells == "Double Bells":
        variation = _get_options(DOUBLEBELL_VARIATIONS)
    elif bells == "Single Bell":
        variation = _get_options(SINGLEBELL_VARIATIONS)
    time = IntPrompt.ask("How long was your session (in minutes)")
    units = _get_units()
    load = IntPrompt.ask(f"What weight did you use (in {units})")
    if Confirm.ask("Did you swing"):
        swings = IntPrompt.ask("How many swings")
    else:
        swings = 0
    return Session(bells, variation, time, load, units, swings)


def display_session(session: Session) -> None:
    """Print a session to the console.
    :param session: The Session object to be displayed in the console.
    :returns: None.
    """
    if session.swings:
        swings = f"   Swings: {session.swings} reps"
    else:
        swings = ""
    print(
        f"""Iron Cardio Session
[green]===================[/green]
    Bells: {session.bells.title()}
Variation: {session.variation}
     Time: {session.time} mins
     Load: {session.load} {session.units}
{swings}
    """
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
            console.print("[yellow]Please enter a p or k[/yellow]")
            continue
        break
    return units


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
            "Are these loads correct? If you confirm, they will be used to generate sessions."
        ):
            break
    return loads


# def simulation() -> None:
#     """A simulation of a year of generated sessions.
#     :returns: None.
#     """
#     sessions = [create_session() for s in range(3 * 52)]
#     stats = Counter()
#     for session in sessions:
#         for c in session:
#             if isinstance(c, int):
#                 c = "Swings"
#             stats.update([c])
#     one_year = dict(sorted(stats.items(), key=lambda x: x[1], reverse=True))
#     width = len(max(one_year.keys(), key=len))
#     for session, count in one_year.items():
#         print(f"{session: >{width}}: " + "#" * count)
#         print(f"{session: >{width}}: " + "#" * count)
