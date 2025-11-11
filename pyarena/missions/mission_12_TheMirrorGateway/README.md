# 🪞 Mission 12: The Mirror Gateway

**Status**: Advanced
**Difficulty**: Advanced
**Focus**: GraphQL API

---

## 🎯 Mission Objective

Create a reflection of your API! Learn GraphQL to offer clients a flexible, efficient alternative to REST, allowing them to request exactly the data they need.

---

## 📚 What You'll Learn

- GraphQL fundamentals
- Schema definition
- Queries and Mutations
- Resolvers
- DataLoaders (N+1 problem)
- GraphQL with FastAPI (Strawberry)
- GraphQL Playground/GraphiQL

---

## ✅ Tasks

### 1. Install Strawberry GraphQL

```bash
poetry add "strawberry-graphql[fastapi]"
```

### 2. Create GraphQL Types

Create `app/graphql/types.py`:

```python
"""
GraphQL Type Definitions
Mirror of Pydantic models for GraphQL
"""

import strawberry
from typing import Optional, List
from datetime import datetime


@strawberry.type
class User:
    """
    TODO: Define User type for GraphQL
    - Match fields from User model
    - Add computed fields if needed
    """
    id: int
    username: str
    email: str
    full_name: Optional[str]
    guild_rank: str
    experience_points: int
    missions_completed: int
    is_active: bool
    created_at: datetime


@strawberry.type
class Mission:
    """
    TODO: Define Mission type
    """
    id: int
    name: str
    difficulty: str
    focus: str
    completed_by: int  # Count of completions


@strawberry.type
class MissionProgress:
    """
    TODO: Define MissionProgress type
    """
    id: int
    user_id: int
    mission_id: int
    mission_name: str
    status: str
    score: float
    started_at: Optional[datetime]
    completed_at: Optional[datetime]


@strawberry.type
class LeaderboardEntry:
    """
    TODO: Leaderboard entry
    """
    rank: int
    user: User
    experience_points: int
    missions_completed: int
```

### 3. Create GraphQL Queries

Create `app/graphql/queries.py`:

```python
"""
GraphQL Queries
Read operations
"""

import strawberry
from typing import List, Optional
from app.graphql.types import User, Mission, MissionProgress, LeaderboardEntry
from app.database import SessionLocal
from app import models


@strawberry.type
class Query:
    """
    TODO: Define all GraphQL queries
    """

    @strawberry.field
    def user(self, id: int) -> Optional[User]:
        """
        Get user by ID
        Example query:
        {
          user(id: 1) {
            username
            email
            guildRank
            experiencePoints
          }
        }
        """
        db = SessionLocal()
        user = db.query(models.User).filter(models.User.id == id).first()
        db.close()

        if not user:
            return None

        return User(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            guild_rank=user.guild_rank,
            experience_points=user.experience_points,
            missions_completed=user.missions_completed,
            is_active=user.is_active,
            created_at=user.created_at
        )

    @strawberry.field
    def users(
        self,
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
        guild_rank: Optional[str] = None
    ) -> List[User]:
        """
        TODO: Get list of users with filtering
        Example:
        {
          users(limit: 10, guildRank: "Apprentice") {
            username
            experiencePoints
          }
        }
        """
        db = SessionLocal()
        query = db.query(models.User)

        if guild_rank:
            query = query.filter(models.User.guild_rank == guild_rank)

        users = query.offset(offset).limit(limit).all()
        db.close()

        return [User(
            id=u.id,
            username=u.username,
            email=u.email,
            full_name=u.full_name,
            guild_rank=u.guild_rank,
            experience_points=u.experience_points,
            missions_completed=u.missions_completed,
            is_active=u.is_active,
            created_at=u.created_at
        ) for u in users]

    @strawberry.field
    def leaderboard(self, limit: Optional[int] = 10) -> List[LeaderboardEntry]:
        """
        TODO: Get leaderboard
        Example:
        {
          leaderboard(limit: 5) {
            rank
            user {
              username
              guildRank
            }
            experiencePoints
          }
        }
        """
        db = SessionLocal()
        users = db.query(models.User).order_by(
            models.User.experience_points.desc()
        ).limit(limit).all()
        db.close()

        return [
            LeaderboardEntry(
                rank=idx + 1,
                user=User(
                    id=u.id,
                    username=u.username,
                    email=u.email,
                    full_name=u.full_name,
                    guild_rank=u.guild_rank,
                    experience_points=u.experience_points,
                    missions_completed=u.missions_completed,
                    is_active=u.is_active,
                    created_at=u.created_at
                ),
                experience_points=u.experience_points,
                missions_completed=u.missions_completed
            )
            for idx, u in enumerate(users)
        ]

    @strawberry.field
    def user_missions(self, user_id: int) -> List[MissionProgress]:
        """
        TODO: Get missions for a user
        """
        pass
```

### 4. Create GraphQL Mutations

Create `app/graphql/mutations.py`:

