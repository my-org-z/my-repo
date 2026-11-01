"""
Exam schemas for HintAI V2.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ExamType(str, Enum):
    DEVOIR = "devoir"
    COMPOSITION = "composition"
    BEPC = "bepec"
    BAC1 = "bac1"
    BAC2 = "bac2"
    QUIZ = "quiz"
    EXERCISE = "exercise"


class AccessLevel(str, Enum):
    FREE = "free"
    BASIC = "basic"
    PRO = "pro"
    PREMIUM = "premium"


class ExamPaperStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class ExamPaperCreate(BaseModel):
    """Schema for creating an exam paper."""
    title: str = Field(..., description="Exam paper title")
    description: Optional[str] = Field(None, description="Exam paper description")
    class_id: int = Field(..., description="School class ID")
    subject_id: int = Field(..., description="Subject ID")
    exam_type_id: int = Field(..., description="Exam type ID")
    year: int = Field(..., description="Exam year")
    country: Optional[str] = Field("Togo", description="Country")
    difficulty_level: Optional[int] = Field(3, description="Difficulty level (1-5)")
    status: Optional[ExamPaperStatus] = Field(ExamPaperStatus.PUBLISHED, description="Exam paper status")
    is_verified: Optional[bool] = Field(False, description="Is verified by a teacher")
    access_level: Optional[AccessLevel] = Field(AccessLevel.FREE, description="Access level")
    is_public: Optional[bool] = Field(True, description="Is public")
    tags: Optional[List[str]] = Field([], description="Tags for filtering")
    extra_data: Optional[dict] = Field({}, description="Additional metadata")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "title": "BEPC 2023 - Mathématiques",
                "description": "Épreuve de mathématiques du BEPC 2023",
                "class_id": 4,
                "subject_id": 1,
                "exam_type_id": 3,
                "year": 2023,
                "country": "Togo",
                "difficulty_level": 4,
                "status": "published",
                "is_verified": True,
                "access_level": "free",
                "is_public": True,
                "tags": ["bepec", "maths", "2023"],
                "extra_data": {},
            }
        }


class ExamPaperUpdate(BaseModel):
    """Schema for updating an exam paper."""
    title: Optional[str] = Field(None, description="Exam paper title")
    description: Optional[str] = Field(None, description="Exam paper description")
    class_id: Optional[int] = Field(None, description="School class ID")
    subject_id: Optional[int] = Field(None, description="Subject ID")
    exam_type_id: Optional[int] = Field(None, description="Exam type ID")
    year: Optional[int] = Field(None, description="Exam year")
    country: Optional[str] = Field(None, description="Country")
    difficulty_level: Optional[int] = Field(None, description="Difficulty level (1-5)")
    status: Optional[ExamPaperStatus] = Field(None, description="Exam paper status")
    is_verified: Optional[bool] = Field(None, description="Is verified by a teacher")
    access_level: Optional[AccessLevel] = Field(None, description="Access level")
    is_public: Optional[bool] = Field(None, description="Is public")
    tags: Optional[List[str]] = Field(None, description="Tags for filtering")
    extra_data: Optional[dict] = Field(None, description="Additional metadata")

    class Config:
        from_attributes = True


class ExamPaperResponse(BaseModel):
    """Schema for exam paper response."""
    id: int
    title: str
    description: Optional[str] = None
    class_id: Optional[int] = None
    subject_id: Optional[int] = None
    exam_type_id: Optional[int] = None
    year: int
    country: str
    difficulty_level: int
    status: ExamPaperStatus
    is_verified: bool
    access_level: AccessLevel
    is_public: bool
    tags: List[str]
    extra_data: dict
    created_at: datetime
    updated_at: Optional[datetime] = None
    published_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "BEPC 2023 - Mathématiques",
                "description": "Épreuve de mathématiques du BEPC 2023",
                "class_id": 4,
                "subject_id": 1,
                "exam_type_id": 3,
                "year": 2023,
                "country": "Togo",
                "difficulty_level": 4,
                "status": "published",
                "is_verified": True,
                "access_level": "free",
                "is_public": True,
                "tags": ["bepec", "maths", "2023"],
                "extra_data": {},
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-15T12:00:00",
                "published_at": "2024-01-01T00:00:00",
            }
        }


class ExamPaperFilter(BaseModel):
    """Schema for filtering exam papers."""
    class_id: Optional[int] = Field(None, description="Filter by class ID")
    subject_id: Optional[int] = Field(None, description="Filter by subject ID")
    exam_type_id: Optional[int] = Field(None, description="Filter by exam type ID")
    year: Optional[int] = Field(None, description="Filter by year")
    country: Optional[str] = Field("Togo", description="Filter by country")
    difficulty_level: Optional[int] = Field(None, description="Filter by difficulty level")
    is_verified: Optional[bool] = Field(None, description="Filter by verification status")
    access_level: Optional[AccessLevel] = Field(None, description="Filter by access level")
    search: Optional[str] = Field(None, description="Search in title and description")
    limit: Optional[int] = Field(20, description="Limit number of results")
    offset: Optional[int] = Field(0, description="Offset for pagination")
    order_by: Optional[str] = Field("year", description="Order by field")
    order: Optional[str] = Field("desc", description="Order direction (asc/desc)")

    class Config:
        from_attributes = True


class ExamDocumentCreate(BaseModel):
    """Schema for creating an exam document."""
    exam_paper_id: int = Field(..., description="Exam paper ID")
    file_path: str = Field(..., description="File path")
    file_url: Optional[str] = Field(None, description="File URL")
    file_name: Optional[str] = Field(None, description="File name")
    file_size: int = Field(..., description="File size in bytes")
    file_hash: str = Field(..., description="File hash (SHA-256)")
    file_type: Optional[str] = Field("pdf", description="File type")
    page_count: Optional[int] = Field(None, description="Number of pages")
    language: Optional[str] = Field("fr", description="Language")
    access_level: Optional[AccessLevel] = Field(AccessLevel.FREE, description="Access level")
    is_public: Optional[bool] = Field(True, description="Is public")

    class Config:
        from_attributes = True


class ExamDocumentResponse(BaseModel):
    """Schema for exam document response."""
    id: int
    exam_paper_id: int
    file_path: str
    file_url: Optional[str] = None
    file_name: Optional[str] = None
    file_size: int
    file_hash: str
    file_type: str
    page_count: Optional[int] = None
    language: str
    access_level: AccessLevel
    is_public: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ExamSolutionCreate(BaseModel):
    """Schema for creating an exam solution."""
    exam_paper_id: int = Field(..., description="Exam paper ID")
    document_id: Optional[int] = Field(None, description="Document ID")
    content: Optional[str] = Field(None, description="Solution content")
    is_official: Optional[bool] = Field(False, description="Is official solution")
    verified_by: Optional[int] = Field(None, description="User ID who verified")

    class Config:
        from_attributes = True


class ExamSolutionResponse(BaseModel):
    """Schema for exam solution response."""
    id: int
    exam_paper_id: int
    document_id: Optional[int] = None
    content: Optional[str] = None
    is_official: bool
    verified_by: Optional[int] = None
    verification_date: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ExamFavoriteCreate(BaseModel):
    """Schema for creating an exam favorite."""
    exam_paper_id: int = Field(..., description="Exam paper ID")

    class Config:
        from_attributes = True


class ExamFavoriteResponse(BaseModel):
    """Schema for exam favorite response."""
    id: int
    user_id: int
    exam_paper_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ExamAttemptCreate(BaseModel):
    """Schema for creating an exam attempt."""
    exam_paper_id: int = Field(..., description="Exam paper ID")

    class Config:
        from_attributes = True


class ExamAttemptResponse(BaseModel):
    """Schema for exam attempt response."""
    id: int
    user_id: int
    exam_paper_id: int
    started_at: datetime
    ended_at: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    status: str
    total_score: float
    max_score: float
    percentage: Optional[float] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ExamAnswerCreate(BaseModel):
    """Schema for creating an exam answer."""
    attempt_id: int = Field(..., description="Exam attempt ID")
    question_number: int = Field(..., description="Question number")
    question_text: Optional[str] = Field(None, description="Question text")
    question_type: Optional[str] = Field(None, description="Question type")
    user_answer: str = Field(..., description="User answer")

    class Config:
        from_attributes = True


class ExamAnswerResponse(BaseModel):
    """Schema for exam answer response."""
    id: int
    attempt_id: int
    question_number: int
    question_text: Optional[str] = None
    question_type: Optional[str] = None
    user_answer: str
    is_correct: Optional[bool] = None
    score: float
    feedback: Optional[str] = None
    correct_answer: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ExamResultResponse(BaseModel):
    """Schema for exam result response."""
    id: int
    attempt_id: int
    total_score: float
    max_score: float
    percentage: float
    grade: Optional[str] = None
    feedback: Optional[str] = None
    strengths: List[str]
    weaknesses: List[str]
    recommendations: Optional[str] = None
    ai_analysis: dict
    created_at: datetime

    class Config:
        from_attributes = True
