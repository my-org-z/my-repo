"""
Study-related models for HintAI V2.
Includes study sessions, goals, plans, and events.
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float, JSON, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from enum import Enum


class StudySessionStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class StudyGoalStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class StudySession(Base):
    """
    Study session (e.g., a Pomodoro session).
    """
    __tablename__ = "study_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Session metadata
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    chapter = Column(String(255))  # Chapter name (not a foreign key to allow flexibility)
    
    # Goals
    goal = Column(Text)  # What the user wants to achieve
    notes = Column(Text)  # Session notes
    
    # Timing
    started_at = Column(DateTime, server_default=func.now())
    ended_at = Column(DateTime)
    duration_minutes = Column(Integer)  # Planned duration
    actual_duration_minutes = Column(Integer)  # Actual duration
    focus_time_minutes = Column(Integer, default=0)  # Time spent focused (without breaks)
    
    # Status
    status = Column(String(20), default=StudySessionStatus.IN_PROGRESS)
    
    # Pomodoro settings
    pomodoro_interval = Column(Integer, default=25)  # Pomodoro interval in minutes
    pomodoro_breaks = Column(Integer, default=5)  # Break duration in minutes
    pomodoro_count = Column(Integer, default=0)  # Number of Pomodoro sessions completed
    
    # Performance
    productivity_score = Column(Float)  # 0-100 score
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="study_sessions")
    subject = relationship("Subject", back_populates="study_sessions")
    chapter_obj = relationship("Chapter", back_populates="study_sessions")
    
    def __repr__(self):
        return f"<StudySession(id={self.id}, user_id={self.user_id}, status={self.status})>"


class StudyGoal(Base):
    """
    Study goal (e.g., "Learn all geometry chapters by next week").
    """
    __tablename__ = "study_goals"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Goal metadata
    title = Column(String(255), nullable=False)
    description = Column(Text)
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    chapter = Column(String(255))  # Chapter name
    
    # Target
    target_date = Column(Date)  # Deadline
    target_xp = Column(Integer)  # XP to gain
    target_hours = Column(Float)  # Hours to study
    
    # Progress
    current_xp = Column(Integer, default=0)
    current_hours = Column(Float, default=0)
    progress_percentage = Column(Float, default=0)
    
    # Status
    status = Column(String(20), default=StudyGoalStatus.PENDING)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    completed_at = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="study_goals")
    subject = relationship("Subject", back_populates="study_goals")
    chapter_obj = relationship("Chapter", back_populates="study_goals")
    
    def __repr__(self):
        return f"<StudyGoal(id={self.id}, user_id={self.user_id}, title={self.title})>"


class StudyPlan(Base):
    """
    Study plan (e.g., "Revision plan for BEPC 2025").
    """
    __tablename__ = "study_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    class_id = Column(Integer, ForeignKey("school_classes.id"))
    
    # Plan metadata
    title = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Timing
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_completed = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="study_plans")
    class_ = relationship("SchoolClass", back_populates="study_plans")
    events = relationship("StudyPlanEvent", back_populates="plan", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<StudyPlan(id={self.id}, user_id={self.user_id}, title={self.title})>"


class StudyPlanEvent(Base):
    """
    Event in a study plan (e.g., "Study Math Chapter 1 on Monday at 2pm").
    """
    __tablename__ = "study_plan_events"
    
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("study_plans.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Event metadata
    title = Column(String(255), nullable=False)
    description = Column(Text)
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    chapter = Column(String(255))  # Chapter name
    
    # Timing
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer)  # Calculated from start/end time
    
    # Reminders
    reminder_sent = Column(Boolean, default=False)
    reminder_time = Column(DateTime)  # When to send reminder
    
    # Status
    is_completed = Column(Boolean, default=False)
    completion_notes = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    plan = relationship("StudyPlan", back_populates="events")
    subject = relationship("Subject", back_populates="study_plan_events")
    chapter_obj = relationship("Chapter", back_populates="study_plan_events")
    
    def __repr__(self):
        return f"<StudyPlanEvent(id={self.id}, plan_id={self.plan_id}, title={self.title})>"
