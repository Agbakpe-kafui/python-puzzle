# 📜 Mission 2: Records of Apprentices

**Status**: Core
**Difficulty**: Beginner
**Focus**: SQLAlchemy & CRUD Operations

---

## 🎯 Mission Objective

Establish the Guild's record-keeping system. Learn to work with databases using SQLAlchemy ORM, create models, and implement full CRUD (Create, Read, Update, Delete) operations.

---

## 📚 What You'll Learn

- SQLAlchemy ORM fundamentals
- Database models and relationships
- CRUD operations
- Pydantic schemas for validation
- Database sessions and dependencies
- Query building and filtering

---

## ✅ Tasks

### 1. Examine the Database Models

Open `app/models.py` and study the `User` model:
- Column definitions and types
- Relationships between models
- Timestamps and defaults

### 2. Explore CRUD Endpoints

The user routes are in `app/routers/users.py`. Test them:

```bash
# Create a user
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "apprentice1", "email": "apprentice@guild.com", "password": "secure123", "full_name": "New Apprentice"}'

# Get all users
curl http://localhost:8000/api/users/

# Get specific user
curl http://localhost:8000/api/users/1
```

### 3. Implement Mission Progress Tracking

Create CRUD operations for the `MissionProgress` model:

```python
# TODO: Add to app/routers/users.py or create new router

@router.post("/{user_id}/missions/")
async def start_mission(
    user_id: int,
    mission_id: int,
    db: Session = Depends(get_db)
):
    """
    TODO: Create a new mission progress record
    - Validate that mission_id is between 1-13
    - Create MissionProgress entry with status "in_progress"
    - Return the created record
    """
    # Your code here
    pass


@router.get("/{user_id}/missions/")
async def get_user_missions(user_id: int, db: Session = Depends(get_db)):
    """
    TODO: Get all missions for a user
    - Query MissionProgress filtered by user_id
    - Return list of missions with their status
    """
    # Your code here
    pass
```

### 4. Add Query Filters

Implement filtering for user queries:

```python
@router.get("/")
async def get_users(
    skip: int = 0,
    limit: int = 100,
    guild_rank: Optional[str] = None,
    min_experience: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    TODO: Add filtering capabilities
    - Filter by guild_rank if provided
    - Filter by minimum experience if provided
    - Implement pagination with skip and limit
    """
    # Your code here
    pass
```

---

## 🧪 Testing Your Solution

```bash
# Test mission progress creation
curl -X POST http://localhost:8000/api/users/1/missions/ \
  -H "Content-Type: application/json" \
  -d '{"mission_id": 1, "mission_name": "The First Flame"}'

# Test filtering users
curl "http://localhost:8000/api/users/?guild_rank=Apprentice&min_experience=10"
```

---

## 📖 Key Concepts

### Defining Models
```python
from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
```

### Querying with SQLAlchemy
```python
# Get all
users = db.query(User).all()

# Filter
users = db.query(User).filter(User.guild_rank == "Apprentice").all()

# Get one
user = db.query(User).filter(User.id == 1).first()

# Order and limit
users = db.query(User).order_by(User.experience_points.desc()).limit(10).all()
```

### Creating Records
```python
new_user = User(username="test", email="test@example.com")
db.add(new_user)
db.commit()
db.refresh(new_user)  # Get the id
```

---

## 🎓 Resources

- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/20/orm/tutorial.html)
- [FastAPI with Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [Pydantic Models](https://docs.pydantic.dev/latest/concepts/models/)

---

## ✨ Completion Criteria

- [ ] Successfully created new users via API
- [ ] Retrieved and filtered user lists
- [ ] Updated user information
- [ ] Implemented mission progress tracking
- [ ] Added query filters (guild_rank, experience)
- [ ] Tested all CRUD operations

---

## 🐛 Common Issues

**Issue**: `no such table: users`
**Solution**: Make sure the database is initialized. The tables are created automatically when the app starts.

**Issue**: `IntegrityError: UNIQUE constraint failed`
**Solution**: Username or email already exists. Use unique values.

---

## ⏭️ Next Mission

Master the records! Then advance to **Mission 3: Seal of the Keeper** to learn JWT authentication and secure your API.

*"A Guild without records is a Guild without history..."*
