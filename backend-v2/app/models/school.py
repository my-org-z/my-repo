"""
School-related models for HintAI V2.
Includes levels, classes, subjects, and chapters.
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.core.database import Base


class SchoolLevel(Base):
    """
    School level (e.g., College, Lycée).
    """
    __tablename__ = "school_levels"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    order = Column(Integer, default=0)  # For sorting
    
    # Relationships
    classes = relationship("SchoolClass", back_populates="level", cascade="all, delete-orphan")
    users = relationship("User", back_populates="school_level")
    
    def __repr__(self):
        return f"<SchoolLevel(id={self.id}, name={self.name})>"


class SchoolClass(Base):
    """
    School class (e.g., 6e, 5e, ..., Terminale).
    """
    __tablename__ = "school_classes"
    
    id = Column(Integer, primary_key=True, index=True)
    level_id = Column(Integer, ForeignKey("school_levels.id"), nullable=False)
    name = Column(String(50), unique=True, nullable=False)  # e.g., "6e", "Seconde"
    short_name = Column(String(10), nullable=False)  # e.g., "6", "2nd"
    description = Column(Text)
    order = Column(Integer, default=0)  # For sorting
    
    # Relationships
    level = relationship("SchoolLevel", back_populates="classes")
    subjects = relationship("Subject", back_populates="classes", cascade="all, delete-orphan")
    users = relationship("User", back_populates="school_class")
    exam_papers = relationship("ExamPaper", back_populates="class_", cascade="all, delete-orphan")
    study_plans = relationship("StudyPlan", back_populates="class_", cascade="all, delete-orphan")
    learning_resources = relationship("LearningResource", back_populates="class_", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<SchoolClass(id={self.id}, name={self.name})>"


class Subject(Base):
    """
    School subject (e.g., Mathématiques, Physique-Chimie).
    """
    __tablename__ = "subjects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)  # e.g., "Mathématiques"
    short_name = Column(String(20), nullable=False)  # e.g., "Maths"
    description = Column(Text)
    icon = Column(String(50))  # Icon name or URL
    color = Column(String(7), default="#4F46E5")  # Hex color code
    order = Column(Integer, default=0)  # For sorting
    
    # Relationships
    chapters = relationship("Chapter", back_populates="subject", cascade="all, delete-orphan")
    classes = relationship("SchoolClass", secondary="subject_classes", back_populates="subjects")
    exam_papers = relationship("ExamPaper", back_populates="subject", cascade="all, delete-orphan")
    study_sessions = relationship("StudySession", back_populates="subject", cascade="all, delete-orphan")
    study_goals = relationship("StudyGoal", back_populates="subject", cascade="all, delete-orphan")
    flashcards = relationship("Flashcard", back_populates="subject", cascade="all, delete-orphan")
    learning_resources = relationship("LearningResource", back_populates="subject", cascade="all, delete-orphan")
    concepts = relationship("Concept", back_populates="subject", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Subject(id={self.id}, name={self.name})>"


# Many-to-many relationship between subjects and classes
subject_classes = Table(
    "subject_classes",
    Base.metadata,
    Column("subject_id", Integer, ForeignKey("subjects.id", ondelete="CASCADE"), primary_key=True),
    Column("class_id", Integer, ForeignKey("school_classes.id", ondelete="CASCADE"), primary_key=True),
)


class Chapter(Base):
    """
    Chapter within a subject (e.g., "Fonctions linéaires" in Math).
    """
    __tablename__ = "chapters"
    
    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    order = Column(Integer, default=0)  # For sorting
    
    # Relationships
    subject = relationship("Subject", back_populates="chapters")
    learning_resources = relationship("LearningResource", back_populates="chapter", cascade="all, delete-orphan")
    study_sessions = relationship("StudySession", back_populates="chapter_obj", cascade="all, delete-orphan")
    study_goals = relationship("StudyGoal", back_populates="chapter_obj", cascade="all, delete-orphan")
    concepts = relationship("Concept", back_populates="chapter", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Chapter(id={self.id}, name={self.name})>"
