"""
Technical analysis models for the Thriving API SDK.

This module contains Pydantic models for technical indicator endpoints
including moving averages, oscillators, and other technical analysis tools.
"""

from typing import Dict, List, Optional, Union, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime

from .base import (
    BaseResponse, SymbolMixin, TimestampMixin, MetadataMixin,
    PriceType, IntervalType
)


class TechnicalDataPoint(BaseModel, TimestampMixin):
    """Base model for technical indicator data points."""
    
    value: Optional[Union[str, float]] = Field(None, description="Indicator value")
    
    def get_value(self) -> Optional[float]:
        """Get indicator value as float."""
        return float(self.value) if self.value is not None else None


class TechnicalIndicatorResponse(BaseResponse, MetadataMixin):
    """Base response model for technical indicators."""
    
    symbol: Optional[str] = Field(None, description="Stock symbol")
    interval: Optional[str] = Field(None, description="Time interval")
    time_period: Optional[int] = Field(None, description="Indicator time period")
    data: Dict[str, Union[str, float]] = Field(..., description="Technical indicator data")
    
    def get_latest_value(self) -> Optional[float]:
        """Get the most recent indicator value."""
        if not self.data:
            return None
        
        # Get the most recent date key
        latest_date = max(self.data.keys())
        value = self.data[latest_date]
        
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
    
    def get_values_list(self) -> List[float]:
        """Get all indicator values as a list of floats."""
        values = []
        for date_key in sorted(self.data.keys(), reverse=True):
            try:
                values.append(float(self.data[date_key]))
            except (ValueError, TypeError):
                continue
        return values
    
    def get_data_for_date(self, date_str: str) -> Optional[float]:
        """Get indicator value for a specific date."""
        value = self.data.get(date_str)
        try:
            return float(value) if value is not None else None
        except (ValueError, TypeError):
            return None


class SMAResponse(TechnicalIndicatorResponse):
    """Response model for Simple Moving Average (SMA) endpoint."""
    
    def get_trend_direction(self, periods: int = 5) -> Optional[str]:
        """Determine trend direction based on recent SMA values."""
        values = self.get_values_list()[:periods]
        if len(values) < 2:
            return None
        
        increasing = sum(1 for i in range(1, len(values)) if values[i-1] < values[i])
        decreasing = sum(1 for i in range(1, len(values)) if values[i-1] > values[i])
        
        if increasing > decreasing:
            return "Upward"
        elif decreasing > increasing:
            return "Downward"
        else:
            return "Sideways"


class EMAResponse(TechnicalIndicatorResponse):
    """Response model for Exponential Moving Average (EMA) endpoint."""
    
    def compare_with_sma(self, sma_response: SMAResponse) -> Optional[str]:
        """Compare EMA with SMA to gauge momentum."""
        ema_value = self.get_latest_value()
        sma_value = sma_response.get_latest_value()
        
        if ema_value is None or sma_value is None:
            return None
        
        if ema_value > sma_value:
            return "Bullish momentum"
        elif ema_value < sma_value:
            return "Bearish momentum"
        else:
            return "Neutral momentum"


class RSIDataPoint(BaseModel, TimestampMixin):
    """RSI indicator data point."""
    
    rsi: Union[str, float] = Field(..., description="RSI value")
    
    def get_rsi(self) -> Optional[float]:
        """Get RSI value as float."""
        try:
            return float(self.rsi)
        except (ValueError, TypeError):
            return None
    
    def get_signal(self) -> str:
        """Get RSI signal interpretation."""
        rsi_val = self.get_rsi()
        if rsi_val is None:
            return "Unknown"
        
        if rsi_val >= 70:
            return "Overbought"
        elif rsi_val <= 30:
            return "Oversold"
        elif rsi_val >= 60:
            return "Bullish"
        elif rsi_val <= 40:
            return "Bearish"
        else:
            return "Neutral"


