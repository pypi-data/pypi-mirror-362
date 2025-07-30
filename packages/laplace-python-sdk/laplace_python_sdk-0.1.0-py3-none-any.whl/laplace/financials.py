"""Financials client for Laplace API."""

from typing import List, Optional


class FinancialsClient:
    """Client for financial data API endpoints."""
    
    def __init__(self, base_client):
        """Initialize the financials client.
        
        Args:
            base_client: The base Laplace client instance
        """
        self._client = base_client