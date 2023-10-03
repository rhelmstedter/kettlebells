import sys
from datetime import date, datetime
from pathlib import Path
from typing import Optional

import typer
from rich import print
from rich.prompt import Confirm, IntPrompt, Prompt
from typing_extensions import Annotated

from . import __version__
from .console import console
from .constants import (
    DATE_FORMAT,
    KETTLEBELLS_DB,
    KETTLEBELLS_HOME,
    SUGGESTION,
    WARNING,
)
from .database import (
    cache_workout,
    confirm_loads,
    initialize_database,
    read_database,
    save_session,
    write_database,
)
from .stats import (
    display_session_stats,
    get_all_time_stats,
    get_best_sessions,
    plot_sessions,
)
from .workouts import Workout, create_custom_workout, random_workout, set_loads

cli = typer.Typer(add_completion=False)


def report_version(display: bool) -> None:
    """Print version and exit."""
    if display:
        print(f"{Path(sys.argv[0]).name} {__version__}")
        raise typer.Exit()


@cli.callback()
def global_options(
    ctx: typer.Context,
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        is_flag=True,
        is_eager=True,
        callback=report_version,
    ),
):
    """Create, save, and track progress of kettlebell workouts."""


@cli.command()
def init(
    ctx: typer.Context,
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        is_flag=True,
        is_eager=True,
    ),
) -> None:
    """Initializes the kettlebells database."""
    initialize_database(
        kettlebells_home=KETTLEBELLS_HOME,
        db_path=KETTLEBELLS_DB,
        force=force,
    )


@cli.command()
def setloads(ctx: typer.Context) -> None:
    """Set units and loads for iron cardio sessions."""
    loads = set_loads()
    data = read_database(KETTLEBELLS_DB)
    data["ic_loads"] = loads
    write_database(KETTLEBELLS_DB, data)


@cli.command()
def workout(ctx: typer.Context, workout_type: str) -> None:
    """Create a random kettlebells workout."""
    confirm_loads(KETTLEBELLS_DB)
    if not workout_type:
        console.print(
            ":warning: [underline]kettlebells workout[/underline] requires a workout type.",
            style=WARNING,
        )
        console.print("Please specify a type of workout.", style=SUGGESTION)
    workout = random_workout(KETTLEBELLS_DB, workout_type)
    cache_workout(KETTLEBELLS_DB, workout)
    workout.display_workout()


@cli.command()
def done(
    ctx: typer.Context, workout_type: Annotated[Optional[str], typer.Argument()] = None
) -> None:
    """Save an kettlebells workout"""
    confirm_loads(KETTLEBELLS_DB)
    data = read_database(KETTLEBELLS_DB)
    if workout_type:
        session = create_custom_workout(workout_type)
        session.display_workout()
    else:
        session = Workout(**data["cached_sessions"][-1])
        console.print("Last workout generated:\n")
        session.display_workout()
    if Confirm.ask("Save this session?"):
        while True:
            session_date = Prompt.ask(
                "Enter the date of the workout (YYYY-MM-DD), or press enter for today"
            )
            if not session_date:
                session_date = date.today().strftime(DATE_FORMAT)
            try:
                datetime.strptime(session_date, DATE_FORMAT)
                break
            except ValueError:
                console.print(
                    ":warning: {session_date} not a valid date.", style=WARNING
                )
                continue
        session.sets = IntPrompt.ask("How many sets did you complete?")
        save_session(KETTLEBELLS_DB, session_date, session)
        bodyweight = data["ic_loads"]["bodyweight"]
        print()
        display_session_stats(session, bodyweight)
    else:
        console.print("Workout not saved.")


@cli.command()
def last(ctx: typer.Context) -> None:
    """Display stats from most recent session in database."""
    data = read_database(KETTLEBELLS_DB)
    last_session = data["saved_sessions"][-1]
    session_date = last_session["date"]
    session = Workout(**last_session["session"])
    bodyweight = data["ic_loads"]["bodyweight"]
    print(f"\nDate: [green]{datetime.strptime(session_date, DATE_FORMAT):%b %d, %Y}\n")
    session.display_workout()
    display_session_stats(session, bodyweight)


@cli.command()
def stats(
    ctx: typer.Context,
    plot: bool = typer.Option(
        False,
        "--plot",
        "-p",
        is_flag=True,
        is_eager=True,
    ),
) -> None:
    """Display stats from most recent workout in database."""
    data = read_database(KETTLEBELLS_DB)
    dates, weight_per_session = get_all_time_stats(data)
    if plot:
        plot_sessions(dates, weight_per_session)


@cli.command()
def best(
    ctx: typer.Context,
) -> None:
    """Display stats from the top ten w in database."""
    data = read_database(KETTLEBELLS_DB)
    get_best_sessions(data)


if __name__ == "__main__":
    cli()
