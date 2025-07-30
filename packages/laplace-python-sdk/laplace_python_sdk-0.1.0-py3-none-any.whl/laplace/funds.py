"""Funds client for Laplace API."""

from typing import List, Optional


class FundsClient:
    """Client for fund-related API endpoints."""
    
    def __init__(self, base_client):
        """Initialize the funds client.
        
        Args:
            base_client: The base Laplace client instance
        """
        self._client = base_client