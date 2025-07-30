"""
PRC API Wrapper
===============

A Python wrapper for the Police Roleplay Community API.
"""

from .client import PRCClient
from .exceptions import PRCError
from .models import PRCResponse, ErrorCode

__version__ = "1.0.3"
__all__ = ["PRCClient", "PRCError", "PRCResponse", "ErrorCode"]