class RSIResponse(BaseResponse, MetadataMixin):
    """Response model for RSI endpoint."""
    
    symbol: Optional[str] = Field(None, description="Stock symbol")
    interval: Optional[str] = Field(None, description="Time interval")
    time_period: Optional[int] = Field(None, description="RSI time period")
    data: Dict[str, RSIDataPoint] = Field(..., description="RSI data points")
    
    def get_latest_rsi(self) -> Optional[RSIDataPoint]:
        """Get the most recent RSI data point."""
        if not self.data:
            return None
        latest_date = max(self.data.keys())
        return self.data[latest_date]
    
    def get_current_signal(self) -> str:
        """Get current RSI signal."""
        latest = self.get_latest_rsi()
        return latest.get_signal() if latest else "Unknown"
    
    def is_divergence_present(self, price_data: List[float], periods: int = 5) -> Optional[bool]:
        """Check for RSI divergence with price."""
        if len(price_data) < periods or len(self.data) < periods:
            return None
        
        rsi_values = []
        for date_key in sorted(self.data.keys(), reverse=True)[:periods]:
            rsi_point = self.data[date_key]
            rsi_val = rsi_point.get_rsi()
            if rsi_val is not None:
                rsi_values.append(rsi_val)
        
        if len(rsi_values) < periods:
            return None
        
        # Simple divergence check: price making higher highs while RSI makes lower highs
        price_trend = price_data[0] > price_data[-1]  # Recent vs older
        rsi_trend = rsi_values[0] > rsi_values[-1]
        
        return price_trend != rsi_trend


class MACDDataPoint(BaseModel, TimestampMixin):
    """MACD indicator data point."""
    
    macd: Union[str, float] = Field(..., description="MACD line value")
    signal: Union[str, float] = Field(..., description="Signal line value")
    histogram: Union[str, float] = Field(..., description="MACD histogram value")
    
    def get_macd(self) -> Optional[float]:
        """Get MACD value as float."""
        try:
            return float(self.macd)
        except (ValueError, TypeError):
            return None
    
    def get_signal(self) -> Optional[float]:
        """Get signal line value as float."""
        try:
            return float(self.signal)
        except (ValueError, TypeError):
            return None
    
    def get_histogram(self) -> Optional[float]:
        """Get histogram value as float."""
        try:
            return float(self.histogram)
        except (ValueError, TypeError):
            return None
    
    def get_crossover_signal(self) -> str:
        """Get MACD crossover signal."""
        macd_val = self.get_macd()
        signal_val = self.get_signal()
        
        if macd_val is None or signal_val is None:
            return "Unknown"
        
        if macd_val > signal_val:
            return "Bullish"
        elif macd_val < signal_val:
            return "Bearish"
        else:
            return "Neutral"


class MACDResponse(BaseResponse, MetadataMixin):
    """Response model for MACD endpoint."""
    
    symbol: Optional[str] = Field(None, description="Stock symbol")
    interval: Optional[str] = Field(None, description="Time interval")
    data: Dict[str, MACDDataPoint] = Field(..., description="MACD data points")
    
    def get_latest_macd(self) -> Optional[MACDDataPoint]:
        """Get the most recent MACD data point."""
        if not self.data:
            return None
        latest_date = max(self.data.keys())
        return self.data[latest_date]
    
    def get_current_signal(self) -> str:
        """Get current MACD signal."""
        latest = self.get_latest_macd()
        return latest.get_crossover_signal() if latest else "Unknown"
    
    def detect_crossover(self, periods: int = 2) -> Optional[str]:
        """Detect recent MACD crossover."""
        if len(self.data) < periods:
            return None
        
        recent_dates = sorted(self.data.keys(), reverse=True)[:periods]
        signals = [self.data[date].get_crossover_signal() for date in recent_dates]
        
        if len(set(signals)) > 1:  # Signal changed
            return f"Crossover detected: {signals[0]}"
        
        return None


