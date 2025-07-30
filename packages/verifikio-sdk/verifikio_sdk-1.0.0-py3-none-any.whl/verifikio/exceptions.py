"""
Verifik.io Python SDK Exceptions

Custom exception classes for the Verifik.io SDK.
"""


class VerifikError(Exception):
    """Base exception for all Verifik.io SDK errors"""
    pass


class AuthenticationError(VerifikError):
    """Raised when API key is invalid or unauthorized"""
    pass


class ValidationError(VerifikError):
    """Raised when request parameters are invalid"""
    pass


class APIError(VerifikError):
    """Raised when the API returns an error response"""
    pass