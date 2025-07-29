"""
Custom exceptions for the Veras SDK.
"""


class VerasError(Exception):
    """Base exception for Veras SDK errors."""
    pass


class AuthenticationError(VerasError):
    """Raised when authentication fails."""
    pass


class ValidationError(VerasError):
    """Raised when input validation fails."""
    pass


class RateLimitError(VerasError):
    """Raised when rate limits are exceeded."""
    pass
