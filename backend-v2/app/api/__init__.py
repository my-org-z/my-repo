# API routers for HintAI V2
# Import and expose all routers

from .auth import router as auth_router
from .users import router as users_router
from .exams import router as exams_router
from .credits import router as credits_router
from .payments import router as payments_router
from .ai import router as ai_router
from .study import router as study_router
from .gamification import router as gamification_router

__all__ = [
    "auth_router",
    "users_router",
    "exams_router",
    "credits_router",
    "payments_router",
    "ai_router",
    "study_router",
    "gamification_router",
]
