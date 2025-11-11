# 🌀 Mission 7: Echo of Time

**Status**: Core
**Difficulty**: Intermediate
**Focus**: Redis Caching & Performance Optimization

---

## 🎯 Mission Objective

Speed up your Guild! Learn to implement caching with Redis to dramatically improve API response times, reduce database load, and handle high traffic efficiently.

---

## 📚 What You'll Learn

- Redis basics and data structures
- Cache strategies (TTL, invalidation)
- Caching decorator patterns
- Background task processing
- Performance monitoring
- Cache warming and expiration

---

## ✅ Tasks

### 1. Set Up Redis

First, start Redis:

```bash
# Using Docker
docker run -d -p 6379:6379 redis:alpine

# Or install locally
# macOS: brew install redis && redis-server
# Linux: sudo apt-get install redis-server && redis-server
```

Test Redis connection:
```bash
redis-cli ping
# Should return: PONG
```

### 2. Explore Cache Utilities

Check out `app/utils/cache_utils.py`:
- Redis connection management
- Cache get/set/delete functions
- Caching decorator
- Cache statistics

### 3. Implement Caching for Analytics

Add caching to expensive analytics queries:

```python
from app.utils.cache_utils import cached, set_cached, get_cached

@router.get("/users/stats")
@cached(expire=300, key_prefix="user_stats")  # Cache for 5 minutes
async def get_user_statistics(db: Session = Depends(get_db)):
    """
    TODO: This is already implemented, but add caching
    - Expensive pandas operations
    - Should be cached
    - Cache key should include any parameters
    """
    # Existing expensive computation
    users = db.query(User).all()
    df = pd.DataFrame([...])
    # ... analytics code ...
    return stats
```

### 4. Create Cache Management Endpoints

Build endpoints to manage cache:

```python
@router.get("/cache/stats")
async def get_cache_statistics():
    """
    TODO: Get Redis cache statistics
    - Total keys
    - Memory usage
    - Hit/miss ratio
    - Uptime
    """
    from app.utils.cache_utils import get_cache_stats
    return await get_cache_stats()


@router.delete("/cache/clear")
async def clear_cache(
    pattern: str = "*",
    admin: User = Depends(get_current_admin_user)
):
    """
    TODO: Clear cache (admin only)
    - Clear all keys matching pattern
    - Default: clear all
    - Return count of keys deleted
    """
    from app.utils.cache_utils import clear_cache_pattern
    count = await clear_cache_pattern(pattern)
    return {"message": f"Cleared {count} cache entries"}


@router.post("/cache/warm")
async def warm_cache(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """
    TODO: Warm up the cache
    - Pre-compute expensive queries
    - Store in cache
    - Run in background
    """
    # Warm user stats
    await get_user_statistics(db)
    # Warm leaderboard
    await get_leaderboard(10, db)
    # Warm mission stats
    await get_mission_statistics(db)

    return {"message": "Cache warming completed"}
```

### 5. Implement Smart Cache Invalidation

Invalidate cache when data changes:

```python
from app.utils.cache_utils import delete_cached, clear_cache_pattern

@router.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    TODO: Invalidate relevant caches after user creation
    - User stats cache
    - Leaderboard cache
    - Any cache that includes user counts
    """
    # Create user
    db_user = User(...)
    db.add(db_user)
    db.commit()

    # Invalidate caches
    await delete_cached("user_stats:*")
    await delete_cached("leaderboard:*")

    return db_user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_update: UserUpdate, ...):
    """
    TODO: Invalidate specific user cache
    - Individual user cache
    - User stats cache
    - Leaderboard if experience changed
    """
    # Update user
    ...

    # Invalidate caches
    await delete_cached(f"user:{user_id}")

    if 'experience_points' in update_data:
        await delete_cached("leaderboard:*")

    return user
```

### 6. Create Rate Limiting with Redis

Implement API rate limiting:

```python
import redis
from datetime import datetime

async def check_rate_limit(user_id: int, limit: int = 100, window: int = 60):
    """
    TODO: Implement rate limiting
    - Use Redis sorted sets or counters
    - Track requests per user per time window
    - Raise exception if limit exceeded
    - Return remaining requests in response headers
    """
    from app.utils.cache_utils import get_redis_client
    client = get_redis_client()

    if client is None:
        return True  # Allow if Redis unavailable

    key = f"rate_limit:{user_id}"
    now = datetime.now().timestamp()

    # Remove old entries
    client.zremrangebyscore(key, 0, now - window)

    # Count requests in window
    request_count = client.zcard(key)

    if request_count >= limit:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Try again in {window} seconds."
        )

    # Add current request
    client.zadd(key, {str(now): now})
    client.expire(key, window)

    return True


@router.get("/protected-endpoint")
async def protected_endpoint(
    current_user: User = Depends(get_current_user)
):
    """
    TODO: Add rate limiting to endpoint
    """
    await check_rate_limit(current_user.id, limit=10, window=60)
    return {"message": "Success"}
```

### 7. Implement Session Storage

Use Redis for session management:

```python
import uuid
import json

async def create_session(user_id: int, data: dict) -> str:
    """
    TODO: Create user session in Redis
    - Generate session ID
    - Store session data
    - Set expiration (24 hours)
    - Return session ID
    """
    from app.utils.cache_utils import set_cached

    session_id = str(uuid.uuid4())
    session_data = {
        "user_id": user_id,
        "created_at": datetime.utcnow().isoformat(),
        **data
    }

    await set_cached(
        f"session:{session_id}",
        session_data,
        expire=86400  # 24 hours
    )

    return session_id


async def get_session(session_id: str) -> dict:
    """Get session data from Redis"""
    from app.utils.cache_utils import get_cached
    return await get_cached(f"session:{session_id}")
```

---

## 🧪 Testing Your Solution

```bash
# Check cache stats
curl http://localhost:8000/api/cache/stats

# Make multiple requests and watch response times improve
time curl http://localhost:8000/api/analytics/users/stats
# First request: slower (database query)
time curl http://localhost:8000/api/analytics/users/stats
# Second request: faster (cached)

# Clear cache
curl -X DELETE http://localhost:8000/api/cache/clear \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# Test rate limiting
for i in {1..15}; do
  curl http://localhost:8000/api/protected-endpoint \
    -H "Authorization: Bearer $TOKEN"
done
# Should get 429 error after 10 requests
```

---

## 📖 Key Concepts

### Basic Redis Operations
```python
import redis

client = redis.Redis(host='localhost', port=6379, db=0)

# Set value
client.set('key', 'value', ex=300)  # Expires in 300 seconds

# Get value
value = client.get('key')

# Delete
client.delete('key')

# Check if exists
if client.exists('key'):
    ...
```

### Cache Patterns
```python
# Read-through cache
async def get_user(user_id: int):
    # Try cache first
    cached = await get_cached(f"user:{user_id}")
    if cached:
        return cached

    # Cache miss - get from DB
    user = db.query(User).filter(User.id == user_id).first()

    # Store in cache
    await set_cached(f"user:{user_id}", user, expire=600)

    return user
```

---

## 🎓 Resources

- [Redis Documentation](https://redis.io/documentation)
- [Redis Python Client](https://redis-py.readthedocs.io/)
- [Caching Strategies](https://aws.amazon.com/caching/best-practices/)
- [Redis Data Types](https://redis.io/docs/data-types/)

---

## 📊 Cache Performance Metrics

Monitor these metrics:
1. **Hit Rate** - % of requests served from cache
2. **Miss Rate** - % of requests requiring DB query
3. **Eviction Rate** - How often cache keys expire
4. **Memory Usage** - Redis memory consumption
5. **Average Latency** - Response time with/without cache

Target: 80%+ hit rate for read-heavy operations

---

## ✨ Completion Criteria

- [ ] Redis connected and running
- [ ] Implemented caching for analytics endpoints
- [ ] Created cache management endpoints
- [ ] Added smart cache invalidation
- [ ] Implemented rate limiting
- [ ] Created session storage (bonus)
- [ ] Measured performance improvements
- [ ] Cache hit rate > 70%

---

## 🐛 Common Issues

**Issue**: `redis.exceptions.ConnectionError`
**Solution**: Ensure Redis is running: `redis-cli ping`

**Issue**: Cache not invalidating
**Solution**: Check your cache key patterns match when deleting.

**Issue**: High memory usage
**Solution**: Set appropriate TTLs and use `maxmemory` policy in Redis config.

---

## ⏭️ Next Mission

Caching implemented! Advance to **Mission 8: Circle of Truth** to learn testing with pytest and ensure code quality.

*"The echo of the past informs the speed of the future..."*
