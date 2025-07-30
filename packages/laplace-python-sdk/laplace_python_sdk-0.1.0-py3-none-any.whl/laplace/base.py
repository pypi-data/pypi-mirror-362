"""Base client for Laplace API."""

from typing import Any, Dict, Optional, Union
import httpx
from pydantic import BaseModel


class LaplaceError(Exception):
    """Base exception for Laplace API errors."""
    pass


class LaplaceAPIError(LaplaceError):
    """Exception raised for API errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class BaseClient:
    """Base client for Laplace API communication."""
    
    def __init__(self, api_key: str, base_url: str = "https://api.finfree.app/api"):
        """Initialize the base client.
        
        Args:
            api_key: Your Laplace API key
            base_url: Base URL for the API (default: https://api.finfree.app/api)
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self._client = httpx.Client(
            headers={
                "User-Agent": "laplace-python-sdk/0.1.0",
            },
            timeout=30.0,
        )
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def close(self):
        """Close the HTTP client."""
        self._client.close()
    
    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Make a request to the API.
        
        Args:
            method: HTTP method
            endpoint: API endpoint (relative to base_url)
            params: Query parameters
            json: JSON body data
            **kwargs: Additional arguments passed to httpx
            
        Returns:
            Response data as dictionary
            
        Raises:
            LaplaceAPIError: If the API request fails
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        # Add API key to params
        if params is None:
            params = {}
        params["api_key"] = self.api_key
        
        try:
            response = self._client.request(
                method=method,
                url=url,
                params=params,
                json=json,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            try:
                error_data = e.response.json()
            except:
                error_data = {"error": e.response.text}
            
            raise LaplaceAPIError(
                message=f"API request failed: {e.response.status_code} {e.response.reason_phrase}",
                status_code=e.response.status_code,
                response=error_data
            ) from e
        except httpx.RequestError as e:
            raise LaplaceAPIError(f"Request failed: {str(e)}") from e
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request."""
        return self._request("GET", endpoint, params=params)
    
    def post(self, endpoint: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a POST request."""
        return self._request("POST", endpoint, json=json)
    
    def put(self, endpoint: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a PUT request."""
        return self._request("PUT", endpoint, json=json)
    
    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make a DELETE request."""
        return self._request("DELETE", endpoint)