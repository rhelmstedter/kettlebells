import sys
from datetime import datetime
from os import environ
from pathlib import Path

import typer
from rich.prompt import Confirm, Prompt
from trogon import Trogon
from typer.main import get_group
from typing_extensions import Annotated

from . import __version__
from .console import console
from .constants import (
    DATE_FORMAT,
    FZF_DEFAULT_OPTS,
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
    filter_by_program,
    get_all_stats,
    plot_workouts,
    print_calendar,
    retrieve_workout,
    top_ten_workouts,
    view_program,
)
from .workouts import (
    Workout,
    create_abf_barbell_workout,
    create_abf_workout,
    create_btb_workout,
    create_custom_workout,
    create_easy_strength_workout,
    create_ic_or_abc,
    create_perfect_workout,
    create_rite_of_passage_workout,
    create_set_based_workout,
    create_time_based_workout,
    create_workout_generator_workout,
    random_ic_or_abc,
    set_loads,
    set_program_loads,
)

cli = typer.Typer(add_completion=False)

environ["FZF_DEFAULT_OPTS"] = FZF_DEFAULT_OPTS


@cli.command()
def tui(ctx: typer.Context):
    Trogon(get_group(cli), click_context=ctx).run()


@cli.command()
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
        help="This will overwrite the existing database.",
    ),
) -> None:
    """Initializes the kettlebells database."""
    initialize_database(
        kettlebells_home=KETTLEBELLS_HOME,
        db_path=KETTLEBELLS_DB,
        force=force,
    )


@cli.command()
def setloads(
    ctx: typer.Context,
    program: bool = typer.Option(
        False,
        "--program",
        "-p",
        is_flag=True,
        is_eager=True,
        help="Add a load for a special program.",
    ),
) -> None:
    """Set units and loads for workouts."""
    data = read_database(KETTLEBELLS_DB)
    if program:
        data["loads"] = set_program_loads(data["loads"])
    else:
        loads = set_loads()
        data["loads"] = loads
    write_database(KETTLEBELLS_DB, data)


@cli.command()
def random(
    ctx: typer.Context,
    workout_type: Annotated[
        str,
        typer.Option("--workout-type", "-w", help="Possible workout types: ic or abc."),
    ],
) -> None:
    """Create a random iron cardio or armor building complex workout."""
    confirm_loads(KETTLEBELLS_DB)
    workout = random_ic_or_abc(KETTLEBELLS_DB, workout_type)
    cache_workout(KETTLEBELLS_DB, workout)
    workout.display_workout()


@cli.command()
def save(
    ctx: typer.Context,
    workout_type: Annotated[
        str,
        typer.Option(
            "--workout-type",
            "-w",
            help="Possible workout-types: ic, abc, btb, dfw, es, pw, wolf, wg, rop, or custom.",
        ),
    ] = None,
) -> None:
    """Save a kettlebell workout.

    If no argument is passed, kettlebells will attempt to use the most recently generated workout.
    """
    confirm_loads(KETTLEBELLS_DB)
    data = read_database(KETTLEBELLS_DB)
    match workout_type:
        case "ic" | "abc":
            workout = create_ic_or_abc(KETTLEBELLS_DB, workout_type)
        case "btb":
            workout = create_btb_workout(KETTLEBELLS_DB)
        case "custom":
            workout = create_custom_workout(KETTLEBELLS_DB)
        case "pw":
            workout = create_perfect_workout(KETTLEBELLS_DB)
        case "giant" | "dfw":
            workout = create_time_based_workout(KETTLEBELLS_DB, workout_type)
        case "wolf":
            workout = create_set_based_workout(KETTLEBELLS_DB, workout_type)
        case "es":
            workout = create_easy_strength_workout(KETTLEBELLS_DB, workout_type)
        case "wg":
            workout = create_workout_generator_workout(KETTLEBELLS_DB)
        case "rop":
            workout = create_rite_of_passage_workout(KETTLEBELLS_DB)
        case "abfb":
            workout = create_abf_barbell_workout(KETTLEBELLS_DB)
        case "abf":
            workout = create_abf_workout(KETTLEBELLS_DB)
        case None:
            workout = Workout(**data["cached_workouts"][-1])
            console.print("Last workout generated:\n")
        case _:
            console.print(
                f"'{workout_type.strip()}' is not an option.",
                style=WARNING,
            )
            console.print(
                "Try running [underline]kettlebells save --help[/underline]",
                style=SUGGESTION,
            )
            return

    if workout is None:
        return
    workout.display_workout()
    if Confirm.ask("Save this workout?"):
        workout_date = _get_date()
        save_workout(KETTLEBELLS_DB, workout_date, workout)
        print()
        workout.display_workout_stats()
    else:
        console.print("Workout not saved.")


