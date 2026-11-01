"""
Learning resource models for HintAI V2.
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from enum import Enum


class ResourceType(str, Enum):
    VIDEO = "video"
    PDF = "pdf"
    ARTICLE = "article"
    QUIZ = "quiz"
    INTERACTIVE = "interactive"
    AUDIO = "audio"


class LearningResource(Base):
    """
    Learning resource (e.g., video, PDF, article).
    """
    __tablename__ = "learning_resources"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Resource metadata
    title = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Categorization
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    class_id = Column(Integer, ForeignKey("school_classes.id"))
    chapter_id = Column(Integer, ForeignKey("chapters.id"))
    
    # Resource type
    resource_type = Column(String(20), nullable=False)  # ResourceType enum
    
    # Content
    content = Column(Text)  # For text-based resources
    file_path = Column(String(255))  # Local file path
    file_url = Column(String(500))  # URL if stored in cloud storage
    
    # Media metadata
    duration_minutes = Column(Integer)  # For videos/audio
    file_size = Column(Integer)  # Size in bytes
    file_hash = Column(String(64))  # SHA-256 hash
    
    # Access control
    is_public = Column(Boolean, default=True)
    is_premium = Column(Boolean, default=False)
    access_level = Column(String(20), default="free")  # free, basic, pro, premium
    
    # Metadata
    author = Column(String(255))
    source = Column(String(255))
    tags = Column(JSON, default=[])  # List of tags
    
    # Status
    is_verified = Column(Boolean, default=False)
    verified_by = Column(Integer, ForeignKey("users.id"))
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    subject = relationship("Subject", back_populates="learning_resources")
    class_ = relationship("SchoolClass", back_populates="learning_resources")
    chapter = relationship("Chapter", back_populates="learning_resources")
    verified_by_user = relationship("User", foreign_keys=[verified_by])
    
    def __repr__(self):
        return f"<LearningResource(id={self.id}, title={self.title})>"
