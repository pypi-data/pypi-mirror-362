"""
Verifik.io Python SDK

A developer-friendly Python SDK for integrating with Verifik.io's trust infrastructure platform.
Provides secure, immutable audit trails for AI agent workflows.
"""

from .client import VerifikClient
from .exceptions import VerifikError, AuthenticationError, ValidationError, APIError

__version__ = "1.2.0"
__author__ = "Verifik.io"
__email__ = "support@verifik.io"
__license__ = "MIT"

__all__ = [
    "VerifikClient",
    "VerifikError",
    "AuthenticationError", 
    "ValidationError",
    "APIError",
]