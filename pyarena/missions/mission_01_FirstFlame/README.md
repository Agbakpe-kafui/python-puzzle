# 🕯️ Mission 1: The First Flame

**Status**: Foundation
**Difficulty**: Beginner
**Focus**: FastAPI Basics

---

## 🎯 Mission Objective

Light the first flame and establish your Guild's headquarters. Learn the foundations of FastAPI by creating your first web application with routes, responses, and automatic documentation.

---

## 📚 What You'll Learn

- FastAPI application structure
- Route decorators and path operations
- Request/Response models with Pydantic
- Automatic API documentation (Swagger/ReDoc)
- JSON responses and status codes

---

## ✅ Tasks

### 1. Explore the Application Structure

The main application is in `app/main.py`. Open it and examine:
- How FastAPI is initialized
- Route definitions with `@app.get()` and `@app.post()`
- Response models

### 2. Test the Endpoints

Run the application:
```bash
cd pyarena
poetry run uvicorn app.main:app --reload
```

Visit these URLs:
- http://localhost:8000/ - Root endpoint
- http://localhost:8000/ping - Health check
- http://localhost:8000/missions - List all missions
- http://localhost:8000/docs - Interactive API documentation

### 3. Create Your First Custom Endpoint

Add a new endpoint to `app/main.py`:

```python
@app.get("/guild/welcome/{username}")
async def welcome_member(username: str):
    """
    TODO: Create a welcome message for new guild members
    - Accept username as a path parameter
    - Return a personalized welcome message
    - Include guild information
    """
    # Your code here
    pass
```

### 4. Add Query Parameters

Extend the endpoint with query parameters:

```python
@app.get("/guild/status")
async def guild_status(include_stats: bool = False, rank: str = "all"):
    """
    TODO: Get guild status with optional filters
    - Use query parameters for filtering
    - Return different data based on parameters
    """
    # Your code here
    pass
```

---

## 🧪 Testing Your Solution

Test your endpoints:
```bash
curl http://localhost:8000/guild/welcome/YourName
curl http://localhost:8000/guild/status?include_stats=true&rank=Apprentice
```

---

## 📖 Key Concepts

### Path Parameters
```python
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}
```

### Query Parameters
```python
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

### Response Models
```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item
```

---

## 🎓 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [FastAPI Tutorial - First Steps](https://fastapi.tiangolo.com/tutorial/first-steps/)
- [Pydantic Models](https://docs.pydantic.dev/)

---

## ✨ Completion Criteria

- [ ] Application runs successfully
- [ ] All default endpoints return expected responses
- [ ] Created custom welcome endpoint
- [ ] Added guild status endpoint with query parameters
- [ ] Tested endpoints using browser or curl
- [ ] Explored automatic API documentation

---

## ⏭️ Next Mission

Once you've lit the First Flame, proceed to **Mission 2: Records of Apprentices** to learn about databases and ORM with SQLAlchemy.

*"Every great journey begins with a single flame..."*
