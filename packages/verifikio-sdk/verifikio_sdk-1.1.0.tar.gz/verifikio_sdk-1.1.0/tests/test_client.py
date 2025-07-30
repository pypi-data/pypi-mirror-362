"""
Unit tests for the Verifik.io Python SDK Client
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from verifikio import VerifikClient
from verifikio.exceptions import VerifikError, AuthenticationError, ValidationError, APIError


class TestVerifikClient:
    """Test suite for VerifikClient class"""

    def test_init_valid_api_key(self):
        """Test client initialization with valid API key"""
        client = VerifikClient(api_key="verifik_live_abc123")
        assert client.api_key == "verifik_live_abc123"
        assert client.base_url == "https://api.verifik.io"
        assert client.timeout == 30

    def test_init_custom_base_url(self):
        """Test client initialization with custom base URL"""
        client = VerifikClient(
            api_key="verifik_live_abc123",
            base_url="https://custom.api.com/",
            timeout=60
        )
        assert client.base_url == "https://custom.api.com"
        assert client.timeout == 60

    def test_init_empty_api_key(self):
        """Test client initialization with empty API key"""
        with pytest.raises(ValueError, match="API key is required"):
            VerifikClient(api_key="")

    def test_init_none_api_key(self):
        """Test client initialization with None API key"""
        with pytest.raises(ValueError, match="API key is required"):
            VerifikClient(api_key=None)

    def test_init_invalid_api_key_format(self):
        """Test client initialization with invalid API key format"""
        with pytest.raises(ValueError, match="Invalid API key format"):
            VerifikClient(api_key="invalid_key")

    def test_session_headers(self):
        """Test that session headers are set correctly"""
        client = VerifikClient(api_key="verifik_live_abc123")
        headers = client.session.headers
        assert headers["Authorization"] == "Bearer verifik_live_abc123"
        assert headers["Content-Type"] == "application/json"
        assert "verifikio-python-sdk" in headers["User-Agent"]

    @patch('verifikio.client.requests.Session.request')
    def test_log_event_minimal(self, mock_request):
        """Test log_event with minimal required parameters"""
        # Mock successful response
        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "log_123", "hash": "hash_456"}
        mock_request.return_value = mock_response

        client = VerifikClient(api_key="verifik_live_abc123")
        result = client.log_event(agent_name="test_agent", action="test_action")

        assert result["id"] == "log_123"
        assert result["hash"] == "hash_456"
        
        # Verify request was made correctly
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert args[0] == "POST"
        assert "/api/v1/logs" in args[1]
        assert kwargs["json"] == {"agentId": "test_agent", "action": "test_action"}

    @patch('verifikio.client.requests.Session.request')
    def test_log_event_full_parameters(self, mock_request):
        """Test log_event with all parameters"""
        # Mock successful response
        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "log_123"}
        mock_request.return_value = mock_response

        client = VerifikClient(api_key="verifik_live_abc123")
        result = client.log_event(
            agent_name="test_agent",
            action="test_action",
            inputs={"key": "value"},
            outputs={"result": "success"},
            metadata={"version": "1.0"},
            workflow_id="workflow_123",
            status="completed"
        )

        assert result["id"] == "log_123"
        
        # Verify request payload
        args, kwargs = mock_request.call_args
        expected_payload = {
            "agentId": "test_agent",
            "action": "test_action",
            "inputs": {"key": "value"},
            "outputs": {"result": "success"},
            "metadata": {"version": "1.0"},
            "workflowId": "workflow_123",
            "status": "completed"
        }
        assert kwargs["json"] == expected_payload

    def test_log_event_invalid_agent_name(self):
        """Test log_event with invalid agent_name"""
        client = VerifikClient(api_key="verifik_live_abc123")
        
        with pytest.raises(ValidationError, match="agent_name must be a non-empty string"):
            client.log_event(agent_name="", action="test_action")
        
        with pytest.raises(ValidationError, match="agent_name must be a non-empty string"):
            client.log_event(agent_name=123, action="test_action")

    def test_log_event_invalid_action(self):
        """Test log_event with invalid action"""
        client = VerifikClient(api_key="verifik_live_abc123")
        
        with pytest.raises(ValidationError, match="action must be a non-empty string"):
            client.log_event(agent_name="test_agent", action="")
        
        with pytest.raises(ValidationError, match="action must be a non-empty string"):
            client.log_event(agent_name="test_agent", action=None)

    def test_log_event_invalid_inputs(self):
        """Test log_event with invalid inputs parameter"""
        client = VerifikClient(api_key="verifik_live_abc123")
        
        with pytest.raises(ValidationError, match="inputs must be a dictionary"):
            client.log_event(agent_name="test_agent", action="test_action", inputs="invalid")

    def test_log_event_invalid_outputs(self):
        """Test log_event with invalid outputs parameter"""
        client = VerifikClient(api_key="verifik_live_abc123")
        
        with pytest.raises(ValidationError, match="outputs must be a dictionary"):
            client.log_event(agent_name="test_agent", action="test_action", outputs="invalid")

    def test_log_event_invalid_metadata(self):
        """Test log_event with invalid metadata parameter"""
        client = VerifikClient(api_key="verifik_live_abc123")
        
        with pytest.raises(ValidationError, match="metadata must be a dictionary"):
            client.log_event(agent_name="test_agent", action="test_action", metadata="invalid")

    def test_log_event_invalid_workflow_id(self):
        """Test log_event with invalid workflow_id parameter"""
        client = VerifikClient(api_key="verifik_live_abc123")
        
        with pytest.raises(ValidationError, match="workflow_id must be a string"):
            client.log_event(agent_name="test_agent", action="test_action", workflow_id=123)

    def test_log_event_invalid_status(self):
        """Test log_event with invalid status parameter"""
        client = VerifikClient(api_key="verifik_live_abc123")
        
        with pytest.raises(ValidationError, match="status must be a string"):
            client.log_event(agent_name="test_agent", action="test_action", status=123)

    @patch('verifikio.client.requests.Session.request')
    def test_log_event_401_error(self, mock_request):
        """Test log_event with 401 authentication error"""
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 401
        mock_request.return_value = mock_response

        client = VerifikClient(api_key="verifik_live_abc123")
        
        with pytest.raises(AuthenticationError, match="Invalid API key"):
            client.log_event(agent_name="test_agent", action="test_action")

    @patch('verifikio.client.requests.Session.request')
    def test_log_event_400_error(self, mock_request):
        """Test log_event with 400 validation error"""
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 400
        mock_response.json.return_value = {"message": "Invalid request"}
        mock_request.return_value = mock_response

        client = VerifikClient(api_key="verifik_live_abc123")
        
        with pytest.raises(ValidationError, match="Validation error: Invalid request"):
            client.log_event(agent_name="test_agent", action="test_action")

    @patch('verifikio.client.requests.Session.request')
    def test_log_event_429_error(self, mock_request):
        """Test log_event with 429 rate limit error"""
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 429
        mock_request.return_value = mock_response

        client = VerifikClient(api_key="verifik_live_abc123")
        
        with pytest.raises(APIError, match="Rate limit exceeded"):
            client.log_event(agent_name="test_agent", action="test_action")

    @patch('verifikio.client.requests.Session.request')
    def test_log_event_500_error(self, mock_request):
        """Test log_event with 500 server error"""
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 500
        mock_request.return_value = mock_response

        client = VerifikClient(api_key="verifik_live_abc123")
        
        with pytest.raises(APIError, match="Server error: 500"):
            client.log_event(agent_name="test_agent", action="test_action")

    @patch('verifikio.client.requests.Session.request')
    def test_get_logs_default_params(self, mock_request):
        """Test get_logs with default parameters"""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = {"logs": [], "pagination": {"total": 0}}
        mock_request.return_value = mock_response

        client = VerifikClient(api_key="verifik_live_abc123")
        result = client.get_logs()

        assert "logs" in result
        assert "pagination" in result
        
        # Verify request parameters
        args, kwargs = mock_request.call_args
        assert args[0] == "GET"
        assert "/api/v1/logs" in args[1]
        assert kwargs["params"] == {"limit": 50, "offset": 0}

    @patch('verifikio.client.requests.Session.request')
    def test_get_logs_custom_params(self, mock_request):
        """Test get_logs with custom parameters"""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = {"logs": []}
        mock_request.return_value = mock_response

        client = VerifikClient(api_key="verifik_live_abc123")
        result = client.get_logs(limit=20, offset=10, workflow_id="workflow_123")

        args, kwargs = mock_request.call_args
        expected_params = {
            "limit": 20,
            "offset": 10,
            "workflowId": "workflow_123"
        }
        assert kwargs["params"] == expected_params

    def test_get_logs_invalid_limit(self):
        """Test get_logs with invalid limit parameter"""
        client = VerifikClient(api_key="verifik_live_abc123")
        
        with pytest.raises(ValidationError, match="limit must be an integer between 1 and 100"):
            client.get_logs(limit=0)
        
        with pytest.raises(ValidationError, match="limit must be an integer between 1 and 100"):
            client.get_logs(limit=101)
        
        with pytest.raises(ValidationError, match="limit must be an integer between 1 and 100"):
            client.get_logs(limit="invalid")

    def test_get_logs_invalid_offset(self):
        """Test get_logs with invalid offset parameter"""
        client = VerifikClient(api_key="verifik_live_abc123")
        
        with pytest.raises(ValidationError, match="offset must be a non-negative integer"):
            client.get_logs(offset=-1)
        
        with pytest.raises(ValidationError, match="offset must be a non-negative integer"):
            client.get_logs(offset="invalid")

    @patch('verifikio.client.requests.Session.request')
    def test_verify_chain(self, mock_request):
        """Test verify_chain method"""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = {"isValid": True}
        mock_request.return_value = mock_response

        client = VerifikClient(api_key="verifik_live_abc123")
        result = client.verify_chain()

        assert result["isValid"] is True
        
        # Verify request
        args, kwargs = mock_request.call_args
        assert args[0] == "GET"
        assert "/api/v1/verify" in args[1]

    @patch('verifikio.client.requests.Session.request')
    def test_get_stats(self, mock_request):
        """Test get_stats method"""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = {"totalLogs": 100, "chainIntegrity": 100}
        mock_request.return_value = mock_response

        client = VerifikClient(api_key="verifik_live_abc123")
        result = client.get_stats()

        assert result["totalLogs"] == 100
        assert result["chainIntegrity"] == 100
        
        # Verify request
        args, kwargs = mock_request.call_args
        assert args[0] == "GET"
        assert "/api/v1/stats" in args[1]

    @patch('verifikio.client.requests.Session.request')
    def test_connection_error(self, mock_request):
        """Test handling of connection errors"""
        mock_request.side_effect = Exception("Connection failed")

        client = VerifikClient(api_key="verifik_live_abc123")
        
        with pytest.raises(VerifikError, match="Request failed"):
            client.log_event(agent_name="test_agent", action="test_action")

    @patch('verifikio.client.requests.Session.request')
    def test_timeout_error(self, mock_request):
        """Test handling of timeout errors"""
        import requests
        mock_request.side_effect = requests.exceptions.Timeout()

        client = VerifikClient(api_key="verifik_live_abc123")
        
        with pytest.raises(VerifikError, match="Request timed out"):
            client.log_event(agent_name="test_agent", action="test_action")

    @patch('verifikio.client.requests.Session.request')
    def test_invalid_json_response(self, mock_request):
        """Test handling of invalid JSON responses"""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_request.return_value = mock_response

        client = VerifikClient(api_key="verifik_live_abc123")
        
        with pytest.raises(APIError, match="Invalid JSON response"):
            client.log_event(agent_name="test_agent", action="test_action")

    def test_context_manager(self):
        """Test context manager support"""
        with VerifikClient(api_key="verifik_live_abc123") as client:
            assert client.api_key == "verifik_live_abc123"
            # Mock session close method
            client.session.close = Mock()
        
        # Verify session was closed
        client.session.close.assert_called_once()

    @patch('verifikio.client.requests.Session.request')
    def test_base_url_trailing_slash(self, mock_request):
        """Test that trailing slashes are handled correctly"""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "test"}
        mock_request.return_value = mock_response

        client = VerifikClient(
            api_key="verifik_live_abc123",
            base_url="https://api.example.com/"
        )
        
        # Base URL should have trailing slash removed
        assert client.base_url == "https://api.example.com"
        
        client.log_event(agent_name="test_agent", action="test_action")
        
        # Verify URL is constructed correctly
        args, kwargs = mock_request.call_args
        assert args[1] == "https://api.example.com/api/v1/logs"