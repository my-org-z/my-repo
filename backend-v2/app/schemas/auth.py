"""
Authentication schemas for HintAI V2.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"


class UserCreate(BaseModel):
    """Schema for creating a new user."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="User password")
    full_name: Optional[str] = Field(None, description="User full name")
    phone_number: Optional[str] = Field(None, description="User phone number")
    role: Optional[UserRole] = Field(UserRole.STUDENT, description="User role")
    country: Optional[str] = Field("Togo", description="User country")
    preferred_language: Optional[str] = Field("fr", description="Preferred language")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "email": "student@example.com",
                "password": "securepassword123",
                "full_name": "John Doe",
                "phone_number": "+22812345678",
                "role": "student",
                "country": "Togo",
                "preferred_language": "fr",
            }
        }


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "email": "student@example.com",
                "password": "securepassword123",
            }
        }


class UserResponse(BaseModel):
    """Schema for user response."""
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    role: UserRole
    avatar_url: Optional[str] = None
    country: str
    city: Optional[str] = None
    credits: int
    xp: int
    level: int
    subscription_status: str
    is_active: bool
    is_verified: bool
    is_premium: bool
    preferred_language: str
    theme: str
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "student@example.com",
                "full_name": "John Doe",
                "phone_number": "+22812345678",
                "role": "student",
                "avatar_url": "https://example.com/avatar.jpg",
                "country": "Togo",
                "city": "Lomé",
                "credits": 20,
                "xp": 100,
                "level": 1,
                "subscription_status": "active",
                "is_active": True,
                "is_verified": False,
                "is_premium": False,
                "preferred_language": "fr",
                "theme": "light",
                "created_at": "2024-01-01T00:00:00",
                "last_login": "2024-01-01T12:00:00",
            }
        }


class TokenResponse(BaseModel):
    """Schema for token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 1800,
            }
        }


class TokenRefreshResponse(BaseModel):
    """Schema for token refresh response."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 1800,
            }
        }
