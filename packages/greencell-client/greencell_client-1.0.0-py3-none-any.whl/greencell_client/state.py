""" state.py
Helper class for managing EVSE state in Greencell EVSE devices.

Classes:
- EvseStateEnum: Enum representing possible EVSE states (IDLE, CONNECTED,
                WAITING_FOR_CAR, CHARGING, FINISHED, ERROR_CAR, ERROR_EVSE, UNKNOWN).
- EvseStateData: Tracks the current EVSE state and notifies registered listeners on changes.
"""

import logging

from collections.abc import Callable
from enum import auto
from .utils import GreencellEnum

_LOGGER = logging.getLogger(__name__)


class EvseStateEnum(GreencellEnum):
    """Enumeration for Greencell EVSE states."""
    IDLE = auto()
    CONNECTED = auto()
    WAITING_FOR_CAR = auto()
    CHARGING = auto()
    FINISHED = auto()
    ERROR_CAR = auto()
    ERROR_EVSE = auto()
    UNKNOWN = auto()


class EvseStateData:
    """Simple internal EVSE state tracker (charging / idle)."""

    def __init__(self) -> None:
        self._state = EvseStateEnum.UNKNOWN
        self._listeners = []

    def update(self, new_state: str) -> None:
        """Update the EVSE state based on the received message."""
        # If new_state matches one of the enum names, use it; otherwise fall back to UNKNOWN
        self._state = EvseStateEnum.__members__.get(new_state, EvseStateEnum.UNKNOWN)

        self._notify_listeners()
        _LOGGER.debug("EVSE state updated to %s", new_state)

    def can_be_stopped(self) -> bool:
        """Check if the EVSE is in a state where charging can be stopped
            (when charging process is allowed by user)."""
        return (
            self._state == EvseStateEnum.WAITING_FOR_CAR
            or self._state == EvseStateEnum.CHARGING
        )

    def can_be_started(self) -> bool:
        """Check if the EVSE is in a state where charging can be started."""
        return (
            self._state == EvseStateEnum.FINISHED
            or self._state == EvseStateEnum.CONNECTED
        )

    def set_charging(self, value: bool) -> None:
        """Set the charging state of the EVSE."""
        self._charging = value

    def register_listener(self, listener: Callable[[], None]) -> None:
        """Register a listener to be notified of state changes."""
        self._listeners.append(listener)

    def _notify_listeners(self) -> None:
        """Notify all registered listeners of a state change."""
        for listener in self._listeners:
            listener()
