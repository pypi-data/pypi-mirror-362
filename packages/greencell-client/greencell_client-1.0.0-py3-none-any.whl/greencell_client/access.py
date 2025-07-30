"""access.py

Helper class for managing Home Assistant access levels for Greencell EVSE devices.

Classes:
- GreencellAccess: tracks the current access level (DISABLED, READ_ONLY, EXECUTE, OFFLINE),
  notifies registered listeners on changes, and provides utility methods:
    * update(new_access_level: str) – parse and set a new access level from its string name.
    * register_listener(listener: Callable) – add callbacks to invoke when access changes.
    * can_execute() -> bool – returns True if the level allows executing commands.
    * is_disabled() -> bool – returns True if access is DISABLED or OFFLINE.
"""
from collections.abc import Callable
from enum import auto
from json import JSONDecodeError
from .utils import GreencellEnum

import logging
import json

_LOGGER = logging.getLogger(__name__)


class GreencellHaAccessLevel(GreencellEnum):
    """Enumeration for Greencell Home Assistant access levels."""
    DISABLED = auto()
    READ_ONLY = auto()
    EXECUTE = auto()
    OFFLINE = auto()


class GreencellAccess:
    """Class to manage access levels for Greencell devices."""

    def __init__(self, access_level: GreencellHaAccessLevel):
        self._access_level = access_level
        self._listeners = []

    def update(self, new_access_level: str) -> None:
        """Update the access level and notify listeners."""
        self._access_level = GreencellHaAccessLevel.__members__.get(
            new_access_level, GreencellHaAccessLevel.DISABLED
        )
        self._notify_listeners()

    def register_listener(self, listener: Callable[[], None]) -> None:
        """Register a listener to be notified when the access level changes."""
        self._listeners.append(listener)

    def _notify_listeners(self) -> None:
        """Notify all registered listeners of the access level change."""
        for listener in self._listeners:
            listener()

    def can_execute(self) -> bool:
        """Check if the current access level allows execution of commands."""
        return self._access_level == GreencellHaAccessLevel.EXECUTE

    def is_disabled(self) -> bool:
        """Check if the current access level is disabled."""
        return (
            self._access_level == GreencellHaAccessLevel.DISABLED
            or self._access_level == GreencellHaAccessLevel.OFFLINE
        )

    def on_msg(self, msg: str) -> None:
        """Handle incoming messages to update access level."""
        try:
            data = json.loads(msg)
        except JSONDecodeError as ex:
            _LOGGER.error("Failed to decode JSON message: %s", ex)
            self.update("DISABLED")
            return

        new_access_level = data.get("level", "DISABLED")
        try:
            self.update(new_access_level)
            _LOGGER.debug("Access level updated to %s", new_access_level)
        except KeyError as ex:
            _LOGGER.error("Invalid access level in message: %s", ex)
        except TypeError as ex:
            _LOGGER.error("Type error while updating access level: %s", ex)
        except ValueError as ex:
            _LOGGER.error("Value error while updating access level: %s", ex)
        except Exception as ex:
            _LOGGER.error("Unexpected error while updating access level: %s", ex)
