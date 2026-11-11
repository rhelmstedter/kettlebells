"""Plots of weight moved: terminal plots (plotext and rich) and an interactive HTML report."""

import calendar
import json
import math
from collections import defaultdict
from datetime import date as date_class
from datetime import datetime, timedelta
from html import escape
from pathlib import Path
from statistics import mean, median

import plotext as plt
from rich.console import Group
from rich.table import Table
from rich.text import Text

from .console import console
from .constants import DATE_FORMAT, SUGGESTION, WARNING
from .workouts import Workout

PLOTLY_URL = "https://cdnjs.cloudflare.com/ajax/libs/plotly.js/3.0.1/plotly.min.js"
PERIODS = ("workout", "week", "month")
BAR_BLOCKS = " ▏▎▍▌▋▊▉█"


def plot_workouts(
    dates: list[str],
    weight_per_workout: list[int],
    plot_type: str,
    show_median: bool,
    show_average: bool,
    year: int | None = None,
    by: str = "workout",
    units: str = "kg",
) -> None:
    """Plot weight moved in the terminal.

    Args:
        dates: A list of the dates stored as a string.
        weight_per_workout: A list of the weight moved per workout.
        plot_type: event, line, or bar.
        show_median: Mark the median (line and bar plots).
        show_average: Mark the mean (line and bar plots).
        year: The year an event plot spans. Defaults to the year of the last workout.
        by: For the line plot, plot each workout or the total per week or month.
        units: The units of the weights.
    """
    if plot_type not in ("event", "line", "bar"):
        console.print(f":warning: {plot_type} not a valid plot.", style=WARNING)
        console.print(
            "Try running [underline]kettlebells stats --help[/underline] to see available plots",
            style=SUGGESTION,
        )
        return
    if by not in PERIODS:
        console.print(f":warning: {by} is not one of {', '.join(PERIODS)}.", style=WARNING)
        return
    if not dates:
        console.print("No workouts to plot.", style=WARNING)
        return

    if plot_type == "bar":
        months, totals = aggregate(dates, weight_per_workout, "month")
        labels = [f"{calendar.month_abbr[int(m[5:7])]}-{m[2:4]}" for m in months]
        console.print()
        console.print(bar_chart("Weight Moved by Month", labels, totals, units, show_median, show_average))
        return

    figure = plt.figure
    figure.clear()
    # Set the theme first: plotext 6 gives each element the theme's colors when it is
    # added, so anything drawn before theme() keeps the default light canvas color.
    # "simple" is plotext 5's "pro": the terminal's own colors for the frame, and
    # colored data.
    #
    # figure.line() and figure.event() always paint a white background in plotext 6.1
    # unless the canvas has a color of its own, so reference lines and events are drawn
    # as signals instead. Signals take colors from the theme in order: the data gets the
    # first (blue) and a reference line the second (green).
    #
    # There are no x-axis labels: with both a title and an x label, plotext 6.1 draws the
    # y tick labels one row off.
    figure.theme("simple")
    if plot_type == "event":
        if not year:
            year = int(dates[-1][:4])
        figure.date().activate(form=DATE_FORMAT)
        figure.draw(_event_strokes(figure, [d for d in dates if d.startswith(str(year))]))
        figure.ruler("y").lim(0, 1)
        figure.ruler("y").ticks([], [])
        figure.ruler("x").lim(f"{year}-01-01", f"{year}-12-31")
        figure.ruler("x").ticks(
            [f"{year}-{m:02}-01" for m in range(1, 13)],
            [calendar.month_abbr[m] for m in range(1, 13)],
        )
        figure.title(f"Workouts Across {year}")
        figure.plot_size(130, 20)
    else:
        xs, ys = aggregate(dates, weight_per_workout, by)
        figure.date().activate(form=DATE_FORMAT)
        figure.draw(figure.signal(xs, ys, marker="hd").lines())
        reference = _reference_value(ys, show_median, show_average)
        if reference is not None and len(xs) > 1:
            figure.draw(figure.signal([xs[0], xs[-1]], [reference, reference], marker="─").lines())
        figure.ruler("y").lim(lower=0)
        figure.ruler("y").ticks(*_number_ticks(max(ys)))
        figure.title(f"Weight Moved Per {by.title()} ({units})")
        figure.plot_size(90, 30)
    console.print()
    figure.show()