class BollingerBandsDataPoint(BaseModel, TimestampMixin):
    """Bollinger Bands data point."""
    
    upper_band: Union[str, float] = Field(..., description="Upper Bollinger Band")
    middle_band: Union[str, float] = Field(..., description="Middle Bollinger Band (SMA)")
    lower_band: Union[str, float] = Field(..., description="Lower Bollinger Band")
    
    def get_upper_band(self) -> Optional[float]:
        """Get upper band value as float."""
        try:
            return float(self.upper_band)
        except (ValueError, TypeError):
            return None
    
    def get_middle_band(self) -> Optional[float]:
        """Get middle band value as float."""
        try:
            return float(self.middle_band)
        except (ValueError, TypeError):
            return None
    
    def get_lower_band(self) -> Optional[float]:
        """Get lower band value as float."""
        try:
            return float(self.lower_band)
        except (ValueError, TypeError):
            return None
    
    def get_band_width(self) -> Optional[float]:
        """Calculate Bollinger Band width."""
        upper = self.get_upper_band()
        lower = self.get_lower_band()
        
        if upper is None or lower is None:
            return None
        
        return upper - lower
    
    def get_price_position(self, price: float) -> Optional[str]:
        """Determine price position relative to bands."""
        upper = self.get_upper_band()
        lower = self.get_lower_band()
        
        if upper is None or lower is None:
            return None
        
        if price > upper:
            return "Above upper band"
        elif price < lower:
            return "Below lower band"
        else:
            return "Within bands"


class BollingerBandsResponse(BaseResponse, MetadataMixin):
    """Response model for Bollinger Bands endpoint."""
    
    symbol: Optional[str] = Field(None, description="Stock symbol")
    interval: Optional[str] = Field(None, description="Time interval")
    time_period: Optional[int] = Field(None, description="Time period")
    data: Dict[str, BollingerBandsDataPoint] = Field(..., description="Bollinger Bands data")
    
    def get_latest_bands(self) -> Optional[BollingerBandsDataPoint]:
        """Get the most recent Bollinger Bands data."""
        if not self.data:
            return None
        latest_date = max(self.data.keys())
        return self.data[latest_date]
    
    def get_volatility_trend(self, periods: int = 5) -> Optional[str]:
        """Analyze volatility trend based on band width."""
        if len(self.data) < periods:
            return None
        
        recent_dates = sorted(self.data.keys(), reverse=True)[:periods]
        widths = []
        
        for date in recent_dates:
            width = self.data[date].get_band_width()
            if width is not None:
                widths.append(width)
        
        if len(widths) < 2:
            return None
        
        if widths[0] > widths[-1]:
            return "Increasing volatility"
        elif widths[0] < widths[-1]:
            return "Decreasing volatility"
        else:
            return "Stable volatility"


class StochasticDataPoint(BaseModel, TimestampMixin):
    """Stochastic oscillator data point."""
    
    k_percent: Union[str, float] = Field(..., description="%K value")
    d_percent: Union[str, float] = Field(..., description="%D value")
    
    def get_k_percent(self) -> Optional[float]:
        """Get %K value as float."""
        try:
            return float(self.k_percent)
        except (ValueError, TypeError):
            return None
    
    def get_d_percent(self) -> Optional[float]:
        """Get %D value as float."""
        try:
            return float(self.d_percent)
        except (ValueError, TypeError):
            return None
    
    def get_signal(self) -> str:
        """Get stochastic signal interpretation."""
        k_val = self.get_k_percent()
        d_val = self.get_d_percent()
        
        if k_val is None or d_val is None:
            return "Unknown"
        
        if k_val >= 80 and d_val >= 80:
            return "Overbought"
        elif k_val <= 20 and d_val <= 20:
            return "Oversold"
        elif k_val > d_val:
            return "Bullish crossover"
        elif k_val < d_val:
            return "Bearish crossover"
        else:
            return "Neutral"


class StochasticResponse(BaseResponse, MetadataMixin):
    """Response model for Stochastic oscillator endpoint."""
    
    symbol: Optional[str] = Field(None, description="Stock symbol")
    interval: Optional[str] = Field(None, description="Time interval")
    data: Dict[str, StochasticDataPoint] = Field(..., description="Stochastic data points")
    
    def get_latest_stochastic(self) -> Optional[StochasticDataPoint]:
        """Get the most recent stochastic data point."""
        if not self.data:
            return None
        latest_date = max(self.data.keys())
        return self.data[latest_date]
    
    def get_current_signal(self) -> str:
        """Get current stochastic signal."""
        latest = self.get_latest_stochastic()
        return latest.get_signal() if latest else "Unknown"
