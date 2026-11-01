# HintAI V2 Backend
# FastAPI Application

from fastapi import FastAPI

app = FastAPI()

# Import routers to register routes
from app.api import (
    auth_router,
    users_router,
    exams_router,
    credits_router,
    payments_router,
    ai_router,
    study_router,
    gamification_router,
)

# Register routers
app.include_router(auth_router.router, prefix="/api/auth", tags=["auth"])
app.include_router(users_router.router, prefix="/api/users", tags=["users"])
app.include_router(exams_router.router, prefix="/api/exams", tags=["exams"])
app.include_router(credits_router.router, prefix="/api/credits", tags=["credits"])
app.include_router(payments_router.router, prefix="/api/payments", tags=["payments"])
app.include_router(ai_router.router, prefix="/api/ai", tags=["ai"])
app.include_router(study_router.router, prefix="/api/study", tags=["study"])
app.include_router(gamification_router.router, prefix="/api/gamification", tags=["gamification"])


@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "version": "2.0.0"}


@app.get("/")
async def root():
    return {
        "message": "Welcome to HintAI V2 API",
        "docs": "/api/docs",
        "redoc": "/api/redoc",
        "health": "/api/health",
    }
