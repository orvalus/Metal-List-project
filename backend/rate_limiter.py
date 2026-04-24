"""
Rate limiting and retry logic for Sputnikmusic scraping.
Implements exponential backoff to avoid IP bans.
"""

import asyncio
import time
from typing import Optional, TypeVar, Callable, Any
import logging

logger = logging.getLogger(__name__)

T = TypeVar("T")


class RateLimiter:
    """
    Exponential backoff rate limiter.
    
    Starts with base_delay (1s), doubles on failure until max_delay (120s).
    Resets to base_delay on success.
    """

    def __init__(
        self,
        base_delay: float = 1.0,
        max_delay: float = 120.0,
        backoff_factor: float = 2.0,
    ):
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor
        self.current_delay = base_delay
        self.last_request_time = 0.0

    async def wait(self):
        """Wait before making a request."""
        now = time.time()
        elapsed = now - self.last_request_time
        delay = max(0, self.current_delay - elapsed)
        
        if delay > 0:
            logger.info(f"Rate limiting: sleeping {delay:.2f}s")
            await asyncio.sleep(delay)
        
        self.last_request_time = time.time()

    def on_success(self):
        """Reset delay on successful request."""
        logger.debug(f"Request successful, resetting delay to {self.base_delay}s")
        self.current_delay = self.base_delay

    def on_failure(self):
        """Increase delay on failed request (exponential backoff)."""
        self.current_delay = min(
            self.current_delay * self.backoff_factor,
            self.max_delay
        )
        logger.warning(f"Request failed, increasing delay to {self.current_delay:.2f}s")

    async def execute_with_retry(
        self,
        func: Callable[..., T],
        *args,
        max_retries: int = 3,
        **kwargs
    ) -> Optional[T]:
        """
        Execute function with retry logic and rate limiting.
        
        Args:
            func: Async function to execute
            max_retries: Number of retry attempts (default 3)
            *args, **kwargs: Arguments to pass to func
            
        Returns:
            Function result or None if all retries fail
        """
        for attempt in range(max_retries):
            try:
                await self.wait()
                result = await func(*args, **kwargs)
                self.on_success()
                return result
                
            except asyncio.TimeoutError:
                logger.warning(f"Timeout on attempt {attempt + 1}/{max_retries}")
                self.on_failure()
                if attempt < max_retries - 1:
                    continue
                return None
                
            except Exception as e:
                logger.error(f"Error on attempt {attempt + 1}/{max_retries}: {e}")
                self.on_failure()
                if attempt < max_retries - 1:
                    continue
                return None

        return None


# Global rate limiter instance
_rate_limiter = RateLimiter(base_delay=1.0, max_delay=120.0)


async def execute_with_rate_limit(
    func: Callable[..., T],
    *args,
    **kwargs
) -> Optional[T]:
    """
    Execute async function with global rate limiter.
    
    Usage:
        result = await execute_with_rate_limit(fetch_url, "https://...")
    """
    return await _rate_limiter.execute_with_retry(func, *args, **kwargs)


def get_rate_limiter() -> RateLimiter:
    """Get the global rate limiter instance."""
    return _rate_limiter
