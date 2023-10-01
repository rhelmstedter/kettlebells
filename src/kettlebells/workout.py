from dataclasses import dataclass


@dataclass
class Workout:
    bells: str
    variation: str
    time: int
    load: int
    units: str
    swings: int
    sets: int
    workout_type: str

    def display_workout(self) -> None:
        """Print an a workout to the console.
        :returns: None.
        """
        if self.swings:
            swings = f"   Swings: {self.swings} reps"
        else:
            swings = ""
        print(
            f"""{self.workout_type.upper()}\n[green]===================[/green]
    Bells: {self.bells.title()}
Variation: {self.variation}
     Time: {self.time} mins
     Load: {self.load} {self.units}
{swings}
"""
        )
