"""
User schemas for HintAI V2.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum
from .auth import UserRole


class UserUpdate(BaseModel):
    """Schema for updating user information."""
    full_name: Optional[str] = Field(None, description="User full name")
    phone_number: Optional[str] = Field(None, description="User phone number")
    avatar_url: Optional[str] = Field(None, description="User avatar URL")
    bio: Optional[str] = Field(None, description="User biography")
    country: Optional[str] = Field(None, description="User country")
    city: Optional[str] = Field(None, description="User city")
    preferred_language: Optional[str] = Field(None, description="Preferred language")
    theme: Optional[str] = Field(None, description="Theme (light/dark)")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "full_name": "John Doe Updated",
                "phone_number": "+22898765432",
                "avatar_url": "https://example.com/new-avatar.jpg",
                "bio": "Student at Lycée de Lomé",
                "country": "Togo",
                "city": "Lomé",
                "preferred_language": "fr",
                "theme": "dark",
            }
        }


class UserProfileResponse(BaseModel):
    """Schema for user profile response."""
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    role: UserRole
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    country: str
    city: Optional[str] = None
    school_level_id: Optional[int] = None
    school_class_id: Optional[int] = None
    credits: int
    xp: int
    level: int
    subscription_status: str
    subscription_plan_id: Optional[int] = None
    subscription_end_date: Optional[datetime] = None
    is_active: bool
    is_verified: bool
    is_premium: bool
    preferred_language: str
    theme: str
    created_at: datetime
    updated_at: Optional[datetime] = None
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
                "bio": "Student at Lycée de Lomé",
                "country": "Togo",
                "city": "Lomé",
                "school_level_id": 1,
                "school_class_id": 5,
                "credits": 20,
                "xp": 150,
                "level": 2,
                "subscription_status": "active",
                "subscription_plan_id": 1,
                "subscription_end_date": "2024-12-31T23:59:59",
                "is_active": True,
                "is_verified": False,
                "is_premium": False,
                "preferred_language": "fr",
                "theme": "light",
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-15T12:00:00",
                "last_login": "2024-01-20T08:00:00",
            }
        }
