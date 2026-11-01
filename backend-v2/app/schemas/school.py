"""
School schemas for HintAI V2.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class SchoolLevelCreate(BaseModel):
    """Schema for creating a school level."""
    name: str = Field(..., description="Level name", example="Collège")
    description: Optional[str] = Field(None, description="Level description")
    order: Optional[int] = Field(0, description="Order for sorting")

    class Config:
        from_attributes = True


class SchoolLevelResponse(BaseModel):
    """Schema for school level response."""
    id: int
    name: str
    description: Optional[str] = None
    order: int
    created_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Collège",
                "description": "Niveau collège (6e à 3e)",
                "order": 0,
                "created_at": "2024-01-01T00:00:00",
            }
        }


class SchoolClassCreate(BaseModel):
    """Schema for creating a school class."""
    level_id: int = Field(..., description="School level ID")
    name: str = Field(..., description="Class name", example="6e")
    short_name: str = Field(..., description="Short name", example="6")
    description: Optional[str] = Field(None, description="Class description")
    order: Optional[int] = Field(0, description="Order for sorting")

    class Config:
        from_attributes = True


class SchoolClassResponse(BaseModel):
    """Schema for school class response."""
    id: int
    level_id: int
    name: str
    short_name: str
    description: Optional[str] = None
    order: int
    created_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "level_id": 1,
                "name": "6e",
                "short_name": "6",
                "description": "Sixième",
                "order": 0,
                "created_at": "2024-01-01T00:00:00",
            }
        }


class SubjectCreate(BaseModel):
    """Schema for creating a subject."""
    name: str = Field(..., description="Subject name", example="Mathématiques")
    short_name: str = Field(..., description="Short name", example="Maths")
    description: Optional[str] = Field(None, description="Subject description")
    icon: Optional[str] = Field(None, description="Icon name or URL")
    color: Optional[str] = Field("#4F46E5", description="Hex color code")
    order: Optional[int] = Field(0, description="Order for sorting")

    class Config:
        from_attributes = True


class SubjectResponse(BaseModel):
    """Schema for subject response."""
    id: int
    name: str
    short_name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    color: str
    order: int
    created_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Mathématiques",
                "short_name": "Maths",
                "description": "Mathématiques pour le collège et le lycée",
                "icon": "math-icon",
                "color": "#4F46E5",
                "order": 0,
                "created_at": "2024-01-01T00:00:00",
            }
        }


class ChapterCreate(BaseModel):
    """Schema for creating a chapter."""
    subject_id: int = Field(..., description="Subject ID")
    name: str = Field(..., description="Chapter name", example="Fonctions linéaires")
    description: Optional[str] = Field(None, description="Chapter description")
    order: Optional[int] = Field(0, description="Order for sorting")

    class Config:
        from_attributes = True


class ChapterResponse(BaseModel):
    """Schema for chapter response."""
    id: int
    subject_id: int
    name: str
    description: Optional[str] = None
    order: int
    created_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "subject_id": 1,
                "name": "Fonctions linéaires",
                "description": "Étude des fonctions linéaires et affines",
                "order": 0,
                "created_at": "2024-01-01T00:00:00",
            }
        }
