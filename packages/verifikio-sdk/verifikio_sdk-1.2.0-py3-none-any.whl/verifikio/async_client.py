"""
Async client for Verifik.io API

Provides asynchronous HTTP operations using aiohttp for better performance
when dealing with multiple API calls or batch operations.
"""

import json
from typing import Dict, List, Optional, Any, Union
from urllib.parse import urljoin

from .exceptions import AuthenticationError, ValidationError, APIError, VerifikError


class AsyncVerifikClient:
    """
    Asynchronous client for interacting with the Verifik.io API.
    
    This client provides async/await support for all API operations,
    enabling better performance when making multiple API calls.
    
    Example:
        import asyncio
        from verifikio import AsyncVerifikClient
        
        async def main():
            client = AsyncVerifikClient(api_key="verifik_live_xxx")
            
            # Log single event
            await client.log_event_async(
                agent_name="my-agent",
                action="processed_data"
            )
            
            # Log multiple events
            events = [
                {"agent_name": "agent1", "action": "action1"},
                {"agent_name": "agent2", "action": "action2"}
            ]
            await client.log_events_async(events)
        
        asyncio.run(main())
    """
    
    def __init__(self, api_key: str, base_url: str = "https://api.verifik.io/v1"):
        """
        Initialize the async Verifik.io client.
        
        Args:
            api_key: Your Verifik.io API key
            base_url: Base URL for the API (default: https://api.verifik.io/v1)
            
        Raises:
            ValueError: If api_key is empty or invalid format
        """
        if not api_key:
            raise ValueError("API key is required")
            
        if not isinstance(api_key, str):
            raise ValueError("API key must be a string")
            
        if not api_key.startswith("verifik_"):
            raise ValueError("Invalid API key format")
            
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self._session = None
        
    async def __aenter__(self):
        """Context manager entry - creates aiohttp session."""
        await self._ensure_session()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - closes aiohttp session."""
        await self.close()
        
    async def _ensure_session(self):
        """Ensure aiohttp session exists, creating if needed."""
        if self._session is None or self._session.closed:
            try:
                import aiohttp
            except ImportError:
                raise ImportError(
                    "aiohttp is required for async operations. "
                    "Install with: pip install verifikio-sdk[async]"
                )
            
            self._session = aiohttp.ClientSession(
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "User-Agent": "Verifik.io-Python-SDK/1.0.0"
                }
            )
            
    async def close(self):
        """Close the aiohttp session."""
        if self._session and not self._session.closed:
            await self._session.close()
            
    async def _request(self, method: str, endpoint: str, json_data: Optional[Dict] = None) -> Dict:
        """
        Make an async HTTP request to the API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            json_data: JSON data to send in request body
            
        Returns:
            Response data as dictionary
            
        Raises:
            Various exceptions based on response status
        """
        await self._ensure_session()
        
        url = urljoin(self.base_url, endpoint)
        
        try:
            async with self._session.request(method, url, json=json_data) as response:
                response_text = await response.text()
                
                # Try to parse JSON response
                try:
                    response_data = json.loads(response_text) if response_text else {}
                except json.JSONDecodeError:
                    response_data = {"message": response_text}
                
                # Handle different status codes
                if response.status == 401:
                    raise AuthenticationError(
                        response_data.get("message", "Invalid or missing API key")
                    )
                elif response.status == 400:
                    raise ValidationError(
                        response_data.get("message", "Invalid request data")
                    )
                elif response.status == 429:
                    raise APIError(
                        response_data.get("message", "Rate limit exceeded")
                    )
                elif response.status >= 500:
                    raise APIError(
                        f"Server error: {response.status} - {response_data.get('message', 'Unknown error')}"
                    )
                elif response.status >= 400:
                    raise APIError(
                        f"Client error: {response.status} - {response_data.get('message', 'Unknown error')}"
                    )
                    
                return response_data
                
        except Exception as e:
            if isinstance(e, (AuthenticationError, ValidationError, APIError)):
                raise
            raise VerifikError(f"Request failed: {str(e)}")
            
    async def log_event_async(
        self,
        agent_name: str,
        action: str,
        inputs: Optional[Dict] = None,
        outputs: Optional[Dict] = None,
        metadata: Optional[Dict] = None,
        workflow_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> Dict:
        """
        Asynchronously log a single audit event.
        
        Args:
            agent_name: Name of the agent performing the action
            action: Action being performed
            inputs: Optional input data
            outputs: Optional output data
            metadata: Optional metadata
            workflow_id: Optional workflow identifier
            status: Optional status (e.g., "success", "error")
            
        Returns:
            API response containing the created log entry
            
        Raises:
            ValidationError: If required parameters are invalid
            AuthenticationError: If API key is invalid
            APIError: If the API request fails
        """
        # Validate required parameters
        if not agent_name or not isinstance(agent_name, str):
            raise ValidationError("agent_name is required and must be a string")
            
        if not action or not isinstance(action, str):
            raise ValidationError("action is required and must be a string")
            
        # Validate optional parameters
        if inputs is not None and not isinstance(inputs, dict):
            raise ValidationError("inputs must be a dictionary")
            
        if outputs is not None and not isinstance(outputs, dict):
            raise ValidationError("outputs must be a dictionary")
            
        if metadata is not None and not isinstance(metadata, dict):
            raise ValidationError("metadata must be a dictionary")
            
        if workflow_id is not None and not isinstance(workflow_id, str):
            raise ValidationError("workflow_id must be a string")
            
        if status is not None and not isinstance(status, str):
            raise ValidationError("status must be a string")
            
        # Build request payload
        payload = {
            "agent_name": agent_name,
            "action": action
        }
        
        if inputs is not None:
            payload["inputs"] = inputs
        if outputs is not None:
            payload["outputs"] = outputs
        if metadata is not None:
            payload["metadata"] = metadata
        if workflow_id is not None:
            payload["workflow_id"] = workflow_id
        if status is not None:
            payload["status"] = status
            
        return await self._request("POST", "/logs", payload)
        
    async def log_events_async(self, events: List[Dict[str, Any]]) -> Dict:
        """
        Asynchronously log multiple audit events in a single batch request.
        
        Args:
            events: List of event dictionaries, each containing:
                - agent_name (required): Name of the agent
                - action (required): Action performed
                - inputs (optional): Input data
                - outputs (optional): Output data
                - metadata (optional): Additional metadata
                - workflow_id (optional): Workflow identifier
                - status (optional): Status of the action
                
        Returns:
            API response containing the created log entries
            
        Raises:
            ValidationError: If events list or individual events are invalid
            AuthenticationError: If API key is invalid
            APIError: If the API request fails
            
        Example:
            events = [
                {
                    "agent_name": "data-processor",
                    "action": "process_batch",
                    "status": "success"
                },
                {
                    "agent_name": "validator",
                    "action": "validate_output",
                    "status": "success"
                }
            ]
            response = await client.log_events_async(events)
        """
        # Validate events parameter
        if not isinstance(events, list):
            raise ValidationError("events must be a list")
            
        if not events:
            raise ValidationError("events list cannot be empty")
            
        # Validate each event
        for i, event in enumerate(events):
            if not isinstance(event, dict):
                raise ValidationError(f"Event at index {i} must be a dictionary")
                
            # Check required fields
            if "agent_name" not in event:
                raise ValidationError(f"Event at index {i} missing required field: agent_name")
            if "action" not in event:
                raise ValidationError(f"Event at index {i} missing required field: action")
                
            # Validate field types
            if not isinstance(event["agent_name"], str):
                raise ValidationError(f"Event at index {i}: agent_name must be a string")
            if not isinstance(event["action"], str):
                raise ValidationError(f"Event at index {i}: action must be a string")
                
            # Validate optional fields if present
            if "inputs" in event and not isinstance(event["inputs"], dict):
                raise ValidationError(f"Event at index {i}: inputs must be a dictionary")
            if "outputs" in event and not isinstance(event["outputs"], dict):
                raise ValidationError(f"Event at index {i}: outputs must be a dictionary")
            if "metadata" in event and not isinstance(event["metadata"], dict):
                raise ValidationError(f"Event at index {i}: metadata must be a dictionary")
            if "workflow_id" in event and not isinstance(event["workflow_id"], str):
                raise ValidationError(f"Event at index {i}: workflow_id must be a string")
            if "status" in event and not isinstance(event["status"], str):
                raise ValidationError(f"Event at index {i}: status must be a string")
                
        # Send batch request
        return await self._request("POST", "/logs", events)
        
    async def get_logs_async(self, limit: int = 50, offset: int = 0) -> Dict:
        """
        Asynchronously retrieve audit logs with pagination.
        
        Args:
            limit: Maximum number of logs to return (default: 50, max: 100)
            offset: Number of logs to skip (default: 0)
            
        Returns:
            Dictionary containing logs array and pagination info
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If the API request fails
        """
        if not isinstance(limit, int) or limit < 1:
            raise ValidationError("limit must be a positive integer")
        if not isinstance(offset, int) or offset < 0:
            raise ValidationError("offset must be a non-negative integer")
            
        return await self._request("GET", f"/logs?limit={limit}&offset={offset}")
        
    async def verify_chain_async(self) -> Dict:
        """
        Asynchronously verify the integrity of the audit log chain.
        
        Returns:
            Dictionary containing verification status and details
            
        Raises:
            APIError: If the API request fails
        """
        return await self._request("GET", "/verify")
        
    async def get_stats_async(self) -> Dict:
        """
        Asynchronously get account statistics and system health.
        
        Returns:
            Dictionary containing account statistics
            
        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API request fails
        """
        return await self._request("GET", "/stats")