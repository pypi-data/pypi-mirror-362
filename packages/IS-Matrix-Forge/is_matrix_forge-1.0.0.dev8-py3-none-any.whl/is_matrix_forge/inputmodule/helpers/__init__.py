from serial import SerialException, Serial
from serial.tools import list_ports

from ...led_matrix.helpers.device import DEVICES
from ...log_engine import ROOT_LOGGER as PARENT_LOGGER

MOD_LOGGER = PARENT_LOGGER.get_child('inputmodule.helpers')


MOD_LOGGER.debug(f'Found {len(DEVICES)} devices.')

if len(DEVICES) == 1:
    DEVICE = DEVICES[0]
else:
    MOD_LOGGER.warning(f'Found {len(DEVICES)} devices. Device choice must be explicit.')

