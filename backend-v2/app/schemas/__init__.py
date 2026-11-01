# Pydantic schemas for HintAI V2

from .auth import (
    UserCreate,
    UserLogin,
    UserResponse,
    TokenResponse,
    TokenRefreshResponse,
)
from .user import UserUpdate, UserProfileResponse
from .exam import (
    ExamPaperCreate,
    ExamPaperUpdate,
    ExamPaperResponse,
    ExamPaperFilter,
    ExamDocumentCreate,
    ExamDocumentResponse,
    ExamSolutionCreate,
    ExamSolutionResponse,
    ExamFavoriteCreate,
    ExamFavoriteResponse,
    ExamAttemptCreate,
    ExamAttemptResponse,
    ExamAnswerCreate,
    ExamAnswerResponse,
    ExamResultResponse,
)
from .school import (
    SchoolLevelCreate,
    SchoolLevelResponse,
    SchoolClassCreate,
    SchoolClassResponse,
    SubjectCreate,
    SubjectResponse,
    ChapterCreate,
    ChapterResponse,
)
from .credit import (
    CreditTransactionCreate,
    CreditTransactionResponse,
    SubscriptionPlanCreate,
    SubscriptionPlanResponse,
    PaymentCreate,
    PaymentResponse,
)
from .ai import (
    AIRequest,
    AIResponse,
    EmbeddingRequest,
    EmbeddingResponse,
    RAGRequest,
    RAGResponse,
)
from .study import (
    StudySessionCreate,
    StudySessionUpdate,
    StudySessionResponse,
    StudyGoalCreate,
    StudyGoalUpdate,
    StudyGoalResponse,
    StudyPlanCreate,
    StudyPlanUpdate,
    StudyPlanResponse,
    StudyPlanEventCreate,
    StudyPlanEventUpdate,
    StudyPlanEventResponse,
)
from .gamification import (
    UserAchievementCreate,
    UserAchievementResponse,
    UserXPCreate,
    UserXPResponse,
    LeaderboardResponse,
)

__all__ = [
    # Auth
    "UserCreate",
    "UserLogin",
    "UserResponse",
    "TokenResponse",
    "TokenRefreshResponse",
    # User
    "UserUpdate",
    "UserProfileResponse",
    # School
    "SchoolLevelCreate",
    "SchoolLevelResponse",
    "SchoolClassCreate",
    "SchoolClassResponse",
    "SubjectCreate",
    "SubjectResponse",
    "ChapterCreate",
    "ChapterResponse",
    # Exam
    "ExamPaperCreate",
    "ExamPaperUpdate",
    "ExamPaperResponse",
    "ExamPaperFilter",
    "ExamDocumentCreate",
    "ExamDocumentResponse",
    "ExamSolutionCreate",
    "ExamSolutionResponse",
    "ExamFavoriteCreate",
    "ExamFavoriteResponse",
    "ExamAttemptCreate",
    "ExamAttemptResponse",
    "ExamAnswerCreate",
    "ExamAnswerResponse",
    "ExamResultResponse",
    # Credit
    "CreditTransactionCreate",
    "CreditTransactionResponse",
    "SubscriptionPlanCreate",
    "SubscriptionPlanResponse",
    "PaymentCreate",
    "PaymentResponse",
    # AI
    "AIRequest",
    "AIResponse",
    "EmbeddingRequest",
    "EmbeddingResponse",
    "RAGRequest",
    "RAGResponse",
    # Study
    "StudySessionCreate",
    "StudySessionUpdate",
    "StudySessionResponse",
    "StudyGoalCreate",
    "StudyGoalUpdate",
    "StudyGoalResponse",
    "StudyPlanCreate",
    "StudyPlanUpdate",
    "StudyPlanResponse",
    "StudyPlanEventCreate",
    "StudyPlanEventUpdate",
    "StudyPlanEventResponse",
    # Gamification
    "UserAchievementCreate",
    "UserAchievementResponse",
    "UserXPCreate",
    "UserXPResponse",
    "LeaderboardResponse",
]
