"""
CDB Fan Control - Simple Coral Dev Board Fan Control

Simple functions to control Coral Dev Board fan.
"""

__version__ = "1.0.0"

from .fan_control import enable_cdb_fan, disable_cdb_fan

__all__ = ["enable_cdb_fan", "disable_cdb_fan"]
