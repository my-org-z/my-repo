# Models for HintAI V2
# SQLAlchemy models for database tables

from .user import User, UserLogin, UserSubscription
from .school import SchoolLevel, SchoolClass, Subject, Chapter
from .exam import (
    ExamType,
    ExamPaper,
    ExamDocument,
    ExamSolution,
    ExamFavorite,
    ExamAttempt,
    ExamAnswer,
    ExamResult,
)
from .study import StudySession, StudyGoal, StudyPlan, StudyPlanEvent
from .study_group import StudyGroup, StudyGroupMember
from .flashcard import Flashcard, FlashcardReview
from .gamification import UserAchievement, UserXP, Leaderboard
from .credit import CreditTransaction, SubscriptionPlan, Payment
from .ai import DocumentEmbedding, Concept, concept_relations
from .resource import LearningResource

__all__ = [
    # User
    "User",
    "UserLogin",
    "UserSubscription",
    # School
    "SchoolLevel",
    "SchoolClass",
    "Subject",
    "Chapter",
    # Exam
    "ExamType",
    "ExamPaper",
    "ExamDocument",
    "ExamSolution",
    "ExamFavorite",
    "ExamAttempt",
    "ExamAnswer",
    "ExamResult",
    # Study
    "StudySession",
    "StudyGoal",
    "StudyPlan",
    "StudyPlanEvent",
    # Study Group
    "StudyGroup",
    "StudyGroupMember",
    # Flashcard
    "Flashcard",
    "FlashcardReview",
    # Gamification
    "UserAchievement",
    "UserXP",
    "Leaderboard",
    # Credit
    "CreditTransaction",
    "SubscriptionPlan",
    "Payment",
    # AI
    "DocumentEmbedding",
    "Concept",
    "concept_relations",
    # Resource
    "LearningResource",
]
