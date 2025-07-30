"""
This module contains utility classes and enums for the Greencell EVSE client.
It includes an enumeration for EVSE types and a base class for Greencell enums.
"""
from enum import Enum
import re


GREENCELL_HABU_DEN_SERIAL_PREFIX = "EVGC02"


class GreencellEnum(Enum):
    """Declaration of EVSE types as string enums."""

    def _generate_next_value_(name, start, count, last_values):
        return name


class GreencellUtils:
    """Utility class for Greencell client operations."""

    @staticmethod
    def device_is_habu_den(serial: str) -> bool:
        """Check if the device is a Habu Den based on its serial number."""
        pattern = r"^EVGC021[A-Z][0-9]{8}ZM[0-9]{4}$"
        return bool(re.fullmatch(pattern, serial))
