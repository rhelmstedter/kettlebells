import sys
from datetime import date, datetime
from pathlib import Path
from typing import Optional

import typer
from rich.prompt import Confirm, Prompt
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
    save_workout,
    write_database,
)
from .stats import (
    get_all_time_stats,
    top_ten_workouts,
    plot_workouts,
)
from .workouts import Workout, Exercise, create_custom_workout, random_workout, set_loads

cli = typer.Typer(add_completion=False)


def report_version(display: bool) -> None:
    """Print version and exit."""
    if display:
        console.print(f"{Path(sys.argv[0]).name} {__version__}")
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
    """Set units and loads for workouts."""
    loads = set_loads()
    data = read_database(KETTLEBELLS_DB)
    data["loads"] = loads
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
        workout = create_custom_workout(KETTLEBELLS_DB, workout_type)
        workout.display_workout()
    else:
        workout = Workout(**data["cached_workouts"][-1])
        workout.exercises = [Exercise(**e) for e in workout.exercises]
        console.print("Last workout generated:\n")
        workout.display_workout()
    if Confirm.ask("Save this workout?"):
        while True:
            workout_date = Prompt.ask(
                "Enter the date of the workout (YYYY-MM-DD), or press enter for today"
            )
            if not workout_date:
                workout_date = date.today().strftime(DATE_FORMAT)
            try:
                datetime.strptime(workout_date, DATE_FORMAT)
                break
            except ValueError:
                console.print(
                    ":warning: {workout_date} not a valid date.", style=WARNING
                )
                continue
        save_workout(KETTLEBELLS_DB, workout_date, workout)
        print()
        workout.display_workout_stats()
    else:
        console.print("Workout not saved.")


@cli.command()
def last(ctx: typer.Context) -> None:
    """Display stats from most recent workout in database."""
    data = read_database(KETTLEBELLS_DB)
    last_workout = data["saved_workouts"][-1]
    workout_date = last_workout["date"]
    workout = Workout(**last_workout["workout"])
    workout.exercises = [Exercise(**e) for e in workout.exercises]
    console.print(f"\nDate: [green]{datetime.strptime(workout_date, DATE_FORMAT):%b %d, %Y}\n")
    workout.display_workout()
    print()
    workout.display_workout_stats()


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
    dates, weight_per_workout = get_all_time_stats(data)
    if plot:
        plot_workouts(dates, weight_per_workout)


@cli.command()
def best(
    ctx: typer.Context,
) -> None:
    """Display stats from the top ten w in database."""
    data = read_database(KETTLEBELLS_DB)
    top_ten_workouts(data)


if __name__ == "__main__":
    cli()
