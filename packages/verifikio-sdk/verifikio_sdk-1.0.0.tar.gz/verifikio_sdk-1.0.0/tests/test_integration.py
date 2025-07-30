"""
Integration tests for Verifik.io SDK

These tests can be run against a real API by setting the VERIFIK_API_KEY environment variable.
"""

import os
import pytest
from verifikio import VerifikClient
from verifikio.exceptions import AuthenticationError


class TestIntegration:
    """Integration test suite - requires real API key"""

    @pytest.fixture
    def api_key(self):
        """Get API key from environment"""
        key = os.getenv("VERIFIK_API_KEY")
        if not key:
            pytest.skip("VERIFIK_API_KEY environment variable not set")
        return key

    @pytest.fixture
    def client(self, api_key):
        """Create client with real API key"""
        return VerifikClient(api_key=api_key)

    def test_authentication_success(self, client):
        """Test successful authentication with real API key"""
        # Should not raise an exception
        stats = client.get_stats()
        assert isinstance(stats, dict)
        assert "totalLogs" in stats

    def test_authentication_failure(self):
        """Test authentication failure with invalid API key"""
        client = VerifikClient(api_key="verifik_live_invalid")
        
        with pytest.raises(AuthenticationError):
            client.get_stats()

    def test_log_event_integration(self, client):
        """Test creating an audit log with real API"""
        response = client.log_event(
            agent_name="test_agent",
            action="integration_test",
            inputs={"test": "data"},
            outputs={"result": "success"},
            metadata={"test_type": "integration"},
            status="success"
        )
        
        assert isinstance(response, dict)
        assert "id" in response
        assert "hash" in response
        assert "timestamp" in response

    def test_get_logs_integration(self, client):
        """Test retrieving logs with real API"""
        response = client.get_logs(limit=5)
        
        assert isinstance(response, dict)
        assert "logs" in response
        assert "pagination" in response
        assert isinstance(response["logs"], list)

    def test_verify_chain_integration(self, client):
        """Test chain verification with real API"""
        response = client.verify_chain()
        
        assert isinstance(response, dict)
        assert "isValid" in response
        assert isinstance(response["isValid"], bool)