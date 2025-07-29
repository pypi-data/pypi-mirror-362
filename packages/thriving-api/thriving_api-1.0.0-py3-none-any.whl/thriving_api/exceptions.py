"""
Exception classes for the Thriving API SDK.

This module defines all custom exceptions that can be raised by the SDK,
providing clear error handling and debugging information.
"""

from typing import Optional, Dict, Any


class ThrivingAPIError(Exception):
    """Base exception class for all Thriving API errors."""
    
    def __init__(
        self, 
        message: str, 
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
        request_id: Optional[str] = None
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}
        self.request_id = request_id
    
    def __str__(self) -> str:
        parts = [self.message]
        if self.status_code:
            parts.append(f"Status: {self.status_code}")
        if self.request_id:
            parts.append(f"Request ID: {self.request_id}")
        return " | ".join(parts)


class AuthenticationError(ThrivingAPIError):
    """Raised when API key authentication fails."""
    
    def __init__(self, message: str = "Invalid or missing API key", **kwargs) -> None:
        super().__init__(message, status_code=401, **kwargs)


class RateLimitError(ThrivingAPIError):
    """Raised when API rate limits are exceeded."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: Optional[int] = None,
        **kwargs: Any
    ) -> None:
        super().__init__(message, status_code=429, **kwargs)
        self.retry_after = retry_after


class ValidationError(ThrivingAPIError):
    """Raised when request validation fails."""

    def __init__(
        self,
        message: str = "Request validation failed",
        validation_errors: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> None:
        super().__init__(message, status_code=400, **kwargs)
        self.validation_errors = validation_errors or {}


class APIConnectionError(ThrivingAPIError):
    """Raised when there are connection issues with the API."""

    def __init__(self, message: str = "Failed to connect to API", **kwargs: Any) -> None:
        super().__init__(message, **kwargs)


class ServerError(ThrivingAPIError):
    """Raised when the API returns a server error (5xx)."""

    def __init__(self, message: str = "Internal server error", **kwargs: Any) -> None:
        super().__init__(message, **kwargs)


class TimeoutError(ThrivingAPIError):
    """Raised when API requests timeout."""

    def __init__(self, message: str = "Request timeout", **kwargs: Any) -> None:
        super().__init__(message, **kwargs)


class QuotaExceededError(ThrivingAPIError):
    """Raised when API quota is exceeded."""

    def __init__(self, message: str = "API quota exceeded", **kwargs: Any) -> None:
        super().__init__(message, status_code=402, **kwargs)


class NotFoundError(ThrivingAPIError):
    """Raised when requested resource is not found."""

    def __init__(self, message: str = "Resource not found", **kwargs: Any) -> None:
        super().__init__(message, status_code=404, **kwargs)


class SymbolNotFoundError(NotFoundError):
    """Raised when a stock symbol is not found."""

    def __init__(self, symbol: str, **kwargs: Any) -> None:
        message = f"Symbol '{symbol}' not found"
        super().__init__(message, **kwargs)
        self.symbol = symbol
