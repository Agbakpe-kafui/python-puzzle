"""
Database Models
SQLAlchemy ORM models for the Guild Management System.
"""

from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    """
    User model representing Guild members.
    Mission 2: Records of Apprentices
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    guild_rank = Column(String, default="Apprentice")
    experience_points = Column(Integer, default=0)
    missions_completed = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    missions = relationship("MissionProgress", back_populates="user")


class MissionProgress(Base):
    """
    Track user progress through missions.
    Mission 2: Records of Apprentices
    """
    __tablename__ = "mission_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    mission_id = Column(Integer, nullable=False)
    mission_name = Column(String, nullable=False)
    status = Column(String, default="not_started")  # not_started, in_progress, completed
    score = Column(Float, default=0.0)
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="missions")


class APILog(Base):
    """
    Log external API calls.
    Mission 4: External Scrolls
    """
    __tablename__ = "api_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    endpoint = Column(String, nullable=False)
    method = Column(String, default="GET")
    status_code = Column(Integer)
    response_time = Column(Float)  # in milliseconds
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CacheEntry(Base):
    """
    Track cache usage and performance.
    Mission 7: Echo of Time
    """
    __tablename__ = "cache_entries"

    id = Column(Integer, primary_key=True, index=True)
    cache_key = Column(String, unique=True, index=True, nullable=False)
    hit_count = Column(Integer, default=0)
    miss_count = Column(Integer, default=0)
    last_accessed = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
