# Rate Limiting & Caching Protection

This document explains how the Metal List project protects against getting IP-banned from Sputnikmusic.

## Problem

Sputnikmusic can block IPs that make too many requests too quickly. If you run audits frequently or debug scraping logic, you risk:
- HTTP 429 (Too Many Requests) responses
- IP ban (temporary or permanent)
- Failed audit results

## Solution: Three-Layer Protection

### 1. **Exponential Backoff Rate Limiter** (`rate_limiter.py`)

When Sputnikmusic requests fail (timeouts, errors), the rate limiter automatically increases the delay between requests.

**How it works:**

```
Request 1: Success ✓              → delay = 1s
Request 2: Timeout ✗              → delay = 2s
Request 3: Timeout ✗              → delay = 4s
Request 4: Timeout ✗              → delay = 8s
...
Request 10: Timeout ✗             → delay = 120s (capped)
Request 11: Success ✓             → delay = 1s (reset!)
```

**Configuration:**

```python
from rate_limiter import RateLimiter

limiter = RateLimiter(
    base_delay=1.0,           # Start with 1 second delay
    max_delay=120.0,          # Never wait more than 2 minutes
    backoff_factor=2.0,       # Double delay on each failure
)
```

**Usage:**

```python
from rate_limiter import execute_with_rate_limit

# Automatically handles retries + delays
result = await execute_with_rate_limit(fetch_url, "https://sputnikmusic.com/...")
```

### 2. **Caching** (`audit_cache.py`)

Audit results are cached in the database for **24 hours**. Repeated audits of the same artist don't hit Sputnikmusic again.

**How it works:**

```
First audit of Black Sabbath:
  1. Check cache            → miss
  2. Fetch from Sputnik     → rate limited
  3. Save to cache          → cache valid for 24h
  
Second audit (1 hour later):
  1. Check cache            → hit!
  2. Return cached result   → instant, no Sputnik request
  
Third audit (25 hours later):
  1. Check cache            → expired
  2. Fetch from Sputnik     → rate limited
  3. Save to cache          → new 24h TTL
```

**Usage:**

```python
from audit_cache import AuditCacheManager

# Check cache first
cached = AuditCacheManager.get_cached_result(session, artist_id)
if cached:
    return cached

# Fetch from Sputnik + save to cache
result = await audit_artist_sputnik(artist_name, db_albums)
AuditCacheManager.cache_result(session, artist_id, artist_name, result)
```

### 3. **Smart Request Headers**

All requests include a realistic User-Agent:

```python
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ..."
}
```

This makes requests look like they're from a real browser, not a bot.

## Behavior

### Success Case

```
Audit Black Sabbath:
  Wait 1s
  Fetch artist search       → ✓ Success
  Reset delay to 1s
  
  Wait 1s
  Fetch discography         → ✓ Success
  Reset delay to 1s
  
  Cache result for 24h
  Return to user (instant)
```

**Total time**: ~2-3 seconds per audit

### Failure Case (Sputnik Rate-Limited)

```
Audit Iron Maiden (server is slow):
  Wait 1s
  Fetch artist search       → timeout
  Increase delay to 2s
  
  Wait 2s
  Fetch artist search       → timeout
  Increase delay to 4s
  
  Wait 4s
  Fetch artist search       → ✓ Success
  Reset delay to 1s
  
  ...continue with discography...
```

**Total time**: ~7-10 seconds (adaptive)

## Testing

```bash
# Run rate limiter tests
pytest test_rate_limiting.py -v

# Tests cover:
# - Exponential backoff logic
# - Delay enforcement
# - Retry logic
# - Success resets
```

**Current status**: 8/8 tests passing ✅

## Configuration

### Adjust Rate Limiter

If Sputnikmusic is still blocking:

```python
# In audit.py
limiter = RateLimiter(
    base_delay=2.0,      # Increase from 1s to 2s
    max_delay=300.0,     # Increase from 120s to 5 minutes
    backoff_factor=2.5,  # Increase from 2.0 to 2.5 (backoff faster)
)
```

### Adjust Cache TTL

If you need fresher data:

```python
# In audit_cache.py
CACHE_TTL_HOURS = 12  # Decrease from 24h to 12h
```

### Disable Caching (Not Recommended)

```python
# In main.py audit route
# Skip cache check:
# cached = AuditCacheManager.get_cached_result(session, artist_id)
# Just fetch fresh
result = await audit_artist_sputnik(artist_name, db_albums)
```

## Monitoring

Check logs to see rate limiting in action:

```
INFO: Searching for artist: Black Sabbath
INFO: Found artist URL: https://www.sputnikmusic.com/bands/...
INFO: Fetching discography: https://...
INFO: Found 15 albums for ...
DEBUG: Request successful, resetting delay to 1.0s
```

If you see warnings:

```
WARNING: Request failed, increasing delay to 2.0s
WARNING: Search failed for Artist (status 429)
WARNING: Timeout on attempt 2/3
```

It means Sputnikmusic is temporarily rate-limiting or slow. The system will back off automatically.

## FAQ

**Q: Why do audits take so long sometimes?**  
A: Rate limiting is working. Sputnikmusic is slow or temporarily blocking. Wait a few minutes and try again.

**Q: Can I disable rate limiting?**  
A: Yes, but don't. You'll get IP-banned. The 1-2 second delay is worth not being blocked.

**Q: How often can I safely audit?**  
A: With caching + rate limiting:
- First audit: 2-3 seconds per artist
- Repeated audits within 24h: instant (cached)
- After 24h: 2-3 seconds per artist

Auditing all 50 artists every day is safe.

**Q: What if caching is stale?**  
A: Delete the cache entry manually:
```python
AuditCacheManager.invalidate_cache(session, artist_id)
```

Next audit will fetch fresh data.

## References

- `rate_limiter.py` — Rate limiter implementation
- `audit_cache.py` — Caching implementation
- `test_rate_limiting.py` — Tests
- `audit.py` — Integration with Sputnikmusic scraper
