"""
Cache Utilities
Redis caching helpers and decorators.
Mission 7: Echo of Time
"""

import json
import functools
from typing import Optional, Any, Callable
from datetime import timedelta
import redis
import os

# Redis configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

# Global redis client (initialized lazily)
_redis_client: Optional[redis.Redis] = None


def get_redis_client() -> Optional[redis.Redis]:
    """
    Get or create Redis client instance.
    Returns None if Redis is not available.
    """
    global _redis_client

    if _redis_client is None:
        try:
            _redis_client = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                db=REDIS_DB,
                password=REDIS_PASSWORD,
                decode_responses=True,
                socket_connect_timeout=5
            )
            # Test connection
            _redis_client.ping()
            print(f"✓ Connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
        except (redis.ConnectionError, redis.TimeoutError) as e:
            print(f"✗ Redis connection failed: {e}")
            print("  Continuing without cache...")
            _redis_client = None

    return _redis_client


async def get_cached(key: str) -> Optional[Any]:
    """
    Get value from cache.
    Returns None if key doesn't exist or Redis is unavailable.
    """
    client = get_redis_client()
    if client is None:
        return None

    try:
        value = client.get(key)
        if value:
            return json.loads(value)
    except Exception as e:
        print(f"Cache get error: {e}")

    return None


async def set_cached(key: str, value: Any, expire: int = 300) -> bool:
    """
    Set value in cache with expiration time (default 5 minutes).
    Returns True if successful, False otherwise.
    """
    client = get_redis_client()
    if client is None:
        return False

    try:
        serialized = json.dumps(value)
        client.setex(key, expire, serialized)
        return True
    except Exception as e:
        print(f"Cache set error: {e}")
        return False


async def delete_cached(key: str) -> bool:
    """
    Delete key from cache.
    Returns True if successful, False otherwise.
    """
    client = get_redis_client()
    if client is None:
        return False

    try:
        client.delete(key)
        return True
    except Exception as e:
        print(f"Cache delete error: {e}")
        return False


async def clear_cache_pattern(pattern: str) -> int:
    """
    Delete all keys matching a pattern.
    Returns number of keys deleted.
    """
    client = get_redis_client()
    if client is None:
        return 0

    try:
        keys = client.keys(pattern)
        if keys:
            return client.delete(*keys)
        return 0
    except Exception as e:
        print(f"Cache clear error: {e}")
        return 0


def cached(expire: int = 300, key_prefix: str = ""):
    """
    Decorator to cache function results.

    Usage:
        @cached(expire=600, key_prefix="user_stats")
        async def get_user_stats(user_id: int):
            # expensive computation
            return stats

    TODO: Add cache invalidation strategies and cache warming.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            cache_key = f"{key_prefix}:{func.__name__}:{str(args)}:{str(kwargs)}"

            # Try to get from cache
            cached_value = await get_cached(cache_key)
            if cached_value is not None:
                return cached_value

            # Execute function and cache result
            result = await func(*args, **kwargs)
            await set_cached(cache_key, result, expire)
            return result

        return wrapper
    return decorator


async def get_cache_stats() -> dict:
    """
    Get Redis cache statistics.
    """
    client = get_redis_client()
    if client is None:
        return {
            "status": "unavailable",
            "message": "Redis not connected"
        }

    try:
        info = client.info()
        return {
            "status": "connected",
            "used_memory": info.get("used_memory_human"),
            "total_keys": client.dbsize(),
            "connected_clients": info.get("connected_clients"),
            "uptime_seconds": info.get("uptime_in_seconds"),
            "hit_rate": _calculate_hit_rate(info)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def _calculate_hit_rate(info: dict) -> float:
    """Calculate cache hit rate from Redis info"""
    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)
    total = hits + misses
    if total == 0:
        return 0.0
    return round((hits / total) * 100, 2)
