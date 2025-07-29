"""
Symbol data module for the Thriving API SDK.

This module provides access to symbol-related endpoints including
search, performance, live quotes, OHLC data, and news.
"""

from typing import List, Optional

from ..base_client import BaseClient
from ..models.symbol import (
    SymbolSearchResponse, PerformanceResponse, LiveQuoteResponse,
    OHLCResponse, NewsResponse
)
from ..exceptions import ValidationError, SymbolNotFoundError


class SymbolModule:
    """Symbol data endpoints wrapper."""
    
    # Valid intervals for different endpoints
    PERFORMANCE_INTERVALS = ["1mo", "3mo", "6mo", "1yr", "5yr", "10yr"]
    QUOTE_INTERVALS = ["1min", "5min", "15min", "30min", "60min"]
    
    def __init__(self, client: BaseClient) -> None:
        """
        Initialize Symbol module.
        
        Args:
            client: Base HTTP client instance
        """
        self.client = client
    
    async def search(self, query: str) -> SymbolSearchResponse:
        """
        Search and validate stock symbols with detailed company information.
        
        This endpoint allows you to search for stock symbols and returns 
        comprehensive information about matching companies.
        
        Args:
            query: Search query (symbol or company name)
            
        Returns:
            SymbolSearchResponse: Search results with symbol matches
            
        Raises:
            ValidationError: If query is invalid
            ThrivingAPIError: For other API errors
            
        Example:
            >>> client = ThrivingAPI(api_key="your-api-key")
            >>> results = await client.symbol.search("AAPL")
            >>> best_match = results.results.get_best_match()
            >>> print(f"Symbol: {best_match.symbol}, Name: {best_match.name}")
        """
        if not query or not isinstance(query, str):
            raise ValidationError("Query must be a non-empty string")
        
        query = query.strip()
        if len(query) < 1:
            raise ValidationError("Query cannot be empty")
        
        response_data = await self.client.get(f"/search/{query}")
        return SymbolSearchResponse(**response_data)
    
    async def get_performance(self, symbol: str, interval: str) -> PerformanceResponse:
        """
        Get comprehensive performance metrics and returns analysis for a stock.
        
        This endpoint provides detailed performance data including returns 
        analysis for various time periods.
        
        Args:
            symbol: Stock symbol (e.g., "AAPL", "TSLA")
            interval: Time interval (1mo, 3mo, 6mo, 1yr, 5yr, 10yr)
            
        Returns:
            PerformanceResponse: Performance metrics and returns data
            
        Raises:
            ValidationError: If symbol or interval is invalid
            SymbolNotFoundError: If symbol is not found
            ThrivingAPIError: For other API errors
            
        Example:
            >>> client = ThrivingAPI(api_key="your-api-key")
            >>> performance = await client.symbol.get_performance("AAPL", "1yr")
            >>> yearly_return = performance.get_performance_float("1yr")
            >>> print(f"1-year return: {yearly_return}%")
        """
        # Validate symbol
        if not self._validate_symbol(symbol):
            raise ValidationError(f"Invalid symbol format: {symbol}")
        
        # Validate interval
        if interval not in self.PERFORMANCE_INTERVALS:
            raise ValidationError(
                f"Invalid interval: {interval}. "
                f"Valid intervals: {', '.join(self.PERFORMANCE_INTERVALS)}"
            )
        
        symbol = symbol.upper().strip()
        
        try:
            response_data = await self.client.get(f"/performance/market/{symbol}/{interval}")
            return PerformanceResponse(**response_data)
        except Exception as e:
            if "not found" in str(e).lower():
                raise SymbolNotFoundError(symbol) from e
            raise
    
    async def get_live_quote(self, symbol: str, interval: str) -> LiveQuoteResponse:
        """
        Get real-time stock quotes with OHLCV data.
        
        This endpoint provides live market data including current stock price,
        OHLC values, trading volume, and price changes.
        
        Args:
            symbol: Stock symbol (e.g., "AAPL", "TSLA")
            interval: Time interval (1min, 5min, 15min, 30min, 60min)
            
        Returns:
            LiveQuoteResponse: Real-time quote data
            
        Raises:
            ValidationError: If symbol or interval is invalid
            SymbolNotFoundError: If symbol is not found
            ThrivingAPIError: For other API errors
            
        Example:
            >>> client = ThrivingAPI(api_key="your-api-key")
            >>> quote = await client.symbol.get_live_quote("AAPL", "1min")
            >>> latest = quote.get_latest_quote()
            >>> print(f"Current price: ${latest.get_close()}")
            >>> print(f"Volume: {latest.get_volume():,}")
        """
        # Validate symbol
        if not self._validate_symbol(symbol):
            raise ValidationError(f"Invalid symbol format: {symbol}")
        
        # Validate interval
        if interval not in self.QUOTE_INTERVALS:
            raise ValidationError(
                f"Invalid interval: {interval}. "
                f"Valid intervals: {', '.join(self.QUOTE_INTERVALS)}"
            )
        
        symbol = symbol.upper().strip()
        
        try:
            response_data = await self.client.get(f"/live-quote/{symbol}/{interval}")
            return LiveQuoteResponse(**response_data)
        except Exception as e:
            if "not found" in str(e).lower():
                raise SymbolNotFoundError(symbol) from e
            raise
    
    async def get_ohlc_daily(self, symbol: str) -> OHLCResponse:
        """
        Get historical daily OHLC (Open, High, Low, Close) data with volume.
        
        This endpoint provides comprehensive daily trading data including
        OHLC prices, volume, dividends, and corporate events.
        
        Args:
            symbol: Stock symbol (e.g., "AAPL", "TSLA")
            
        Returns:
            OHLCResponse: Historical daily OHLC data
            
        Raises:
            ValidationError: If symbol is invalid
            SymbolNotFoundError: If symbol is not found
            ThrivingAPIError: For other API errors
            
        Example:
            >>> client = ThrivingAPI(api_key="your-api-key")
            >>> ohlc = await client.symbol.get_ohlc_daily("AAPL")
            >>> latest = ohlc.get_latest_data()
            >>> print(f"Latest close: ${latest.get_close()}")
            >>> print(f"Date: {latest.date}")
        """
        # Validate symbol
        if not self._validate_symbol(symbol):
            raise ValidationError(f"Invalid symbol format: {symbol}")
        
        symbol = symbol.upper().strip()
        
        try:
            response_data = await self.client.get(f"/ohlc-daily/{symbol}")
            return OHLCResponse(**response_data)
        except Exception as e:
            if "not found" in str(e).lower():
                raise SymbolNotFoundError(symbol) from e
            raise
    
    async def get_news(self, symbol: str) -> NewsResponse:
        """
        Get latest news articles and press releases for a specific stock symbol.
        
        This endpoint provides recent news coverage including company news,
        market analysis, earnings announcements, and sentiment analysis.
        
        Args:
            symbol: Stock symbol (e.g., "AAPL", "TSLA")
            
        Returns:
            NewsResponse: News articles and sentiment data
            
        Raises:
            ValidationError: If symbol is invalid
            SymbolNotFoundError: If symbol is not found
            ThrivingAPIError: For other API errors
            
        Example:
            >>> client = ThrivingAPI(api_key="your-api-key")
            >>> news = await client.symbol.get_news("AAPL")
            >>> latest_article = news.get_latest_article()
            >>> print(f"Title: {latest_article.title}")
            >>> print(f"Sentiment: {latest_article.overall_sentiment_label}")
        """
        # Validate symbol
        if not self._validate_symbol(symbol):
            raise ValidationError(f"Invalid symbol format: {symbol}")
        
        symbol = symbol.upper().strip()
        
        try:
            response_data = await self.client.get(f"/news/{symbol}")
            return NewsResponse(**response_data)
        except Exception as e:
            if "not found" in str(e).lower():
                raise SymbolNotFoundError(symbol) from e
            raise
    
    def _validate_symbol(self, symbol: str) -> bool:
        """
        Validate symbol format.
        
        Args:
            symbol: Stock symbol to validate
            
        Returns:
            bool: True if symbol format is valid
        """
        if not symbol or not isinstance(symbol, str):
            return False
        
        symbol = symbol.upper().strip()
        return (
            symbol.replace(".", "").replace("-", "").isalnum() and 
            1 <= len(symbol) <= 10
        )
    
    def get_valid_performance_intervals(self) -> List[str]:
        """
        Get list of valid performance intervals.
        
        Returns:
            List[str]: Valid performance intervals
        """
        return self.PERFORMANCE_INTERVALS.copy()
    
    def get_valid_quote_intervals(self) -> List[str]:
        """
        Get list of valid quote intervals.
        
        Returns:
            List[str]: Valid quote intervals
        """
        return self.QUOTE_INTERVALS.copy()
    
    def is_valid_performance_interval(self, interval: str) -> bool:
        """
        Check if performance interval is valid.
        
        Args:
            interval: Interval to validate
            
        Returns:
            bool: True if interval is valid
        """
        return interval in self.PERFORMANCE_INTERVALS
    
    def is_valid_quote_interval(self, interval: str) -> bool:
        """
        Check if quote interval is valid.
        
        Args:
            interval: Interval to validate
            
        Returns:
            bool: True if interval is valid
        """
        return interval in self.QUOTE_INTERVALS