@cli.command()
def view(
    ctx: typer.Context,
    preview: Annotated[
        bool,
        typer.Option(
            "--preview",
            "-p",
            help="Display a preview of workouts in database.",
            is_flag=True,
        ),
    ] = False,
    program: Annotated[
        bool,
        typer.Option(
            "--program",
            "-P",
            help="Filter out workouts of a certain program.",
            is_flag=True,
        ),
    ] = False,
    display_workout: Annotated[
        bool,
        typer.Option(
            "--display_workout",
            "-d",
            help="Display individual workouts in a program.",
            is_flag=True,
        ),
    ] = False,
) -> None:
    """Display stats of a given workout or program."""
    data = read_database(KETTLEBELLS_DB)
    if program:
        data, program = filter_by_program(data)
        table = view_program(data, program, display_workout)
        console.print(table)
        get_all_stats(data, program)
        return
    try:
        date, workout = retrieve_workout(data, preview)
        console.print(
            f"\nDate: [green]{datetime.strptime(date, DATE_FORMAT):%b %d, %Y}\n"
        )
        workout.display_workout()
        print()
        workout.display_workout_stats()
    except TypeError:
        return


@cli.command()
def last(ctx: typer.Context) -> None:
    """Display stats from most recent workout in database."""
    data = read_database(KETTLEBELLS_DB)
    last_workout = data["saved_workouts"][-1]
    workout_date = last_workout["date"]
    workout = Workout(**last_workout["workout"])
    console.print(
        f"\nDate: [green]{datetime.strptime(workout_date, DATE_FORMAT):%b %d, %Y}\n"
    )
    workout.display_workout()
    print()
    workout.display_workout_stats()


@cli.command()
def stats(
    ctx: typer.Context,
    plot: Annotated[
        str,
        typer.Option(
            "--plot",
            "-p",
            help="Possible plots: line, event, bar.",
        ),
    ] = "",
    year: Annotated[
        int,
        typer.Option(
            "--year",
            "-y",
            help="Year to display calendar and event plot for.",
        ),
    ] = None,
    sort: Annotated[
        str,
        typer.Option(
            "--sort",
            "-S",
            help="Sort the best table. Possible arguments: weight-moved, reps, weight-density, rep-density.",
        ),
    ] = "weight-moved",
    start: Annotated[
        str,
        typer.Option(
            "--start",
            "-s",
            help="Start date (YYYY-MM-DD).",
        ),
    ] = None,
    end: Annotated[
        str,
        typer.Option(
            "--end",
            "-e",
            help="End date (YYYY-MM-DD).",
        ),
    ] = None,
    calendar: Annotated[
        bool,
        typer.Option(
            "--calendar",
            "-c",
            help="Highlight days workouts were completed in a calendar.",
            is_flag=True,
        ),
    ] = False,
    median: Annotated[
        bool,
        typer.Option(
            "--median",
            "-m",
            help="A horizontal line at the median weight per workout. Use in conjunction with --plot.",
            is_flag=True,
        ),
    ] = False,
    average: Annotated[
        bool,
        typer.Option(
            "--average",
            "-a",
            help="A horizontal line at the mean weight per workout. Use in conjunction with --plot.",
            is_flag=True,
        ),
    ] = False,
    best: Annotated[
        bool,
        typer.Option(
            "--best",
            "-b",
            help="Show the top ten workouts in a table.",
            is_flag=True,
        ),
    ] = None,
) -> None:
    """Display stats from all workouts in database."""
    data = read_database(KETTLEBELLS_DB)
    if calendar and not year:
        year = datetime.now().year
    if year:
        dates, weight_per_workout = get_all_stats(
            data,
            start=f"{year}-01-01",
            end=f"{year}-12-31",
            year=year,
        )
    else:
        dates, weight_per_workout = get_all_stats(data, start=start, end=end)
    if plot:
        plot_workouts(dates, weight_per_workout, plot, median, average, year)
    if calendar:
        print_calendar(data, year)
    if best:
        console.print(top_ten_workouts(data, sort))


def _get_date() -> str:
    """A helper function to get the date of a workout.

    Returns:
        A str of the date formatted as YYYY-MM-DD.
    """
    while True:
        workout_date = Prompt.ask(
            "Enter the date of the workout (YYYY-MM-DD), or press enter for today"
        )
        if not workout_date:
            workout_date = datetime.now().strftime(DATE_FORMAT)
        try:
            datetime.strptime(workout_date, DATE_FORMAT)
            break
        except ValueError:
            console.print(f":warning: {workout_date} not a valid date.", style=WARNING)
            continue
    return workout_date


if __name__ == "__main__":
    cli()
