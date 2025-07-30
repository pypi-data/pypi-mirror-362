"""
LangChain Integration for Verifik.io SDK

This module provides a callback handler for LangChain that automatically
logs chain executions, tool usage, and errors to Verifik.io.
"""

from typing import Any, Dict, List, Optional, Union
from uuid import UUID
import json
from datetime import datetime

try:
    from langchain.callbacks.base import BaseCallbackHandler
    from langchain.schema import AgentAction, AgentFinish, LLMResult
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    BaseCallbackHandler = object
    AgentAction = Any
    AgentFinish = Any
    LLMResult = Any

from ..client import VerifikClient
from ..exceptions import VerifikError


class VerifikLangChainHandler(BaseCallbackHandler):
    """
    Callback handler for LangChain that logs events to Verifik.io.
    
    This handler extends LangChain's BaseCallbackHandler to automatically
    log chain executions, tool usage, LLM calls, and errors to Verifik.io's
    audit trail.
    
    Example:
        >>> from verifikio import VerifikClient
        >>> from verifikio.integrations.langchain import VerifikLangChainHandler
        >>> from langchain.chains import LLMChain
        >>> from langchain.llms import OpenAI
        >>> 
        >>> # Initialize Verifik.io client and handler
        >>> client = VerifikClient(api_key="verifik_live_xxx")
        >>> handler = VerifikLangChainHandler(client, workflow_id="qa-chain-001")
        >>> 
        >>> # Use with any LangChain component
        >>> llm = OpenAI(callbacks=[handler])
        >>> chain = LLMChain(llm=llm, prompt=prompt, callbacks=[handler])
        >>> 
        >>> # All chain executions are automatically logged
        >>> result = chain.run("What is the capital of France?")
    """
    
    def __init__(
        self,
        client: VerifikClient,
        workflow_id: Optional[str] = None,
        log_errors: bool = True,
        log_llm_calls: bool = True,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the LangChain callback handler.
        
        Args:
            client: Initialized VerifikClient instance
            workflow_id: Optional workflow identifier for grouping related logs
            log_errors: Whether to log errors as separate events (default: True)
            log_llm_calls: Whether to log individual LLM calls (default: True)
            metadata: Additional metadata to include with all logs
        """
        if not LANGCHAIN_AVAILABLE:
            raise ImportError(
                "LangChain is not installed. Install it with: pip install langchain"
            )
        
        super().__init__()
        self.client = client
        self.workflow_id = workflow_id or f"langchain-{datetime.utcnow().isoformat()}"
        self.log_errors = log_errors
        self.log_llm_calls = log_llm_calls
        self.base_metadata = metadata or {}
        self._run_context = {}
    
    def on_chain_start(
        self,
        serialized: Dict[str, Any],
        inputs: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any
    ) -> None:
        """Called when a chain starts running."""
        try:
            self._run_context[run_id] = {
                "start_time": datetime.utcnow().isoformat(),
                "chain_type": serialized.get("name", "unknown"),
                "parent_run_id": parent_run_id
            }
            
            metadata = {
                **self.base_metadata,
                "framework": "langchain",
                "event_type": "chain_start",
                "chain_type": serialized.get("name", "unknown"),
                "run_id": str(run_id)
            }
            
            if parent_run_id:
                metadata["parent_run_id"] = str(parent_run_id)
            
            self.client.log_event(
                agent_name=f"langchain-{serialized.get('name', 'chain')}",
                action="chain_started",
                inputs=self._truncate_data(inputs),
                metadata=metadata,
                workflow_id=self.workflow_id,
                status="in_progress"
            )
        except Exception as e:
            if self.log_errors:
                self._log_error("chain_start_error", str(e), run_id=str(run_id))
    
    def on_chain_end(
        self,
        outputs: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any
    ) -> None:
        """Called when a chain finishes running."""
        try:
            context = self._run_context.get(run_id, {})
            
            metadata = {
                **self.base_metadata,
                "framework": "langchain",
                "event_type": "chain_end",
                "chain_type": context.get("chain_type", "unknown"),
                "run_id": str(run_id),
                "duration": self._calculate_duration(context.get("start_time"))
            }
            
            if parent_run_id:
                metadata["parent_run_id"] = str(parent_run_id)
            
            self.client.log_event(
                agent_name=f"langchain-{context.get('chain_type', 'chain')}",
                action="chain_completed",
                outputs=self._truncate_data(outputs),
                metadata=metadata,
                workflow_id=self.workflow_id,
                status="success"
            )
            
            # Clean up context
            self._run_context.pop(run_id, None)
            
        except Exception as e:
            if self.log_errors:
                self._log_error("chain_end_error", str(e), run_id=str(run_id))
    
    def on_chain_error(
        self,
        error: Union[Exception, KeyboardInterrupt],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any
    ) -> None:
        """Called when a chain encounters an error."""
        try:
            context = self._run_context.get(run_id, {})
            
            metadata = {
                **self.base_metadata,
                "framework": "langchain",
                "event_type": "chain_error",
                "chain_type": context.get("chain_type", "unknown"),
                "error_type": type(error).__name__,
                "run_id": str(run_id),
                "duration": self._calculate_duration(context.get("start_time"))
            }
            
            if parent_run_id:
                metadata["parent_run_id"] = str(parent_run_id)
            
            self.client.log_event(
                agent_name=f"langchain-{context.get('chain_type', 'chain')}",
                action="chain_failed",
                outputs={"error": str(error)},
                metadata=metadata,
                workflow_id=self.workflow_id,
                status="error"
            )
            
            # Clean up context
            self._run_context.pop(run_id, None)
            
        except Exception as e:
            if self.log_errors:
                self._log_error("chain_error_logging_failed", str(e))
    
    def on_tool_start(
        self,
        serialized: Dict[str, Any],
        input_str: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any
    ) -> None:
        """Called when a tool starts running."""
        try:
            tool_name = serialized.get("name", "unknown_tool")
            
            metadata = {
                **self.base_metadata,
                "framework": "langchain",
                "event_type": "tool_start",
                "tool_name": tool_name,
                "run_id": str(run_id)
            }
            
            if parent_run_id:
                metadata["parent_run_id"] = str(parent_run_id)
            
            self.client.log_event(
                agent_name=f"langchain-tool-{tool_name}",
                action="tool_started",
                inputs={"input": input_str[:1000]},  # Truncate long inputs
                metadata=metadata,
                workflow_id=self.workflow_id,
                status="in_progress"
            )
        except Exception as e:
            if self.log_errors:
                self._log_error("tool_start_error", str(e), run_id=str(run_id))
    
    def on_tool_end(
        self,
        output: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any
    ) -> None:
        """Called when a tool finishes running."""
        try:
            metadata = {
                **self.base_metadata,
                "framework": "langchain",
                "event_type": "tool_end",
                "run_id": str(run_id)
            }
            
            if parent_run_id:
                metadata["parent_run_id"] = str(parent_run_id)
            
            self.client.log_event(
                agent_name="langchain-tool",
                action="tool_completed",
                outputs={"output": output[:1000]},  # Truncate long outputs
                metadata=metadata,
                workflow_id=self.workflow_id,
                status="success"
            )
        except Exception as e:
            if self.log_errors:
                self._log_error("tool_end_error", str(e), run_id=str(run_id))
    
    def on_tool_error(
        self,
        error: Union[Exception, KeyboardInterrupt],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any
    ) -> None:
        """Called when a tool encounters an error."""
        try:
            metadata = {
                **self.base_metadata,
                "framework": "langchain",
                "event_type": "tool_error",
                "error_type": type(error).__name__,
                "run_id": str(run_id)
            }
            
            if parent_run_id:
                metadata["parent_run_id"] = str(parent_run_id)
            
            self.client.log_event(
                agent_name="langchain-tool",
                action="tool_failed",
                outputs={"error": str(error)},
                metadata=metadata,
                workflow_id=self.workflow_id,
                status="error"
            )
        except Exception as e:
            if self.log_errors:
                self._log_error("tool_error_logging_failed", str(e))
    
    def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any
    ) -> None:
        """Called when an LLM starts running."""
        if not self.log_llm_calls:
            return
            
        try:
            metadata = {
                **self.base_metadata,
                "framework": "langchain",
                "event_type": "llm_start",
                "llm_type": serialized.get("name", "unknown"),
                "prompt_count": len(prompts),
                "run_id": str(run_id)
            }
            
            if parent_run_id:
                metadata["parent_run_id"] = str(parent_run_id)
            
            # Log only first prompt to avoid excessive data
            inputs = {"prompt": prompts[0][:500] if prompts else ""}
            if len(prompts) > 1:
                inputs["additional_prompts"] = len(prompts) - 1
            
            self.client.log_event(
                agent_name=f"langchain-llm-{serialized.get('name', 'unknown')}",
                action="llm_started",
                inputs=inputs,
                metadata=metadata,
                workflow_id=self.workflow_id,
                status="in_progress"
            )
        except Exception as e:
            if self.log_errors:
                self._log_error("llm_start_error", str(e), run_id=str(run_id))
    
    def on_llm_end(
        self,
        response: LLMResult,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any
    ) -> None:
        """Called when an LLM finishes running."""
        if not self.log_llm_calls:
            return
            
        try:
            metadata = {
                **self.base_metadata,
                "framework": "langchain",
                "event_type": "llm_end",
                "run_id": str(run_id)
            }
            
            if parent_run_id:
                metadata["parent_run_id"] = str(parent_run_id)
            
            # Extract token usage if available
            if hasattr(response, "llm_output") and response.llm_output:
                if "token_usage" in response.llm_output:
                    metadata["token_usage"] = response.llm_output["token_usage"]
            
            # Log first generation only
            output_text = ""
            if response.generations and response.generations[0]:
                output_text = response.generations[0][0].text[:500]
            
            self.client.log_event(
                agent_name="langchain-llm",
                action="llm_completed",
                outputs={"response": output_text},
                metadata=metadata,
                workflow_id=self.workflow_id,
                status="success"
            )
        except Exception as e:
            if self.log_errors:
                self._log_error("llm_end_error", str(e), run_id=str(run_id))
    
    def on_agent_action(
        self,
        action: AgentAction,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any
    ) -> None:
        """Called when an agent takes an action."""
        try:
            metadata = {
                **self.base_metadata,
                "framework": "langchain",
                "event_type": "agent_action",
                "tool": action.tool,
                "run_id": str(run_id)
            }
            
            if parent_run_id:
                metadata["parent_run_id"] = str(parent_run_id)
            
            self.client.log_event(
                agent_name="langchain-agent",
                action=f"agent_action_{action.tool}",
                inputs={
                    "tool": action.tool,
                    "tool_input": str(action.tool_input)[:500]
                },
                outputs={"log": action.log[:500] if action.log else ""},
                metadata=metadata,
                workflow_id=self.workflow_id,
                status="in_progress"
            )
        except Exception as e:
            if self.log_errors:
                self._log_error("agent_action_error", str(e), run_id=str(run_id))
    
    def on_agent_finish(
        self,
        finish: AgentFinish,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any
    ) -> None:
        """Called when an agent finishes."""
        try:
            metadata = {
                **self.base_metadata,
                "framework": "langchain",
                "event_type": "agent_finish",
                "run_id": str(run_id)
            }
            
            if parent_run_id:
                metadata["parent_run_id"] = str(parent_run_id)
            
            self.client.log_event(
                agent_name="langchain-agent",
                action="agent_finished",
                outputs={
                    "return_values": self._truncate_data(finish.return_values),
                    "log": finish.log[:500] if finish.log else ""
                },
                metadata=metadata,
                workflow_id=self.workflow_id,
                status="success"
            )
        except Exception as e:
            if self.log_errors:
                self._log_error("agent_finish_error", str(e), run_id=str(run_id))
    
    def _truncate_data(self, data: Any, max_length: int = 1000) -> Any:
        """Truncate data to avoid excessive log sizes."""
        if isinstance(data, str):
            return data[:max_length]
        elif isinstance(data, dict):
            return {k: self._truncate_data(v, max_length // len(data)) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._truncate_data(item, max_length // len(data)) for item in data[:10]]
        else:
            return str(data)[:max_length]
    
    def _calculate_duration(self, start_time: Optional[str]) -> Optional[float]:
        """Calculate duration in seconds from start time."""
        if not start_time:
            return None
        try:
            start = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            duration = (datetime.utcnow() - start).total_seconds()
            return round(duration, 2)
        except:
            return None
    
    def _log_error(self, error_type: str, error_message: str, **kwargs: Any) -> None:
        """Log an error event."""
        try:
            metadata = {
                **self.base_metadata,
                "framework": "langchain",
                "event_type": "handler_error",
                "error_type": error_type,
                **kwargs
            }
            
            self.client.log_event(
                agent_name="langchain-handler",
                action="error",
                outputs={"error": error_message},
                metadata=metadata,
                workflow_id=self.workflow_id,
                status="error"
            )
        except:
            # Silently fail to avoid infinite error loops
            pass