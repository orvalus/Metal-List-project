"""
Tests for rate limiting and audit caching.
"""

import pytest
import asyncio
import time
from rate_limiter import RateLimiter


def test_rate_limiter_initialization():
    """Test rate limiter is initialized with correct values."""
    limiter = RateLimiter(base_delay=1.0, max_delay=120.0)
    assert limiter.base_delay == 1.0
    assert limiter.max_delay == 120.0
    assert limiter.current_delay == 1.0


def test_rate_limiter_resets_on_success():
    """Test that delay resets after successful request."""
    limiter = RateLimiter(base_delay=1.0, max_delay=120.0)
    
    # Simulate failure to increase delay
    limiter.on_failure()
    assert limiter.current_delay == 2.0
    
    # Reset on success
    limiter.on_success()
    assert limiter.current_delay == 1.0


def test_rate_limiter_exponential_backoff():
    """Test exponential backoff increases delay correctly."""
    limiter = RateLimiter(base_delay=1.0, max_delay=120.0, backoff_factor=2.0)
    
    assert limiter.current_delay == 1.0
    limiter.on_failure()
    assert limiter.current_delay == 2.0
    limiter.on_failure()
    assert limiter.current_delay == 4.0
    limiter.on_failure()
    assert limiter.current_delay == 8.0


def test_rate_limiter_caps_at_max_delay():
    """Test that delay never exceeds max_delay."""
    limiter = RateLimiter(base_delay=1.0, max_delay=10.0, backoff_factor=2.0)
    
    for _ in range(10):  # Force many failures
        limiter.on_failure()
    
    assert limiter.current_delay == 10.0  # Capped at max


@pytest.mark.asyncio
async def test_rate_limiter_wait_enforces_delay():
    """Test that wait() enforces the rate limit delay."""
    limiter = RateLimiter(base_delay=0.05, max_delay=10.0)
    
    # First wait (no delay since no prior request)
    await limiter.wait()
    
    # Second wait should enforce delay
    start = time.time()
    await limiter.wait()
    elapsed = time.time() - start
    
    # Should have waited approximately the base delay (with margin for overhead)
    assert elapsed >= 0.04, f"Wait was too short: {elapsed}s"


@pytest.mark.asyncio
async def test_rate_limiter_retry_logic():
    """Test retry logic with max retries."""
    limiter = RateLimiter(base_delay=0.01, max_delay=1.0)
    
    call_count = 0
    
    async def failing_func():
        nonlocal call_count
        call_count += 1
        raise Exception("Simulated failure")
    
    result = await limiter.execute_with_retry(failing_func, max_retries=3)
    
    assert result is None
    assert call_count == 3  # Should have retried 3 times


@pytest.mark.asyncio
async def test_rate_limiter_success_on_retry():
    """Test that function succeeds on retry after initial failure."""
    limiter = RateLimiter(base_delay=0.01, max_delay=1.0)
    
    call_count = 0
    
    async def sometimes_fails():
        nonlocal call_count
        call_count += 1
        if call_count < 2:
            raise Exception("First call fails")
        return "success"
    
    result = await limiter.execute_with_retry(sometimes_fails, max_retries=3)
    
    assert result == "success"
    assert call_count == 2  # Failed once, succeeded on second try


@pytest.mark.asyncio
async def test_rate_limiter_resets_on_success_in_retry():
    """Test that delay resets when retry succeeds."""
    limiter = RateLimiter(base_delay=1.0, max_delay=120.0)
    
    call_count = 0
    
    async def sometimes_fails():
        nonlocal call_count
        call_count += 1
        if call_count < 2:
            raise Exception("First call fails")
        return "success"
    
    result = await limiter.execute_with_retry(sometimes_fails, max_retries=3)
    
    assert result == "success"
    # After successful retry, delay should reset
    assert limiter.current_delay == 1.0
