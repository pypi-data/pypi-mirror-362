# Copyright 2025, Euro NCAP IVZW
# Created by IVEX NV (https://ivex.ai)
#
# Licensed under the Apache License 2.0.
# See http://www.apache.org/licenses/LICENSE-2.0 for details.

from typing import List
import logging
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class Measurement(BaseModel):
    name: str
    values: List[float]

    @property
    def modifier(self) -> float:
        return self.evaluate_measurement()

    def evaluate_measurement(self) -> float:
        if self.name == "DAMAGE":
            return (
                0.0
                if self.values[0] < 0.42
                else (20.0 if self.values[0] < 0.47 else 40.0)
            )
        elif self.name == "Shoulder belt load":
            return 0.0 if self.values[0] < 6.0 else 40.0
        elif self.name == "Pedal blocking":
            return 0.0 if self.values[0] < 50.0 else 20.0
        elif self.name == "Pedal displacement - rearward":
            return (
                0.0
                if self.values[0] < 100.0
                else (50.0 if self.values[0] < 200.0 else 100.0)
            )
        elif self.name == "Pedal displacement - vertical":
            return 0.0 if self.values[0] < 72.0 else 20.0
        elif self.name == "Excursion":
            return (
                0.0
                if self.values[0] < 450.0
                else (50.0 if self.values[0] < 550.0 else 100.0)
            )
        elif self.name == "Shoulder load":
            return 0.0 if self.values[0] < 3.0 else 100.0
        elif self.name == "Viscous Criterion":
            return 0.0 if self.values[0] < 1.0 else 100.0
        elif self.name == "Effective height modifier":
            return 100.0 if self.values[0] < 790.0 else 0.0
        elif self.name in ["Knee load - Variable, left", "Knee load - Variable, right"]:
            if len(self.values) < 2:
                raise ValueError(
                    f"'values' must contain at least two elements for measurement '{self.name}'"
                )
            return 0.0 if self.values[0] < 3.8 and self.values[1] < 6.0 else 20.0
        elif self.name == "Fpubic symphysis":
            return 0.0 if self.values[0] < 2.8 else 25.0
        elif self.name == "Fy lumbar":
            return 0.0 if self.values[0] < 2.0 else 25.0
        elif self.name == "Fz lumbar":
            return 0.0 if self.values[0] < 3.5 else 25.0
        elif self.name == "Mx lumbar":
            return 0.0 if self.values[0] < 120.0 else 25.0
        else:
            raise ValueError(f"Unknown measurement: {self.name}")
