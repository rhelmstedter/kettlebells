import sys
from datetime import date, datetime
from pathlib import Path

import typer
from rich import print
from rich.prompt import Confirm, IntPrompt, Prompt

from . import __version__
from .console import console
from .constants import DATE_FORMAT, IRON_CARDIO_DB, IRON_CARDIO_HOME
from .iron_cardio import (
    Session,
    create_custom_session,
    create_session,
    display_session,
    set_loads,
)
from .iron_cardio_database import (
    cache_session,
    confirm_loads,
    initialize_database,
    read_database,
    save_session,
    write_database,
)
from .iron_cardio_stats import (
    display_session_stats,
    get_all_time_stats,
    get_best_sessions,
    plot_sessions,
)

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
    """Create, save, and track progress of Iron Cardio Sessions."""


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
    """Initializes the Iron Cardio database."""
    initialize_database(
        iron_cardio_home=IRON_CARDIO_HOME,
        db_path=IRON_CARDIO_DB,
        force=force,
    )


@cli.command()
def setloads(ctx: typer.Context) -> None:
    """Set units and loads for iron cardio sessions."""
    loads = set_loads()
    data = read_database(IRON_CARDIO_DB)
    data["loads"] = loads
    write_database(IRON_CARDIO_DB, data)


@cli.command()
def session(ctx: typer.Context) -> None:
    """Create a random Iron Cardio session."""
    confirm_loads(IRON_CARDIO_DB)
    session = create_session(IRON_CARDIO_DB)
    cache_session(IRON_CARDIO_DB, session)
    display_session(session)


@cli.command()
def done(
    ctx: typer.Context,
    custom: bool = typer.Option(
        False,
        "--custom",
        "-c",
        is_flag=True,
        is_eager=True,
    ),
) -> None:
    """Save an Iron Cardio session"""
    confirm_loads(IRON_CARDIO_DB)
    data = read_database(IRON_CARDIO_DB)
    if custom:
        session = create_custom_session()
        display_session(session)
    else:
        session = Session(**data["cached_sessions"][-1])
        console.print("Last workout generated:\n")
        display_session(session)
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
                console.print("[yellow]Please enter a valid date[/yellow]")
                continue
        session.sets = IntPrompt.ask("How many sets did you complete?")
        save_session(IRON_CARDIO_DB, session_date, session)
        bodyweight = data["loads"]["bodyweight"]
        print()
        display_session_stats(session, bodyweight)


@cli.command()
def last(ctx: typer.Context) -> None:
    """Display stats from most recent session in database."""
    data = read_database(IRON_CARDIO_DB)
    last_session = data["saved_sessions"][-1]
    session_date = last_session["date"]
    session = Session(**last_session["session"])
    bodyweight = data["loads"]["bodyweight"]
    print(f"\nDate: [green]{datetime.strptime(session_date, DATE_FORMAT): %b %d, %Y}\n")
    display_session(session)
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
    """Display stats from most recent session in database."""
    data = read_database(IRON_CARDIO_DB)
    dates, weight_per_session = get_all_time_stats(data)
    if plot:
        plot_sessions(dates, weight_per_session)


@cli.command()
def best(
    ctx: typer.Context,
) -> None:
    """Display stats from most recent session in database."""
    data = read_database(IRON_CARDIO_DB)
    get_best_sessions(data)


if __name__ == "__main__":
    cli()
