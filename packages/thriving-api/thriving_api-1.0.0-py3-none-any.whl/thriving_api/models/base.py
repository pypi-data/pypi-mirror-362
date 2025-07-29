"""
Base models for the Thriving API SDK.

This module contains base Pydantic models that are used across
all API response types.
"""

from typing import Any, Dict, List, Optional, Union
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class BaseResponse(BaseModel):
    """Base response model for all API responses."""
    
    model_config = ConfigDict(
        extra="allow",  # Allow extra fields for forward compatibility
        str_strip_whitespace=True,
        validate_assignment=True,
    )
    
    success: bool = Field(..., description="Whether the request was successful")


class ErrorResponse(BaseResponse):
    """Error response model."""
    
    success: bool = Field(False, description="Always false for error responses")
    error: str = Field(..., description="Error message")
    message: Optional[str] = Field(None, description="Additional error details")
    errors: Optional[List[str]] = Field(None, description="List of validation errors")


class PaginatedResponse(BaseResponse):
    """Base model for paginated responses."""
    
    total_count: Optional[int] = Field(None, description="Total number of items")
    page: Optional[int] = Field(None, description="Current page number")
    per_page: Optional[int] = Field(None, description="Items per page")
    has_more: Optional[bool] = Field(None, description="Whether there are more pages")


class TimestampMixin(BaseModel):
    """Mixin for models that include timestamp information."""
    
    timestamp: Optional[Union[int, datetime]] = Field(None, description="Unix timestamp or datetime")
    date: Optional[str] = Field(None, description="Date string (YYYY-MM-DD format)")
    
    def get_datetime(self) -> Optional[datetime]:
        """Convert timestamp to datetime object."""
        if isinstance(self.timestamp, datetime):
            return self.timestamp
        elif isinstance(self.timestamp, (int, float)):
            return datetime.fromtimestamp(self.timestamp)
        return None


class SymbolMixin(BaseModel):
    """Mixin for models that include symbol information."""
    
    symbol: str = Field(..., description="Stock symbol (e.g., AAPL, TSLA)")
    
    def get_symbol_upper(self) -> str:
        """Get symbol in uppercase."""
        return self.symbol.upper()


class MarketDataMixin(BaseModel):
    """Mixin for models that include basic market data."""
    
    open: Optional[Union[str, float]] = Field(None, description="Opening price")
    high: Optional[Union[str, float]] = Field(None, description="High price")
    low: Optional[Union[str, float]] = Field(None, description="Low price")
    close: Optional[Union[str, float]] = Field(None, description="Closing price")
    volume: Optional[Union[str, int]] = Field(None, description="Trading volume")
    
    def get_open(self) -> Optional[float]:
        """Get opening price as float."""
        return float(self.open) if self.open is not None else None
    
    def get_high(self) -> Optional[float]:
        """Get high price as float."""
        return float(self.high) if self.high is not None else None
    
    def get_low(self) -> Optional[float]:
        """Get low price as float."""
        return float(self.low) if self.low is not None else None
    
    def get_close(self) -> Optional[float]:
        """Get closing price as float."""
        return float(self.close) if self.close is not None else None
    
    def get_volume(self) -> Optional[int]:
        """Get volume as integer."""
        return int(self.volume) if self.volume is not None else None


class ValidationMixin(BaseModel):
    """Mixin that provides common validation methods."""
    
    def is_valid_symbol(self, symbol: str) -> bool:
        """Check if symbol format is valid."""
        if not symbol or not isinstance(symbol, str):
            return False
        # Basic symbol validation - alphanumeric and dots/hyphens
        return symbol.replace(".", "").replace("-", "").isalnum() and len(symbol) <= 10
    
    def is_valid_interval(self, interval: str, valid_intervals: List[str]) -> bool:
        """Check if interval is valid."""
        return interval in valid_intervals
    
    def is_positive_number(self, value: Union[str, int, float]) -> bool:
        """Check if value is a positive number."""
        try:
            return float(value) > 0
        except (ValueError, TypeError):
            return False


class MetadataMixin(BaseModel):
    """Mixin for API metadata information."""
    
    request_id: Optional[str] = Field(None, description="Unique request identifier")
    processing_time_ms: Optional[int] = Field(None, description="Processing time in milliseconds")
    cached: Optional[bool] = Field(None, description="Whether response was cached")
    data_source: Optional[str] = Field(None, description="Source of the data")
    last_updated: Optional[Union[int, datetime, str]] = Field(None, description="When data was last updated")


# Common field validators and types
SymbolType = str
IntervalType = str
PriceType = Union[str, float]
VolumeType = Union[str, int]
TimestampType = Union[int, datetime, str]
PercentageType = Union[str, float]
