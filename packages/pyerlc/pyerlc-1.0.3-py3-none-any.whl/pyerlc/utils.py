"""
Utility functions for the PRC API Wrapper.
"""

from datetime import datetime
from typing import Union, List, Dict, Any, Optional, TypeVar, Type
from .models import *

T = TypeVar('T')

def format_timestamp(timestamp: Union[int, float]) -> str:
    """Convert Unix timestamp to readable string."""
    try:
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
        return str(timestamp)

def validate_server_key(server_key: str) -> bool:
    """Basic validation for the server key format."""
    if not server_key or not isinstance(server_key, str):
        return False
    # Simple length check (adjust with actual format rules if known)
    if len(server_key) < 10:
        return False
    return True

def safe_get(data: Dict[str, Any], key: str, default: Any = None) -> Any:
    """Safely get a value from a dictionary."""
    return data.get(key, default)

def chunk_list(lst: List[T], chunk_size: int) -> List[List[T]]:
    """Split a list into chunks of specified size."""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]
