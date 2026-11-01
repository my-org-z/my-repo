"""
Gamification models for HintAI V2.
Includes achievements, XP, and leaderboards.
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend_v2.app.core.database import Base
from enum import Enum


class AchievementType(str, Enum):
    DAILY_STREAK = "daily_streak"
    EXAM_PASSED = "exam_passed"
    CREDITS_EARNED = "credits_earned"
    STUDY_SESSION_COMPLETED = "study_session_completed"
    FLASHCARD_MASTERED = "flashcard_mastered"
    LEVEL_UP = "level_up"
    FIRST_LOGIN = "first_login"
    FIRST_EXAM = "first_exam"
    PERFECT_SCORE = "perfect_score"
    HELP_OTHERS = "help_others"


class UserAchievement(Base):
    """
    User's achievements (badges).
    """
    __tablename__ = "user_achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Achievement metadata
    achievement_type = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    icon = Column(String(50))  # Icon name or URL
    
    # Rewards
    xp_reward = Column(Integer, default=0)
    credit_reward = Column(Integer, default=0)
    
    # Status
    is_unlocked = Column(Boolean, default=False)
    unlocked_at = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="achievements")
    
    __table_args__ = (
        UniqueConstraint("user_id", "achievement_type", name="uq_user_achievement"),
    )
    
    def __repr__(self):
        return f"<UserAchievement(user_id={self.user_id}, achievement_type={self.achievement_type})>"


class UserXP(Base):
    """
    Track XP transactions for users.
    """
    __tablename__ = "user_xp"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # XP details
    amount = Column(Integer, nullable=False)  # Positive for XP gained
    reason = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Metadata
    metadata = Column(JSON, default={})
    reference_id = Column(String(100))  # Reference to related entity
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="xp_transactions")
    
    def __repr__(self):
        return f"<UserXP(id={self.id}, user_id={self.user_id}, amount={self.amount})>"


class Leaderboard(Base):
    """
    Leaderboard for users (weekly, monthly, all-time).
    """
    __tablename__ = "leaderboards"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Leaderboard type
    period = Column(String(20), nullable=False)  # daily, weekly, monthly, all_time
    period_start = Column(DateTime, nullable=False)  # Start of the period
    
    # Scores
    xp = Column(Integer, default=0)
    level = Column(Integer, default=0)
    exam_score = Column(Float, default=0)  # Average exam score
    study_time_minutes = Column(Integer, default=0)
    
    # Rank
    rank = Column(Integer)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    user = relationship("User")
    
    __table_args__ = (
        UniqueConstraint("user_id", "period", "period_start", name="uq_leaderboard_user_period"),
    )
    
    def __repr__(self):
        return f"<Leaderboard(user_id={self.user_id}, period={self.period}, rank={self.rank})>"


# Fix: Define UniqueConstraint for UserAchievement and Leaderboard
from sqlalchemy import UniqueConstraint

UserAchievement.__table_args__ = (
    UniqueConstraint("user_id", "achievement_type", name="uq_user_achievement"),
)

Leaderboard.__table_args__ = (
    UniqueConstraint("user_id", "period", "period_start", name="uq_leaderboard_user_period"),
)
