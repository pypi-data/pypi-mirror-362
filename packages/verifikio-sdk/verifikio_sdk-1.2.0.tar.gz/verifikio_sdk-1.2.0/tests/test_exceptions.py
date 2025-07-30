"""
Unit tests for Verifik.io SDK exceptions
"""

import pytest
from verifikio.exceptions import VerifikError, AuthenticationError, ValidationError, APIError


class TestExceptions:
    """Test suite for SDK exceptions"""

    def test_verifik_error_inheritance(self):
        """Test that VerifikError is base exception"""
        error = VerifikError("Test error")
        assert isinstance(error, Exception)
        assert str(error) == "Test error"

    def test_authentication_error_inheritance(self):
        """Test that AuthenticationError inherits from VerifikError"""
        error = AuthenticationError("Auth failed")
        assert isinstance(error, VerifikError)
        assert isinstance(error, Exception)
        assert str(error) == "Auth failed"

    def test_validation_error_inheritance(self):
        """Test that ValidationError inherits from VerifikError"""
        error = ValidationError("Validation failed")
        assert isinstance(error, VerifikError)
        assert isinstance(error, Exception)
        assert str(error) == "Validation failed"

    def test_api_error_inheritance(self):
        """Test that APIError inherits from VerifikError"""
        error = APIError("API failed")
        assert isinstance(error, VerifikError)
        assert isinstance(error, Exception)
        assert str(error) == "API failed"

    def test_exception_hierarchy(self):
        """Test exception hierarchy for proper catching"""
        # Test that specific exceptions can be caught by base class
        try:
            raise AuthenticationError("Auth error")
        except VerifikError as e:
            assert isinstance(e, AuthenticationError)
            assert str(e) == "Auth error"
        
        try:
            raise ValidationError("Validation error")
        except VerifikError as e:
            assert isinstance(e, ValidationError)
            assert str(e) == "Validation error"
        
        try:
            raise APIError("API error")
        except VerifikError as e:
            assert isinstance(e, APIError)
            assert str(e) == "API error"