def aggregate(dates: list[str], weights: list[int], by: str) -> tuple[list[str], list[int]]:
    """Total the weights per week (starting Monday) or month; "workout" leaves them as is.

    Returns:
        The period start dates (YYYY-MM-DD) and the totals, in date order.
    """
    if by == "workout":
        return list(dates), list(weights)
    totals: dict[str, int] = defaultdict(int)
    for day, weight in zip(dates, weights):
        parsed = datetime.strptime(day, DATE_FORMAT).date()
        if by == "week":
            start = parsed - timedelta(days=parsed.weekday())
        else:
            start = parsed.replace(day=1)
        totals[start.isoformat()] += weight
    periods = sorted(totals)
    return periods, [totals[p] for p in periods]


def bar_chart(
    title: str,
    labels: list[str],
    values: list[int],
    units: str,
    show_median: bool = False,
    show_average: bool = False,
    width: int = 50,
) -> Group:
    """A horizontal bar chart with exact lengths (to 1/8 of a character) and values.

    A median or mean, if asked for, is marked with a green column.
    """
    top = max(values) or 1
    reference = _reference_value(values, show_median, show_average)
    marker = round(reference / top * width) if reference is not None else None
    table = Table(box=None, show_header=False, padding=(0, 1), pad_edge=False)
    table.add_column(justify="right", style="bold")
    table.add_column(no_wrap=True)
    table.add_column(justify="right")
    for label, value in zip(labels, values):
        eighths = round(value / top * width * 8)
        bar = BAR_BLOCKS[-1] * (eighths // 8) + (BAR_BLOCKS[eighths % 8] if eighths % 8 else "")
        bar = bar.ljust(width)
        text = Text(bar, style="blue")
        if marker is not None:
            column = min(marker, width - 1)
            text.stylize("green", column, column + 1)
            if bar[column] == " ":
                text = text[:column] + Text("│", style="green") + text[column + 1 :]
        table.add_row(label, text, f"{value:,}")
    parts = [Text(f"{title} ({units})", style="bold"), table]
    if reference is not None:
        kind = "Median" if show_median else "Mean"
        parts.append(Text(f"│ {kind}: {reference:,.0f} {units}", style="green"))
    return Group(*parts)


def _event_strokes(figure, dates: list[str]):
    """One signal of vertical strokes, one per date, with the strokes not joined."""
    xs = [d for d in dates for _ in (0, 1)]
    ys = [y for _ in dates for y in (0, 1)]
    signal = figure.signal(xs, ys, marker="│").lines()
    for index in range(2, len(xs), 2):
        signal.line(index, False)
    return signal


def _reference_value(values: list[int], show_median: bool, show_average: bool) -> float | None:
    if show_median:
        return median(values)
    if show_average:
        return mean(values)
    return None


def _number_ticks(maximum: float, count: int = 6) -> tuple[list[int], list[str]]:
    """Round, evenly spaced ticks from 0 to at least maximum, with thousands separators.

    plotext 6 labels large values in scientific notation (1.0e4) by default.
    """
    rough = max(maximum, 1) / (count - 1)
    magnitude = 10 ** math.floor(math.log10(rough))
    step = next(m * magnitude for m in (1, 2, 5, 10) if m * magnitude >= rough)
    positions = [int(step * i) for i in range(math.ceil(maximum / step) + 1)]
    return positions, [f"{p:,}" for p in positions]


def write_html_report(path: Path, entries: list[tuple[str, Workout]], units: str, title: str) -> Path:
    """Write an interactive HTML page of the given workouts.

    The page loads plotly.js from a CDN, so it needs an internet connection to draw the
    charts but no extra Python packages.

    Args:
        path: Where to write the page.
        entries: (date, workout) pairs in date order.
        units: The database units.
        title: The page heading, e.g. "All Time Stats".
    """
    rows = []
    for day, workout in entries:
        stats = workout.calc_workout_stats()
        rows.append(
            {
                "date": day,
                "type": workout.workout_type.title(),
                "variation": workout.variation,
                "time": workout.time,
                "weight": stats["weight moved"],
                "reps": stats["reps"],
                "notes": workout.notes,
            }
        )
    weights = [r["weight"] for r in rows]
    summary = [
        ("Workouts", f"{len(rows):,}"),
        ("Weight moved", f"{sum(weights):,} {units}"),
        ("Reps", f"{sum(r['reps'] for r in rows):,}"),
        ("Time", _format_minutes(sum(r["time"] for r in rows))),
        ("Median per workout", f"{median(weights):,.0f} {units}" if weights else "–"),
    ]
    # json.dumps doesn't escape "</", which would end the <script> early; notes are free text.
    payload = json.dumps({"rows": rows, "units": units}).replace("</", "<\\/")
    tiles = "".join(
        f'<div class="tile"><span>{escape(label)}</span><strong>{escape(value)}</strong></div>'
        for label, value in summary
    )
    first, last = (rows[0]["date"], rows[-1]["date"]) if rows else ("", "")
    html = HTML_TEMPLATE.format(
        title=escape(title),
        range=escape(f"{first} to {last}" if rows else "No workouts"),
        generated=escape(date_class.today().isoformat()),
        tiles=tiles,
        payload=payload,
        plotly_url=PLOTLY_URL,
    )
    path.write_text(html)
    return path


def _format_minutes(minutes: int) -> str:
    hours, mins = divmod(minutes, 60)
    return f"{hours:,} h {mins:02} min"


HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Kettlebells Stats</title>
<style>
  :root {{ --bg: #ffffff; --fg: #1f2328; --muted: #656d76; --card: #f6f8fa; --line: #d0d7de;
          --data: #4c6ef5; --ref: #2f9e44; }}
  @media (prefers-color-scheme: dark) {{
    :root {{ --bg: #0d1117; --fg: #e6edf3; --muted: #8d96a0; --card: #161b22; --line: #30363d;
            --data: #7c9cff; --ref: #51cf66; }}
  }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: var(--bg); color: var(--fg);
          font: 15px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
  main {{ max-width: 1100px; margin: 0 auto; padding: 24px 16px 48px; }}
  h1 {{ margin: 0; font-size: 24px; }}
  .sub {{ color: var(--muted); margin: 4px 0 20px; }}
  .tiles {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; }}
  .tile {{ background: var(--card); border: 1px solid var(--line); border-radius: 8px; padding: 12px; }}
  .tile span {{ display: block; color: var(--muted); font-size: 13px; }}
  .tile strong {{ font-size: 20px; font-variant-numeric: tabular-nums; }}
  section {{ margin-top: 28px; }}
  .head {{ display: flex; flex-wrap: wrap; align-items: baseline; justify-content: space-between; gap: 8px; }}
  h2 {{ font-size: 17px; margin: 0; }}
  .controls {{ display: flex; flex-wrap: wrap; gap: 6px; }}
  button {{ font: inherit; font-size: 13px; padding: 4px 10px; border-radius: 6px; cursor: pointer;
           border: 1px solid var(--line); background: var(--card); color: var(--fg); }}
  button[aria-pressed="true"] {{ background: var(--data); border-color: var(--data); color: #fff; }}
  .chart {{ height: 420px; margin-top: 8px; }}
  .note {{ color: var(--muted); font-size: 13px; }}
</style>
</head>
<body>
<main>
  <h1>{title}</h1>
  <p class="sub">{range} · generated {generated}</p>
  <div class="tiles">{tiles}</div>

  <section>
    <div class="head">
      <h2>Weight moved</h2>
      <div class="controls" id="period" role="group" aria-label="Group by">
        <button data-by="workout" aria-pressed="true">Per workout</button>
        <button data-by="week" aria-pressed="false">Per week</button>
        <button data-by="month" aria-pressed="false">Per month</button>
      </div>
    </div>
    <div id="line" class="chart" style="height: 460px"></div>
    <p class="note">Hover for details. Drag to zoom, double-click to reset. Click a legend
      entry to hide it.</p>
  </section>

  <section>
    <div class="head"><h2>Workouts per week</h2></div>
    <div id="weeks" class="chart" style="height: 260px"></div>
  </section>
</main>

<script id="data" type="application/json">{payload}</script>
<script src="{plotly_url}"></script>
<script>
(function () {{
  var data = JSON.parse(document.getElementById("data").textContent);
  var rows = data.rows, units = data.units;
  if (typeof Plotly === "undefined") {{
    document.querySelectorAll(".chart").forEach(function (el) {{
      el.textContent = "The charts need an internet connection to load plotly.js.";
    }});
    return;
  }}
  var css = getComputedStyle(document.documentElement);
  var color = function (name) {{ return css.getPropertyValue(name).trim(); }};
  var layoutBase = function () {{
    return {{
      paper_bgcolor: "rgba(0,0,0,0)", plot_bgcolor: "rgba(0,0,0,0)",
      font: {{ color: color("--fg") }}, margin: {{ l: 64, r: 16, t: 24, b: 40 }},
      xaxis: {{ type: "date", gridcolor: color("--line") }},
      yaxis: {{ rangemode: "tozero", gridcolor: color("--line"), tickformat: "," }},
      // Below the plot, so plotly's toolbar (top right, on hover) can't cover it.
      legend: {{ orientation: "h", x: 0, y: -0.12, yanchor: "top" }}, hovermode: "closest"
    }};
  }};
  var config = {{ responsive: true, displaylogo: false }};

  function periodStart(day, by) {{
    var d = new Date(day + "T00:00:00Z");
    if (by === "week") {{ d.setUTCDate(d.getUTCDate() - ((d.getUTCDay() + 6) % 7)); }}
    if (by === "month") {{ d.setUTCDate(1); }}
    return d.toISOString().slice(0, 10);
  }}
  function median(values) {{
    var s = values.slice().sort(function (a, b) {{ return a - b; }});
    var m = Math.floor(s.length / 2);
    return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2;
  }}
  function fmt(n) {{ return Math.round(n).toLocaleString(); }}
  // Workout types, variations and notes are typed by the user; keep markup out of the hover labels.
  function esc(s) {{ return String(s).replace(/[<>&]/g, ""); }}

  function drawLine(by) {{
    var xs = [], ys = [], text = [];
    if (by === "workout") {{
      rows.forEach(function (r) {{
        xs.push(r.date); ys.push(r.weight);
        text.push("<b>" + r.date + "</b><br>" + esc(r.type) + " · " + esc(r.variation) + "<br>" +
          fmt(r.weight) + " " + units + " · " + r.reps + " reps · " + r.time + " min" +
          (r.notes ? "<br><i>" + esc(r.notes) + "</i>" : ""));
      }});
    }} else {{
      var totals = {{}}, counts = {{}};
      rows.forEach(function (r) {{
        var k = periodStart(r.date, by);
        totals[k] = (totals[k] || 0) + r.weight; counts[k] = (counts[k] || 0) + 1;
      }});
      Object.keys(totals).sort().forEach(function (k) {{
        xs.push(k); ys.push(totals[k]);
        text.push("<b>" + (by === "week" ? "Week of " : "") + k + "</b><br>" + fmt(totals[k]) + " " +
          units + " · " + counts[k] + " workout" + (counts[k] === 1 ? "" : "s"));
      }});
    }}
    var label = by === "workout" ? "Per workout" : by === "week" ? "Per week" : "Per month";
    var traces = [{{
      x: xs, y: ys, text: text, hovertemplate: "%{{text}}<extra></extra>", name: label,
      type: by === "month" ? "bar" : "scatter", mode: "lines+markers",
      line: {{ color: color("--data"), width: 1.5 }}, marker: {{ color: color("--data"), size: 5 }}
    }}];
    if (ys.length > 1) {{
      var med = median(ys), avg = ys.reduce(function (a, b) {{ return a + b; }}, 0) / ys.length;
      [["Median", med, "dash"], ["Mean", avg, "dot"]].forEach(function (ref) {{
        traces.push({{ x: [xs[0], xs[xs.length - 1]], y: [ref[1], ref[1]], mode: "lines",
          name: ref[0] + " " + fmt(ref[1]) + " " + units, hoverinfo: "skip",
          line: {{ color: color("--ref"), dash: ref[2], width: 1.5 }},
          visible: ref[0] === "Median" ? true : "legendonly" }});
      }});
    }}
    var layout = layoutBase();
    layout.yaxis.title = {{ text: units }};
    Plotly.react("line", traces, layout, config);
  }}

  function drawWeeks() {{
    var counts = {{}};
    rows.forEach(function (r) {{ var k = periodStart(r.date, "week"); counts[k] = (counts[k] || 0) + 1; }});
    var keys = Object.keys(counts).sort();
    var layout = layoutBase();
    layout.yaxis.title = {{ text: "workouts" }};
    layout.yaxis.dtick = 1;
    Plotly.react("weeks", [{{ x: keys, y: keys.map(function (k) {{ return counts[k]; }}), type: "bar",
      marker: {{ color: color("--data") }}, hovertemplate: "Week of %{{x}}<br>%{{y}} workouts<extra></extra>" }}],
      layout, config);
  }}

  var buttons = document.querySelectorAll("#period button");
  buttons.forEach(function (b) {{
    b.addEventListener("click", function () {{
      buttons.forEach(function (o) {{ o.setAttribute("aria-pressed", o === b ? "true" : "false"); }});
      drawLine(b.dataset.by);
    }});
  }});
  drawLine("workout");
  drawWeeks();
}})();
</script>
</body>
</html>
"""
