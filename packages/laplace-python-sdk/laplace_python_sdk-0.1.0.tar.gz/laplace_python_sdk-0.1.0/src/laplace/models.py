"""Pydantic models for Laplace API responses."""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class Stock(BaseModel):
    """Stock model from the stocks API."""
    id: str
    name: str
    active: bool
    symbol: str
    sector_id: str = Field(alias="sectorId")
    asset_type: str = Field(alias="assetType")
    industry_id: str = Field(alias="industryId")
    updated_date: str = Field(alias="updatedDate")


class StockDetail(BaseModel):
    """Detailed stock information from stock detail API."""
    id: str
    name: str
    active: bool
    region: str
    symbol: str
    sector_id: str = Field(alias="sectorId")
    asset_type: str = Field(alias="assetType")
    asset_class: str = Field(alias="assetClass")
    industry_id: str = Field(alias="industryId")
    description: str
    updated_date: str = Field(alias="updatedDate")
    short_description: str = Field(alias="shortDescription")
    localized_description: Dict[str, str] = Field(alias="localized_description")
    localized_short_description: Dict[str, str] = Field(alias="localizedShortDescription")
    
    model_config = {"populate_by_name": True}


class PriceCandle(BaseModel):
    """Individual price candle data."""
    c: float  # close
    d: float  # timestamp
    h: float  # high
    l: float  # low
    o: float  # open


class StockPriceData(BaseModel):
    """Stock price data with different time intervals."""
    symbol: str
    one_day: List[PriceCandle] = Field(default_factory=list, alias="1D")
    one_week: List[PriceCandle] = Field(default_factory=list, alias="1W")
    one_month: List[PriceCandle] = Field(default_factory=list, alias="1M")
    three_months: List[PriceCandle] = Field(default_factory=list, alias="3M")
    one_year: List[PriceCandle] = Field(default_factory=list, alias="1Y")
    two_years: List[PriceCandle] = Field(default_factory=list, alias="2Y")
    three_years: List[PriceCandle] = Field(default_factory=list, alias="3Y")
    five_years: List[PriceCandle] = Field(default_factory=list, alias="5Y")
    
    model_config = {"populate_by_name": True}


class TickRule(BaseModel):
    """Tick rule for stock pricing."""
    price_from: float = Field(alias="priceFrom")
    price_to: float = Field(alias="priceTo")
    tick_size: float = Field(alias="tickSize")
    
    model_config = {"populate_by_name": True}


class StockRules(BaseModel):
    """Stock tick rules and price limits."""
    rules: List[TickRule]
    base_price: float = Field(alias="basePrice")
    additional_price: int = Field(alias="additionalPrice")
    lower_price_limit: float = Field(alias="lowerPriceLimit")
    upper_price_limit: float = Field(alias="upperPriceLimit")
    
    model_config = {"populate_by_name": True}


class StockRestriction(BaseModel):
    """Stock restriction information."""
    id: int
    title: str
    symbol: Optional[str] = None
    market: Optional[str] = None
    start_date: Optional[str] = Field(None, alias="startDate")
    end_date: Optional[str] = Field(None, alias="endDate")
    description: str
    
    model_config = {"populate_by_name": True}


class CollectionStock(BaseModel):
    """Stock information within a collection."""
    id: str
    name: str
    symbol: str
    sector_id: str = Field(alias="sectorId")
    asset_type: str = Field(alias="assetType")
    industry_id: str = Field(alias="industryId")
    
    model_config = {"populate_by_name": True}


class Collection(BaseModel):
    """Collection model."""
    id: str
    title: str
    region: List[str]
    image_url: str = Field(alias="imageUrl")
    avatar_url: str = Field(alias="avatarUrl")
    num_stocks: int = Field(alias="numStocks")
    asset_class: str = Field(alias="assetClass")
    
    model_config = {"populate_by_name": True}


class CollectionDetail(BaseModel):
    """Detailed collection information."""
    id: str
    title: str
    region: List[str]
    stocks: List[CollectionStock]
    image_url: str = Field(alias="imageUrl")
    avatar_url: str = Field(alias="avatarUrl")
    num_stocks: int = Field(alias="numStocks")
    asset_class: str = Field(alias="assetClass")
    
    model_config = {"populate_by_name": True}


class Theme(BaseModel):
    """Theme model."""
    id: str
    title: str
    region: List[str]
    image_url: str = Field(alias="imageUrl")
    avatar_url: str = Field(alias="avatarUrl")
    num_stocks: int = Field(alias="numStocks")
    asset_class: str = Field(alias="assetClass")
    
    model_config = {"populate_by_name": True}


class ThemeDetail(BaseModel):
    """Detailed theme information."""
    id: str
    title: str
    region: List[str]
    stocks: List[CollectionStock]
    image_url: str = Field(alias="imageUrl")
    avatar_url: str = Field(alias="avatarUrl")
    num_stocks: int = Field(alias="numStocks")
    asset_class: str = Field(alias="assetClass")
    
    model_config = {"populate_by_name": True}


class Industry(BaseModel):
    """Industry model."""
    id: str
    title: str
    image_url: str = Field(alias="imageUrl")
    avatar_url: str = Field(alias="avatarUrl")
    num_stocks: int = Field(alias="numStocks")
    
    model_config = {"populate_by_name": True}


class IndustryDetail(BaseModel):
    """Detailed industry information."""
    id: str
    title: str
    region: List[str]
    stocks: List[CollectionStock]
    image_url: str = Field(alias="imageUrl")
    avatar_url: str = Field(alias="avatarUrl")
    num_stocks: int = Field(alias="numStocks")
    asset_class: str = Field(alias="assetClass")
    
    model_config = {"populate_by_name": True}


class Sector(BaseModel):
    """Sector model."""
    id: str
    title: str
    image_url: str = Field(alias="imageUrl")
    avatar_url: str = Field(alias="avatarUrl")
    num_stocks: int = Field(alias="numStocks")
    
    model_config = {"populate_by_name": True}


class SectorDetail(BaseModel):
    """Detailed sector information."""
    id: str
    title: str
    region: List[str]
    stocks: List[CollectionStock]
    image_url: str = Field(alias="imageUrl")
    avatar_url: str = Field(alias="avatarUrl")
    num_stocks: int = Field(alias="numStocks")
    asset_class: str = Field(alias="assetClass")
    
    model_config = {"populate_by_name": True}