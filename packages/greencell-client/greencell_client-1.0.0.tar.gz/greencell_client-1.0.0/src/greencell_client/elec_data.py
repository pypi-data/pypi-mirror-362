"""elec_data.py
Helper classes for managing electrical data in Greencell EVSE devices.

Classes:
- ElecData3Phase: stores electrical data for 3 phases (l1, l2, l3) and provides methods to update
                  and retrieve data.
- ElecDataSinglePhase: stores single-value data like power, with methods to update
                       and retrieve the value.
"""

from dataclasses import dataclass, fields
from typing import Optional, Any


@dataclass
class ElecData3Phase:
    """Dataclass storing electrical data (e.g. current or voltage) for 3 phases."""
    l1: Optional[Any] = None
    l2: Optional[Any] = None
    l3: Optional[Any] = None

    def update_data(self, new_data: dict) -> None:
        """Update sensor data if the dictionary contains keys corresponding to the phases."""
        for f in fields(self):
            if f.name in new_data:
                setattr(self, f.name, new_data[f.name])

    def get_value(self, phase: str) -> Optional[Any]:
        """Get the value for a specific phase."""
        for f in fields(self):
            if f.name == phase:
                return getattr(self, f.name)
        raise ValueError(f"Invalid phase: {phase}. Valid phases are \
                         {', '.join(f.name for f in fields(self))}.")


@dataclass
class ElecDataSinglePhase:
    """Dataclass storing single-value data like power, etc."""
    value: Optional[Any] = None

    def update_data(self, new_data) -> None:
        self.value = new_data

    @property
    def data(self) -> Optional[Any]:
        return self.value
