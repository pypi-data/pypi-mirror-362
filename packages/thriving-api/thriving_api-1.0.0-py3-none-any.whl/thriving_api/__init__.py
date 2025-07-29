"""
Thriving API Python SDK

Official Python SDK for the Thriving API - AI-powered financial analysis and trading intelligence.

This SDK provides comprehensive access to:
- AI-powered stock analysis and trading recommendations
- Real-time and historical market data
- Technical indicators and analysis tools
- Company fundamentals and earnings data
- Options chain data
- Market status and news

Example:
    >>> from thriving_api import ThrivingAPI
    >>> client = ThrivingAPI(api_key="your-api-key")
    >>> analysis = client.ai.analyze_symbol("AAPL")
    >>> print(analysis.action)  # "buy", "sell", or "wait"
"""

from .client import ThrivingAPI
from .exceptions import (
    ThrivingAPIError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    APIConnectionError,
)

__version__ = "1.0.0"
__author__ = "Thriving"
__email__ = "support@tradethriving.com"

__all__ = [
    "ThrivingAPI",
    "ThrivingAPIError",
    "AuthenticationError", 
    "RateLimitError",
    "ValidationError",
    "APIConnectionError",
]
