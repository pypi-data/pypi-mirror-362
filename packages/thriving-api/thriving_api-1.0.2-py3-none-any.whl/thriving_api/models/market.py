"""
Market data models for the Thriving API SDK.

This module contains Pydantic models for market-related endpoints
including market status and general market information.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime, time

from .base import BaseResponse, MetadataMixin


class MarketInfo(BaseModel):
    """Individual market information."""
    
    market_type: str = Field(..., description="Type of market (e.g., 'Equity')")
    region: str = Field(..., description="Market region")
    primary_exchanges: str = Field(..., description="Primary exchanges")
    local_open: str = Field(..., description="Local market open time")
    local_close: str = Field(..., description="Local market close time")
    current_status: str = Field(..., description="Current market status")
    notes: Optional[str] = Field(None, description="Additional notes")
    
    def get_open_time(self) -> Optional[time]:
        """Get market open time as time object."""
        try:
            return datetime.strptime(self.local_open, "%H:%M").time()
        except (ValueError, TypeError):
            return None
    
    def get_close_time(self) -> Optional[time]:
        """Get market close time as time object."""
        try:
            return datetime.strptime(self.local_close, "%H:%M").time()
        except (ValueError, TypeError):
            return None
    
    def is_open(self) -> bool:
        """Check if market is currently open."""
        return self.current_status.lower() == "open"
    
    def is_closed(self) -> bool:
        """Check if market is currently closed."""
        return self.current_status.lower() == "closed"
    
    def is_pre_market(self) -> bool:
        """Check if market is in pre-market hours."""
        return "pre" in self.current_status.lower()
    
    def is_after_hours(self) -> bool:
        """Check if market is in after-hours trading."""
        return "after" in self.current_status.lower() or "extended" in self.current_status.lower()
    
    def get_exchanges_list(self) -> List[str]:
        """Get list of primary exchanges."""
        return [exchange.strip() for exchange in self.primary_exchanges.split(",")]
    
    def get_trading_hours_info(self) -> Dict[str, Any]:
        """Get comprehensive trading hours information."""
        return {
            "market_type": self.market_type,
            "region": self.region,
            "open_time": self.local_open,
            "close_time": self.local_close,
            "current_status": self.current_status,
            "is_open": self.is_open(),
            "is_closed": self.is_closed(),
            "is_pre_market": self.is_pre_market(),
            "is_after_hours": self.is_after_hours(),
            "exchanges": self.get_exchanges_list(),
            "notes": self.notes,
        }


class MarketStatusResponse(BaseResponse, MetadataMixin):
    """Response model for market status endpoint."""
    
    markets: List[MarketInfo] = Field(..., description="List of market information")
    
    def get_market_by_region(self, region: str) -> Optional[MarketInfo]:
        """Get market information for a specific region."""
        for market in self.markets:
            if market.region.lower() == region.lower():
                return market
        return None
    
    def get_market_by_type(self, market_type: str) -> List[MarketInfo]:
        """Get all markets of a specific type."""
        return [
            market for market in self.markets
            if market.market_type.lower() == market_type.lower()
        ]
    
    def get_open_markets(self) -> List[MarketInfo]:
        """Get all currently open markets."""
        return [market for market in self.markets if market.is_open()]
    
    def get_closed_markets(self) -> List[MarketInfo]:
        """Get all currently closed markets."""
        return [market for market in self.markets if market.is_closed()]
    
    def get_us_market(self) -> Optional[MarketInfo]:
        """Get US market information."""
        return self.get_market_by_region("United States")
    
    def is_us_market_open(self) -> bool:
        """Check if US market is currently open."""
        us_market = self.get_us_market()
        return us_market.is_open() if us_market else False
    
    def get_market_summary(self) -> Dict[str, Any]:
        """Get summary of all market statuses."""
        summary = {
            "total_markets": len(self.markets),
            "open_markets": len(self.get_open_markets()),
            "closed_markets": len(self.get_closed_markets()),
            "market_types": list(set(market.market_type for market in self.markets)),
            "regions": list(set(market.region for market in self.markets)),
        }
        
        # Add status breakdown
        status_counts = {}
        for market in self.markets:
            status = market.current_status
            status_counts[status] = status_counts.get(status, 0) + 1
        
        summary["status_breakdown"] = status_counts
        
        return summary
    
    def get_trading_schedule(self) -> Dict[str, Dict[str, str]]:
        """Get trading schedule for all markets."""
        schedule = {}
        for market in self.markets:
            key = f"{market.region} ({market.market_type})"
            schedule[key] = {
                "open": market.local_open,
                "close": market.local_close,
                "status": market.current_status,
                "exchanges": market.primary_exchanges,
            }
        return schedule
    
    def get_next_market_open(self) -> Optional[Dict[str, Any]]:
        """Get information about the next market to open."""
        closed_markets = self.get_closed_markets()
        if not closed_markets:
            return None
        
        # This is a simplified implementation
        # In a real scenario, you'd need timezone information and current time
        next_market = None
        earliest_open = None
        
        for market in closed_markets:
            open_time = market.get_open_time()
            if open_time and (earliest_open is None or open_time < earliest_open):
                earliest_open = open_time
                next_market = market
        
        if next_market:
            return {
                "market": next_market.region,
                "market_type": next_market.market_type,
                "open_time": next_market.local_open,
                "exchanges": next_market.get_exchanges_list(),
            }
        
        return None
