"""
Data models for the Thriving API SDK.

This module contains all Pydantic models for request/response validation
and type safety across the SDK.
"""

from .base import BaseResponse, ErrorResponse
from .ai import AIAnalysisResponse, AIAnalysis
from .symbol import (
    SymbolSearchResponse, SymbolMatch, SymbolSearchResults,
    PerformanceResponse, LiveQuoteResponse, OHLCResponse, OHLCData,
    NewsResponse, NewsItem, NewsFeed
)
from .company import (
    FundamentalsResponse, CompanyFundamentals,
    EarningsResponse, CompanyEarnings,
    CompanyDetailsResponse, CompanyDetails
)
from .technical import (
    TechnicalIndicatorResponse, TechnicalDataPoint,
    SMAResponse, EMAResponse, RSIResponse, MACDResponse,
    BollingerBandsResponse, StochasticResponse
)
from .options import (
    OptionsChainResponse, OptionContract, OptionsData
)
from .market import (
    MarketStatusResponse, MarketInfo
)

__all__ = [
    # Base models
    "BaseResponse",
    "ErrorResponse",
    
    # AI models
    "AIAnalysisResponse",
    "AIAnalysis",
    
    # Symbol models
    "SymbolSearchResponse",
    "SymbolMatch", 
    "SymbolSearchResults",
    "PerformanceResponse",
    "LiveQuoteResponse",
    "OHLCResponse",
    "OHLCData",
    "NewsResponse",
    "NewsItem",
    "NewsFeed",
    
    # Company models
    "FundamentalsResponse",
    "CompanyFundamentals",
    "EarningsResponse", 
    "CompanyEarnings",
    "CompanyDetailsResponse",
    "CompanyDetails",
    
    # Technical models
    "TechnicalIndicatorResponse",
    "TechnicalDataPoint",
    "SMAResponse",
    "EMAResponse", 
    "RSIResponse",
    "MACDResponse",
    "BollingerBandsResponse",
    "StochasticResponse",
    
    # Options models
    "OptionsChainResponse",
    "OptionContract",
    "OptionsData",
    
    # Market models
    "MarketStatusResponse",
    "MarketInfo",
]
