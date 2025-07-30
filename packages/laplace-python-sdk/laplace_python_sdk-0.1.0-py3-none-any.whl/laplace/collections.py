"""Collections client for Laplace API."""

from typing import List, Optional
from .models import (
    Collection, CollectionDetail, Theme, ThemeDetail, 
    Industry, IndustryDetail, Sector, SectorDetail
)


class CollectionsClient:
    """Client for collection-related API endpoints."""
    
    def __init__(self, base_client):
        """Initialize the collections client.
        
        Args:
            base_client: The base Laplace client instance
        """
        self._client = base_client
    
    def get_collections(self, region: str, locale: str = "en") -> List[Collection]:
        """Get all collections in a specific region.
        
        Args:
            region: Region code (tr, us)
            locale: Locale code (tr, en) (default: en)
            
        Returns:
            List[Collection]: List of collections
        """
        params = {
            "region": region,
            "locale": locale
        }
        
        response = self._client.get("v1/collection", params=params)
        return [Collection(**collection) for collection in response]
    
    def get_collection_detail(self, collection_id: str, region: str, locale: str = "en") -> CollectionDetail:
        """Retrieve detailed information about a specific collection by its ID.
        
        Args:
            collection_id: Unique identifier for the collection
            region: Region code (tr, us)
            locale: Locale code (tr, en) (default: en)
            
        Returns:
            CollectionDetail: Detailed collection information
        """
        params = {
            "locale": locale,
            "region": region
        }
        
        response = self._client.get(f"v1/collection/{collection_id}", params=params)
        return CollectionDetail(**response)
    
    def get_themes(self, region: str, locale: str = "en") -> List[Theme]:
        """Retrieve a list of themes along with the number of stocks in each.
        
        Args:
            region: Region code (tr, us)
            locale: Locale code (tr, en) (default: en)
            
        Returns:
            List[Theme]: List of themes
        """
        params = {
            "region": region,
            "locale": locale
        }
        
        response = self._client.get("v1/theme", params=params)
        return [Theme(**theme) for theme in response]
    
    def get_theme_detail(self, theme_id: str, region: str, locale: str = "en") -> ThemeDetail:
        """Retrieve detailed information about a specific theme.
        
        Args:
            theme_id: Unique identifier for the theme
            region: Region code (tr, us)
            locale: Locale code (tr, en) (default: en)
            
        Returns:
            ThemeDetail: Detailed theme information
        """
        params = {
            "locale": locale,
            "region": region
        }
        
        response = self._client.get(f"v1/theme/{theme_id}", params=params)
        return ThemeDetail(**response)
    
    def get_industries(self, region: str, locale: str = "en") -> List[Industry]:
        """Retrieve a list of industries along with the number of stocks in each.
        
        Args:
            region: Region code (tr, us)
            locale: Locale code (tr, en) (default: en)
            
        Returns:
            List[Industry]: List of industries
        """
        params = {
            "region": region,
            "locale": locale
        }
        
        response = self._client.get("v1/industry", params=params)
        return [Industry(**industry) for industry in response]
    
    def get_industry_detail(self, industry_id: str, region: str, locale: str = "en") -> IndustryDetail:
        """Retrieve detailed information about a specific industry.
        
        Args:
            industry_id: Unique identifier for the industry
            region: Region code (tr, us)
            locale: Locale code (tr, en) (default: en)
            
        Returns:
            IndustryDetail: Detailed industry information
        """
        params = {
            "locale": locale,
            "region": region
        }
        
        response = self._client.get(f"v1/industry/{industry_id}", params=params)
        return IndustryDetail(**response)
    
    def get_sectors(self, region: str, locale: str = "en") -> List[Sector]:
        """Retrieve a list of sectors along with the number of stocks in each.
        
        Args:
            region: Region code (tr, us)
            locale: Locale code (tr, en) (default: en)
            
        Returns:
            List[Sector]: List of sectors
        """
        params = {
            "region": region,
            "locale": locale
        }
        
        response = self._client.get("v1/sector", params=params)
        return [Sector(**sector) for sector in response]
    
    def get_sector_detail(self, sector_id: str, region: str, locale: str = "en") -> SectorDetail:
        """Retrieve detailed information about a specific sector.
        
        Args:
            sector_id: Unique identifier for the sector
            region: Region code (tr, us)
            locale: Locale code (tr, en) (default: en)
            
        Returns:
            SectorDetail: Detailed sector information
        """
        params = {
            "locale": locale,
            "region": region
        }
        
        response = self._client.get(f"v1/sector/{sector_id}", params=params)
        return SectorDetail(**response)