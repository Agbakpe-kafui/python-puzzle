# 🌐 Mission 4: External Scrolls

**Status**: Core
**Difficulty**: Intermediate
**Focus**: External API Integration with httpx

---

## 🎯 Mission Objective

Connect to the outside world! Learn to integrate with external APIs using the httpx library, handle responses, manage errors, and log API usage.

---

## 📚 What You'll Learn

- Making HTTP requests with httpx (async)
- Error handling for network requests
- API authentication patterns
- Response parsing and validation
- Background tasks for logging
- Timeout handling

---

## ✅ Tasks

### 1. Explore External API Routes

Check out `app/routers/external.py`:
- Basic API fetching with `httpx`
- Error handling for network issues
- Background task logging

### 2. Test the External API Endpoints

```bash
# Get your token first
TOKEN="<your-token>"

# Fetch from an external API
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/external/fetch?url=https://api.github.com/users/octocat"

# Get GitHub user info
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/external/github/user/octocat

# Try the public APIs list
curl http://localhost:8000/api/external/public-apis
```

### 3. Implement Weather API Integration

Add a weather endpoint using a free weather API:

```python
@router.get("/weather/{city}")
async def get_weather(
    city: str,
    current_user: User = Depends(get_current_user)
):
    """
    TODO: Fetch weather data for a city
    - Use a free weather API (e.g., OpenWeatherMap, WeatherAPI)
    - Handle API key from environment variables
    - Parse and return relevant weather data
    - Handle city not found errors

    Example API: https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}
    """
    # Your code here
    pass
```

### 4. Add Cryptocurrency Price Checker

Integrate with a crypto API:

```python
@router.get("/crypto/{symbol}")
async def get_crypto_price(
    symbol: str,
    currency: str = "usd",
    current_user: User = Depends(get_current_user)
):
    """
    TODO: Get cryptocurrency price
    - Use CoinGecko or similar free API
    - Support multiple currencies
    - Return price, 24h change, market cap
    - Cache results to avoid rate limiting

    Example: https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd
    """
    # Your code here
    pass
```

### 5. Implement Retry Logic

Add retry mechanism for failed requests:

```python
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def fetch_with_retry(url: str, headers: dict = None) -> dict:
    """
    TODO: Fetch URL with automatic retries
    - Use tenacity library for retry logic
    - Implement exponential backoff
    - Log retry attempts
    - Raise appropriate exceptions after max retries
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, timeout=10.0)
        response.raise_for_status()
        return response.json()
```

### 6. Create API Usage Dashboard

Build an endpoint to view API usage statistics:

```python
@router.get("/usage/dashboard")
async def api_usage_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    TODO: Create API usage dashboard
    - Query APILog table
    - Group by endpoint
    - Calculate success rate, avg response time
    - Show most used APIs
    - Filter by date range
    """
    # Your code here
    pass
```

---

## 🧪 Testing Your Solution

```bash
# Test weather API
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/external/weather/London

# Test crypto prices
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/external/crypto/bitcoin

# Check API usage
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/external/usage/dashboard
```

---

## 📖 Key Concepts

### Basic httpx Request
```python
import httpx

async with httpx.AsyncClient() as client:
    response = await client.get("https://api.example.com/data")
    data = response.json()
```

### Error Handling
```python
try:
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)
        response.raise_for_status()  # Raises exception for 4xx/5xx
        return response.json()
except httpx.TimeoutException:
    # Handle timeout
except httpx.HTTPStatusError as e:
    # Handle HTTP errors (404, 500, etc.)
except httpx.RequestError as e:
    # Handle connection errors
```

### Background Tasks
```python
from fastapi import BackgroundTasks

def log_request(url: str, status: int):
    # This runs after response is sent
    db.add(APILog(url=url, status=status))
    db.commit()

@router.get("/endpoint")
async def endpoint(background_tasks: BackgroundTasks):
    background_tasks.add_task(log_request, "https://api.example.com", 200)
    return {"status": "ok"}
```

---

## 🎓 Resources

- [httpx Documentation](https://www.python-httpx.org/)
- [FastAPI Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/)
- [Public APIs List](https://github.com/public-apis/public-apis)
- [Free API Services](https://free-apis.github.io/)

---

## 🌐 Free APIs to Practice With

1. **JSONPlaceholder** - https://jsonplaceholder.typicode.com/
2. **CoinGecko** - https://www.coingecko.com/en/api
3. **REST Countries** - https://restcountries.com/
4. **OpenWeatherMap** - https://openweathermap.org/api (free tier)
5. **The Dog API** - https://thedogapi.com/
6. **NASA APOD** - https://api.nasa.gov/

---

## ✨ Completion Criteria

- [ ] Successfully fetched data from external APIs
- [ ] Implemented proper error handling
- [ ] Created weather and crypto endpoints
- [ ] Added retry logic for failed requests
- [ ] API calls are logged in the database
- [ ] Usage dashboard shows statistics
- [ ] Tested with multiple different APIs

---

## 🐛 Common Issues

**Issue**: `httpx.ConnectError`
**Solution**: Check internet connection and URL validity.

**Issue**: `422 Unprocessable Entity` when parsing responses
**Solution**: Inspect the actual response structure - it might differ from your expectations.

**Issue**: Rate limiting errors (429)
**Solution**: Implement caching and respect API rate limits.

---

## ⏭️ Next Mission

External APIs mastered! Advance to **Mission 5: Parallel Prophecies** to learn async programming and concurrent operations.

*"The scrolls from distant lands hold knowledge untold..."*
