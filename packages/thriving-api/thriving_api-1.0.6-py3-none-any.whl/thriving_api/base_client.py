"""
Base client implementation for the Thriving API SDK.

This module provides the core HTTP client functionality with authentication,
rate limiting, error handling, and retry logic.
"""

import asyncio
import json
import time
from typing import Optional, Dict, Any, Union, Tuple
from urllib.parse import urljoin

import httpx
from pydantic import BaseModel

from .exceptions import (
    ThrivingAPIError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    APIConnectionError,
    ServerError,
    TimeoutError,
    QuotaExceededError,
    NotFoundError,
)
from .rate_limiter import RateLimiter


class BaseClient:
    """Base HTTP client for the Thriving API."""
    
    BASE_URL = "https://ai.tradethriving.com"
    DEFAULT_TIMEOUT = 30.0
    MAX_RETRIES = 3
    
    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = MAX_RETRIES,
        requests_per_second: int = 30,
        burst_limit: int = 60,
        enable_rate_limiting: bool = True,
    ) -> None:
        """
        Initialize the base client.
        
        Args:
            api_key: Your Thriving API key
            base_url: Override the default API base URL
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            requests_per_second: Rate limit for requests per second
            burst_limit: Maximum burst requests allowed
            enable_rate_limiting: Whether to enable client-side rate limiting
        """
        self.api_key = api_key
        self.base_url = base_url or self.BASE_URL
        self.timeout = timeout
        self.max_retries = max_retries
        
        # Initialize rate limiter
        self.rate_limiter = RateLimiter(
            requests_per_second=requests_per_second,
            burst_limit=burst_limit,
            adaptive=True
        ) if enable_rate_limiting else None
        
        # Create HTTP client
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout),
            headers=self._get_default_headers(),
            limits=httpx.Limits(max_connections=10, max_keepalive_connections=5)
        )
        
        # Track request statistics
        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "rate_limited_requests": 0,
            "retried_requests": 0,
        }
    
    def _get_default_headers(self) -> Dict[str, str]:
        """Get default headers for all requests."""
        return {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "thriving-api-python/1.0.0",
        }
    
    def _build_url(self, endpoint: str) -> str:
        """Build full URL from endpoint."""
        return urljoin(self.base_url.rstrip("/") + "/", endpoint.lstrip("/"))
    
    def _handle_response_error(self, response: httpx.Response) -> None:
        """Handle HTTP error responses."""
        status_code = response.status_code
        
        try:
            error_data = response.json()
            error_message = error_data.get("error", error_data.get("message", "Unknown error"))
        except (json.JSONDecodeError, ValueError):
            error_message = response.text or f"HTTP {status_code} error"
        
        # Extract request ID if available
        request_id = response.headers.get("x-request-id")
        
        # Map status codes to specific exceptions
        if status_code == 401:
            raise AuthenticationError(error_message, response_data=error_data, request_id=request_id)
        elif status_code == 402:
            raise QuotaExceededError(error_message, response_data=error_data, request_id=request_id)
        elif status_code == 404:
            raise NotFoundError(error_message, response_data=error_data, request_id=request_id)
        elif status_code == 400:
            raise ValidationError(error_message, response_data=error_data, request_id=request_id)
        elif status_code == 429:
            retry_after = response.headers.get("retry-after")
            retry_after_int = int(retry_after) if retry_after else None
            raise RateLimitError(
                error_message, 
                retry_after=retry_after_int,
                response_data=error_data, 
                request_id=request_id
            )
        elif 500 <= status_code < 600:
            raise ServerError(error_message, status_code=status_code, response_data=error_data, request_id=request_id)
        else:
            raise ThrivingAPIError(
                error_message, 
                status_code=status_code, 
                response_data=error_data, 
                request_id=request_id
            )
    
    async def _make_request_with_retries(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> httpx.Response:
        """Make HTTP request with retry logic."""
        url = self._build_url(endpoint)
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                # Apply rate limiting
                if self.rate_limiter:
                    await self.rate_limiter.acquire()
                
                # Update stats
                self.stats["total_requests"] += 1
                if attempt > 0:
                    self.stats["retried_requests"] += 1
                
                # Make the request
                response = await self._client.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json_data,
                    **kwargs
                )
                
                # Update rate limiter from response headers
                if self.rate_limiter:
                    self.rate_limiter.update_from_response(dict(response.headers))
                
                # Handle rate limiting
                if response.status_code == 429:
                    self.stats["rate_limited_requests"] += 1
                    
                    if self.rate_limiter:
                        retry_after = response.headers.get("retry-after")
                        retry_after_int = int(retry_after) if retry_after else None
                        wait_time = self.rate_limiter.handle_rate_limit_response(retry_after_int)
                        
                        if attempt < self.max_retries:
                            await asyncio.sleep(wait_time)
                            continue
                    
                    # If we're out of retries or no rate limiter, raise the error
                    self._handle_response_error(response)
                
                # Handle other HTTP errors
                if not response.is_success:
                    # For server errors, retry if we have attempts left
                    if 500 <= response.status_code < 600 and attempt < self.max_retries:
                        wait_time = min(60, 2 ** attempt)  # Exponential backoff
                        await asyncio.sleep(wait_time)
                        continue
                    
                    self._handle_response_error(response)
                
                # Success - reset rate limit tracking
                if self.rate_limiter:
                    self.rate_limiter.reset_rate_limit_tracking()
                
                self.stats["successful_requests"] += 1
                return response
                
            except (httpx.ConnectError, httpx.TimeoutException) as e:
                last_exception = APIConnectionError(f"Connection error: {str(e)}")
                if attempt < self.max_retries:
                    wait_time = min(60, 2 ** attempt)
                    await asyncio.sleep(wait_time)
                    continue
            
            except (RateLimitError, AuthenticationError, ValidationError, QuotaExceededError) as e:
                # Don't retry these errors
                self.stats["failed_requests"] += 1
                raise e
            
            except Exception as e:
                last_exception = ThrivingAPIError(f"Unexpected error: {str(e)}")
                if attempt < self.max_retries:
                    wait_time = min(60, 2 ** attempt)
                    await asyncio.sleep(wait_time)
                    continue
        
        # If we get here, all retries failed
        self.stats["failed_requests"] += 1
        if last_exception:
            raise last_exception
        else:
            raise ThrivingAPIError("All retry attempts failed")
    
    async def get(
        self, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Make a GET request."""
        response = await self._make_request_with_retries("GET", endpoint, params=params, **kwargs)
        return response.json()
    
    async def post(
        self, 
        endpoint: str, 
        json_data: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Make a POST request."""
        response = await self._make_request_with_retries("POST", endpoint, json_data=json_data, **kwargs)
        return response.json()
    
    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get client statistics."""
        stats = self.stats.copy()
        if self.rate_limiter:
            stats.update(self.rate_limiter.get_stats())
        return stats
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
