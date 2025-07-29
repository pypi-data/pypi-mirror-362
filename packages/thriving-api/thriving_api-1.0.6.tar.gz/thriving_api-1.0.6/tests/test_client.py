"""
Tests for the main ThrivingAPI client.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from thriving_api import ThrivingAPI, AuthenticationError
from thriving_api.base_client import BaseClient


class TestThrivingAPI:
    """Test cases for the main ThrivingAPI client."""
    
    def test_init_with_valid_api_key(self):
        """Test client initialization with valid API key."""
        client = ThrivingAPI(api_key="test-api-key")
        
        assert client._base_client.api_key == "test-api-key"
        assert client.ai is not None
        assert client.symbol is not None
        assert client.company is not None
        assert client.technical is not None
        assert client.options is not None
        assert client.market is not None
    
    def test_init_with_empty_api_key(self):
        """Test client initialization with empty API key."""
        with pytest.raises(AuthenticationError):
            ThrivingAPI(api_key="")
    
    def test_init_with_none_api_key(self):
        """Test client initialization with None API key."""
        with pytest.raises(AuthenticationError):
            ThrivingAPI(api_key=None)
    
    def test_init_with_whitespace_api_key(self):
        """Test client initialization with whitespace-only API key."""
        with pytest.raises(AuthenticationError):
            ThrivingAPI(api_key="   ")
    
    def test_init_with_custom_config(self):
        """Test client initialization with custom configuration."""
        client = ThrivingAPI(
            api_key="test-api-key",
            base_url="https://custom-api.example.com",
            timeout=60.0,
            max_retries=5,
            requests_per_second=50
        )
        
        assert client.base_url == "https://custom-api.example.com"
        assert client.timeout == 60.0
        assert client.max_retries == 5
    
    def test_properties(self):
        """Test client properties."""
        client = ThrivingAPI(api_key="test-api-key")
        
        assert client.base_url == "https://ai.tradethriving.com"
        assert client.timeout == 30.0
        assert client.max_retries == 3
        assert client.is_rate_limiting_enabled() is True
    
    def test_get_stats(self):
        """Test getting client statistics."""
        client = ThrivingAPI(api_key="test-api-key")
        
        # Mock the base client stats
        client._base_client.get_stats = MagicMock(return_value={
            "total_requests": 10,
            "successful_requests": 8,
            "failed_requests": 2
        })
        
        stats = client.get_stats()
        assert stats["total_requests"] == 10
        assert stats["successful_requests"] == 8
        assert stats["failed_requests"] == 2
    
    def test_get_rate_limit_info_enabled(self):
        """Test getting rate limit info when enabled."""
        client = ThrivingAPI(api_key="test-api-key", enable_rate_limiting=True)
        
        # Mock the rate limiter
        client._base_client.rate_limiter = MagicMock()
        client._base_client.rate_limiter.get_stats.return_value = {
            "requests_per_second": 30,
            "available_tokens": 25.5
        }
        
        rate_info = client.get_rate_limit_info()
        assert rate_info["enabled"] is True
        assert rate_info["requests_per_second"] == 30
        assert rate_info["available_tokens"] == 25.5
    
    def test_get_rate_limit_info_disabled(self):
        """Test getting rate limit info when disabled."""
        client = ThrivingAPI(api_key="test-api-key", enable_rate_limiting=False)
        
        rate_info = client.get_rate_limit_info()
        assert rate_info["enabled"] is False
    
    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test using client as async context manager."""
        async with ThrivingAPI(api_key="test-api-key") as client:
            assert client is not None
            assert isinstance(client, ThrivingAPI)
        
        # Client should be closed after context manager exits
        # In a real test, we'd verify the HTTP client is closed
    
    @pytest.mark.asyncio
    async def test_close(self):
        """Test closing the client."""
        client = ThrivingAPI(api_key="test-api-key")
        
        # Mock the base client close method
        client._base_client.close = AsyncMock()
        
        await client.close()
        client._base_client.close.assert_called_once()
    
    def test_repr(self):
        """Test string representation of client."""
        client = ThrivingAPI(api_key="test-api-key")
        
        repr_str = repr(client)
        assert "ThrivingAPI" in repr_str
        assert "https://ai.tradethriving.com" in repr_str
        assert "30.0" in repr_str


class TestCreateClient:
    """Test cases for the create_client convenience function."""
    
    def test_create_client_basic(self):
        """Test creating client with basic parameters."""
        from thriving_api import create_client
        
        client = create_client(api_key="test-api-key")
        
        assert isinstance(client, ThrivingAPI)
        assert client._base_client.api_key == "test-api-key"
    
    def test_create_client_with_kwargs(self):
        """Test creating client with additional kwargs."""
        from thriving_api import create_client
        
        client = create_client(
            api_key="test-api-key",
            timeout=60.0,
            max_retries=5
        )
        
        assert isinstance(client, ThrivingAPI)
        assert client.timeout == 60.0
        assert client.max_retries == 5


# Fixtures for testing
@pytest.fixture
def mock_client():
    """Create a mock ThrivingAPI client for testing."""
    client = ThrivingAPI(api_key="test-api-key")
    
    # Mock the base client to avoid actual HTTP requests
    client._base_client = MagicMock(spec=BaseClient)
    client._base_client.api_key = "test-api-key"
    client._base_client.base_url = "https://ai.tradethriving.com"
    client._base_client.timeout = 30.0
    client._base_client.max_retries = 3
    
    return client


@pytest.fixture
def sample_api_response():
    """Sample API response for testing."""
    return {
        "success": True,
        "analysis": {
            "symbol": "AAPL",
            "action": "buy",
            "trade_score": 75.5,
            "confidence": 0.85,
            "current_price": 150.25,
            "optimal_stop_loss": 147.87,
            "stop_loss_percentage": -1.58,
            "analysis_time": 1642694400,
            "interval": "daily"
        }
    }
