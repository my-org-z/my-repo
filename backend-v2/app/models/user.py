"""
User models for HintAI V2.
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from enum import Enum
import datetime


class UserRole(str, Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"


class UserSubscriptionStatus(str, Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    PENDING = "pending"


class User(Base):
    """
    User model representing a student, teacher, or admin.
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    phone_number = Column(String(20))
    
    # Profile
    role = Column(String(20), default=UserRole.STUDENT)
    avatar_url = Column(String(255))
    bio = Column(Text)
    
    # School info
    school_level_id = Column(Integer, ForeignKey("school_levels.id"))
    school_class_id = Column(Integer, ForeignKey("school_classes.id"))
    
    # Location (for Togo)
    country = Column(String(50), default="Togo")
    city = Column(String(50))
    
    # Credits
    credits = Column(Integer, default=20)  # Free plan starts with 20 credits
    
    # Gamification
    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    
    # Subscription
    subscription_status = Column(String(20), default=UserSubscriptionStatus.PENDING)
    subscription_plan_id = Column(Integer, ForeignKey("subscription_plans.id"))
    subscription_end_date = Column(DateTime)
    
    # Preferences
    preferred_language = Column(String(10), default="fr")
    theme = Column(String(10), default="light")  # light or dark
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_premium = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    last_login = Column(DateTime)
    
    # Relationships
    school_level = relationship("SchoolLevel", back_populates="users")
    school_class = relationship("SchoolClass", back_populates="users")
    subscription_plan = relationship("SubscriptionPlan", back_populates="users")
    
    # User activities
    logins = relationship("UserLogin", back_populates="user", cascade="all, delete-orphan")
    subscriptions = relationship("UserSubscription", back_populates="user", cascade="all, delete-orphan")
    
    # Exam activities
    exam_favorites = relationship("ExamFavorite", back_populates="user", cascade="all, delete-orphan")
    exam_attempts = relationship("ExamAttempt", back_populates="user", cascade="all, delete-orphan")
    
    # Study activities
    study_sessions = relationship("StudySession", back_populates="user", cascade="all, delete-orphan")
    study_goals = relationship("StudyGoal", back_populates="user", cascade="all, delete-orphan")
    study_plans = relationship("StudyPlan", back_populates="user", cascade="all, delete-orphan")
    
    # Flashcards
    flashcards = relationship("Flashcard", back_populates="user", cascade="all, delete-orphan")
    
    # Groups
    study_groups_created = relationship("StudyGroup", back_populates="created_by", cascade="all, delete-orphan")
    study_group_memberships = relationship("StudyGroupMember", back_populates="user", cascade="all, delete-orphan")
    
    # Gamification
    achievements = relationship("UserAchievement", back_populates="user", cascade="all, delete-orphan")
    xp_transactions = relationship("UserXP", back_populates="user", cascade="all, delete-orphan")
    
    # Credits
    credit_transactions = relationship("CreditTransaction", back_populates="user", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="user", cascade="all, delete-orphan")
    
    # AI
    document_embeddings = relationship("DocumentEmbedding", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"


class UserLogin(Base):
    """
    Track user login history.
    """
    __tablename__ = "user_logins"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    ip_address = Column(String(50))
    user_agent = Column(Text)
    device_info = Column(JSON)
    
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="logins")


class UserSubscription(Base):
    """
    Track user subscription history.
    """
    __tablename__ = "user_subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    subscription_plan_id = Column(Integer, ForeignKey("subscription_plans.id"), nullable=False)
    
    status = Column(String(20), default=UserSubscriptionStatus.ACTIVE)
    start_date = Column(DateTime, server_default=func.now())
    end_date = Column(DateTime)
    auto_renew = Column(Boolean, default=True)
    payment_method = Column(String(20))  # tmoney, momo, card
    transaction_id = Column(String(100))
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="subscriptions")
    subscription_plan = relationship("SubscriptionPlan", back_populates="subscriptions")
