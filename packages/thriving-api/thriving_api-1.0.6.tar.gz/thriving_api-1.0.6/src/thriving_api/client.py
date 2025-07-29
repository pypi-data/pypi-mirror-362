"""
Main client for the Thriving API SDK.

This module provides the primary ThrivingAPI client class that serves as the
entry point for all API interactions.
"""

from typing import Optional

from .base_client import BaseClient
from .modules import AIModule, SymbolModule, CompanyModule, TechnicalModule, OptionsModule, MarketModule
from .exceptions import AuthenticationError


class ThrivingAPI:
    """
    Main client for the Thriving API.
    
    This is the primary interface for interacting with the Thriving API.
    It provides access to all API endpoints through specialized modules.
    
    Example:
        >>> # Initialize client
        >>> client = ThrivingAPI(api_key="your-api-key")
        >>> 
        >>> # Get AI analysis
        >>> analysis = await client.ai.analyze_symbol("AAPL")
        >>> print(f"Action: {analysis.analysis.action}")
        >>> 
        >>> # Search for symbols
        >>> results = await client.symbol.search("Apple")
        >>> 
        >>> # Get company fundamentals
        >>> fundamentals = await client.company.get_fundamentals("AAPL")
        >>> 
        >>> # Get technical indicators
        >>> rsi = await client.technical.get_rsi("AAPL", "daily", 14)
        >>> 
        >>> # Get options chain
        >>> options = await client.options.get_chain("AAPL")
        >>> 
        >>> # Get market status
        >>> status = await client.market.get_status()
        >>> 
        >>> # Close client when done
        >>> await client.close()
    
    Context Manager Usage:
        >>> async with ThrivingAPI(api_key="your-api-key") as client:
        ...     analysis = await client.ai.analyze_symbol("AAPL")
        ...     print(analysis.analysis.action)
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
        max_retries: int = 3,
        requests_per_second: int = 30,
        burst_limit: int = 60,
        enable_rate_limiting: bool = True,
    ) -> None:
        """
        Initialize the Thriving API client.
        
        Args:
            api_key: Your Thriving API key (required)
            base_url: Override the default API base URL
            timeout: Request timeout in seconds (default: 30.0)
            max_retries: Maximum number of retry attempts (default: 3)
            requests_per_second: Rate limit for requests per second (default: 30)
            burst_limit: Maximum burst requests allowed (default: 60)
            enable_rate_limiting: Whether to enable client-side rate limiting (default: True)
            
        Raises:
            AuthenticationError: If API key is invalid or missing
            
        Example:
            >>> # Basic usage
            >>> client = ThrivingAPI(api_key="your-api-key")
            >>> 
            >>> # Custom configuration
            >>> client = ThrivingAPI(
            ...     api_key="your-api-key",
            ...     timeout=60.0,
            ...     max_retries=5,
            ...     requests_per_second=20
            ... )
        """
        # Validate API key
        if not api_key or not isinstance(api_key, str):
            raise AuthenticationError("API key is required and must be a non-empty string")
        
        api_key = api_key.strip()
        if not api_key:
            raise AuthenticationError("API key cannot be empty")
        
        # Initialize base client
        self._base_client = BaseClient(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            requests_per_second=requests_per_second,
            burst_limit=burst_limit,
            enable_rate_limiting=enable_rate_limiting,
        )
        
        # Initialize API modules
        self.ai = AIModule(self._base_client)
        self.symbol = SymbolModule(self._base_client)
        self.company = CompanyModule(self._base_client)
        self.technical = TechnicalModule(self._base_client)
        self.options = OptionsModule(self._base_client)
        self.market = MarketModule(self._base_client)
    
    async def close(self) -> None:
        """
        Close the HTTP client and clean up resources.
        
        This should be called when you're done using the client to properly
        close HTTP connections and free resources.
        
        Example:
            >>> client = ThrivingAPI(api_key="your-api-key")
            >>> # ... use client ...
            >>> await client.close()
        """
        await self._base_client.close()
    
    def get_stats(self) -> dict:
        """
        Get client statistics including request counts and rate limiting info.
        
        Returns:
            dict: Client statistics and metrics
            
        Example:
            >>> client = ThrivingAPI(api_key="your-api-key")
            >>> stats = client.get_stats()
            >>> print(f"Total requests: {stats['total_requests']}")
            >>> print(f"Success rate: {stats['successful_requests'] / stats['total_requests'] * 100:.1f}%")
        """
        return self._base_client.get_stats()
    
    @property
    def base_url(self) -> str:
        """Get the base URL being used by the client."""
        return self._base_client.base_url
    
    @property
    def timeout(self) -> float:
        """Get the request timeout setting."""
        return self._base_client.timeout
    
    @property
    def max_retries(self) -> int:
        """Get the maximum retry attempts setting."""
        return self._base_client.max_retries
    
    def is_rate_limiting_enabled(self) -> bool:
        """Check if client-side rate limiting is enabled."""
        return self._base_client.rate_limiter is not None
    
    def get_rate_limit_info(self) -> dict:
        """
        Get current rate limiting information.
        
        Returns:
            dict: Rate limiting statistics and settings
        """
        if not self._base_client.rate_limiter:
            return {"enabled": False}
        
        stats = self._base_client.rate_limiter.get_stats()
        stats["enabled"] = True
        return stats
    
    # Context manager support
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
    
    def __repr__(self) -> str:
        """String representation of the client."""
        return f"ThrivingAPI(base_url='{self.base_url}', timeout={self.timeout})"


# Convenience function for quick access
def create_client(
    api_key: str,
    **kwargs
) -> ThrivingAPI:
    """
    Create a new Thriving API client instance.
    
    This is a convenience function that creates a ThrivingAPI client
    with the provided configuration.
    
    Args:
        api_key: Your Thriving API key
        **kwargs: Additional configuration options
        
    Returns:
        ThrivingAPI: Configured client instance
        
    Example:
        >>> from thriving_api import create_client
        >>> client = create_client(api_key="your-api-key", timeout=60.0)
    """
    return ThrivingAPI(api_key=api_key, **kwargs)
