"""
EG4 Python Client Library

A Python library that provides both async and sync methods to interact with 
the EG4 Inverter cloud API. It handles login, data retrieval, and session 
management efficiently — ideal for integration with Home Assistant, MCP, 
automation platforms, or custom monitoring solutions.

Features:
- Asynchronous and synchronous support
- Automatic re-authentication on session expiry
- Modular structure for future expandability
- Support for multiple inverters from a single account
"""

from .client import EG4Inverter
from .exceptions import EG4AuthError, EG4APIError
from .models import DailyChartData, DailyChartDataPoint

__version__ = "0.1.2"
__author__ = "Matt Dreyer"
__email__ = "matt_dreyer@hotmail.com"

__all__ = [
    "EG4Inverter",
]