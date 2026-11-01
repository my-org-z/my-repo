# Models for HintAI V2
# SQLAlchemy models for database tables

from app.core.database import Base

from .user import User, UserLogin, UserSubscription, UserRole, UserSubscriptionStatus
from .school import SchoolLevel, SchoolClass, Subject, Chapter, subject_classes
from .exam import (
    ExamType,
    ExamTypeModel,
    ExamPaper,
    ExamDocument,
    ExamSolution,
    ExamFavorite,
    ExamAttempt,
    ExamAnswer,
    ExamResult,
    AccessLevel,
    ExamPaperStatus,
)
from .study import StudySession, StudyGoal, StudyPlan, StudyPlanEvent, StudySessionStatus, StudyGoalStatus
from .study_group import StudyGroup, StudyGroupMember, StudyGroupRole
from .flashcard import Flashcard, FlashcardReview, FlashcardDifficulty
from .gamification import UserAchievement, UserXP, Leaderboard, AchievementType
from .credit import CreditTransaction, SubscriptionPlan, Payment, TransactionType, PaymentStatus, PaymentMethod
from .ai import DocumentEmbedding, Concept, concept_relations
from .resource import LearningResource, ResourceType

__all__ = [
    # User
    "User",
    "UserLogin",
    "UserSubscription",
    "UserRole",
    "UserSubscriptionStatus",
    # School
    "SchoolLevel",
    "SchoolClass",
    "Subject",
    "Chapter",
    "subject_classes",
    # Exam
    "ExamType",
    "ExamTypeModel",
    "ExamPaper",
    "ExamDocument",
    "ExamSolution",
    "ExamFavorite",
    "ExamAttempt",
    "ExamAnswer",
    "ExamResult",
    "AccessLevel",
    "ExamPaperStatus",
    # Study
    "StudySession",
    "StudyGoal",
    "StudyPlan",
    "StudyPlanEvent",
    "StudySessionStatus",
    "StudyGoalStatus",
    # Study Group
    "StudyGroup",
    "StudyGroupMember",
    "StudyGroupRole",
    # Flashcard
    "Flashcard",
    "FlashcardReview",
    "FlashcardDifficulty",
    # Gamification
    "UserAchievement",
    "UserXP",
    "Leaderboard",
    "AchievementType",
    # Credit
    "CreditTransaction",
    "SubscriptionPlan",
    "Payment",
    "TransactionType",
    "PaymentStatus",
    "PaymentMethod",
    # AI
    "DocumentEmbedding",
    "Concept",
    "concept_relations",
    # Resource
    "LearningResource",
    "ResourceType",
]
