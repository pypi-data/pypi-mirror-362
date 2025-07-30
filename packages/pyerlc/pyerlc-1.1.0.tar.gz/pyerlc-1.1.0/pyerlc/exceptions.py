"""
Custom exceptions for the PRC API Wrapper.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import PRCResponse


class PRCError(Exception):
    """Base exception for PRC API errors."""

    def __init__(self, response: "PRCResponse"):
        self.response = response
        self.error_code = response.error_code
        self.status_code = response.status_code
        super().__init__(response.error_message or "An error occurred with the PRC API.")


class PRCConnectionError(PRCError):
    """Exception raised when connection to PRC API fails."""
    pass


class PRCAuthenticationError(PRCError):
    """Exception raised when authentication fails."""
    pass


class PRCRateLimitError(PRCError):
    """Exception raised when rate limit is exceeded."""
    pass


class PRCServerError(PRCError):
    """Exception raised when server returns 5xx error."""
    pass
