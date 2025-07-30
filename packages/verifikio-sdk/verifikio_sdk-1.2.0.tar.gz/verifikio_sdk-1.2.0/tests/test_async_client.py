"""
Unit tests for the AsyncVerifikClient
"""

import pytest
import json
from unittest.mock import AsyncMock, Mock, patch
from verifikio.async_client import AsyncVerifikClient
from verifikio.exceptions import AuthenticationError, ValidationError, APIError


class TestAsyncVerifikClient:
    """Test suite for AsyncVerifikClient class"""
    
    @pytest.fixture
    def client(self):
        """Create a test client instance"""
        return AsyncVerifikClient(api_key="verifik_test_key")
    
    @pytest.mark.asyncio
    async def test_init_valid_api_key(self):
        """Test client initialization with valid API key"""
        client = AsyncVerifikClient(api_key="verifik_test_key")
        assert client.api_key == "verifik_test_key"
        assert client.base_url == "https://api.verifik.io/v1"
        assert client._session is None
        
    @pytest.mark.asyncio
    async def test_init_custom_base_url(self):
        """Test client initialization with custom base URL"""
        client = AsyncVerifikClient(
            api_key="verifik_test_key",
            base_url="http://localhost:5000/api/v1"
        )
        assert client.base_url == "http://localhost:5000/api/v1"
        
    def test_init_empty_api_key(self):
        """Test client initialization with empty API key"""
        with pytest.raises(ValueError, match="API key is required"):
            AsyncVerifikClient(api_key="")
            
    def test_init_invalid_api_key_format(self):
        """Test client initialization with invalid API key format"""
        with pytest.raises(ValueError, match="Invalid API key format"):
            AsyncVerifikClient(api_key="invalid_key")
            
    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test context manager functionality"""
        async with AsyncVerifikClient(api_key="verifik_test_key") as client:
            assert client is not None
            # Session should be created when needed
            
    @pytest.mark.asyncio
    async def test_log_event_async_minimal(self, client):
        """Test log_event_async with minimal parameters"""
        mock_response = AsyncMock()
        mock_response.status = 201
        mock_response.text = AsyncMock(return_value=json.dumps({
            "id": 123,
            "agent_name": "test-agent",
            "action": "test-action"
        }))
        
        with patch('aiohttp.ClientSession.request', return_value=mock_response):
            result = await client.log_event_async(
                agent_name="test-agent",
                action="test-action"
            )
            
            assert result["id"] == 123
            assert result["agent_name"] == "test-agent"
            assert result["action"] == "test-action"
            
    @pytest.mark.asyncio
    async def test_log_event_async_full_parameters(self, client):
        """Test log_event_async with all parameters"""
        mock_response = AsyncMock()
        mock_response.status = 201
        mock_response.text = AsyncMock(return_value=json.dumps({
            "id": 123,
            "agent_name": "test-agent",
            "action": "test-action",
            "inputs": {"data": "test"},
            "outputs": {"result": "success"},
            "metadata": {"version": "1.0"},
            "workflow_id": "wf-123",
            "status": "success"
        }))
        
        with patch('aiohttp.ClientSession.request', return_value=mock_response):
            result = await client.log_event_async(
                agent_name="test-agent",
                action="test-action",
                inputs={"data": "test"},
                outputs={"result": "success"},
                metadata={"version": "1.0"},
                workflow_id="wf-123",
                status="success"
            )
            
            assert result["status"] == "success"
            assert result["workflow_id"] == "wf-123"
            
    @pytest.mark.asyncio
    async def test_log_event_async_invalid_agent_name(self, client):
        """Test log_event_async with invalid agent_name"""
        with pytest.raises(ValidationError, match="agent_name is required"):
            await client.log_event_async(agent_name="", action="test")
            
    @pytest.mark.asyncio
    async def test_log_event_async_invalid_inputs(self, client):
        """Test log_event_async with invalid inputs"""
        with pytest.raises(ValidationError, match="inputs must be a dictionary"):
            await client.log_event_async(
                agent_name="test",
                action="test",
                inputs="invalid"
            )
            
    @pytest.mark.asyncio
    async def test_log_events_async_single_event(self, client):
        """Test log_events_async with single event"""
        mock_response = AsyncMock()
        mock_response.status = 201
        mock_response.text = AsyncMock(return_value=json.dumps({
            "logs": [{"id": 1, "agent_name": "agent1", "action": "action1"}],
            "count": 1
        }))
        
        with patch('aiohttp.ClientSession.request', return_value=mock_response):
            events = [{"agent_name": "agent1", "action": "action1"}]
            result = await client.log_events_async(events)
            
            assert "logs" in result
            assert result["count"] == 1
            
    @pytest.mark.asyncio
    async def test_log_events_async_multiple_events(self, client):
        """Test log_events_async with multiple events"""
        mock_response = AsyncMock()
        mock_response.status = 201
        mock_response.text = AsyncMock(return_value=json.dumps({
            "logs": [
                {"id": 1, "agent_name": "agent1", "action": "action1"},
                {"id": 2, "agent_name": "agent2", "action": "action2"},
                {"id": 3, "agent_name": "agent3", "action": "action3"}
            ],
            "count": 3
        }))
        
        with patch('aiohttp.ClientSession.request', return_value=mock_response):
            events = [
                {"agent_name": "agent1", "action": "action1"},
                {"agent_name": "agent2", "action": "action2"},
                {"agent_name": "agent3", "action": "action3"}
            ]
            result = await client.log_events_async(events)
            
            assert "logs" in result
            assert result["count"] == 3
            assert len(result["logs"]) == 3
            
    @pytest.mark.asyncio
    async def test_log_events_async_invalid_events_type(self, client):
        """Test log_events_async with invalid events type"""
        with pytest.raises(ValidationError, match="events must be a list"):
            await client.log_events_async("invalid")
            
    @pytest.mark.asyncio
    async def test_log_events_async_empty_list(self, client):
        """Test log_events_async with empty list"""
        with pytest.raises(ValidationError, match="events list cannot be empty"):
            await client.log_events_async([])
            
    @pytest.mark.asyncio
    async def test_log_events_async_missing_required_field(self, client):
        """Test log_events_async with event missing required field"""
        with pytest.raises(ValidationError, match="missing required field: agent_name"):
            await client.log_events_async([{"action": "test"}])
            
    @pytest.mark.asyncio
    async def test_log_events_async_invalid_field_type(self, client):
        """Test log_events_async with invalid field type"""
        with pytest.raises(ValidationError, match="agent_name must be a string"):
            await client.log_events_async([{"agent_name": 123, "action": "test"}])
            
    @pytest.mark.asyncio
    async def test_get_logs_async(self, client):
        """Test get_logs_async method"""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(return_value=json.dumps({
            "logs": [{"id": 1}, {"id": 2}],
            "total": 2,
            "limit": 50,
            "offset": 0
        }))
        
        with patch('aiohttp.ClientSession.request', return_value=mock_response):
            result = await client.get_logs_async()
            
            assert "logs" in result
            assert result["total"] == 2
            
    @pytest.mark.asyncio
    async def test_verify_chain_async(self, client):
        """Test verify_chain_async method"""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(return_value=json.dumps({
            "isValid": True,
            "lastVerifiedHash": "abc123"
        }))
        
        with patch('aiohttp.ClientSession.request', return_value=mock_response):
            result = await client.verify_chain_async()
            
            assert result["isValid"] is True
            assert result["lastVerifiedHash"] == "abc123"
            
    @pytest.mark.asyncio
    async def test_get_stats_async(self, client):
        """Test get_stats_async method"""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(return_value=json.dumps({
            "totalLogs": 150,
            "chainIntegrity": 100
        }))
        
        with patch('aiohttp.ClientSession.request', return_value=mock_response):
            result = await client.get_stats_async()
            
            assert result["totalLogs"] == 150
            assert result["chainIntegrity"] == 100
            
    @pytest.mark.asyncio
    async def test_authentication_error(self, client):
        """Test handling of 401 authentication error"""
        mock_response = AsyncMock()
        mock_response.status = 401
        mock_response.text = AsyncMock(return_value=json.dumps({
            "message": "Invalid API key"
        }))
        
        with patch('aiohttp.ClientSession.request', return_value=mock_response):
            with pytest.raises(AuthenticationError, match="Invalid API key"):
                await client.log_event_async(
                    agent_name="test",
                    action="test"
                )
                
    @pytest.mark.asyncio
    async def test_validation_error_from_api(self, client):
        """Test handling of 400 validation error from API"""
        mock_response = AsyncMock()
        mock_response.status = 400
        mock_response.text = AsyncMock(return_value=json.dumps({
            "message": "Invalid request data"
        }))
        
        with patch('aiohttp.ClientSession.request', return_value=mock_response):
            with pytest.raises(ValidationError, match="Invalid request data"):
                await client.log_event_async(
                    agent_name="test",
                    action="test"
                )
                
    @pytest.mark.asyncio
    async def test_rate_limit_error(self, client):
        """Test handling of 429 rate limit error"""
        mock_response = AsyncMock()
        mock_response.status = 429
        mock_response.text = AsyncMock(return_value=json.dumps({
            "message": "Rate limit exceeded"
        }))
        
        with patch('aiohttp.ClientSession.request', return_value=mock_response):
            with pytest.raises(APIError, match="Rate limit exceeded"):
                await client.log_event_async(
                    agent_name="test",
                    action="test"
                )
                
    @pytest.mark.asyncio
    async def test_server_error(self, client):
        """Test handling of 500 server error"""
        mock_response = AsyncMock()
        mock_response.status = 500
        mock_response.text = AsyncMock(return_value=json.dumps({
            "message": "Internal server error"
        }))
        
        with patch('aiohttp.ClientSession.request', return_value=mock_response):
            with pytest.raises(APIError, match="Server error: 500"):
                await client.log_event_async(
                    agent_name="test",
                    action="test"
                )
                
    @pytest.mark.asyncio
    async def test_no_aiohttp_installed(self):
        """Test error when aiohttp is not installed"""
        with patch.dict('sys.modules', {'aiohttp': None}):
            client = AsyncVerifikClient(api_key="verifik_test_key")
            with pytest.raises(ImportError, match="aiohttp is required"):
                await client.log_event_async(
                    agent_name="test",
                    action="test"
                )
                
    @pytest.mark.asyncio
    async def test_session_closure(self, client):
        """Test that session is properly closed"""
        mock_session = AsyncMock()
        mock_session.closed = False
        client._session = mock_session
        
        await client.close()
        mock_session.close.assert_called_once()