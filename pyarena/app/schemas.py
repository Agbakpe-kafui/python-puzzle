"""
Pydantic Schemas
Request/Response models for API validation and serialization.
"""

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional, List


# User Schemas
class UserBase(BaseModel):
    """Base user schema with common fields"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """Schema for updating user information"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    guild_rank: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user responses (excludes password)"""
    id: int
    is_active: bool
    is_admin: bool
    guild_rank: str
    experience_points: int
    missions_completed: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Authentication Schemas
class Token(BaseModel):
    """JWT Token response"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Data stored in JWT token"""
    username: Optional[str] = None


class LoginRequest(BaseModel):
    """Login credentials"""
    username: str
    password: str


# Mission Schemas
class MissionProgressBase(BaseModel):
    """Base mission progress schema"""
    mission_id: int
    mission_name: str
    status: str = "not_started"


class MissionProgressCreate(MissionProgressBase):
    """Schema for creating mission progress record"""
    pass


class MissionProgressUpdate(BaseModel):
    """Schema for updating mission progress"""
    status: Optional[str] = None
    score: Optional[float] = None


class MissionProgressResponse(MissionProgressBase):
    """Schema for mission progress responses"""
    id: int
    user_id: int
    score: float
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# API Log Schemas
class APILogCreate(BaseModel):
    """Schema for creating API log entry"""
    endpoint: str
    method: str = "GET"
    status_code: int
    response_time: float


class APILogResponse(APILogCreate):
    """Schema for API log responses"""
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Analytics Schemas
class UserStats(BaseModel):
    """User statistics for analytics"""
    total_users: int
    active_users: int
    total_missions_completed: int
    average_experience: float


class MissionStats(BaseModel):
    """Mission completion statistics"""
    mission_id: int
    mission_name: str
    total_attempts: int
    completion_rate: float
    average_score: float


# External API Schemas
class ExternalAPIRequest(BaseModel):
    """Schema for external API requests"""
    url: str
    method: str = "GET"
    headers: Optional[dict] = None
    params: Optional[dict] = None


class ExternalAPIResponse(BaseModel):
    """Schema for external API responses"""
    status_code: int
    data: dict
    response_time: float
