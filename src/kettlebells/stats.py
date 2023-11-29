import calendar
from collections import defaultdict
from datetime import datetime
from statistics import mean, median

import pandas as pd
import plotext as plt
from iterfzf import iterfzf
from rich import box
from rich.align import Align
from rich.columns import Columns
from rich.table import Table
from rich.text import Text

from .console import console
from .constants import DATE_FORMAT, KETTLEBELLS_HOME
from .workouts import Workout, _print_helper


def get_all_time_stats(data: dict, program: str | None = None) -> tuple[list[str], list[int]]:
    """Print stats from all workout in the database.
    :data: A dict of the data in the database.
    :returns: Lists of both dates and weight moved per workout.
    """
    units = data["loads"]["units"]
    dates = []
    stats = []
    workouts = []
    for workout_data in data["saved_workouts"]:
        date = workout_data["date"]
        dates.append(date)
        workout = Workout(**workout_data["workout"])
        stats.append(workout.calc_workout_stats())
        workouts.append(workout)
    days, remaining_mins = divmod(sum(workout.time for workout in workouts), 60 * 24)
    hours, mins = divmod(remaining_mins, 60)
    weight_per_workout = [stat["weight moved"] for stat in stats]
    total_weight_moved = sum(weight_per_workout)
    total_reps = sum(stat["reps"] for stat in stats)
    average_weight_density = mean(stat["weight density"] for stat in stats)
    average_rep_density = mean(stat["rep density"] for stat in stats)
    if program:
        title = f"{program.title()} Stats"
    else:
        title = "All Time Stats"
    console.print()
    console.print(title)
    console.print("=" * len(title), style="green")
    stats_to_print = [
        ("Total Workouts", f"{len(stats):,}"),
        ("Total Time", f"{days} days {hours:02} hours {mins:02} mins"),
        ("Total Weight Moved", f"{total_weight_moved:,} {units}"),
        ("Total Reps", f"{total_reps:,}"),
        ("Mean Weight Density", f"{average_weight_density:.1f} {units}/min"),
        ("Mean Rep Density", f"{average_rep_density:.1f} reps/min"),
    ]
    _print_helper(stats_to_print)
    return dates, weight_per_workout


def plot_workouts(
    dates: list[str],
    weight_per_workout: list[int],
    plot_type: str,
    show_median: bool,
    show_average: bool,
) -> None:
    """Plot weight moved per workout.

    Args:
        dates: A list of the dates stored as a string.
        weight_per_workout: A list of the weight moved per workout.
    """
    match plot_type:
        case "event":
            x_axis = []
            for date in dates:
                year, month, day = date.split("-")
                x_axis.append("-".join((year[-2:], month, day)))
            plt.date_form("y-m-d")
            plt.plotsize(130, 20)
            plt.title("Workouts Across the Year")
            plt.xlabel("Months")
            year = str(datetime.today().year)[-2:]
            plt.xlim(f"{year}-01-01", f"{year}-12-31")
            plt.event_plot(x_axis, marker="hd")
            ticks = [f"23-{m}-01" for m in range(1, 13)]
            xlabels = [calendar.month_abbr[m] for m in range(1, 13)]
            plt.xticks(ticks, xlabels)
        case "line":
            x_axis = []
            for date in dates:
                year, month, day = date.split("-")
                x_axis.append("-".join((year[-2:], month, day)))
            if show_median:
                plt.hline(median(weight_per_workout), "green")
            elif show_average:
                plt.hline(mean(weight_per_workout), "green")
            plt.date_form("y-m-d")
            plt.title("Weight Moved Per Workout")
            plt.xlabel("Date")
            plt.ylim(lower=0)
            plt.plotsize(90, 30)
            plt.plot(x_axis, weight_per_workout, marker="hd")
        case "bar":
            data = defaultdict(int)
            for date, weight in zip(dates, weight_per_workout):
                year, month, _ = date.split("-")
                month = calendar.month_abbr[int(month)]
                data["-".join((month, year[-2:]))] += weight
            if show_median:
                plt.vline(median(data.values()), "green")
            elif show_average:
                plt.vline(mean(data.values()), "green")
            plt.title("Weight Moved by Month")
            plt.xlabel("Weight Moved")
            plt.plotsize(90, 30)
            plt.bar(data.keys(), data.values(), orientation="h")

    plt.theme("pro")
    console.print()
    plt.show()


def top_ten_workouts(data: dict, sort: str) -> Table:
    """Get the top ten workouts based on weight moved.

    Args:
        data: A dict of the data from the database.
        sort: A str of which parameter to sort the table by.

    Returns: A rich Table of the top ten workouts.
    """
    units = data["loads"]["units"]
    workouts = []
    for workout_data in data["saved_workouts"]:
        date = workout_data["date"]
        workout = Workout(**workout_data["workout"])
        workouts.append((date, workout, workout.calc_workout_stats()))

    sort = sort.replace("-", " ")
    if sort == "time":
        workouts = sorted(workouts, key=lambda x: x[1].time, reverse=True)
    else:
        workouts = sorted(workouts, key=lambda x: x[2][sort], reverse=True)

    if len(workouts) > 10:
        workouts = workouts[:10]

    columns = [
        ("Date\n", "green"),
        ("Workout Type\n", "magenta"),
        ("Variation\n", "magenta"),
        ("Time\n(mins)", "magenta"),
        (f"Weight Moved\n({units})", "blue"),
        ("Reps\n", "blue"),
        (f"Weight Density\n({units}/min)", "blue"),
        ("Rep Density\n(reps/min)", "blue"),
    ]
    top_ten_table = Table(title=f"Top Ten Workouts by {sort.title()}")
    for col, style in columns:
        top_ten_table.add_column(col, style=style, justify="right")

    for date, workout, stats in workouts:
        top_ten_table.add_row(
            date,
            workout.workout_type.title(),
            workout.variation,
            f"{workout.time}",
            f"{stats['weight moved']:,}",
            f"{stats['reps']}",
            f"{stats['weight density']:.1f}",
            f"{stats['rep density']:.1f}",
        )
    return top_ten_table


