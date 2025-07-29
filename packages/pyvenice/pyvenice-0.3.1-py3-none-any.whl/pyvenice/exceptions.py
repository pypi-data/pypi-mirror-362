"""
Exception classes for Venice.ai API errors.
"""

from typing import Optional, Dict, Any


class VeniceAPIError(Exception):
    """Base exception for all Venice API errors."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class AuthenticationError(VeniceAPIError):
    """Raised when authentication fails (401)."""

    pass


class InvalidRequestError(VeniceAPIError):
    """Raised when request parameters are invalid (400, 415)."""

    pass


class InsufficientBalanceError(VeniceAPIError):
    """Raised when account has insufficient balance (402)."""

    pass


class RateLimitError(VeniceAPIError):
    """Raised when rate limit is exceeded (429)."""

    pass


class InferenceError(VeniceAPIError):
    """Raised when inference processing fails (500)."""

    pass


class ModelCapacityError(VeniceAPIError):
    """Raised when model is at capacity (503)."""

    pass


class TimeoutError(VeniceAPIError):
    """Raised when request times out (504)."""

    pass
