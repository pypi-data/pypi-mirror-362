""" mqtt_parser.py
This module contains utilities required to parsing MQTT messages for the Greencell EVSE client.
"""

import json
import logging

from json import JSONDecodeError
from .elec_data import ElecData3Phase, ElecDataSinglePhase


_LOGGER = logging.getLogger(__name__)


def _get_json_value(data: str) -> dict:
    """Extract JSON data from a string."""
    try:
        return json.loads(data)
    except JSONDecodeError as ex:
        _LOGGER.error("Invalid JSON payload: %s", ex)
        return {}


class MqttParser:
    """Parser for MQTT messages related to Greencell EVSE devices."""

    @staticmethod
    def parse_3phase_msg(msg: str, ThreePhaseData: ElecData3Phase) -> bool:
        """Parse current data from MQTT message and update the 3Phase data object.
        :param msg: The MQTT message containing current data.
        :param ThreePhaseData: An instance of ElecData3Phase to update with parsed data.
        :return: True if parsing was successful, False otherwise.
        """

        data = _get_json_value(msg)
        if not data:
            return False

        try:
            ThreePhaseData.update_data(data)
            return True
        except KeyError as ex:
            _LOGGER.error("Key error while updating 3-phase data: %s", ex)
            return False
        except TypeError as ex:
            _LOGGER.error("Type error while updating 3-phase data: %s", ex)
            return False
        except ValueError as ex:
            _LOGGER.error("Value error while updating 3-phase data: %s", ex)
            return False
        except Exception as ex:
            _LOGGER.error("Unexpected error while updating 3-phase data: %s", ex)
            return False

    @staticmethod
    def parse_single_phase_msg(msg: str, key: str, SinglePhaseData: ElecDataSinglePhase) -> bool:
        """Parse current data from MQTT message and update the single phase data object.
        :param msg: The MQTT message containing current data.
        :param key: The key in the JSON data to extract single phase value.
        :param SinglePhaseData: An instance of ElecDataSinglePhase to update with parsed data.
        :return: True if parsing was successful, False otherwise.
        """

        data = _get_json_value(msg)
        if not data:
            return False

        try:
            value = data[key]
            if value is None:
                _LOGGER.error("Key '%s' not found in message: %s", key, msg)
                return False
        except KeyError as ex:
            _LOGGER.error("Key error while parsing single phase data: %s", ex)
            return False

        try:
            SinglePhaseData.update_data(value)
            return True
        except TypeError as ex:
            _LOGGER.error("Type error while updating single phase data: %s", ex)
            return False
        except ValueError as ex:
            _LOGGER.error("Value error while updating single phase data: %s", ex)
            return False
        except Exception as ex:
            _LOGGER.error("Unexpected error while updating single phase data: %s", ex)
            return False