def filter_by_program(data: dict) -> tuple[dict, str]:
    programs = {w["workout"]["workout_type"] for w in data["saved_workouts"]}
    program = iterfzf(
        programs,
        multi=False,
    )
    workouts = []
    for workout_data in data["saved_workouts"]:
        workout_type = workout_data["workout"]['workout_type']
        if workout_type == program:
            workouts.append(workout_data)
    data["saved_workouts"] = workouts
    return data, program


def view_program(data: dict, program: str) -> Table:
    """Create a table based on a program.

    Args:
        data: A dict of the data from the database.
        program: The name of a workout program.

    Returns: A rich Table of the workouts from a program.
    """
    units = data["loads"]["units"]
    workouts = []
    for workout_data in data["saved_workouts"]:
        date = workout_data["date"]
        workout = Workout(**workout_data["workout"])
        load = [exercise.load for exercise in workout.exercises]
        if len(set(load)) == 1:
            load = load[0]
        else:
            load = "Varied"
        workouts.append((date, workout, load, workout.calc_workout_stats()))

    columns = [
        ("Date\n", "green"),
        ("Workout Type\n", "magenta"),
        ("Variation\n", "magenta"),
        ("Time\n(mins)", "magenta"),
        (f"load\n({units})", "blue"),
        (f"Weight Moved\n({units})", "blue"),
        ("Reps\n", "blue"),
        (f"Weight Density\n({units}/min)", "blue"),
        ("Rep Density\n(reps/min)", "blue"),
    ]
    program_table = Table(title=program.title())
    for col, style in columns:
        program_table.add_column(col, style=style, justify="right")

    for date, workout, load, stats in workouts:
        program_table.add_row(
            date,
            workout.workout_type.title(),
            workout.variation,
            f"{workout.time}",
            f"{load}",
            f"{stats['weight moved']:,}",
            f"{stats['reps']}",
            f"{stats['weight density']:.1f}",
            f"{stats['rep density']:.1f}",
        )
    return program_table


def retrieve_workout(data: dict, preview: bool) -> tuple[str, Workout] | None:
    data = {w["date"]: Workout(**w["workout"]) for w in data["saved_workouts"]}
    if preview:
        date = iterfzf(
            data.keys(),
            multi=False,
            preview="rg {} " + str(KETTLEBELLS_HOME) + """ -A 20 -I """,
        )
    else:
        date = iterfzf(
            data.keys(),
            multi=False,
        )
    if date:
        workout = data[date]
        return date, workout
    return


def table_to_df(rich_table: Table) -> pd.DataFrame:
    """Convert a rich.Table obj into a pandas.DataFrame obj with any rich formatting removed from the values.
    Args:
        rich_table (Table): A rich Table that should be populated by the DataFrame values.
    Returns:
        DataFrame: A pandas DataFrame with the Table data as its values."""

    table_data = {x.header.strip(): [Text.from_markup(y).plain for y in x.cells] for x in rich_table.columns}
    return pd.DataFrame(table_data)


def print_calendar(data: dict, year: int):
    """Highlight workout days and print a yearly calendar.

    Args:
        data: The database dictionary.
        year: The year of the calendar to print.

    """
    cal = calendar.Calendar()
    workout_dates = _get_dates(data)
    month_tables = []
    for month in range(1, 13):
        table = Table(
            title=f"{calendar.month_name[month]} {year}",
            style="blue",
            box=box.SIMPLE_HEAVY,
            padding=0,
        )
        for week_day in cal.iterweekdays():
            table.add_column("{:.3}".format(calendar.day_name[week_day]), justify="right")
        month_days = cal.monthdayscalendar(year, month)
        for weekdays in month_days:
            days = []
            for index, day in enumerate(weekdays):
                day_label = Text(str(day or ""))
                if day and (day, month, year) in workout_dates:
                    day_label.stylize("green")
                days.append(day_label)
            table.add_row(*days)
        month_tables.append(Align.center(table))

    columns = Columns(month_tables, padding=1, width=30)
    console.print()
    console.rule(str(year), style="magenta")
    console.print()
    console.print(columns, justify="center")
    console.rule(style="magenta")
    console.print()


def _get_dates(data: dict) -> list[tuple[int]]:
    workout_dates = []
    for workout in data["saved_workouts"]:
        workout_date = datetime.strptime(workout["date"], DATE_FORMAT)
        workout_dates.append((workout_date.day, workout_date.month, workout_date.year))
    return workout_dates
