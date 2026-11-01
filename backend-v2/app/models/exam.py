"""
Exam-related models for HintAI V2.
Includes exam types, papers, documents, solutions, favorites, attempts, answers, and results.
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend_v2.app.core.database import Base
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


class ExamTypeModel(Base):
    """
    Type of exam (e.g., Devoir, Composition, BEPC, BAC1, BAC2).
    """
    __tablename__ = "exam_types"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    is_official = Column(Boolean, default=False)  # BEPC/BAC = True
    order = Column(Integer, default=0)  # For sorting
    
    # Relationships
    exam_papers = relationship("ExamPaper", back_populates="exam_type", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<ExamType(id={self.id}, name={self.name})>"


class ExamPaper(Base):
    """
    Exam paper (e.g., a specific BEPC 2023 Math exam).
    """
    __tablename__ = "exam_papers"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Foreign keys
    class_id = Column(Integer, ForeignKey("school_classes.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    exam_type_id = Column(Integer, ForeignKey("exam_types.id"))
    
    # Exam metadata
    year = Column(Integer, nullable=False)
    country = Column(String(50), default="Togo")
    difficulty_level = Column(Integer, default=3)  # 1-5
    status = Column(String(20), default=ExamPaperStatus.PUBLISHED)
    is_verified = Column(Boolean, default=False)  # Corrigé validé par un prof
    
    # Access control
    access_level = Column(String(20), default=AccessLevel.FREE)
    is_public = Column(Boolean, default=True)
    
    # SEO & Metadata
    tags = Column(JSON, default=[])  # List of tags for filtering
    metadata = Column(JSON, default={})  # Additional metadata
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    published_at = Column(DateTime)
    
    # Relationships
    class_ = relationship("SchoolClass", back_populates="exam_papers")
    subject = relationship("Subject", back_populates="exam_papers")
    exam_type = relationship("ExamTypeModel", back_populates="exam_papers")
    
    # Documents
    documents = relationship("ExamDocument", back_populates="exam_paper", cascade="all, delete-orphan")
    solutions = relationship("ExamSolution", back_populates="exam_paper", cascade="all, delete-orphan")
    
    # User interactions
    favorites = relationship("ExamFavorite", back_populates="exam_paper", cascade="all, delete-orphan")
    attempts = relationship("ExamAttempt", back_populates="exam_paper", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<ExamPaper(id={self.id}, title={self.title})>"


class ExamDocument(Base):
    """
    Document associated with an exam paper (PDF, image, etc.).
    """
    __tablename__ = "exam_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    exam_paper_id = Column(Integer, ForeignKey("exam_papers.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # File metadata
    file_path = Column(String(255), nullable=False)
    file_url = Column(String(500))  # URL if stored in cloud storage
    file_name = Column(String(255))
    file_size = Column(Integer, nullable=False)  # Size in bytes
    file_hash = Column(String(64), nullable=False)  # SHA-256 hash
    file_type = Column(String(50), default="pdf")  # pdf, jpg, png, etc.
    
    # Document metadata
    page_count = Column(Integer)
    language = Column(String(10), default="fr")
    
    # Access control
    access_level = Column(String(20), default=AccessLevel.FREE)
    is_public = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    exam_paper = relationship("ExamPaper", back_populates="documents")
    solution = relationship("ExamSolution", back_populates="document", uselist=False)
    
    def __repr__(self):
        return f"<ExamDocument(id={self.id}, file_name={self.file_name})>"


class ExamSolution(Base):
    """
    Solution for an exam paper.
    """
    __tablename__ = "exam_solutions"
    
    id = Column(Integer, primary_key=True, index=True)
    exam_paper_id = Column(Integer, ForeignKey("exam_papers.id", ondelete="CASCADE"), nullable=False, index=True)
    document_id = Column(Integer, ForeignKey("exam_documents.id", ondelete="SET NULL"))
    
    # Solution content
    content = Column(Text)  # Text version of the solution
    
    # Metadata
    is_official = Column(Boolean, default=False)  # Official solution
    verified_by = Column(Integer, ForeignKey("users.id"))  # Who verified this solution
    verification_date = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    exam_paper = relationship("ExamPaper", back_populates="solutions")
    document = relationship("ExamDocument", back_populates="solution")
    verified_by_user = relationship("User", foreign_keys=[verified_by])
    
    def __repr__(self):
        return f"<ExamSolution(id={self.id}, exam_paper_id={self.exam_paper_id})>"


class ExamFavorite(Base):
    """
    User's favorite exam papers.
    """
    __tablename__ = "exam_favorites"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    exam_paper_id = Column(Integer, ForeignKey("exam_papers.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="exam_favorites")
    exam_paper = relationship("ExamPaper", back_populates="favorites")
    
    __table_args__ = (
        UniqueConstraint("user_id", "exam_paper_id", name="uq_user_exam_favorite"),
    )
    
    def __repr__(self):
        return f"<ExamFavorite(user_id={self.user_id}, exam_paper_id={self.exam_paper_id})>"


class ExamAttempt(Base):
    """
    User's attempt at an exam.
    """
    __tablename__ = "exam_attempts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    exam_paper_id = Column(Integer, ForeignKey("exam_papers.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Attempt metadata
    started_at = Column(DateTime, server_default=func.now())
    ended_at = Column(DateTime)
    duration_minutes = Column(Integer)  # Actual duration in minutes
    
    # Status
    status = Column(String(20), default="in_progress")  # in_progress, completed, abandoned
    
    # Scores
    total_score = Column(Float, default=0)
    max_score = Column(Float, default=0)
    percentage = Column(Float)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="exam_attempts")
    exam_paper = relationship("ExamPaper", back_populates="attempts")
    answers = relationship("ExamAnswer", back_populates="attempt", cascade="all, delete-orphan")
    result = relationship("ExamResult", back_populates="attempt", uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<ExamAttempt(id={self.id}, user_id={self.user_id}, status={self.status})>"


class ExamAnswer(Base):
    """
    User's answer to an exam question.
    """
    __tablename__ = "exam_answers"
    
    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("exam_attempts.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Question metadata
    question_number = Column(Integer, nullable=False)
    question_text = Column(Text)
    question_type = Column(String(20))  # multiple_choice, open_ended, etc.
    
    # User's answer
    user_answer = Column(Text)
    is_correct = Column(Boolean)
    score = Column(Float, default=0)
    
    # Feedback
    feedback = Column(Text)
    correct_answer = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    attempt = relationship("ExamAttempt", back_populates="answers")
    
    def __repr__(self):
        return f"<ExamAnswer(id={self.id}, attempt_id={self.attempt_id})>"


class ExamResult(Base):
    """
    Result of an exam attempt.
    """
    __tablename__ = "exam_results"
    
    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("exam_attempts.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    
    # Scores
    total_score = Column(Float, nullable=False)
    max_score = Column(Float, nullable=False)
    percentage = Column(Float, nullable=False)
    grade = Column(String(10))  # A, B, C, etc.
    
    # Feedback
    feedback = Column(Text)
    strengths = Column(JSON, default=[])  # List of strengths
    weaknesses = Column(JSON, default=[])  # List of weaknesses
    recommendations = Column(Text)
    
    # AI Analysis
    ai_analysis = Column(JSON, default={})
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    attempt = relationship("ExamAttempt", back_populates="result")
    
    def __repr__(self):
        return f"<ExamResult(id={self.id}, attempt_id={self.attempt_id}, percentage={self.percentage})>"


# Fix: Define UniqueConstraint for ExamFavorite
from sqlalchemy import UniqueConstraint

ExamFavorite.__table_args__ = (
    UniqueConstraint("user_id", "exam_paper_id", name="uq_user_exam_favorite"),
)
