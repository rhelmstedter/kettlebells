from statistics import mean

import plotext as plt
from rich.table import Table

from .console import console
from .workouts import Workout, Exercise


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
        workout = Workout(**workout_data["workout"])
        workout.exercises = [Exercise(**exercise) for exercise in workout.exercises]
        stats.append(workout.calc_workout_stats())
        workouts.append(workout)
    total_mins = sum(workout.time for workout in workouts)
    weight_per_workout = [stat["weight moved"] for stat in stats]
    total_weight_moved = sum(weight_per_workout)
    total_reps = sum(stat["reps"] for stat in stats)
    average_density = mean(stat["density"] for stat in stats)
    console.print("\nAll Time Stats")
    console.print("==============", style="green")
    console.print(f"    Total Workouts: {len(stats):,}")
    console.print(f"        Total Time: {total_mins} mins")
    console.print(f"Total Weight Moved: {total_weight_moved:,} {units}")
    console.print(f"        Total Reps: {total_reps:,}")
    console.print(f"   Average Density: {average_density:.1f} kg/min")
    return dates, weight_per_workout


def plot_workouts(dates: list[str], weight_per_workout: list[int]) -> None:
    """ Plot weight per workout.
    :param dates: A list of the dates stored as a string.
    :param weight_per_workout: A list of the weight moved per workout.
    :returns: None
    """
    background_color = "yellow"
    foreground_color = "black"
    plt.clear_color()
    plt.date_form("Y-m-d")
    plt.plot(dates, weight_per_workout, marker="hd", color=foreground_color)
    plt.ticks_color(foreground_color)
    plt.plotsize(100, 30)
    plt.canvas_color(background_color)
    plt.axes_color(background_color)
    plt.title("Weight Moved Per Workout")
    plt.xlabel("Date")
    plt.show()


def top_ten_workouts(data: dict):
    """Get the top ten workouts based on weight moved.
    :param data: A dict of the data from the database.
    :returns: None"""
    units = data["loads"]["units"]
    if units.startswith("k"):
        units = "kg"
    workouts = []
    for workout_data in data["saved_workouts"]:
        date = workout_data["date"]
        workout = Workout(**workout_data["workout"])
        workout.exercises = [Exercise(**e) for e in workout.exercises]
        workouts.append((date, workout, workout.calc_workout_stats()))

    best_workouts_weight = sorted(
        workouts, key=lambda x: x[2]["weight moved"], reverse=True
    )
    if len(best_workouts_weight) > 10:
        best_workouts_weight = best_workouts_weight[:10]

    columns = [
        ("Date", "green"),
        ("Variation", "magenta"),
        ("Time (mins)", "magenta"),
        (f"Weight Moved ({units})", "blue"),
        ("Reps", "blue"),
        ("Density (kg/min)", "blue"),
    ]
    weight_table = Table(title="Best workouts by Weight moved")
    for col, style in columns:
        weight_table.add_column(col, style=style, justify="right")
    for date, workout, stats in best_workouts_weight:
        weight_table.add_row(
            date,
            workout.variation,
            f"{workout.time}",
            f"{stats['weight moved']:,}",
            f"{stats['reps']}",
            f"{stats['density']:.1f}",
        )
    console.print(weight_table)
