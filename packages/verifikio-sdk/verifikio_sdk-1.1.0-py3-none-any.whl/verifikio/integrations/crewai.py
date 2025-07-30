"""
CrewAI Integration for Verifik.io SDK

This module provides a callback handler for CrewAI that automatically
logs agent actions and task completions to Verifik.io.
"""

from typing import Any, Dict, Optional, List
import json
from datetime import datetime

try:
    from crewai.agent import Agent
    from crewai.task import Task
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False
    Agent = Any
    Task = Any

from ..client import VerifikClient
from ..exceptions import VerifikError


class VerifikCrewAIHandler:
    """
    Callback handler for CrewAI that logs events to Verifik.io.
    
    This handler integrates with CrewAI's callback system to automatically
    log agent actions, task executions, and their results to Verifik.io's
    audit trail.
    
    Example:
        >>> from verifikio import VerifikClient
        >>> from verifikio.integrations.crewai import VerifikCrewAIHandler
        >>> from crewai import Agent, Task, Crew
        >>> 
        >>> # Initialize Verifik.io client and handler
        >>> client = VerifikClient(api_key="verifik_live_xxx")
        >>> handler = VerifikCrewAIHandler(client, workflow_id="research-crew-001")
        >>> 
        >>> # Create CrewAI agents with Verifik.io logging
        >>> researcher = Agent(
        ...     role="Researcher",
        ...     goal="Research the latest AI trends",
        ...     backstory="You are an expert AI researcher",
        ...     callbacks=[handler]
        ... )
        >>> 
        >>> # Run tasks - all actions are automatically logged
        >>> task = Task(
        ...     description="Research GPT-4 capabilities",
        ...     agent=researcher,
        ...     callbacks=[handler]
        ... )
    """
    
    def __init__(
        self,
        client: VerifikClient,
        workflow_id: Optional[str] = None,
        log_errors: bool = True,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the CrewAI callback handler.
        
        Args:
            client: Initialized VerifikClient instance
            workflow_id: Optional workflow identifier for grouping related logs
            log_errors: Whether to log errors as separate events (default: True)
            metadata: Additional metadata to include with all logs
        """
        if not CREWAI_AVAILABLE:
            raise ImportError(
                "CrewAI is not installed. Install it with: pip install crewai"
            )
        
        self.client = client
        self.workflow_id = workflow_id or f"crewai-{datetime.utcnow().isoformat()}"
        self.log_errors = log_errors
        self.base_metadata = metadata or {}
        self._task_context = {}
        
    def on_agent_action(self, agent: Agent, action: str, **kwargs: Any) -> None:
        """
        Called when an agent performs an action.
        
        Args:
            agent: The CrewAI agent performing the action
            action: The action being performed
            **kwargs: Additional action parameters
        """
        try:
            metadata = {
                **self.base_metadata,
                "agent_role": agent.role,
                "agent_goal": agent.goal,
                "framework": "crewai",
                "event_type": "agent_action"
            }
            
            # Add any tool information if present
            if "tool" in kwargs:
                metadata["tool_name"] = str(kwargs["tool"])
            
            self.client.log_event(
                agent_name=f"crewai-{agent.role}",
                action=action,
                inputs=kwargs.get("inputs", {}),
                outputs=kwargs.get("outputs"),
                metadata=metadata,
                workflow_id=self.workflow_id,
                status="in_progress"
            )
        except Exception as e:
            if self.log_errors:
                self._log_error("agent_action_error", str(e), agent_name=agent.role)
    
    def on_task_start(self, task: Task, agent: Agent) -> None:
        """
        Called when a task starts execution.
        
        Args:
            task: The task being started
            agent: The agent executing the task
        """
        try:
            task_id = id(task)
            self._task_context[task_id] = {
                "start_time": datetime.utcnow().isoformat(),
                "agent_role": agent.role,
                "description": task.description
            }
            
            metadata = {
                **self.base_metadata,
                "agent_role": agent.role,
                "task_description": task.description[:200],  # Truncate long descriptions
                "framework": "crewai",
                "event_type": "task_start"
            }
            
            self.client.log_event(
                agent_name=f"crewai-{agent.role}",
                action="task_started",
                inputs={"task": task.description},
                metadata=metadata,
                workflow_id=self.workflow_id,
                status="in_progress"
            )
        except Exception as e:
            if self.log_errors:
                self._log_error("task_start_error", str(e), agent_name=agent.role)
    
    def on_task_complete(self, task: Task, output: Any) -> None:
        """
        Called when a task completes successfully.
        
        Args:
            task: The completed task
            output: The task output/result
        """
        try:
            task_id = id(task)
            context = self._task_context.get(task_id, {})
            
            metadata = {
                **self.base_metadata,
                "framework": "crewai",
                "event_type": "task_complete",
                "task_description": task.description[:200],
                "duration": self._calculate_duration(context.get("start_time"))
            }
            
            if context.get("agent_role"):
                metadata["agent_role"] = context["agent_role"]
            
            # Serialize output for storage
            output_data = self._serialize_output(output)
            
            self.client.log_event(
                agent_name=f"crewai-{context.get('agent_role', 'unknown')}",
                action="task_completed",
                inputs={"task": task.description},
                outputs={"result": output_data},
                metadata=metadata,
                workflow_id=self.workflow_id,
                status="success"
            )
            
            # Clean up context
            self._task_context.pop(task_id, None)
            
        except Exception as e:
            if self.log_errors:
                self._log_error("task_complete_error", str(e))
    
    def on_task_error(self, task: Task, error: Exception) -> None:
        """
        Called when a task encounters an error.
        
        Args:
            task: The task that failed
            error: The exception that occurred
        """
        try:
            task_id = id(task)
            context = self._task_context.get(task_id, {})
            
            metadata = {
                **self.base_metadata,
                "framework": "crewai",
                "event_type": "task_error",
                "task_description": task.description[:200],
                "error_type": type(error).__name__,
                "error_message": str(error),
                "duration": self._calculate_duration(context.get("start_time"))
            }
            
            if context.get("agent_role"):
                metadata["agent_role"] = context["agent_role"]
            
            self.client.log_event(
                agent_name=f"crewai-{context.get('agent_role', 'unknown')}",
                action="task_failed",
                inputs={"task": task.description},
                outputs={"error": str(error)},
                metadata=metadata,
                workflow_id=self.workflow_id,
                status="error"
            )
            
            # Clean up context
            self._task_context.pop(task_id, None)
            
        except Exception as e:
            if self.log_errors:
                self._log_error("task_error_logging_failed", str(e))
    
    def on_crew_complete(self, results: List[Any]) -> None:
        """
        Called when an entire crew finishes execution.
        
        Args:
            results: List of results from all tasks
        """
        try:
            metadata = {
                **self.base_metadata,
                "framework": "crewai",
                "event_type": "crew_complete",
                "task_count": len(results)
            }
            
            self.client.log_event(
                agent_name="crewai-crew",
                action="crew_completed",
                outputs={"results_count": len(results)},
                metadata=metadata,
                workflow_id=self.workflow_id,
                status="success"
            )
        except Exception as e:
            if self.log_errors:
                self._log_error("crew_complete_error", str(e))
    
    def _serialize_output(self, output: Any) -> Any:
        """Safely serialize output for storage."""
        if isinstance(output, (str, int, float, bool, type(None))):
            return output
        elif isinstance(output, (list, dict)):
            try:
                # Test if it's JSON serializable
                json.dumps(output)
                return output
            except (TypeError, ValueError):
                return str(output)
        else:
            return str(output)
    
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
                "framework": "crewai",
                "event_type": "handler_error",
                "error_type": error_type,
                **kwargs
            }
            
            self.client.log_event(
                agent_name="crewai-handler",
                action="error",
                outputs={"error": error_message},
                metadata=metadata,
                workflow_id=self.workflow_id,
                status="error"
            )
        except:
            # Silently fail to avoid infinite error loops
            pass