from statistics import mean

import plotext as plt
from rich.table import Table

from .console import console
from .workouts import Workout


def get_all_time_stats(data: dict) -> tuple[list[str], list[int]]:
    """Print stats from all workout in the database.
    :data: A dict of the data in the database.
    :returns: Lists of both dates and weight moved per session.
    """
    units = data["loads"]["units"]
    dates = []
    stats = []
    sessions = []
    for session_data in data["saved_sessions"]:
        date = session_data["date"]
        session = Workout(**session_data["session"])
        dates.append(date)
        stats.append(session.calc_session_stats())
        sessions.append(session)
    total_mins = sum(session.time for session in sessions)
    weight_per_session = [stat["weight moved"] for stat in stats]
    total_weight_moved = sum(weight_per_session)
    total_reps = sum(stat["reps"] for stat in stats)
    average_pace = mean(stat["pace"] for stat in stats)
    print("\nAll Time Stats")
    console.print("==============", style="green")
    print(f"    Total Sessions: {len(stats):,}")
    print(f"        Total Time: {total_mins} mins")
    print(f"Total Weight Moved: {total_weight_moved:,} {units}")
    print(f"        Total Reps: {total_reps:,}")
    print(f"      Average Pace: {average_pace:.1f} sec/rep")
    return dates, weight_per_session


def plot_workouts(dates: list[str], weight_per_workout: list[int]) -> None:
    """ Plot weight per workout.
    :param dates: A list of the dates stored as a string.
    :param weight_per_session: A list of the weight moved per session.
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
    plt.title("Weight Moved Per Session")
    plt.xlabel("Date")
    plt.show()


def top_ten_workouts(data: dict):
    """Get the best sessions based on weight moved.
    :param data: A dict of the data from the database.
    :returns: None"""
    units = data["loads"]["units"]
    if units.startswith("k"):
        units = "kg"
    sessions = []
    for session_data in data["saved_sessions"]:
        date = session_data["date"]
        session = Workout(**session_data["session"])
        sessions.append((date, session, session.calc_session_stats()))

    best_sessions_weight = sorted(
        sessions, key=lambda x: x[2]["weight moved"], reverse=True
    )
    if len(best_sessions_weight) > 10:
        best_sessions_weight = best_sessions_weight[:10]

    columns = [
        ("Date", "green"),
        ("Variation", "magenta"),
        ("Time (mins)", "magenta"),
        (f"Weight Moved ({units})", "blue"),
        ("Reps", "blue"),
        ("Pace (sec/rep)", "blue"),
    ]
    weight_table = Table(title="Best Sessions by Weight moved")
    for col, style in columns:
        weight_table.add_column(col, style=style, justify="right")
    for date, session, stats in best_sessions_weight:
        weight_table.add_row(
            date,
            session.variation,
            f"{session.time}",
            f"{stats['weight moved']:,}",
            f"{stats['reps']}",
            f"{stats['pace']:.1f}",
        )
    console.print(weight_table)
