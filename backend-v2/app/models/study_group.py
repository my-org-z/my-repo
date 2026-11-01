"""
Study group models for HintAI V2.
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from enum import Enum


class StudyGroupRole(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"


class StudyGroup(Base):
    """
    Study group for collaborative learning.
    """
    __tablename__ = "study_groups"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Group metadata
    name = Column(String(255), nullable=False)
    description = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Settings
    max_members = Column(Integer, default=10)
    is_private = Column(Boolean, default=False)
    invite_code = Column(String(20), unique=True)  # Code to join the group
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    created_by_user = relationship("User", foreign_keys=[created_by], back_populates="study_groups_created")
    members = relationship("StudyGroupMember", back_populates="group", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<StudyGroup(id={self.id}, name={self.name})>"


class StudyGroupMember(Base):
    """
    Member of a study group.
    """
    __tablename__ = "study_group_members"
    
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("study_groups.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Member metadata
    role = Column(String(20), default=StudyGroupRole.MEMBER)
    joined_at = Column(DateTime, server_default=func.now())
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    group = relationship("StudyGroup", back_populates="members")
    user = relationship("User", back_populates="study_group_memberships")
    
    def __repr__(self):
        return f"<StudyGroupMember(group_id={self.group_id}, user_id={self.user_id}, role={self.role})>"


# Fix: Define UniqueConstraint for StudyGroupMember
StudyGroupMember.__table_args__ = (
    UniqueConstraint("group_id", "user_id", name="uq_group_user"),
)


# Fix: Define UniqueConstraint for StudyGroupMember
from sqlalchemy import UniqueConstraint

StudyGroupMember.__table_args__ = (
    UniqueConstraint("group_id", "user_id", name="uq_group_user"),
)
