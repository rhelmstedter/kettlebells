import calendar
from datetime import datetime
from statistics import mean

import plotext as plt
from dacite import from_dict
from rich import box
from rich.align import Align
from rich.columns import Columns
from rich.table import Table
from rich.text import Text

from .console import console
from .workouts import Workout
from .constants import DATE_FORMAT


def get_all_time_stats(data: dict) -> tuple[list[str], list[int]]:
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
        workout = from_dict(Workout, workout_data["workout"])
        stats.append(workout.calc_workout_stats())
        workouts.append(workout)
    total_mins = sum(workout.time for workout in workouts)
    weight_per_workout = [stat["weight moved"] for stat in stats]
    total_weight_moved = sum(weight_per_workout)
    total_reps = sum(stat["reps"] for stat in stats)
    average_weight_density = mean(stat["weight density"] for stat in stats)
    average_rep_density = mean(stat["rep density"] for stat in stats)
    console.print("\nAll Time Stats")
    console.print("==============", style="green")
    console.print(f"     Total Workouts: {len(stats):,}")
    console.print(f"         Total Time: {total_mins} mins")
    console.print(f" Total Weight Moved: {total_weight_moved:,} {units}")
    console.print(f"         Total Reps: {total_reps:,}")
    console.print(f"Mean Weight Density: {average_weight_density:.1f} {units}/min")
    console.print(f"   Mean Rep Density: {average_rep_density:.1f} reps/min")
    return dates, weight_per_workout


def plot_workouts(dates: list[str], weight_per_workout: list[int]) -> None:
    """Plot weight moved per workout.

    Args:
        dates: A list of the dates stored as a string.
        weight_per_workout: A list of the weight moved per workout.
    """
    x_axis = []
    for date in dates:
        year, month, day = date.split("-")
        x_axis.append("-".join((year[-2:], month, day)))

    plt.date_form("y-m-d")
    plt.plot(x_axis, weight_per_workout, marker="hd")
    plt.plotsize(70, 20)
    # plt.ticks_color(foreground_color)
    # plt.canvas_color()
    # plt.axes_color()
    plt.title("Weight Moved Per Workout")
    plt.xlabel("Date")
    plt.ylim(lower=0)
    plt.clear_color()
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
        workout = from_dict(Workout, workout_data["workout"])
        workouts.append((date, workout, workout.calc_workout_stats()))

    match sort:
        case "weight-moved":
            title = "Weight Moved"
            workouts = sorted(
                workouts, key=lambda x: x[2]["weight moved"], reverse=True
            )
        case "reps":
            title = "Reps"
            workouts = sorted(workouts, key=lambda x: x[2]["reps"], reverse=True)
        case "density":
            title = "Density"
            workouts = sorted(
                workouts, key=lambda x: x[2]["weight density"], reverse=True
            )
        case "time":
            title = "Time"
            workouts = sorted(workouts, key=lambda x: x[1].time, reverse=True)
    if len(workouts) > 10:
        workouts = workouts[:10]

    columns = [
        ("Date", "green"),
        ("Workout Type", "magenta"),
        ("Variation", "magenta"),
        ("Time (mins)", "magenta"),
        (f"Weight Moved ({units})", "blue"),
        ("Reps", "blue"),
        ("Weight Density (kg/min)", "blue"),
        ("Rep Density (reps/min)", "blue"),
    ]
    top_ten_table = Table(title=f"Top Ten Workouts by {title}")
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


def print_calendar(data: dict, year: int):
    """Highlight workout days and print a yearly calendar.

    Args:
        data: The database dictionary.
        year: The year of the calendar to print.

    """
    cal = calendar.Calendar()
    workout_dates = []
    for workout in data["saved_workouts"]:
        workout_date = datetime.strptime(workout["date"], DATE_FORMAT)
        workout_dates.append((workout_date.day, workout_date.month, workout_date.year))

    month_tables = []
    for month in range(1, 13):
        table = Table(
            title=f"{calendar.month_name[month]} {year}",
            style="blue",
            box=box.SIMPLE_HEAVY,
            padding=0,
        )
        for week_day in cal.iterweekdays():
            table.add_column(
                "{:.3}".format(calendar.day_name[week_day]), justify="right"
            )
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
