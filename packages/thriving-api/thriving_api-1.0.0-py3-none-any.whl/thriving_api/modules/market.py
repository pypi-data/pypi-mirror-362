"""
Market data module for the Thriving API SDK.

This module provides access to market-related endpoints including
market status and general market information.
"""

from ..base_client import BaseClient
from ..models.market import MarketStatusResponse


class MarketModule:
    """Market data endpoints wrapper."""
    
    def __init__(self, client: BaseClient) -> None:
        """
        Initialize Market module.
        
        Args:
            client: Base HTTP client instance
        """
        self.client = client
    
    async def get_status(self) -> MarketStatusResponse:
        """
        Get real-time market status and trading hours information.
        
        This endpoint provides comprehensive market status information including
        current market status (open/closed/pre-market/after-hours), trading hours,
        and information for multiple markets and regions.
        
        Returns:
            MarketStatusResponse: Market status and trading hours data
            
        Raises:
            ThrivingAPIError: For API errors
            
        Example:
            >>> client = ThrivingAPI(api_key="your-api-key")
            >>> status = await client.market.get_status()
            >>> 
            >>> # Check if US market is open
            >>> if status.is_us_market_open():
            ...     print("US market is currently open")
            >>> else:
            ...     print("US market is closed")
            >>> 
            >>> # Get market summary
            >>> summary = status.get_market_summary()
            >>> print(f"Total markets: {summary['total_markets']}")
            >>> print(f"Open markets: {summary['open_markets']}")
            >>> 
            >>> # Get trading schedule
            >>> schedule = status.get_trading_schedule()
            >>> for market, info in schedule.items():
            ...     print(f"{market}: {info['open']} - {info['close']} ({info['status']})")
        """
        response_data = await self.client.get("/markets/status")
        return MarketStatusResponse(**response_data)
    
    def is_market_hours(self, market_response: MarketStatusResponse, region: str = "United States") -> bool:
        """
        Check if a specific market is currently in trading hours.
        
        Args:
            market_response: Market status response
            region: Market region to check (default: "United States")
            
        Returns:
            bool: True if market is open
        """
        market = market_response.get_market_by_region(region)
        return market.is_open() if market else False
    
    def get_market_hours_info(self, market_response: MarketStatusResponse, region: str = "United States") -> dict:
        """
        Get detailed trading hours information for a market.
        
        Args:
            market_response: Market status response
            region: Market region (default: "United States")
            
        Returns:
            dict: Trading hours information
        """
        market = market_response.get_market_by_region(region)
        if not market:
            return {"error": f"Market not found for region: {region}"}
        
        return market.get_trading_hours_info()
    
    def analyze_global_markets(self, market_response: MarketStatusResponse) -> dict:
        """
        Analyze global market status and activity.
        
        Args:
            market_response: Market status response
            
        Returns:
            dict: Global market analysis
        """
        analysis = {
            "total_markets": len(market_response.markets),
            "open_markets": [],
            "closed_markets": [],
            "pre_market": [],
            "after_hours": [],
            "regions": set(),
            "market_types": set()
        }
        
        for market in market_response.markets:
            analysis["regions"].add(market.region)
            analysis["market_types"].add(market.market_type)
            
            if market.is_open():
                analysis["open_markets"].append({
                    "region": market.region,
                    "type": market.market_type,
                    "exchanges": market.get_exchanges_list()
                })
            elif market.is_closed():
                analysis["closed_markets"].append({
                    "region": market.region,
                    "type": market.market_type,
                    "next_open": market.local_open
                })
            elif market.is_pre_market():
                analysis["pre_market"].append({
                    "region": market.region,
                    "type": market.market_type
                })
            elif market.is_after_hours():
                analysis["after_hours"].append({
                    "region": market.region,
                    "type": market.market_type
                })
        
        # Convert sets to lists for JSON serialization
        analysis["regions"] = list(analysis["regions"])
        analysis["market_types"] = list(analysis["market_types"])
        
        # Add summary statistics
        analysis["summary"] = {
            "open_count": len(analysis["open_markets"]),
            "closed_count": len(analysis["closed_markets"]),
            "pre_market_count": len(analysis["pre_market"]),
            "after_hours_count": len(analysis["after_hours"]),
            "total_regions": len(analysis["regions"]),
            "total_market_types": len(analysis["market_types"])
        }
        
        return analysis
    
    def get_next_market_events(self, market_response: MarketStatusResponse) -> dict:
        """
        Get information about upcoming market events (opens/closes).
        
        Args:
            market_response: Market status response
            
        Returns:
            dict: Upcoming market events
        """
        events = {
            "next_opens": [],
            "next_closes": [],
            "currently_trading": []
        }
        
        for market in market_response.markets:
            market_info = {
                "region": market.region,
                "type": market.market_type,
                "exchanges": market.get_exchanges_list()
            }
            
            if market.is_open():
                events["currently_trading"].append({
                    **market_info,
                    "closes_at": market.local_close
                })
                events["next_closes"].append({
                    **market_info,
                    "close_time": market.local_close
                })
            else:
                events["next_opens"].append({
                    **market_info,
                    "open_time": market.local_open
                })
        
        return events
