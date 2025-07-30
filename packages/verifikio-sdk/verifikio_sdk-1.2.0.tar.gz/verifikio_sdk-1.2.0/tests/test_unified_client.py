"""
Unit tests for the unified VerifikClient with async_mode support
"""

import json
import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock, MagicMock

from verifikio import VerifikClient
from verifikio.exceptions import AuthenticationError, ValidationError, APIError, VerifikError


class TestUnifiedVerifikClient:
    """Test suite for unified VerifikClient with async_mode"""
    
    def test_init_sync_mode(self):
        """Test client initialization in sync mode"""
        client = VerifikClient(api_key="verifik_live_test123")
        assert client.api_key == "verifik_live_test123"
        assert client.base_url == "https://api.verifik.io/v1"
        assert client.async_mode is False
        assert client.timeout == 30
        
    def test_init_async_mode(self):
        """Test client initialization in async mode"""
        client = VerifikClient(api_key="verifik_live_test123", async_mode=True)
        assert client.api_key == "verifik_live_test123"
        assert client.async_mode is True
        assert client._session is None  # Session created on first use
        
    def test_init_custom_params(self):
        """Test client initialization with custom parameters"""
        client = VerifikClient(
            api_key="verifik_live_test123",
            base_url="https://custom.api.com",
            timeout=60,
            async_mode=True
        )
        assert client.base_url == "https://custom.api.com"
        assert client.timeout == 60
        assert client.async_mode is True
        
    def test_context_manager_sync(self):
        """Test context manager in sync mode"""
        with VerifikClient(api_key="verifik_live_test123") as client:
            assert client.api_key == "verifik_live_test123"
            assert client.async_mode is False
            
    async def test_context_manager_async(self):
        """Test context manager in async mode"""
        async with VerifikClient(api_key="verifik_live_test123", async_mode=True) as client:
            assert client.api_key == "verifik_live_test123"
            assert client.async_mode is True
            
    def test_context_manager_wrong_mode_sync(self):
        """Test using async context manager with sync client"""
        client = VerifikClient(api_key="verifik_live_test123", async_mode=False)
        with pytest.raises(RuntimeError, match="Use 'with' for sync mode"):
            asyncio.run(client.__aenter__())
            
    def test_context_manager_wrong_mode_async(self):
        """Test using sync context manager with async client"""
        client = VerifikClient(api_key="verifik_live_test123", async_mode=True)
        with pytest.raises(RuntimeError, match="Use 'async with' for async mode"):
            client.__enter__()
            
    @patch('requests.Session')
    def test_log_event_sync(self, mock_session_class):
        """Test log_event in sync mode"""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "log123", "status": "success"}
        
        # Mock session
        mock_session = Mock()
        mock_session.request.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        client = VerifikClient(api_key="verifik_live_test123")
        response = client.log_event(
            agent_name="test-agent",
            action="test-action"
        )
        
        assert response == {"id": "log123", "status": "success"}
        mock_session.request.assert_called_once()
        
    @pytest.mark.asyncio
    async def test_log_event_async(self):
        """Test log_event in async mode"""
        client = VerifikClient(api_key="verifik_live_test123", async_mode=True)
        
        # Mock aiohttp session
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(return_value='{"id": "log123", "status": "success"}')
        
        mock_session = AsyncMock()
        mock_session.request.return_value.__aenter__.return_value = mock_response
        mock_session.closed = False
        
        with patch('aiohttp.ClientSession', return_value=mock_session):
            response = await client.log_event(
                agent_name="test-agent",
                action="test-action"
            )
            
        assert response == {"id": "log123", "status": "success"}
        
    @patch('requests.Session')
    def test_log_batch_sync(self, mock_session_class):
        """Test log_batch in sync mode"""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"id": "log1", "status": "success"},
            {"id": "log2", "status": "success"}
        ]
        
        # Mock session
        mock_session = Mock()
        mock_session.request.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        client = VerifikClient(api_key="verifik_live_test123")
        batch = [
            {"agent_name": "agent1", "action": "action1"},
            {"agent_name": "agent2", "action": "action2"}
        ]
        response = client.log_batch(batch)
        
        assert len(response) == 2
        assert response[0]["id"] == "log1"
        assert response[1]["id"] == "log2"
        
        # Verify the request was made with the batch data
        mock_session.request.assert_called_once()
        call_args = mock_session.request.call_args
        assert call_args[1]["json"] == batch
        
    @pytest.mark.asyncio
    async def test_log_batch_async(self):
        """Test log_batch in async mode"""
        client = VerifikClient(api_key="verifik_live_test123", async_mode=True)
        
        # Mock aiohttp session
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(return_value='[{"id": "log1"}, {"id": "log2"}]')
        
        mock_session = AsyncMock()
        mock_session.request.return_value.__aenter__.return_value = mock_response
        mock_session.closed = False
        
        with patch('aiohttp.ClientSession', return_value=mock_session):
            batch = [
                {"agent_name": "agent1", "action": "action1"},
                {"agent_name": "agent2", "action": "action2"}
            ]
            response = await client.log_batch(batch)
            
        assert len(response) == 2
        assert response[0]["id"] == "log1"
        assert response[1]["id"] == "log2"
        
    def test_log_batch_validation(self):
        """Test log_batch validation"""
        client = VerifikClient(api_key="verifik_live_test123")
        
        # Test invalid type
        with pytest.raises(ValidationError, match="events must be a list"):
            client.log_batch("not-a-list")
            
        # Test empty list
        with pytest.raises(ValidationError, match="events list cannot be empty"):
            client.log_batch([])
            
        # Test invalid event type
        with pytest.raises(ValidationError, match="Event at index 0 must be a dictionary"):
            client.log_batch(["not-a-dict"])
            
        # Test missing required field
        with pytest.raises(ValidationError, match="missing required field: agent_name"):
            client.log_batch([{"action": "test"}])
            
        # Test invalid field type
        with pytest.raises(ValidationError, match="agent_name must be a string"):
            client.log_batch([{"agent_name": 123, "action": "test"}])
            
    @pytest.mark.asyncio
    async def test_async_methods_return_coroutines(self):
        """Test that all methods return coroutines in async mode"""
        client = VerifikClient(api_key="verifik_live_test123", async_mode=True)
        
        # Test log_event returns coroutine
        coro = client.log_event("agent", "action")
        assert asyncio.iscoroutine(coro)
        coro.close()
        
        # Test log_batch returns coroutine
        coro = client.log_batch([{"agent_name": "agent", "action": "action"}])
        assert asyncio.iscoroutine(coro)
        coro.close()
        
        # Test get_logs returns coroutine
        coro = client.get_logs()
        assert asyncio.iscoroutine(coro)
        coro.close()
        
        # Test verify_chain returns coroutine
        coro = client.verify_chain()
        assert asyncio.iscoroutine(coro)
        coro.close()
        
        # Test get_stats returns coroutine
        coro = client.get_stats()
        assert asyncio.iscoroutine(coro)
        coro.close()
        
    def test_sync_methods_return_values(self):
        """Test that all methods return values directly in sync mode"""
        client = VerifikClient(api_key="verifik_live_test123")
        
        with patch.object(client, '_sync_request', return_value={"result": "test"}):
            # Test log_event returns value
            result = client.log_event("agent", "action")
            assert result == {"result": "test"}
            assert not asyncio.iscoroutine(result)
            
            # Test log_batch returns value
            result = client.log_batch([{"agent_name": "agent", "action": "action"}])
            assert result == {"result": "test"}
            assert not asyncio.iscoroutine(result)
            
    @pytest.mark.asyncio
    async def test_no_aiohttp_error(self):
        """Test error when aiohttp is not installed"""
        client = VerifikClient(api_key="verifik_live_test123", async_mode=True)
        
        with patch.dict('sys.modules', {'aiohttp': None}):
            with pytest.raises(ImportError, match="aiohttp is required for async mode"):
                await client._ensure_async_session()
                
    @pytest.mark.asyncio
    async def test_session_reuse(self):
        """Test that async session is reused across requests"""
        client = VerifikClient(api_key="verifik_live_test123", async_mode=True)
        
        mock_session = AsyncMock()
        mock_session.closed = False
        
        with patch('aiohttp.ClientSession', return_value=mock_session) as mock_class:
            await client._ensure_async_session()
            session1 = client._session
            
            await client._ensure_async_session()
            session2 = client._session
            
            # Should reuse same session
            assert session1 is session2
            # Should only create one session
            mock_class.assert_called_once()
            
    @pytest.mark.asyncio
    async def test_close_async(self):
        """Test closing async client"""
        client = VerifikClient(api_key="verifik_live_test123", async_mode=True)
        
        mock_session = AsyncMock()
        mock_session.closed = False
        client._session = mock_session
        
        await client.close()
        mock_session.close.assert_called_once()
        
    def test_close_sync(self):
        """Test closing sync client"""
        client = VerifikClient(api_key="verifik_live_test123")
        
        mock_session = Mock()
        client._session = mock_session
        
        client.close()
        mock_session.close.assert_called_once()