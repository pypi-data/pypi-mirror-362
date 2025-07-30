"""
LED Matrix Module.

This module provides a high-level interface for interacting with LED matrix devices.
It combines functionality from various modules to provide a simple API for controlling
LED matrices, displaying patterns, animations, and battery status.
"""

from __future__ import annotations

# Standard library
from pathlib import Path
from typing import Optional, Union, List

# Third-party
from serial.tools.list_ports_common import ListPortInfo

# Inspyre-Softworks
from is_matrix_forge.led_matrix.display.grid import Grid, generate_blank_grid
from is_matrix_forge.led_matrix.display.animations import goodbye_animation
from is_matrix_forge.led_matrix.helpers.device import get_devices
from is_matrix_forge.common.helpers import percentage_to_value



