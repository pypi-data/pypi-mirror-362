### `src/ipapp/__init__.py`

"""
ipapp – tiny client for the ip.app service.
"""

from .client import (
    IPAppError,
    get_ip,
    get_asn,
    get_tz,
    get_location,
)

__all__ = [
    "IPAppError",
    "get_ip",
    "get_asn",
    "get_tz",
    "get_location",
]

__version__ = "4.0.2"