```python
"""
GraphQL Mutations
Write operations
"""

import strawberry
from typing import Optional
from app.graphql.types import User
from app.database import SessionLocal
from app import models
from app.utils.auth_utils import get_password_hash


@strawberry.type
class Mutation:
    """
    TODO: Define all GraphQL mutations
    """

    @strawberry.mutation
    def create_user(
        self,
        username: str,
        email: str,
        password: str,
        full_name: Optional[str] = None
    ) -> User:
        """
        Create a new user
        Example:
        mutation {
          createUser(
            username: "newuser"
            email: "new@example.com"
            password: "secure123"
          ) {
            id
            username
            email
          }
        }
        """
        db = SessionLocal()

        # Check if exists
        existing = db.query(models.User).filter(
            (models.User.username == username) |
            (models.User.email == email)
        ).first()

        if existing:
            db.close()
            raise Exception("User already exists")

        # Create user
        user = models.User(
            username=username,
            email=email,
            full_name=full_name,
            hashed_password=get_password_hash(password)
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        result = User(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            guild_rank=user.guild_rank,
            experience_points=user.experience_points,
            missions_completed=user.missions_completed,
            is_active=user.is_active,
            created_at=user.created_at
        )

        db.close()
        return result

    @strawberry.mutation
    def update_user(
        self,
        user_id: int,
        email: Optional[str] = None,
        full_name: Optional[str] = None
    ) -> Optional[User]:
        """
        TODO: Update user information
        """
        pass

    @strawberry.mutation
    def complete_mission(
        self,
        user_id: int,
        mission_id: int,
        score: float = 100.0
    ) -> User:
        """
        TODO: Mark mission as completed
        - Award experience points
        - Update guild rank
        - Return updated user
        """
        pass
```

### 5. Set Up GraphQL Router

Create `app/graphql/schema.py`:

```python
"""
GraphQL Schema
Combines queries and mutations
"""

import strawberry
from app.graphql.queries import Query
from app.graphql.mutations import Mutation

schema = strawberry.Schema(query=Query, mutation=Mutation)
```

Add to `app/main.py`:

```python
from strawberry.fastapi import GraphQLRouter
from app.graphql.schema import schema

# Create GraphQL router
graphql_app = GraphQLRouter(schema)

# Mount GraphQL
app.include_router(graphql_app, prefix="/graphql")
```

### 6. Test GraphQL Queries

Access GraphQL Playground: http://localhost:8000/graphql

Try these queries:

```graphql
# Get user
{
  user(id: 1) {
    username
    email
    guildRank
    experiencePoints
    missionsCompleted
  }
}

# Get leaderboard
{
  leaderboard(limit: 5) {
    rank
    user {
      username
      guildRank
    }
    experiencePoints
  }
}

# Create user
mutation {
  createUser(
    username: "graphqluser"
    email: "graphql@example.com"
    password: "secure123"
    fullName: "GraphQL Tester"
  ) {
    id
    username
    email
    guildRank
  }
}

# Nested query
{
  users(limit: 5) {
    username
    experiencePoints
    missions {
      missionName
      status
      score
    }
  }
}
```

### 7. Implement DataLoader (Bonus)

Solve N+1 query problem:

```python
from strawberry.dataloader import DataLoader

async def load_users(keys: List[int]) -> List[Optional[User]]:
    """
    TODO: Batch load users
    - Load multiple users in one query
    - Prevents N+1 problem
    """
    db = SessionLocal()
    users = db.query(models.User).filter(models.User.id.in_(keys)).all()
    db.close()

    user_map = {u.id: u for u in users}
    return [user_map.get(key) for key in keys]

user_loader = DataLoader(load_fn=load_users)
```

---

## 🧪 Testing Your Solution

Visit http://localhost:8000/graphql and try:

```graphql
# Query multiple users efficiently
{
  user1: user(id: 1) {
    username
    experiencePoints
  }
  user2: user(id: 2) {
    username
    experiencePoints
  }
  topUsers: users(limit: 3) {
    username
    guildRank
  }
}
```

---

## 📖 Key Concepts

### GraphQL vs REST
```
REST:
  GET /users → All user fields
  GET /users/1/missions → Separate request

GraphQL:
  One request, exact fields needed
  {
    user(id: 1) {
      username
      missions { name status }
    }
  }
```

---

## 🎓 Resources

- [GraphQL Official Docs](https://graphql.org/learn/)
- [Strawberry Documentation](https://strawberry.rocks/)
- [GraphQL Best Practices](https://graphql.org/learn/best-practices/)

---

## ✨ Completion Criteria

- [ ] Installed Strawberry GraphQL
- [ ] Created GraphQL types
- [ ] Implemented queries
- [ ] Implemented mutations
- [ ] Set up GraphQL Playground
- [ ] Tested complex nested queries
- [ ] (Bonus) Implemented DataLoader

---

## ⏭️ Next Mission

GraphQL gateway created! Advance to **Mission 13: The Sky Forge** for cloud deployment!

*"The mirror shows many paths to the same truth..."*
