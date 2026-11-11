import sys
import webbrowser
from datetime import datetime
from os import environ
from pathlib import Path

import typer
from iterfzf import iterfzf
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
    delete_workout,
    initialize_database,
    read_database,
    replace_workout,
    save_workout,
    save_workouts,
    update_database,
    write_database,
)
from .entry import EntryError, parse_lines
from .names import exercise_aliases, known_exercises, workout_type_aliases
from .plots import plot_workouts, write_html_report
from .stats import (
    filter_by_program,
    get_all_stats,
    get_entries,
    get_exercises_by_movement,
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
    create_from_template,
    create_ic_or_abc,
    create_perfect_workout,
    create_rite_of_passage_workout,
    create_set_based_workout,
    create_template,
    create_time_based_workout,
    create_workout_generator_workout,
    edit_workout,
    random_ic_or_abc,
    repeat_last_workout,
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
def update(
    ctx: typer.Context,
) -> None:
    """Update the database with new exercises."""
    update_database(KETTLEBELLS_DB)


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
def template(
    ctx: typer.Context,
) -> None:
    """Create or update a template for a program (any workout type).

    Use it with `kettlebells save --template`; `save -w es` uses the easy strength templates.
    """
    confirm_loads(KETTLEBELLS_DB)
    create_template(KETTLEBELLS_DB)


@cli.command()
def save(
    ctx: typer.Context,
    workout_type: Annotated[
        str,
        typer.Option(
            "--workout-type",
            "-w",
            help="Possible workout-types: ic, abc, abf, abfb, btb, dfw, es, giant, pw, wolf, wg, rop, or custom.",
        ),
    ] = "",
    repeat: Annotated[
        bool,
        typer.Option(
            "--repeat",
            "-r",
            help="Copy your last workout of a type (-w, or pick one) and bump the day. "
            "Press Enter to keep each exercise or type a new value.",
            is_flag=True,
        ),
    ] = False,
    template: Annotated[
        bool,
        typer.Option(
            "--template",
            "-t",
            help="Start from a saved template (-w to pick the workout type, or pick one).",
            is_flag=True,
        ),
    ] = False,
) -> None:
    """Save a kettlebell workout.

    If no argument is passed, kettlebells will attempt to use the most recently generated workout.
    """
    confirm_loads(KETTLEBELLS_DB)
    if repeat or template:
        data = read_database(KETTLEBELLS_DB)
        resolved = workout_type_aliases(data).get(workout_type.strip().casefold(), workout_type.strip())
        if repeat:
            workout = repeat_last_workout(KETTLEBELLS_DB, resolved or None)
        else:
            workout = create_from_template(KETTLEBELLS_DB, resolved or None)
        _confirm_and_save(workout)
        return
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
            workout = create_easy_strength_workout(KETTLEBELLS_DB)
        case "wg":
            workout = create_workout_generator_workout(KETTLEBELLS_DB)
        case "rop":
            workout = create_rite_of_passage_workout(KETTLEBELLS_DB)
        case "abfb":
            workout = create_abf_barbell_workout(KETTLEBELLS_DB)
        case "abf":
            workout = create_abf_workout(KETTLEBELLS_DB)
        case "":
            data = read_database(KETTLEBELLS_DB)
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

    _confirm_and_save(workout)


def _confirm_and_save(workout: Workout | None) -> None:
    if workout is None:
        return
    workout.display_workout()
    if Confirm.ask("Save this workout?"):
        workout_date = _get_date()
        workout.notes = Prompt.ask("Notes (Enter for none)", default="", show_default=False).strip()
        save_workout(KETTLEBELLS_DB, workout_date, workout)
        print()
        workout.display_workout_stats()
    else:
        console.print("Workout not saved.")


@cli.command()
def add(
    ctx: typer.Context,
    date: Annotated[str, typer.Argument(help="Date of the workout (YYYY-MM-DD).")] = "",
    entry: Annotated[
        str,
        typer.Argument(help='The workout, e.g. "ES D11 16min; SGD 2x5@185lb; Chin 2x5+25lb; AW 1x10".'),
    ] = "",
    file: Annotated[
        Path | None,
        typer.Option(
            "--file",
            "-f",
            help="A text file with one 'YYYY-MM-DD <workout>' per line.",
            exists=True,
            dir_okay=False,
        ),
    ] = None,
    yes: Annotated[
        bool,
        typer.Option("--yes", "-y", help="Save without asking for confirmation.", is_flag=True),
    ] = False,
) -> None:
    """Save workouts written in the quick-entry format.

    Segments are separated by semicolons. The first is the workout type (es, ic, or a
    name), an optional variation (D11, W2D3) and the time (16min). Each exercise is a
    name or short name, sets x reps, and an optional load: @32, @185lb, or +25lb
    (added weight on bodyweight exercises). Text in (parentheses) and "note: ..."
    segments are saved as notes. Run `kettlebells alias` to see the short names.
    """
    confirm_loads(KETTLEBELLS_DB)
    data = read_database(KETTLEBELLS_DB)
    if file:
        lines = file.read_text().splitlines()
    elif date and entry:
        lines = [f"{date} {entry}"]
    else:
        console.print(":warning: Give a date and a workout, or --file.", style=WARNING)
        console.print("Try running [underline]kettlebells add --help[/underline]", style=SUGGESTION)
        raise typer.Exit(1)
    try:
        parsed = parse_lines(lines, data)
    except EntryError as error:
        console.print(f":warning: {error}", style=WARNING)
        raise typer.Exit(1)
    if not parsed:
        console.print("No workouts found.")
        return
    workouts = [(workout_date, Workout(**fields)) for workout_date, fields in parsed]
    for workout_date, workout in workouts:
        console.print(f"\nDate: [green]{datetime.strptime(workout_date, DATE_FORMAT):%b %d, %Y}\n")
        workout.display_workout()
    label = "this workout" if len(workouts) == 1 else f"these {len(workouts)} workouts"
    if yes or Confirm.ask(f"Save {label}?"):
        save_workouts(KETTLEBELLS_DB, workouts)
        console.print(f"Saved {label}.")
    else:
        console.print("Nothing saved.")


@cli.command()
def edit(
    ctx: typer.Context,
    date: Annotated[str, typer.Argument(help="Date of the workout to edit (YYYY-MM-DD).")] = "",
) -> None:
    """Edit a saved workout. Press Enter to keep each value."""
    data = read_database(KETTLEBELLS_DB)
    index = _pick_saved_workout(data, date)
    if index is None:
        return
    entry = data["saved_workouts"][index]
    workout = Workout(**entry["workout"])
    workout.display_workout()
    new_date, new_workout = edit_workout(KETTLEBELLS_DB, entry["date"], workout)
    console.print()
    new_workout.display_workout()
    if Confirm.ask("Save these changes?"):
        replace_workout(KETTLEBELLS_DB, index, new_date, new_workout)
        console.print("Workout updated.")
    else:
        console.print("No changes saved.")


@cli.command()
def delete(
    ctx: typer.Context,
    date: Annotated[str, typer.Argument(help="Date of the workout to delete (YYYY-MM-DD).")] = "",
) -> None:
    """Delete a saved workout. The database is backed up first."""
    data = read_database(KETTLEBELLS_DB)
    index = _pick_saved_workout(data, date)
    if index is None:
        return
    entry = data["saved_workouts"][index]
    console.print(f"\nDate: [green]{datetime.strptime(entry['date'], DATE_FORMAT):%b %d, %Y}\n")
    Workout(**entry["workout"]).display_workout()
    if Confirm.ask("Delete this workout?", default=False):
        delete_workout(KETTLEBELLS_DB, index)
        console.print("Workout deleted. A backup of the database is next to it in ~/.kettlebells.")
    else:
        console.print("Workout not deleted.")


@cli.command()
def alias(
    ctx: typer.Context,
    short: Annotated[str, typer.Argument(help="The short name, e.g. SGD.")] = "",
    name: Annotated[str, typer.Argument(help='The full name, e.g. "Snatch Grip Deadlift".')] = "",
    workout: Annotated[
        bool,
        typer.Option("--workout", "-w", help="The alias is for a workout type, not an exercise.", is_flag=True),
    ] = False,
    remove: Annotated[
        bool,
        typer.Option("--remove", "-r", help="Remove the alias.", is_flag=True),
    ] = False,
) -> None:
    """List, add, or remove short names used by `kettlebells add` and `save -w`."""
    data = read_database(KETTLEBELLS_DB)
    kind = "workout_types" if workout else "exercises"
    user_aliases = data.setdefault("aliases", {}).setdefault(kind, {})
    if not short:
        for label, aliases in (
            ("Exercises", exercise_aliases(data)),
            ("Workout types", workout_type_aliases(data)),
        ):
            console.print(label)
            console.print("-" * len(label), style="green")
            for key, value in sorted(aliases.items()):
                console.print(f"  {key.upper():>6}: {value}")
            console.print()
        return
    key = short.strip().casefold()
    if remove:
        if user_aliases.pop(key, None) is None:
            console.print(f"'{short}' is not one of your aliases.", style=WARNING)
            return
        console.print(f"Removed '{short}'.")
    else:
        if not name:
            console.print(":warning: Give the full name too.", style=WARNING)
            raise typer.Exit(1)
        name = name.strip()
        if not workout and name.casefold() not in known_exercises(data):
            console.print(f"Note: '{name}' is a new exercise name.", style=SUGGESTION)
        user_aliases[key] = name
        console.print(f"{short.upper()} -> {name}")
    write_database(KETTLEBELLS_DB, data)


def _pick_saved_workout(data: dict, date: str = "") -> int | None:
    """Choose a saved workout, newest first. Returns its index."""
    entries = [
        (i, e)
        for i, e in enumerate(data["saved_workouts"])
        if not date or e["date"] == date
    ]
    if not entries:
        console.print(f":warning: No saved workouts{' on ' + date if date else ''}.", style=WARNING)
        return None
    if len(entries) == 1 and date:
        return entries[0][0]
    labels = {
        f"{e['date']}  {e['workout']['workout_type'].title()}  {e['workout']['variation']}  "
        f"#{i}": i
        for i, e in reversed(entries)
    }
    choice = iterfzf(labels.keys(), multi=False)
    return labels.get(choice) if choice else None


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
        data, program_name = filter_by_program(data)
        table = view_program(data, program_name, display_workout)
        console.print(table)
        get_all_stats(data, program_name)
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
    by: Annotated[
        str,
        typer.Option(
            "--by",
            help="For the line plot: plot each workout, or the total per week or month.",
        ),
    ] = "workout",
    html: Annotated[
        bool,
        typer.Option(
            "--html",
            help="Write an interactive HTML report to ~/.kettlebells/stats.html and open it.",
            is_flag=True,
        ),
    ] = False,
    year: Annotated[
        int | None,
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
    ] = "",
    end: Annotated[
        str,
        typer.Option(
            "--end",
            "-e",
            help="End date (YYYY-MM-DD).",
        ),
    ] = "",
    calendar: Annotated[
        bool,
        typer.Option(
            "--calendar",
            "-c",
            help="Highlight days workouts were completed in a calendar.",
            is_flag=True,
        ),
    ] = False,
    by_movement: Annotated[
        bool,
        typer.Option(
            "--by-movement",
            "-M",
            help="Count the reps by movement.",
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
    ] = False,
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
        plot_workouts(
            dates, weight_per_workout, plot, median, average, year, by=by, units=data["loads"]["units"]
        )
    if html:
        _write_report(data, start, end, year)
    if calendar:
        print_calendar(data, year)
    if best:
        console.print(top_ten_workouts(data, sort))
    if by_movement and year:
        start = f"{year}-01-01"
        end = f"{year}-12-31"
        console.print(get_exercises_by_movement(data, start, end))
    if by_movement and not year:
        console.print(get_exercises_by_movement(data, start, end))


def _write_report(data: dict, start: str, end: str, year: int | None) -> None:
    if year:
        start, end, title = f"{year}-01-01", f"{year}-12-31", f"Stats from {year}"
    elif start or end:
        title = f"Stats from {start or 'the start'} to {end or 'today'}"
    else:
        title = "All Time Stats"
    path = write_html_report(
        KETTLEBELLS_HOME / "stats.html", get_entries(data, start, end), data["loads"]["units"], title
    )
    console.print(f"Report saved to {path}")
    webbrowser.open(path.as_uri())


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
