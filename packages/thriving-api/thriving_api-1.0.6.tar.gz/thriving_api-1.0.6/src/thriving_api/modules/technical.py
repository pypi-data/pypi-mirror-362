"""
Technical analysis module for the Thriving API SDK.

This module provides access to technical indicator endpoints including
moving averages, oscillators, and other technical analysis tools.
"""

from typing import List

from ..base_client import BaseClient
from ..models.technical import (
    SMAResponse, EMAResponse, RSIResponse, MACDResponse,
    BollingerBandsResponse, StochasticResponse, TechnicalIndicatorResponse
)
from ..exceptions import ValidationError, SymbolNotFoundError


class TechnicalModule:
    """Technical analysis endpoints wrapper."""
    
    # Valid intervals for technical indicators
    VALID_INTERVALS = ["1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"]
    
    def __init__(self, client: BaseClient) -> None:
        """
        Initialize Technical module.
        
        Args:
            client: Base HTTP client instance
        """
        self.client = client
    
    async def get_sma(self, symbol: str, interval: str, time_period: int) -> SMAResponse:
        """
        Get Simple Moving Average (SMA) indicator.
        
        Args:
            symbol: Stock symbol (e.g., "AAPL", "TSLA")
            interval: Time interval (daily, weekly, monthly, etc.)
            time_period: Number of periods for calculation
            
        Returns:
            SMAResponse: SMA indicator data
        """
        self._validate_inputs(symbol, interval, time_period)
        symbol = symbol.upper().strip()
        
        try:
            response_data = await self.client.get(f"/sma/{symbol}/{interval}/{time_period}")
            return SMAResponse(**response_data)
        except Exception as e:
            if "not found" in str(e).lower():
                raise SymbolNotFoundError(symbol) from e
            raise
    
    async def get_ema(self, symbol: str, interval: str, time_period: int) -> EMAResponse:
        """
        Get Exponential Moving Average (EMA) indicator.
        
        Args:
            symbol: Stock symbol (e.g., "AAPL", "TSLA")
            interval: Time interval (daily, weekly, monthly, etc.)
            time_period: Number of periods for calculation
            
        Returns:
            EMAResponse: EMA indicator data
        """
        self._validate_inputs(symbol, interval, time_period)
        symbol = symbol.upper().strip()
        
        try:
            response_data = await self.client.get(f"/ema/{symbol}/{interval}/{time_period}")
            return EMAResponse(**response_data)
        except Exception as e:
            if "not found" in str(e).lower():
                raise SymbolNotFoundError(symbol) from e
            raise
    
    async def get_rsi(self, symbol: str, interval: str, time_period: int) -> RSIResponse:
        """
        Get Relative Strength Index (RSI) indicator.
        
        Args:
            symbol: Stock symbol (e.g., "AAPL", "TSLA")
            interval: Time interval (daily, weekly, monthly, etc.)
            time_period: Number of periods for calculation (typically 14)
            
        Returns:
            RSIResponse: RSI indicator data
        """
        self._validate_inputs(symbol, interval, time_period)
        symbol = symbol.upper().strip()
        
        try:
            response_data = await self.client.get(f"/rsi/{symbol}/{interval}/{time_period}")
            return RSIResponse(**response_data)
        except Exception as e:
            if "not found" in str(e).lower():
                raise SymbolNotFoundError(symbol) from e
            raise
    
    async def get_macd(self, symbol: str, interval: str) -> MACDResponse:
        """
        Get MACD (Moving Average Convergence Divergence) indicator.
        
        Args:
            symbol: Stock symbol (e.g., "AAPL", "TSLA")
            interval: Time interval (daily, weekly, monthly, etc.)
            
        Returns:
            MACDResponse: MACD indicator data
        """
        self._validate_symbol_interval(symbol, interval)
        symbol = symbol.upper().strip()
        
        try:
            response_data = await self.client.get(f"/macd/{symbol}/{interval}")
            return MACDResponse(**response_data)
        except Exception as e:
            if "not found" in str(e).lower():
                raise SymbolNotFoundError(symbol) from e
            raise
    
    async def get_bollinger_bands(self, symbol: str, interval: str, time_period: int) -> BollingerBandsResponse:
        """
        Get Bollinger Bands indicator.
        
        Args:
            symbol: Stock symbol (e.g., "AAPL", "TSLA")
            interval: Time interval (daily, weekly, monthly, etc.)
            time_period: Number of periods for calculation (typically 20)
            
        Returns:
            BollingerBandsResponse: Bollinger Bands data
        """
        self._validate_inputs(symbol, interval, time_period)
        symbol = symbol.upper().strip()
        
        try:
            response_data = await self.client.get(f"/bbands/{symbol}/{interval}/{time_period}")
            return BollingerBandsResponse(**response_data)
        except Exception as e:
            if "not found" in str(e).lower():
                raise SymbolNotFoundError(symbol) from e
            raise
    
    async def get_stochastic(self, symbol: str, interval: str) -> StochasticResponse:
        """
        Get Stochastic Oscillator indicator.
        
        Args:
            symbol: Stock symbol (e.g., "AAPL", "TSLA")
            interval: Time interval (daily, weekly, monthly, etc.)
            
        Returns:
            StochasticResponse: Stochastic oscillator data
        """
        self._validate_symbol_interval(symbol, interval)
        symbol = symbol.upper().strip()
        
        try:
            response_data = await self.client.get(f"/stoch/{symbol}/{interval}")
            return StochasticResponse(**response_data)
        except Exception as e:
            if "not found" in str(e).lower():
                raise SymbolNotFoundError(symbol) from e
            raise
    
    # Generic method for other technical indicators
    async def get_indicator(self, indicator: str, symbol: str, interval: str, time_period: int = None) -> TechnicalIndicatorResponse:
        """
        Get any technical indicator by name.
        
        Args:
            indicator: Indicator name (e.g., "adx", "cci", "williams", etc.)
            symbol: Stock symbol (e.g., "AAPL", "TSLA")
            interval: Time interval (daily, weekly, monthly, etc.)
            time_period: Number of periods for calculation (if required)
            
        Returns:
            TechnicalIndicatorResponse: Technical indicator data
        """
        self._validate_symbol_interval(symbol, interval)
        symbol = symbol.upper().strip()
        
        # Build endpoint URL
        if time_period:
            endpoint = f"/{indicator}/{symbol}/{interval}/{time_period}"
        else:
            endpoint = f"/{indicator}/{symbol}/{interval}"
        
        try:
            response_data = await self.client.get(endpoint)
            return TechnicalIndicatorResponse(**response_data)
        except Exception as e:
            if "not found" in str(e).lower():
                raise SymbolNotFoundError(symbol) from e
            raise
    
    def _validate_inputs(self, symbol: str, interval: str, time_period: int) -> None:
        """Validate common inputs for technical indicators."""
        self._validate_symbol_interval(symbol, interval)
        
        if not isinstance(time_period, int) or time_period < 1:
            raise ValidationError("Time period must be a positive integer")
        
        if time_period > 200:
            raise ValidationError("Time period cannot exceed 200")
    
    def _validate_symbol_interval(self, symbol: str, interval: str) -> None:
        """Validate symbol and interval."""
        if not self._validate_symbol(symbol):
            raise ValidationError(f"Invalid symbol format: {symbol}")
        
        if interval not in self.VALID_INTERVALS:
            raise ValidationError(
                f"Invalid interval: {interval}. "
                f"Valid intervals: {', '.join(self.VALID_INTERVALS)}"
            )
    
    def _validate_symbol(self, symbol: str) -> bool:
        """Validate symbol format."""
        if not symbol or not isinstance(symbol, str):
            return False
        
        symbol = symbol.upper().strip()
        return (
            symbol.replace(".", "").replace("-", "").isalnum() and 
            1 <= len(symbol) <= 10
        )
    
    def get_valid_intervals(self) -> List[str]:
        """Get list of valid intervals."""
        return self.VALID_INTERVALS.copy()
    
    def is_valid_interval(self, interval: str) -> bool:
        """Check if interval is valid."""
        return interval in self.VALID_INTERVALS
