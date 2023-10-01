from dataclasses import dataclass
from workout import Workout


@dataclass
class ArmorBuildingComplex(Workout):
    workout_type: str = "ABC"
