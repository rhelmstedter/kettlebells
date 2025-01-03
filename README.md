
# Table of Contents

1.  [Installation](#orgc30a08d)
    1.  [uv](#org644f9b3)
    2.  [pipx](#org3e526d7)
2.  [Usage](#org61925e3)
    1.  [Initialize](#org9dc1f6a)
    2.  [Update Exercises](#orgf9f1c9d)
    3.  [Commands](#org6ca217f)
        1.  [save](#orgaa12efc)
        2.  [random](#orgfe3c69f)
        3.  [last](#org319bbb1)
        4.  [view](#orgb4c7591)
        5.  [stats](#org85a8277)

kettlebells is a CLI designed to create, save, and track the progress of kettlebell workouts. The inspiration for this project came from [Pat Flynn&rsquo;s conversation with Bret Jones](https://www.chroniclesofstrength.com/what-strength-aerobics-are-and-how-to-use-them-w-brett-jones/). (For a more detailed look at Iron Cardio, go checkout the [Iron Cardio Book](https://strongandfit.com/products/iron-cardio-by-brett-jones) by Bret Jones.) After starting an [initial project](https://github.com/rhelmstedter/iron-cardio) that focused only on iron cardio, I wanted to be able to add more. This is essentially a fork of the iron-cardio project designed to add various workouts such as the armor building complex, and dry fighting weight.

As of version 0.2.1, the way workouts are constructed has completely changed. This will allow users to construct their own custom workouts in the future. It will also allow the stats to keep track of how many reps of each type of exercise have been done.


<a id="orgc30a08d"></a>

# Installation


<a id="org644f9b3"></a>

## [uv](https://github.com/astral-sh/uv)

    uv tool install kettlebells


<a id="org3e526d7"></a>

## [pipx](https://github.com/pypa/pipx)

    pipx install kettlebells


<a id="org61925e3"></a>

# Usage


<a id="org9dc1f6a"></a>

## Initialize

Run the `init` command to create the database.

    kettlebells init

Next, run the `setloads` command. This sets the units to either pounds (lbs) or kilograms (kg), the user&rsquo;s bodyweight, and the loads for the light, medium, and heavy kettlebell. This command can be run as needed when the user is ready to move up in load or bodyweight changes.

    kettlebells setloads


<a id="orgf9f1c9d"></a>

## Update Exercises

Occasionally, new exercises are added to the database. If you have already initialized in a previous version, run the `update` command.

    kettlebells update


<a id="org6ca217f"></a>

## Commands


<a id="orgaa12efc"></a>

### save

The `save` command saves workouts to the database. The current options are:

-   [ic](#org119a057)
-   [abc](#orgeaf2c20)
-   [btb](#org251f683)
-   [dfw](#orgfdfc716)
-   [pw](#orga37f1b5)
-   [rop](#orgbb8663a)
-   [wolf](#org264a3d2)
-   [custom](#org5463923)

When run with no option, the `save` command will attempt to use the most recently generated random workout. Otherwise, use the `--workout-type` option to manually enter a workout, e.g.:

    kettlebells save --workout-type abc

1.  dfw

    When the `save` command is run with the workout type of `dfw`, a dry fighting weight workout is saved. See [the original post](https://www.strongfirst.com/dry-fighting-weight/) for more details
    
        kettlebells save --workout-type dfw

2.  btb

    The save command with a workout type of `btb` allows the user to save a Back to Basics Workout. These workouts are constructed based on The Pat Flynn Show episode with Dan John [The BEST Kettlebell Program for GEGINNERS | THE BTBKP](https://patflynnshow.libsyn.com/the-best-kettlebell-program-for-beginners-the-btbkp). The choices are ladders of 2-3-5 clean and presses followed by either snatches or double front squats. The warm up and cool exercises are not included in the workout.
    
        kettlebells save --workout-type btb
    
    The program options are:
    
    <table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">
    
    
    <colgroup>
    <col  class="org-left" />
    
    <col  class="org-left" />
    </colgroup>
    <thead>
    <tr>
    <th scope="col" class="org-left">First block</th>
    <th scope="col" class="org-left">Second Block</th>
    </tr>
    </thead>
    <tbody>
    <tr>
    <td class="org-left">2 ladders</td>
    <td class="org-left">60 Snatches</td>
    </tr>
    
    <tr>
    <td class="org-left">3 ladders</td>
    <td class="org-left">80 Snatches</td>
    </tr>
    
    <tr>
    <td class="org-left">5 ladders</td>
    <td class="org-left">100 Snatches</td>
    </tr>
    </tbody>
    <tbody>
    <tr>
    <td class="org-left">2 ladders</td>
    <td class="org-left">10 sets of 5 Double Front Squats</td>
    </tr>
    
    <tr>
    <td class="org-left">3 ladders</td>
    <td class="org-left">10 sets of 5 Double Front Squats</td>
    </tr>
    
    <tr>
    <td class="org-left">5 ladders</td>
    <td class="org-left">10 sets of 5 Double Front Squats</td>
    </tr>
    </tbody>
    </table>

3.  pw

    The save command with a workout type of `pw` saves versions of [Dan John&rsquo;s Perfect Workout](https://youtu.be/aHQLx_HhFqo?si=b68xBn41-tcGDVJE). While in the video Dan does hip thrusts until it burns, for ease of recording the workout, `kettlebells` offers a set number of reps for the hip thrust.
    
        kettlebells save --workout-type pw
    
    The program options are:
    
    <table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">
    
    
    <colgroup>
    <col  class="org-left" />
    
    <col  class="org-left" />
    
    <col  class="org-right" />
    
    <col  class="org-right" />
    </colgroup>
    <thead>
    <tr>
    <th scope="col" class="org-left">Variation</th>
    <th scope="col" class="org-left">Exercises</th>
    <th scope="col" class="org-right">Sets</th>
    <th scope="col" class="org-right">Reps</th>
    </tr>
    </thead>
    <tbody>
    <tr>
    <td class="org-left"><b>Original</b></td>
    <td class="org-left">Half-kneeling Press</td>
    <td class="org-right">3</td>
    <td class="org-right">8</td>
    </tr>
    
    <tr>
    <td class="org-left">&#xa0;</td>
    <td class="org-left">Hanging Leg Raise</td>
    <td class="org-right">3</td>
    <td class="org-right">8</td>
    </tr>
    
    <tr>
    <td class="org-left">&#xa0;</td>
    <td class="org-left">Banded Hip Thrust</td>
    <td class="org-right">3</td>
    <td class="org-right">15</td>
    </tr>
    
    <tr>
    <td class="org-left">&#xa0;</td>
    <td class="org-left">Bulgarian Goat Bag Swing</td>
    <td class="org-right">3</td>
    <td class="org-right">8</td>
    </tr>
    
    <tr>
    <td class="org-left">&#xa0;</td>
    <td class="org-left">Goblet Squat / Broomstick Overhead Squat</td>
    <td class="org-right">1</td>
    <td class="org-right">8</td>
    </tr>
    </tbody>
    <tbody>
    <tr>
    <td class="org-left"><b>Indoor</b></td>
    <td class="org-left">Half-kneeling Press</td>
    <td class="org-right">3</td>
    <td class="org-right">8</td>
    </tr>
    
    <tr>
    <td class="org-left">&#xa0;</td>
    <td class="org-left">Child&rsquo;s Pose</td>
    <td class="org-right">3</td>
    <td class="org-right">20 secs</td>
    </tr>
    
    <tr>
    <td class="org-left">&#xa0;</td>
    <td class="org-left">Hip Thrust / Clam Shell (15, 14, 13&#x2026;)</td>
    <td class="org-right">1</td>
    <td class="org-right">120</td>
    </tr>
    
    <tr>
    <td class="org-left">&#xa0;</td>
    <td class="org-left">Goblet Squat / Broomstick Overhead Squat</td>
    <td class="org-right">1</td>
    <td class="org-right">8</td>
    </tr>
    </tbody>
    <tbody>
    <tr>
    <td class="org-left"><b>The Bull</b></td>
    <td class="org-left">Half-kneeling Press</td>
    <td class="org-right">3</td>
    <td class="org-right">8</td>
    </tr>
    
    <tr>
    <td class="org-left">&#xa0;</td>
    <td class="org-left">Hanging Leg Raise</td>
    <td class="org-right">3</td>
    <td class="org-right">8</td>
    </tr>
    
    <tr>
    <td class="org-left">&#xa0;</td>
    <td class="org-left">Bulgarian Goat Bag Swing</td>
    <td class="org-right">3</td>
    <td class="org-right">8</td>
    </tr>
    
    <tr>
    <td class="org-left">&#xa0;</td>
    <td class="org-left">Bent Over Rows</td>
    <td class="org-right">3</td>
    <td class="org-right">8</td>
    </tr>
    
    <tr>
    <td class="org-left">&#xa0;</td>
    <td class="org-left">Goblet Squat / Broomstick Overhead Squat</td>
    <td class="org-right">1</td>
    <td class="org-right">8</td>
    </tr>
    </tbody>
    </table>

4.  rop

    The save command with a workout type of `rop` saves versions of Pavel Tsatsouline&rsquo;s rite of passage program from [Enter The Kettlebell](https://www.amazon.com/Enter-Kettlebell-Strength-Secret-Supermen/dp/1942812132). The clean and press and pullups are calculated as ladders, while the swings and snatches are straight sets.
    
        kettlebells save --workout-type rop

5.  wolf

    The save command with a workout type of `wolf` saves workouts from the free program [The Wolf](https://chasingstrength.com/reports/double-kettlebell-complex/) from [Geoff Neupert](https://chasingstrength.com). This is a gasser for sure.
    
        kettlebells save --workout-type wolf

6.  custom

    When the `save` command is run with the workout type of `custom`, the user can save a custom workout. Custom workouts need a `workout_type` and a `variation`. The default is `custom`. Exercises are chosen via [iterfzf](https://github.com/dahlia/iterfzf). Select `Other` to add a custom exercise. Select `Done` or press escape when finished adding all the exercises.
    
        kettlebells save --workout-type custom
    
    1.  Reps and Loads for Custom Exercises
    
        Unilateral exercises such as the single arm overhead press (simply &ldquo;Press&rdquo; in the program) should have the reps doubled. For example, if the set and rep scheme is 3 sets of 8 single arm overhead presses on the left and right arm, that should be saved as 16 reps per set for that exercise.
        
        When the stats are calculated, any exercise that has &ldquo;Double&rdquo; in it has the load multiplied by 2. So Double Pressing a pair of 24 kg kettlebells should be saved as a load of 24 kg, but the calculations will result in 48 kg per rep. If using uneven sized bells, use the average weight of the two bells rounded to the nearest integer.
    
    2.  Suggested Use for Complexes
    
        Consider a workout out like the [8 - 5 - 3 Rep Scheme](https://www.youtube.com/watch?v=nHPfglRCp6M&t=13s) from Pat Flynn. The `workout_type` would be &ldquo;complex&rdquo;, the `variation` would be &ldquo;8-5-3 Rep Scheme&rdquo;. Technically, a set consists of 8 Goblet Squats, 5 Start Stop Swings, 3 Push-ups. Then you would repeat this for 5 rounds. However, in `kettlebells` the user will add each exercise separately. So the Goblet Squat would be 5 sets of 8. The Start Stop Swing would be 5 sets of 5, and the Push-up would be 5 sets of 3.


<a id="orgfe3c69f"></a>

### random

The work out command generates a random workout. The current options are:

-   `ic` (Iron Cardio)
-   `abc` (Armor Building Complex)

1.  iron-cardio

    The `random` command with a workout type of `ic`, generates a random iron cardio workout.
    
        kettlebells random --workout-type ic
    
    Iron cardio workouts are built from the following parameters:
    
    <table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">
    
    
    <colgroup>
    <col  class="org-left" />
    
    <col  class="org-left" />
    </colgroup>
    <thead>
    <tr>
    <th scope="col" class="org-left">Parameter</th>
    <th scope="col" class="org-left">Options</th>
    </tr>
    </thead>
    <tbody>
    <tr>
    <td class="org-left"><b>Single Bell Variations</b></td>
    <td class="org-left">Classic</td>
    </tr>
    
    <tr>
    <td class="org-left">&#xa0;</td>
    <td class="org-left">Classic + Pull-up</td>
    </tr>
    
    <tr>
    <td class="org-left">&#xa0;</td>
    <td class="org-left">Classic + Snatch</td>
    </tr>
    
    <tr>
    <td class="org-left">&#xa0;</td>
    <td class="org-left">Traveling 2s</td>
    </tr>
    </tbody>
    <tbody>
    <tr>
    <td class="org-left"><b>Double Bell Variations</b></td>
    <td class="org-left">Double Classic</td>
    </tr>
    
    <tr>
    <td class="org-left">&#xa0;</td>
    <td class="org-left">Double Classic + Pull-up</td>
    </tr>
    
    <tr>
    <td class="org-left">&#xa0;</td>
    <td class="org-left">Double Traveling 2s</td>
    </tr>
    </tbody>
    <tbody>
    <tr>
    <td class="org-left"><b>TIMES</b></td>
    <td class="org-left">30 mins</td>
    </tr>
    
    <tr>
    <td class="org-left">&#xa0;</td>
    <td class="org-left">20 mins</td>
    </tr>
    
    <tr>
    <td class="org-left">&#xa0;</td>
    <td class="org-left">10 mins</td>
    </tr>
    </tbody>
    <tbody>
    <tr>
    <td class="org-left"><b>LOADS</b></td>
    <td class="org-left">heavy</td>
    </tr>
    
    <tr>
    <td class="org-left">&#xa0;</td>
    <td class="org-left">medium</td>
    </tr>
    
    <tr>
    <td class="org-left">&#xa0;</td>
    <td class="org-left">light</td>
    </tr>
    </tbody>
    <tbody>
    <tr>
    <td class="org-left"><b>SWINGS</b></td>
    <td class="org-left">0 - 150</td>
    </tr>
    </tbody>
    </table>

2.  abc

    The random command with a workout type of `abc` will generate a random armor building complex workout.
    
        kettlebells random --workout-type abc
    
    <table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">
    
    
    <colgroup>
    <col  class="org-left" />
    
    <col  class="org-left" />
    </colgroup>
    <thead>
    <tr>
    <th scope="col" class="org-left">Parameter</th>
    <th scope="col" class="org-left">Options</th>
    </tr>
    </thead>
    <tbody>
    <tr>
    <td class="org-left"><b>Single Bell Variations</b></td>
    <td class="org-left">Armor Building Complex 2.0</td>
    </tr>
    </tbody>
    <tbody>
    <tr>
    <td class="org-left"><b>Double Bell Variations</b></td>
    <td class="org-left">Armor Building Complex</td>
    </tr>
    </tbody>
    <tbody>
    <tr>
    <td class="org-left"><b>TIMES</b></td>
    <td class="org-left">30 mins</td>
    </tr>
    
    <tr>
    <td class="org-left">&#xa0;</td>
    <td class="org-left">25 mins</td>
    </tr>
    
    <tr>
    <td class="org-left">&#xa0;</td>
    <td class="org-left">20 mins</td>
    </tr>
    
    <tr>
    <td class="org-left">&#xa0;</td>
    <td class="org-left">15 mins</td>
    </tr>
    
    <tr>
    <td class="org-left">&#xa0;</td>
    <td class="org-left">10 mins</td>
    </tr>
    </tbody>
    <tbody>
    <tr>
    <td class="org-left"><b>LOADS</b></td>
    <td class="org-left">heavy</td>
    </tr>
    
    <tr>
    <td class="org-left">&#xa0;</td>
    <td class="org-left">medium</td>
    </tr>
    
    <tr>
    <td class="org-left">&#xa0;</td>
    <td class="org-left">light</td>
    </tr>
    </tbody>
    <tbody>
    <tr>
    <td class="org-left"><b>SWINGS</b></td>
    <td class="org-left">0 - 100</td>
    </tr>
    </tbody>
    </table>


<a id="org319bbb1"></a>

### last

The `last` command displays the last saved workout and calculates the stats for it.

    kettlebells last


<a id="orgb4c7591"></a>

### view

Use the `view` command to search for previous workouts by date. If you have [ripgrep](https://github.com/BurntSushi/ripgrep#installation) installed, use the `--preview` flag to view more information about the workout based on the date.

    kettlebells view --preview

Use the `--Program` flag to filter workouts based on a certain workout<sub>type</sub>.

    kettlebells view --Program


<a id="org85a8277"></a>

### stats

The `stats` command displays the aggregated workout count, time, weight moved, number of reps, and density for all workout in the database.

    kettlebells stats

1.  Filtering by time

    The stats command can be filtered using three arguments: `--start`, `--end`, `--year`.
    
    Here is an example using `--start` and `--end` to get the stats from Jan 2024.
    
        kettlebells stats --start 2024-01-01 --end 2024-02-01
    
    If you want to see an entire year, just use `--year`.
    
        kettlebells stats --year 2024
    
    All three time filters work with the plots. And `--year` works with the calendar command covered later.

2.  plot

    To display a line plot of the weight moved per workout, use the `--plot line` option. Add a line at the median with `--median` or at the mean with `--average`.
    
        kettlebells stats --plot line
    
    To display a horizontal bar plot grouped by month, use the `--plot bar` option.
    
        kettlebells stats --plot bar
    
    To display an event plot of the current year, use the `--plot event` option.
    
        kettlebells stats --plot event

3.  calendar

    To display a calendar of workouts in a given year, use the `--calendar` flag and pass the year as the argument.
    
        kettlebells stats --calendar -y 2023

4.  best

    The `best` command displays the top ten workout based on the weight moved.
    
        kettlebells stats --best
    
    Use the `--sort` option to sort the table by:
    
    -   weight-moved (default)
    -   reps
    -   weight-density
    -   rep-density
    -   time

