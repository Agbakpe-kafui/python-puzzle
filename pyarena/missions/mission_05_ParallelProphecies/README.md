# ⚡ Mission 5: Parallel Prophecies

**Status**: Core
**Difficulty**: Intermediate-Advanced
**Focus**: Async Programming & Concurrency

---

## 🎯 Mission Objective

Unlock the power of parallelism! Master Python's async/await syntax, understand concurrency concepts, and dramatically improve performance by running operations in parallel.

---

## 📚 What You'll Learn

- async/await syntax
- asyncio fundamentals
- Concurrent API requests
- Event loop understanding
- Performance optimization
- Async context managers
- Task gathering and timeouts

---

## ✅ Tasks

### 1. Understand the Async Demo

Test the async demonstration endpoint:

```bash
curl http://localhost:8000/api/external/async-demo
```

Notice how 3 tasks taking 1, 2, and 1.5 seconds run in ~2 seconds total (not 4.5).

### 2. Examine Parallel API Fetching

Look at `app/routers/external.py` - the `fetch_multiple_apis` function:

```bash
# Test parallel fetching
curl -X POST http://localhost:8000/api/external/fetch-multiple \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '["https://api.github.com/users/octocat", "https://api.github.com/users/torvalds"]'
```

### 3. Create Async Database Operations

Upgrade to async database operations:

```python
# TODO: Install asyncpg and create async version
# pip install asyncpg databases

from databases import Database

DATABASE_URL = "postgresql://user:password@localhost/pyarena"
database = Database(DATABASE_URL)

@router.on_event("startup")
async def startup():
    await database.connect()

@router.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@router.get("/users/async")
async def get_users_async():
    """
    TODO: Implement async database query
    - Use databases library for async DB access
    - Query users asynchronously
    - Compare performance with sync version
    """
    query = "SELECT * FROM users"
    users = await database.fetch_all(query)
    return users
```

### 4. Build Concurrent Data Aggregator

Create an endpoint that fetches from multiple sources simultaneously:

```python
@router.get("/aggregate/user-info/{username}")
async def aggregate_user_info(username: str):
    """
    TODO: Aggregate user data from multiple sources
    - Fetch from GitHub API
    - Fetch from GitLab API (if exists)
    - Fetch from local database
    - Run all requests concurrently
    - Merge results into one response
    """

    async def get_github_data():
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://api.github.com/users/{username}")
            return response.json() if response.status_code == 200 else None

    async def get_gitlab_data():
        # TODO: Implement GitLab fetch
        pass

    async def get_local_data():
        # TODO: Query local database
        pass

    # Run all concurrently
    github, gitlab, local = await asyncio.gather(
        get_github_data(),
        get_gitlab_data(),
        get_local_data(),
        return_exceptions=True  # Don't fail if one source fails
    )

    return {
        "username": username,
        "github": github,
        "gitlab": gitlab,
        "local": local
    }
```

### 5. Implement Async Task Queue

Create a background task processor:

```python
from asyncio import Queue
import asyncio

task_queue = Queue()
results = {}

async def process_tasks():
    """
    TODO: Background task processor
    - Process tasks from the queue
    - Run tasks concurrently (with limit)
    - Store results
    - Handle errors gracefully
    """
    while True:
        task = await task_queue.get()
        try:
            # Process task
            result = await execute_task(task)
            results[task['id']] = result
        except Exception as e:
            results[task['id']] = {"error": str(e)}
        finally:
            task_queue.task_done()

@router.post("/tasks/submit")
async def submit_task(task_data: dict):
    """Submit a task to the queue"""
    task_id = str(uuid.uuid4())
    await task_queue.put({"id": task_id, "data": task_data})
    return {"task_id": task_id, "status": "queued"}

@router.get("/tasks/{task_id}")
async def get_task_result(task_id: str):
    """Get task result"""
    if task_id in results:
        return results[task_id]
    return {"status": "pending"}
```

### 6. Add Timeout and Cancellation

Implement proper timeout handling:

```python
@router.get("/fetch-with-timeout")
async def fetch_with_timeout(url: str, timeout: int = 5):
    """
    TODO: Fetch with timeout
    - Use asyncio.wait_for for timeout
    - Handle TimeoutError
    - Cancel tasks properly
    - Return appropriate error messages
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await asyncio.wait_for(
                client.get(url),
                timeout=timeout
            )
            return response.json()
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=408,
            detail=f"Request timed out after {timeout} seconds"
        )
```

---

## 🧪 Testing Your Solution

```bash
# Test async operations
time curl http://localhost:8000/api/external/async-demo

# Compare with sequential (would take longer)
# Parallel: ~2 seconds
# Sequential: ~4.5 seconds

# Test concurrent API fetching
curl -X POST http://localhost:8000/api/external/fetch-multiple \
  -H "Content-Type: application/json" \
  -d '["https://api.github.com/", "https://httpbin.org/delay/1", "https://jsonplaceholder.typicode.com/posts/1"]'
```

---

## 📖 Key Concepts

### Async Function Definition
```python
async def my_async_function():
    await asyncio.sleep(1)
    return "done"
```

### Awaiting Multiple Tasks
```python
# Sequential (slow)
result1 = await task1()
result2 = await task2()

# Concurrent (fast)
result1, result2 = await asyncio.gather(task1(), task2())
```

### Async Context Managers
```python
async with httpx.AsyncClient() as client:
    response = await client.get(url)
```

### Creating Tasks
```python
# Start task in background
task = asyncio.create_task(my_coroutine())

# Wait for it later
result = await task
```

---

## 🎓 Resources

- [Python asyncio Documentation](https://docs.python.org/3/library/asyncio.html)
- [Real Python - Async IO](https://realpython.com/async-io-python/)
- [FastAPI Async](https://fastapi.tiangolo.com/async/)
- [Understanding Python's Async](https://www.youtube.com/watch?v=iG6fr81xHKA)

---

## 📊 Performance Comparison

```python
# Measure performance difference
import time

# Sequential
start = time.time()
result1 = fetch_api1()  # 1 second
result2 = fetch_api2()  # 1 second
result3 = fetch_api3()  # 1 second
print(f"Sequential: {time.time() - start}s")  # ~3 seconds

# Concurrent
start = time.time()
results = await asyncio.gather(
    fetch_api1(),
    fetch_api2(),
    fetch_api3()
)
print(f"Concurrent: {time.time() - start}s")  # ~1 second
```

---

## ✨ Completion Criteria

- [ ] Understood async/await syntax
- [ ] Successfully ran multiple operations in parallel
- [ ] Implemented concurrent API fetching
- [ ] Created async database operations (bonus)
- [ ] Built data aggregator with asyncio.gather
- [ ] Implemented task queue with async processing
- [ ] Added proper timeout handling
- [ ] Measured and compared performance improvements

---

## 🐛 Common Issues

**Issue**: `RuntimeError: This event loop is already running`
**Solution**: Don't nest event loops. Use `await` instead of `asyncio.run()` inside async functions.

**Issue**: Async function not awaited
**Solution**: Always `await` async functions, or they won't execute.

**Issue**: `SyntaxError: 'await' outside async function`
**Solution**: Can only use `await` inside `async def` functions.

---

## ⏭️ Next Mission

Concurrency mastered! Progress to **Mission 6: The Guild Archives** to learn data analysis with pandas and numpy.

*"Time flows differently when prophecies run in parallel..."*
