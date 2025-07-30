"""
Unit tests for LangChain integration.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
from uuid import UUID

from verifikio import VerifikClient
from verifikio.exceptions import VerifikError


class TestVerifikLangChainHandler:
    """Test suite for VerifikLangChainHandler."""
    
    @pytest.fixture
    def mock_client(self):
        """Create a mock VerifikClient."""
        client = Mock(spec=VerifikClient)
        client.log_event = Mock(return_value={"id": "test123", "hash": "abc123"})
        return client
    
    @pytest.fixture
    def test_run_id(self):
        """Create a test run ID."""
        return UUID("12345678-1234-5678-1234-567812345678")
    
    @pytest.fixture
    def test_parent_run_id(self):
        """Create a test parent run ID."""
        return UUID("87654321-4321-8765-4321-876543218765")
    
    def test_import_error_without_langchain(self):
        """Test that ImportError is raised when LangChain is not installed."""
        with patch('verifikio.integrations.langchain.LANGCHAIN_AVAILABLE', False):
            from verifikio.integrations.langchain import VerifikLangChainHandler
            
            client = Mock(spec=VerifikClient)
            with pytest.raises(ImportError, match="LangChain is not installed"):
                VerifikLangChainHandler(client)
    
    def test_handler_initialization(self, mock_client):
        """Test handler initialization with various parameters."""
        with patch('verifikio.integrations.langchain.LANGCHAIN_AVAILABLE', True):
            from verifikio.integrations.langchain import VerifikLangChainHandler
            
            # Default initialization
            handler = VerifikLangChainHandler(mock_client)
            assert handler.client == mock_client
            assert handler.log_errors is True
            assert handler.log_llm_calls is True
            assert handler.base_metadata == {}
            assert handler.workflow_id.startswith("langchain-")
            
            # Custom initialization
            handler = VerifikLangChainHandler(
                mock_client,
                workflow_id="test-workflow",
                log_errors=False,
                log_llm_calls=False,
                metadata={"env": "test"}
            )
            assert handler.workflow_id == "test-workflow"
            assert handler.log_errors is False
            assert handler.log_llm_calls is False
            assert handler.base_metadata == {"env": "test"}
    
    def test_on_chain_start(self, mock_client, test_run_id, test_parent_run_id):
        """Test logging chain start events."""
        with patch('verifikio.integrations.langchain.LANGCHAIN_AVAILABLE', True):
            from verifikio.integrations.langchain import VerifikLangChainHandler
            
            handler = VerifikLangChainHandler(mock_client, workflow_id="test-123")
            
            serialized = {"name": "LLMChain", "type": "chain"}
            inputs = {"prompt": "What is AI?", "context": "Technology"}
            
            handler.on_chain_start(
                serialized,
                inputs,
                run_id=test_run_id,
                parent_run_id=test_parent_run_id
            )
            
            mock_client.log_event.assert_called_once()
            call_args = mock_client.log_event.call_args[1]
            
            assert call_args["agent_name"] == "langchain-LLMChain"
            assert call_args["action"] == "chain_started"
            assert call_args["inputs"] == inputs
            assert call_args["workflow_id"] == "test-123"
            assert call_args["status"] == "in_progress"
            assert call_args["metadata"]["chain_type"] == "LLMChain"
            assert call_args["metadata"]["run_id"] == str(test_run_id)
            assert call_args["metadata"]["parent_run_id"] == str(test_parent_run_id)
            
            # Verify context is stored
            assert test_run_id in handler._run_context
    
    def test_on_chain_end(self, mock_client, test_run_id):
        """Test logging chain end events."""
        with patch('verifikio.integrations.langchain.LANGCHAIN_AVAILABLE', True):
            from verifikio.integrations.langchain import VerifikLangChainHandler
            
            handler = VerifikLangChainHandler(mock_client)
            
            # Set up context
            handler._run_context[test_run_id] = {
                "start_time": datetime.utcnow().isoformat(),
                "chain_type": "LLMChain"
            }
            
            outputs = {"text": "AI is artificial intelligence"}
            handler.on_chain_end(outputs, run_id=test_run_id)
            
            mock_client.log_event.assert_called_once()
            call_args = mock_client.log_event.call_args[1]
            
            assert call_args["agent_name"] == "langchain-LLMChain"
            assert call_args["action"] == "chain_completed"
            assert call_args["outputs"] == outputs
            assert call_args["status"] == "success"
            assert "duration" in call_args["metadata"]
            
            # Verify context is cleaned up
            assert test_run_id not in handler._run_context
    
    def test_on_chain_error(self, mock_client, test_run_id):
        """Test logging chain error events."""
        with patch('verifikio.integrations.langchain.LANGCHAIN_AVAILABLE', True):
            from verifikio.integrations.langchain import VerifikLangChainHandler
            
            handler = VerifikLangChainHandler(mock_client)
            
            # Set up context
            handler._run_context[test_run_id] = {
                "start_time": datetime.utcnow().isoformat(),
                "chain_type": "LLMChain"
            }
            
            error = ValueError("Invalid prompt format")
            handler.on_chain_error(error, run_id=test_run_id)
            
            mock_client.log_event.assert_called_once()
            call_args = mock_client.log_event.call_args[1]
            
            assert call_args["agent_name"] == "langchain-LLMChain"
            assert call_args["action"] == "chain_failed"
            assert call_args["outputs"]["error"] == "Invalid prompt format"
            assert call_args["status"] == "error"
            assert call_args["metadata"]["error_type"] == "ValueError"
            
            # Verify context is cleaned up
            assert test_run_id not in handler._run_context
    
    def test_on_tool_start(self, mock_client, test_run_id):
        """Test logging tool start events."""
        with patch('verifikio.integrations.langchain.LANGCHAIN_AVAILABLE', True):
            from verifikio.integrations.langchain import VerifikLangChainHandler
            
            handler = VerifikLangChainHandler(mock_client)
            
            serialized = {"name": "WebSearch", "type": "tool"}
            input_str = "search for GPT-4 capabilities"
            
            handler.on_tool_start(serialized, input_str, run_id=test_run_id)
            
            mock_client.log_event.assert_called_once()
            call_args = mock_client.log_event.call_args[1]
            
            assert call_args["agent_name"] == "langchain-tool-WebSearch"
            assert call_args["action"] == "tool_started"
            assert call_args["inputs"]["input"] == input_str
            assert call_args["status"] == "in_progress"
            assert call_args["metadata"]["tool_name"] == "WebSearch"
    
    def test_on_tool_end(self, mock_client, test_run_id):
        """Test logging tool end events."""
        with patch('verifikio.integrations.langchain.LANGCHAIN_AVAILABLE', True):
            from verifikio.integrations.langchain import VerifikLangChainHandler
            
            handler = VerifikLangChainHandler(mock_client)
            
            output = "Found 10 results about GPT-4"
            handler.on_tool_end(output, run_id=test_run_id)
            
            mock_client.log_event.assert_called_once()
            call_args = mock_client.log_event.call_args[1]
            
            assert call_args["agent_name"] == "langchain-tool"
            assert call_args["action"] == "tool_completed"
            assert call_args["outputs"]["output"] == output
            assert call_args["status"] == "success"
    
    def test_on_tool_error(self, mock_client, test_run_id):
        """Test logging tool error events."""
        with patch('verifikio.integrations.langchain.LANGCHAIN_AVAILABLE', True):
            from verifikio.integrations.langchain import VerifikLangChainHandler
            
            handler = VerifikLangChainHandler(mock_client)
            
            error = ConnectionError("Network timeout")
            handler.on_tool_error(error, run_id=test_run_id)
            
            mock_client.log_event.assert_called_once()
            call_args = mock_client.log_event.call_args[1]
            
            assert call_args["agent_name"] == "langchain-tool"
            assert call_args["action"] == "tool_failed"
            assert call_args["outputs"]["error"] == "Network timeout"
            assert call_args["status"] == "error"
            assert call_args["metadata"]["error_type"] == "ConnectionError"
    
    def test_on_llm_start(self, mock_client, test_run_id):
        """Test logging LLM start events."""
        with patch('verifikio.integrations.langchain.LANGCHAIN_AVAILABLE', True):
            from verifikio.integrations.langchain import VerifikLangChainHandler
            
            handler = VerifikLangChainHandler(mock_client)
            
            serialized = {"name": "OpenAI", "type": "llm"}
            prompts = ["What is AI?", "Explain machine learning"]
            
            handler.on_llm_start(serialized, prompts, run_id=test_run_id)
            
            mock_client.log_event.assert_called_once()
            call_args = mock_client.log_event.call_args[1]
            
            assert call_args["agent_name"] == "langchain-llm-OpenAI"
            assert call_args["action"] == "llm_started"
            assert call_args["inputs"]["prompt"] == "What is AI?"
            assert call_args["inputs"]["additional_prompts"] == 1
            assert call_args["metadata"]["prompt_count"] == 2
            
            # Test with log_llm_calls=False
            handler.log_llm_calls = False
            mock_client.reset_mock()
            handler.on_llm_start(serialized, prompts, run_id=test_run_id)
            mock_client.log_event.assert_not_called()
    
    def test_on_llm_end(self, mock_client, test_run_id):
        """Test logging LLM end events."""
        with patch('verifikio.integrations.langchain.LANGCHAIN_AVAILABLE', True):
            from verifikio.integrations.langchain import VerifikLangChainHandler
            
            handler = VerifikLangChainHandler(mock_client)
            
            # Create mock LLMResult
            mock_generation = Mock()
            mock_generation.text = "AI is artificial intelligence that can learn and adapt"
            
            mock_result = Mock()
            mock_result.generations = [[mock_generation]]
            mock_result.llm_output = {
                "token_usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 20,
                    "total_tokens": 30
                }
            }
            
            handler.on_llm_end(mock_result, run_id=test_run_id)
            
            mock_client.log_event.assert_called_once()
            call_args = mock_client.log_event.call_args[1]
            
            assert call_args["agent_name"] == "langchain-llm"
            assert call_args["action"] == "llm_completed"
            assert "AI is artificial intelligence" in call_args["outputs"]["response"]
            assert call_args["metadata"]["token_usage"]["total_tokens"] == 30
    
    def test_on_agent_action(self, mock_client, test_run_id):
        """Test logging agent action events."""
        with patch('verifikio.integrations.langchain.LANGCHAIN_AVAILABLE', True):
            from verifikio.integrations.langchain import VerifikLangChainHandler
            
            handler = VerifikLangChainHandler(mock_client)
            
            # Create mock AgentAction
            mock_action = Mock()
            mock_action.tool = "Calculator"
            mock_action.tool_input = "2 + 2"
            mock_action.log = "Using calculator to compute 2 + 2"
            
            handler.on_agent_action(mock_action, run_id=test_run_id)
            
            mock_client.log_event.assert_called_once()
            call_args = mock_client.log_event.call_args[1]
            
            assert call_args["agent_name"] == "langchain-agent"
            assert call_args["action"] == "agent_action_Calculator"
            assert call_args["inputs"]["tool"] == "Calculator"
            assert call_args["inputs"]["tool_input"] == "2 + 2"
            assert call_args["outputs"]["log"] == "Using calculator to compute 2 + 2"
    
    def test_on_agent_finish(self, mock_client, test_run_id):
        """Test logging agent finish events."""
        with patch('verifikio.integrations.langchain.LANGCHAIN_AVAILABLE', True):
            from verifikio.integrations.langchain import VerifikLangChainHandler
            
            handler = VerifikLangChainHandler(mock_client)
            
            # Create mock AgentFinish
            mock_finish = Mock()
            mock_finish.return_values = {"output": "The answer is 4"}
            mock_finish.log = "Calculation complete"
            
            handler.on_agent_finish(mock_finish, run_id=test_run_id)
            
            mock_client.log_event.assert_called_once()
            call_args = mock_client.log_event.call_args[1]
            
            assert call_args["agent_name"] == "langchain-agent"
            assert call_args["action"] == "agent_finished"
            assert call_args["outputs"]["return_values"] == {"output": "The answer is 4"}
            assert call_args["outputs"]["log"] == "Calculation complete"
    
    def test_truncate_data(self, mock_client):
        """Test data truncation."""
        with patch('verifikio.integrations.langchain.LANGCHAIN_AVAILABLE', True):
            from verifikio.integrations.langchain import VerifikLangChainHandler
            
            handler = VerifikLangChainHandler(mock_client)
            
            # Test string truncation
            long_string = "a" * 2000
            assert len(handler._truncate_data(long_string, 100)) == 100
            
            # Test dict truncation
            data = {"key1": "a" * 100, "key2": "b" * 100}
            truncated = handler._truncate_data(data, 100)
            assert len(str(truncated["key1"])) <= 50
            assert len(str(truncated["key2"])) <= 50
            
            # Test list truncation
            long_list = list(range(20))
            truncated = handler._truncate_data(long_list, 100)
            assert len(truncated) == 10
    
    def test_error_handling(self, mock_client, test_run_id):
        """Test error handling in callbacks."""
        with patch('verifikio.integrations.langchain.LANGCHAIN_AVAILABLE', True):
            from verifikio.integrations.langchain import VerifikLangChainHandler
            
            handler = VerifikLangChainHandler(mock_client)
            
            # Simulate error in log_event
            mock_client.log_event.side_effect = [Exception("API error"), None]
            
            # Should not raise exception
            handler.on_chain_start(
                {"name": "TestChain"},
                {"input": "test"},
                run_id=test_run_id
            )
            
            # Should have logged the error
            assert mock_client.log_event.call_count == 2
            error_call = mock_client.log_event.call_args_list[1][1]
            assert error_call["agent_name"] == "langchain-handler"
            assert error_call["action"] == "error"
            assert "API error" in error_call["outputs"]["error"]