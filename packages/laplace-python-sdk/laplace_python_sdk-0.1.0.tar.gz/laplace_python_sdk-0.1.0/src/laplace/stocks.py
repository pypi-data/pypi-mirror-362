"""Stocks client for Laplace API."""

from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from enum import Enum
from .models import Stock, StockDetail, StockPriceData, PriceCandle, StockRules, StockRestriction


class HistoricalPriceInterval(Enum):
    """Historical price interval options."""
    ONE_MINUTE = "1m"
    THREE_MINUTE = "3m"
    FIVE_MINUTE = "5m"
    FIFTEEN_MINUTE = "15m"
    THIRTY_MINUTE = "30m"
    ONE_HOUR = "1h"
    TWO_HOUR = "2h"
    ONE_DAY = "1d"
    FIVE_DAY = "5d"
    SEVEN_DAY = "7d"
    THIRTY_DAY = "30d"


class StocksClient:
    """Client for stock-related API endpoints."""
    
    def __init__(self, base_client):
        """Initialize the stocks client.
        
        Args:
            base_client: The base Laplace client instance
        """
        self._client = base_client
    
    def _format_datetime(self, dt: datetime) -> str:
        """Format datetime to API required format: YYYY-MM-DD HH:MM:SS"""
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    
    def get_all(self, region: str, page: int = 1, page_size: int = 10) -> List[Stock]:
        """Retrieve a list of all stocks available in the specified region.
        
        Args:
            region: Region code (tr, us)
            page: Page number (default: 1)
            page_size: Page size (default: 10)
            
        Returns:
            List[Stock]: List of stocks
        """
        params = {
            "page": page,
            "pageSize": page_size,
            "region": region
        }
        
        response = self._client.get("v2/stock/all", params=params)
        return [Stock(**stock) for stock in response]
    
    def get_detail_by_id(self, stock_id: str, locale: str = "en") -> StockDetail:
        """Retrieve detailed information about a specific stock using its unique identifier.
        
        Args:
            stock_id: Unique identifier for the stock
            locale: Locale code (tr, en) (default: en)
            
        Returns:
            StockDetail: Detailed stock information
        """
        params = {"locale": locale}
        response = self._client.get(f"v1/stock/{stock_id}", params=params)
        return StockDetail(**response)
    
    def get_detail_by_symbol(self, symbol: str, region: str, asset_class: str = "equity", locale: str = "en") -> StockDetail:
        """Retrieve detailed information about a specific stock using its symbol.
        
        Args:
            symbol: Stock symbol (e.g., "AAPL")
            region: Region code (tr, us)
            asset_class: Asset class (equity, stock) (default: equity)
            locale: Locale code (tr, en) (default: en)
            
        Returns:
            StockDetail: Detailed stock information
        """
        params = {
            "locale": locale,
            "symbol": symbol,
            "region": region,
            "asset_class": asset_class
        }
        
        response = self._client.get("v1/stock/detail", params=params)
        return StockDetail(**response)
    
    def get_price(self, region: str, symbols: List[str], keys: Optional[List[str]] = None) -> List[StockPriceData]:
        """Retrieve the historical price of stocks in a specified region.
        
        Args:
            region: Region code (tr, us)
            symbols: List of stock symbols
            keys: List of time periods for which data is required. 
                  Allowable values: 1D, 1W, 1M, 3M, 1Y, 5Y (optional)
            
        Returns:
            List[StockPriceData]: List of stock price data
        """
        params = {
            "region": region,
            "symbols": ",".join(symbols)
        }
        
        if keys:
            params["keys"] = ",".join(keys)
            
        response = self._client.get("v1/stock/price", params=params)
        return [StockPriceData(**stock_data) for stock_data in response]
    
    def get_price_with_interval(
        self, 
        symbol: str, 
        region: str, 
        from_date: datetime, 
        to_date: datetime, 
        interval: Union[HistoricalPriceInterval, str]
    ) -> List[PriceCandle]:
        """Retrieve the historical price of a stock with custom date range and interval.
        
        Args:
            symbol: Stock symbol or stock ID
            region: Region code (tr, us)
            from_date: Start date and time
            to_date: End date and time
            interval: Price interval (use HistoricalPriceInterval enum or string)
            
        Returns:
            List[PriceCandle]: List of price candles
        """
        interval_value = interval.value if isinstance(interval, HistoricalPriceInterval) else interval
        
        params = {
            "stock": symbol,
            "region": region,
            "fromDate": self._format_datetime(from_date),
            "toDate": self._format_datetime(to_date),
            "interval": interval_value
        }
        
        response = self._client.get("v1/stock/price/interval", params=params)
        return [PriceCandle(**candle) for candle in response]
    
    def get_tick_rules(self, region: str = "tr") -> StockRules:
        """Retrieve the tick rules for creating orderbook and price limits.
        
        Note: This endpoint only works with the "tr" region.
        
        Args:
            region: Region code (must be "tr")
            
        Returns:
            StockRules: Tick rules and price limits
        """
        if region != "tr":
            raise ValueError("Tick rules endpoint only works with the 'tr' region")
            
        params = {"region": region}
        response = self._client.get("v1/stock/rules", params=params)
        return StockRules(**response)
    
    def get_restrictions(self, region: str = "tr") -> List[StockRestriction]:
        """Retrieve the restrictions for a stock.
        
        Note: This endpoint only works with the "tr" region.
        
        Args:
            region: Region code (must be "tr")
            
        Returns:
            List[StockRestriction]: List of stock restrictions
        """
        if region != "tr":
            raise ValueError("Restrictions endpoint only works with the 'tr' region")
            
        params = {"region": region}
        response = self._client.get("v1/stock/restrictions", params=params)
        return [StockRestriction(**restriction) for restriction in response]
    
    def get_all_restrictions(self, region: str = "tr") -> List[StockRestriction]:
        """Retrieve the active restrictions for all stocks.
        
        Note: This endpoint only works with the "tr" region.
        
        Args:
            region: Region code (must be "tr")
            
        Returns:
            List[StockRestriction]: List of all stock restrictions
        """
        if region != "tr":
            raise ValueError("All restrictions endpoint only works with the 'tr' region")
            
        params = {"region": region}
        response = self._client.get("v1/stock/restrictions/all", params=params)
        return [StockRestriction(**restriction) for restriction in response]