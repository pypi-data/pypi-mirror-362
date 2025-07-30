"""
Unit tests for CrewAI integration.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime

from verifikio import VerifikClient
from verifikio.exceptions import VerifikError


class TestVerifikCrewAIHandler:
    """Test suite for VerifikCrewAIHandler."""
    
    @pytest.fixture
    def mock_client(self):
        """Create a mock VerifikClient."""
        client = Mock(spec=VerifikClient)
        client.log_event = Mock(return_value={"id": "test123", "hash": "abc123"})
        return client
    
    @pytest.fixture
    def mock_agent(self):
        """Create a mock CrewAI agent."""
        agent = Mock()
        agent.role = "Researcher"
        agent.goal = "Research AI trends"
        agent.backstory = "Expert researcher"
        return agent
    
    @pytest.fixture
    def mock_task(self):
        """Create a mock CrewAI task."""
        task = Mock()
        task.description = "Research GPT-4 capabilities"
        return task
    
    def test_import_error_without_crewai(self):
        """Test that ImportError is raised when CrewAI is not installed."""
        with patch('verifikio.integrations.crewai.CREWAI_AVAILABLE', False):
            from verifikio.integrations.crewai import VerifikCrewAIHandler
            
            client = Mock(spec=VerifikClient)
            with pytest.raises(ImportError, match="CrewAI is not installed"):
                VerifikCrewAIHandler(client)
    
    def test_handler_initialization(self, mock_client):
        """Test handler initialization with various parameters."""
        # Import here to ensure CREWAI_AVAILABLE is mocked properly
        with patch('verifikio.integrations.crewai.CREWAI_AVAILABLE', True):
            from verifikio.integrations.crewai import VerifikCrewAIHandler
            
            # Default initialization
            handler = VerifikCrewAIHandler(mock_client)
            assert handler.client == mock_client
            assert handler.log_errors is True
            assert handler.base_metadata == {}
            assert handler.workflow_id.startswith("crewai-")
            
            # Custom initialization
            handler = VerifikCrewAIHandler(
                mock_client,
                workflow_id="test-workflow",
                log_errors=False,
                metadata={"env": "test"}
            )
            assert handler.workflow_id == "test-workflow"
            assert handler.log_errors is False
            assert handler.base_metadata == {"env": "test"}
    
    def test_on_agent_action(self, mock_client, mock_agent):
        """Test logging agent actions."""
        with patch('verifikio.integrations.crewai.CREWAI_AVAILABLE', True):
            from verifikio.integrations.crewai import VerifikCrewAIHandler
            
            handler = VerifikCrewAIHandler(mock_client, workflow_id="test-123")
            
            # Test basic action
            handler.on_agent_action(
                mock_agent,
                "analyzing_data",
                inputs={"query": "test"},
                outputs={"result": "success"}
            )
            
            mock_client.log_event.assert_called_once()
            call_args = mock_client.log_event.call_args[1]
            
            assert call_args["agent_name"] == "crewai-Researcher"
            assert call_args["action"] == "analyzing_data"
            assert call_args["inputs"] == {"query": "test"}
            assert call_args["outputs"] == {"result": "success"}
            assert call_args["workflow_id"] == "test-123"
            assert call_args["status"] == "in_progress"
            assert call_args["metadata"]["agent_role"] == "Researcher"
            assert call_args["metadata"]["framework"] == "crewai"
            
            # Test with tool
            mock_client.reset_mock()
            handler.on_agent_action(
                mock_agent,
                "using_tool",
                tool="web_search",
                inputs={"query": "GPT-4"}
            )
            
            call_args = mock_client.log_event.call_args[1]
            assert call_args["metadata"]["tool_name"] == "web_search"
    
    def test_on_task_start(self, mock_client, mock_agent, mock_task):
        """Test logging task start events."""
        with patch('verifikio.integrations.crewai.CREWAI_AVAILABLE', True):
            from verifikio.integrations.crewai import VerifikCrewAIHandler
            
            handler = VerifikCrewAIHandler(mock_client)
            handler.on_task_start(mock_task, mock_agent)
            
            mock_client.log_event.assert_called_once()
            call_args = mock_client.log_event.call_args[1]
            
            assert call_args["agent_name"] == "crewai-Researcher"
            assert call_args["action"] == "task_started"
            assert call_args["inputs"]["task"] == "Research GPT-4 capabilities"
            assert call_args["status"] == "in_progress"
            assert call_args["metadata"]["task_description"] == "Research GPT-4 capabilities"
            
            # Verify context is stored
            task_id = id(mock_task)
            assert task_id in handler._task_context
            assert handler._task_context[task_id]["agent_role"] == "Researcher"
    
    def test_on_task_complete(self, mock_client, mock_agent, mock_task):
        """Test logging task completion events."""
        with patch('verifikio.integrations.crewai.CREWAI_AVAILABLE', True):
            from verifikio.integrations.crewai import VerifikCrewAIHandler
            
            handler = VerifikCrewAIHandler(mock_client)
            
            # Set up context
            task_id = id(mock_task)
            handler._task_context[task_id] = {
                "start_time": datetime.utcnow().isoformat(),
                "agent_role": "Researcher",
                "description": "Research GPT-4 capabilities"
            }
            
            # Complete task
            output = {"findings": ["GPT-4 is advanced", "Multimodal capabilities"]}
            handler.on_task_complete(mock_task, output)
            
            mock_client.log_event.assert_called_once()
            call_args = mock_client.log_event.call_args[1]
            
            assert call_args["agent_name"] == "crewai-Researcher"
            assert call_args["action"] == "task_completed"
            assert call_args["outputs"]["result"] == output
            assert call_args["status"] == "success"
            assert "duration" in call_args["metadata"]
            
            # Verify context is cleaned up
            assert task_id not in handler._task_context
    
    def test_on_task_error(self, mock_client, mock_agent, mock_task):
        """Test logging task error events."""
        with patch('verifikio.integrations.crewai.CREWAI_AVAILABLE', True):
            from verifikio.integrations.crewai import VerifikCrewAIHandler
            
            handler = VerifikCrewAIHandler(mock_client)
            
            # Set up context
            task_id = id(mock_task)
            handler._task_context[task_id] = {
                "start_time": datetime.utcnow().isoformat(),
                "agent_role": "Researcher"
            }
            
            # Task fails
            error = ValueError("API rate limit exceeded")
            handler.on_task_error(mock_task, error)
            
            mock_client.log_event.assert_called_once()
            call_args = mock_client.log_event.call_args[1]
            
            assert call_args["agent_name"] == "crewai-Researcher"
            assert call_args["action"] == "task_failed"
            assert call_args["outputs"]["error"] == "API rate limit exceeded"
            assert call_args["status"] == "error"
            assert call_args["metadata"]["error_type"] == "ValueError"
            
            # Verify context is cleaned up
            assert task_id not in handler._task_context
    
    def test_on_crew_complete(self, mock_client):
        """Test logging crew completion events."""
        with patch('verifikio.integrations.crewai.CREWAI_AVAILABLE', True):
            from verifikio.integrations.crewai import VerifikCrewAIHandler
            
            handler = VerifikCrewAIHandler(mock_client)
            
            results = ["Result 1", "Result 2", "Result 3"]
            handler.on_crew_complete(results)
            
            mock_client.log_event.assert_called_once()
            call_args = mock_client.log_event.call_args[1]
            
            assert call_args["agent_name"] == "crewai-crew"
            assert call_args["action"] == "crew_completed"
            assert call_args["outputs"]["results_count"] == 3
            assert call_args["status"] == "success"
            assert call_args["metadata"]["task_count"] == 3
    
    def test_error_handling(self, mock_client, mock_agent):
        """Test error handling in callbacks."""
        with patch('verifikio.integrations.crewai.CREWAI_AVAILABLE', True):
            from verifikio.integrations.crewai import VerifikCrewAIHandler
            
            handler = VerifikCrewAIHandler(mock_client)
            
            # Simulate error in log_event
            mock_client.log_event.side_effect = [Exception("Network error"), None]
            
            # Should not raise exception
            handler.on_agent_action(mock_agent, "test_action")
            
            # Should have logged the error
            assert mock_client.log_event.call_count == 2
            error_call = mock_client.log_event.call_args_list[1][1]
            assert error_call["agent_name"] == "crewai-handler"
            assert error_call["action"] == "error"
            assert "Network error" in error_call["outputs"]["error"]
    
    def test_serialize_output(self, mock_client):
        """Test output serialization."""
        with patch('verifikio.integrations.crewai.CREWAI_AVAILABLE', True):
            from verifikio.integrations.crewai import VerifikCrewAIHandler
            
            handler = VerifikCrewAIHandler(mock_client)
            
            # Test various data types
            assert handler._serialize_output("string") == "string"
            assert handler._serialize_output(123) == 123
            assert handler._serialize_output(True) == True
            assert handler._serialize_output(None) is None
            assert handler._serialize_output([1, 2, 3]) == [1, 2, 3]
            assert handler._serialize_output({"key": "value"}) == {"key": "value"}
            
            # Test non-serializable object
            class CustomObject:
                def __str__(self):
                    return "custom_object"
            
            assert handler._serialize_output(CustomObject()) == "custom_object"
    
    def test_calculate_duration(self, mock_client):
        """Test duration calculation."""
        with patch('verifikio.integrations.crewai.CREWAI_AVAILABLE', True):
            from verifikio.integrations.crewai import VerifikCrewAIHandler
            
            handler = VerifikCrewAIHandler(mock_client)
            
            # Test with valid timestamp
            past_time = "2024-01-01T12:00:00"
            with patch('verifikio.integrations.crewai.datetime') as mock_datetime:
                mock_datetime.utcnow.return_value = datetime(2024, 1, 1, 12, 0, 10)
                mock_datetime.fromisoformat = datetime.fromisoformat
                
                duration = handler._calculate_duration(past_time)
                assert duration == 10.0
            
            # Test with None
            assert handler._calculate_duration(None) is None
            
            # Test with invalid timestamp
            assert handler._calculate_duration("invalid") is None