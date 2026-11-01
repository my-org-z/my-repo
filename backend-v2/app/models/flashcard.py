"""
Flashcard models for HintAI V2.
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from enum import Enum


class FlashcardDifficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Flashcard(Base):
    """
    Flashcard for spaced repetition learning.
    """
    __tablename__ = "flashcards"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Flashcard content
    front_text = Column(Text, nullable=False)  # Question/term
    back_text = Column(Text, nullable=False)  # Answer/definition
    
    # Metadata
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    chapter = Column(String(255))  # Chapter name
    tags = Column(JSON, default=[])  # List of tags
    
    # Difficulty
    difficulty_level = Column(Integer, default=1)  # 1-5
    difficulty = Column(String(20), default=FlashcardDifficulty.MEDIUM)
    
    # Spaced repetition
    last_reviewed = Column(DateTime)
    next_review = Column(DateTime)
    review_count = Column(Integer, default=0)
    mastery_level = Column(Integer, default=0)  # 0-100%
    
    # Status
    is_public = Column(Boolean, default=False)  # Can be shared with others
    is_verified = Column(Boolean, default=False)  # Verified by a teacher
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="flashcards")
    subject = relationship("Subject", back_populates="flashcards")
    reviews = relationship("FlashcardReview", back_populates="flashcard", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Flashcard(id={self.id}, front_text={self.front_text[:20]}...)>"


class FlashcardReview(Base):
    """
    Review session for a flashcard.
    """
    __tablename__ = "flashcard_reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    flashcard_id = Column(Integer, ForeignKey("flashcards.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Review metadata
    ease_factor = Column(Float, default=2.5)  # Ease factor for spaced repetition (SM-2 algorithm)
    interval_days = Column(Integer, default=1)  # Days until next review
    performance = Column(Integer)  # 0-5 (how well the user remembered)
    
    # Timestamps
    reviewed_at = Column(DateTime, server_default=func.now())
    next_review_at = Column(DateTime)
    
    # Relationships
    flashcard = relationship("Flashcard", back_populates="reviews")
    user = relationship("User")
    
    def __repr__(self):
        return f"<FlashcardReview(id={self.id}, flashcard_id={self.flashcard_id}, performance={self.performance})>"
