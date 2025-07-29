"""
Rate limiting implementation for the Thriving API SDK.

This module provides intelligent rate limiting to prevent API quota exhaustion
and handle rate limit responses gracefully.
"""

import asyncio
import time
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from threading import Lock


@dataclass
class RateLimitInfo:
    """Information about current rate limit status."""
    requests_per_second: int = 30  # Default rate limit
    burst_limit: int = 60  # Default burst limit
    remaining_requests: Optional[int] = None
    reset_time: Optional[float] = None
    retry_after: Optional[int] = None


class TokenBucket:
    """Token bucket algorithm for rate limiting."""
    
    def __init__(self, capacity: int, refill_rate: float) -> None:
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.last_refill = time.time()
        self._lock = Lock()
    
    def consume(self, tokens: int = 1) -> bool:
        """Try to consume tokens from the bucket."""
        with self._lock:
            now = time.time()
            # Add tokens based on time elapsed
            elapsed = now - self.last_refill
            self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
            self.last_refill = now
            
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False
    
    def wait_time(self, tokens: int = 1) -> float:
        """Calculate how long to wait for tokens to be available."""
        with self._lock:
            if self.tokens >= tokens:
                return 0.0
            needed_tokens = tokens - self.tokens
            return needed_tokens / self.refill_rate


class RateLimiter:
    """Advanced rate limiter with adaptive behavior."""
    
    def __init__(
        self,
        requests_per_second: int = 30,
        burst_limit: int = 60,
        adaptive: bool = True
    ) -> None:
        self.adaptive = adaptive
        self.rate_limit_info = RateLimitInfo(
            requests_per_second=requests_per_second,
            burst_limit=burst_limit
        )
        
        # Create token bucket
        self.token_bucket = TokenBucket(
            capacity=burst_limit,
            refill_rate=requests_per_second
        )
        
        # Track recent requests for adaptive behavior
        self.recent_requests: list[float] = []
        self.consecutive_rate_limits = 0
        self._lock = Lock()
    
    async def acquire(self) -> None:
        """Acquire permission to make a request."""
        # Try to consume a token
        if not self.token_bucket.consume():
            # Calculate wait time
            wait_time = self.token_bucket.wait_time()
            if wait_time > 0:
                await asyncio.sleep(wait_time)
                # Try again after waiting
                if not self.token_bucket.consume():
                    # Fallback: wait a bit more
                    await asyncio.sleep(0.1)
        
        # Track this request
        with self._lock:
            now = time.time()
            self.recent_requests.append(now)
            # Keep only requests from last minute
            self.recent_requests = [
                req_time for req_time in self.recent_requests 
                if now - req_time < 60
            ]
    
    def update_from_response(self, headers: Dict[str, str]) -> None:
        """Update rate limit info from API response headers."""
        if not self.adaptive:
            return
        
        # Parse common rate limit headers
        remaining = headers.get('x-ratelimit-remaining')
        reset_time = headers.get('x-ratelimit-reset')
        retry_after = headers.get('retry-after')
        
        with self._lock:
            if remaining is not None:
                try:
                    self.rate_limit_info.remaining_requests = int(remaining)
                except ValueError:
                    pass
            
            if reset_time is not None:
                try:
                    self.rate_limit_info.reset_time = float(reset_time)
                except ValueError:
                    pass
            
            if retry_after is not None:
                try:
                    self.rate_limit_info.retry_after = int(retry_after)
                except ValueError:
                    pass
    
    def handle_rate_limit_response(self, retry_after: Optional[int] = None) -> float:
        """Handle a rate limit response and return wait time."""
        with self._lock:
            self.consecutive_rate_limits += 1
            
            # Use retry-after header if available
            if retry_after:
                wait_time = retry_after
            elif self.rate_limit_info.retry_after:
                wait_time = self.rate_limit_info.retry_after
            else:
                # Exponential backoff based on consecutive rate limits
                wait_time = min(60, 2 ** self.consecutive_rate_limits)
            
            # Adjust token bucket to be more conservative
            if self.adaptive and self.consecutive_rate_limits > 1:
                # Reduce rate by 20% for each consecutive rate limit
                reduction_factor = 0.8 ** self.consecutive_rate_limits
                new_rate = max(1, self.rate_limit_info.requests_per_second * reduction_factor)
                self.token_bucket.refill_rate = new_rate
        
        return wait_time
    
    def reset_rate_limit_tracking(self) -> None:
        """Reset rate limit tracking after successful requests."""
        with self._lock:
            if self.consecutive_rate_limits > 0:
                self.consecutive_rate_limits = 0
                # Restore original rate
                self.token_bucket.refill_rate = self.rate_limit_info.requests_per_second
    
    def get_current_rate(self) -> float:
        """Get current effective rate limit."""
        return self.token_bucket.refill_rate
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current rate limiter statistics."""
        with self._lock:
            now = time.time()
            recent_count = len([
                req for req in self.recent_requests 
                if now - req < 60
            ])
            
            return {
                "requests_per_second": self.rate_limit_info.requests_per_second,
                "current_rate": self.token_bucket.refill_rate,
                "burst_limit": self.rate_limit_info.burst_limit,
                "available_tokens": self.token_bucket.tokens,
                "recent_requests_per_minute": recent_count,
                "consecutive_rate_limits": self.consecutive_rate_limits,
                "remaining_requests": self.rate_limit_info.remaining_requests,
            }
