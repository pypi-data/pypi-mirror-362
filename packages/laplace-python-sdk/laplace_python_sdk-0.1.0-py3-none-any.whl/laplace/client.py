"""Main Laplace client."""

from typing import Optional
from .base import BaseClient
from .stocks import StocksClient
from .collections import CollectionsClient
from .financials import FinancialsClient
from .funds import FundsClient
from .li import LaplaceIntelligenceClient


class LaplaceClient(BaseClient):
    """Main Laplace API client with all sub-clients."""
    
    def __init__(self, api_key: str, base_url: str = "https://api.finfree.app/api"):
        """Initialize the Laplace client.
        
        Args:
            api_key: Your Laplace API key
            base_url: Base URL for the API (default: https://laplace.finfree.co/api)
        """
        super().__init__(api_key, base_url)
        
        # Initialize sub-clients
        self.stocks = StocksClient(self)
        self.collections = CollectionsClient(self)
        self.financials = FinancialsClient(self)
        self.funds = FundsClient(self)
        self.li = LaplaceIntelligenceClient(self)