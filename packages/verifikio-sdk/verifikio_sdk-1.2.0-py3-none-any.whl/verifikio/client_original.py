"""
Verifik.io Python SDK Client

Main client class for interacting with the Verifik.io API.
"""

import json
import requests
from typing import Dict, Any, Optional, Union
from urllib.parse import urljoin

from .exceptions import VerifikError, AuthenticationError, ValidationError, APIError


class VerifikClient:
    """
    Official Verifik.io Python SDK Client
    
    A simple, developer-friendly client for recording audit logs with Verifik.io's
    trust infrastructure platform.
    
    Args:
        api_key (str): Your Verifik.io API key (format: verifik_live_*)
        base_url (str, optional): Base URL for the API. Defaults to production.
        timeout (int, optional): Request timeout in seconds. Defaults to 30.
        
    Example:
        >>> from verifikio import VerifikClient
        >>> client = VerifikClient(api_key="verifik_live_abc123...")
        >>> 
        >>> # Log a simple event
        >>> response = client.log_event(
        ...     agent_name="data_processor",
        ...     action="process_customer_data",
        ...     status="success"
        ... )
        >>> print(response["id"])  # Audit log ID
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.verifik.io",
        timeout: int = 30
    ):
        if not api_key:
            raise ValueError("API key is required")
        
        if not api_key.startswith("verifik_"):
            raise ValueError("Invalid API key format. Must start with 'verifik_'")
        
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        
        # Set up session with default headers
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": f"verifikio-python-sdk/1.0.0"
        })
    
    def log_event(
        self,
        agent_name: str,
        action: str,
        inputs: Optional[Dict[str, Any]] = None,
        outputs: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        workflow_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new audit log entry
        
        Records an audit log event with the specified parameters. All logs are
        automatically hash-chained and verified for integrity.
        
        Args:
            agent_name (str): Name/identifier of the AI agent or service
            action (str): The action that was performed
            inputs (dict, optional): Input data/parameters for the action
            outputs (dict, optional): Output data/results from the action
            metadata (dict, optional): Additional metadata about the event
            workflow_id (str, optional): Workflow or session identifier
            status (str, optional): Status of the action (e.g., "success", "error", "pending")
            
        Returns:
            dict: The created audit log entry with ID, hash, and verification details
            
        Raises:
            ValidationError: If required parameters are missing or invalid
            AuthenticationError: If API key is invalid or unauthorized
            APIError: If the API returns an error response
            VerifikError: For other SDK-related errors
            
        Example:
            >>> response = client.log_event(
            ...     agent_name="email_agent",
            ...     action="send_notification",
            ...     inputs={"recipient": "user@example.com", "template": "welcome"},
            ...     outputs={"message_id": "msg_123", "status": "sent"},
            ...     metadata={"campaign_id": "camp_456"},
            ...     workflow_id="workflow_789",
            ...     status="success"
            ... )
            >>> print(f"Log created with ID: {response['id']}")
        """
        # Validate required parameters
        if not agent_name or not isinstance(agent_name, str):
            raise ValidationError("agent_name must be a non-empty string")
        
        if not action or not isinstance(action, str):
            raise ValidationError("action must be a non-empty string")
        
        # Prepare payload
        payload = {
            "agentId": agent_name,
            "action": action
        }
        
        # Add optional parameters if provided
        if inputs is not None:
            if not isinstance(inputs, dict):
                raise ValidationError("inputs must be a dictionary")
            payload["inputs"] = inputs
        
        if outputs is not None:
            if not isinstance(outputs, dict):
                raise ValidationError("outputs must be a dictionary")
            payload["outputs"] = outputs
        
        if metadata is not None:
            if not isinstance(metadata, dict):
                raise ValidationError("metadata must be a dictionary")
            payload["metadata"] = metadata
        
        if workflow_id is not None:
            if not isinstance(workflow_id, str):
                raise ValidationError("workflow_id must be a string")
            payload["workflowId"] = workflow_id
        
        if status is not None:
            if not isinstance(status, str):
                raise ValidationError("status must be a string")
            payload["status"] = status
        
        # Make API request
        return self._make_request("POST", "/api/v1/logs", data=payload)
    
    def get_logs(
        self,
        limit: int = 50,
        offset: int = 0,
        workflow_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Retrieve audit logs
        
        Fetches a paginated list of audit logs from your account.
        
        Args:
            limit (int, optional): Number of logs to return (max 100). Defaults to 50.
            offset (int, optional): Number of logs to skip. Defaults to 0.
            workflow_id (str, optional): Filter by workflow ID
            
        Returns:
            dict: Paginated list of audit logs with pagination metadata
            
        Raises:
            ValidationError: If parameters are invalid
            AuthenticationError: If API key is invalid or unauthorized
            APIError: If the API returns an error response
        """
        if not isinstance(limit, int) or limit < 1 or limit > 100:
            raise ValidationError("limit must be an integer between 1 and 100")
        
        if not isinstance(offset, int) or offset < 0:
            raise ValidationError("offset must be a non-negative integer")
        
        params = {
            "limit": limit,
            "offset": offset
        }
        
        if workflow_id:
            params["workflowId"] = workflow_id
        
        return self._make_request("GET", "/api/v1/logs", params=params)
    
    def verify_chain(self) -> Dict[str, Any]:
        """
        Verify the integrity of the audit log chain
        
        Checks that all audit logs in your account maintain proper hash chain
        integrity and have not been tampered with.
        
        Returns:
            dict: Verification results including status and any integrity issues
            
        Raises:
            AuthenticationError: If API key is invalid or unauthorized
            APIError: If the API returns an error response
        """
        return self._make_request("GET", "/api/v1/verify")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get account statistics
        
        Returns statistics about your account including log count, chain status,
        and usage metrics.
        
        Returns:
            dict: Account statistics and metrics
            
        Raises:
            AuthenticationError: If API key is invalid or unauthorized
            APIError: If the API returns an error response
        """
        return self._make_request("GET", "/api/v1/stats")
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make an authenticated request to the Verifik.io API
        
        Args:
            method (str): HTTP method (GET, POST, etc.)
            endpoint (str): API endpoint path
            data (dict, optional): JSON data for POST requests
            params (dict, optional): Query parameters for GET requests
            
        Returns:
            dict: Parsed JSON response
            
        Raises:
            AuthenticationError: If API key is invalid or unauthorized
            APIError: If the API returns an error response
            VerifikError: For connection or other errors
        """
        url = urljoin(self.base_url, endpoint)
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=self.timeout
            )
            
            # Handle different response status codes
            if response.status_code == 401:
                raise AuthenticationError("Invalid API key or unauthorized access")
            elif response.status_code == 400:
                try:
                    error_data = response.json()
                    error_message = error_data.get("message", "Bad request")
                except:
                    error_message = "Bad request"
                raise ValidationError(f"Validation error: {error_message}")
            elif response.status_code == 429:
                raise APIError("Rate limit exceeded. Please try again later.")
            elif response.status_code >= 500:
                raise APIError(f"Server error: {response.status_code}")
            elif not response.ok:
                raise APIError(f"API request failed: {response.status_code}")
            
            # Parse JSON response
            try:
                return response.json()
            except json.JSONDecodeError:
                raise APIError("Invalid JSON response from API")
                
        except requests.exceptions.Timeout:
            raise VerifikError("Request timed out")
        except requests.exceptions.ConnectionError:
            raise VerifikError("Connection error. Please check your network connection.")
        except requests.exceptions.RequestException as e:
            raise VerifikError(f"Request failed: {str(e)}")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup session"""
        self.session.close()