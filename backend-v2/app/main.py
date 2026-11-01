"""
Main FastAPI application for HintAI V2.
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.database import get_db
from app.core.security import verify_token
import logging
from datetime import datetime

# Create FastAPI app
app = FastAPI(
    title="HintAI V2 API",
    description="AI-Powered Educational Platform for K12 & High School Students in Togo",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(settings.LOG_FILE),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


# Global exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors."""
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "detail": exc.errors(),
            "message": "Invalid request data",
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    logger.error(f"HTTP Error {exc.status_code}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail if isinstance(exc.detail, str) else "Error",
            "message": exc.detail if isinstance(exc.detail, str) else str(exc.detail),
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors."""
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
        },
    )


# Middleware for request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests."""
    start_time = datetime.now()
    logger.info(f"Request: {request.method} {request.url}")
    
    response = await call_next(request)
    
    duration = (datetime.now() - start_time).total_seconds() * 1000
    logger.info(f"Response: {response.status_code} in {duration:.2f}ms")
    
    return response


# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Check API health."""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat(),
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to HintAI V2 API",
        "version": "2.0.0",
        "docs": "/api/docs",
        "redoc": "/api/redoc",
        "health": "/api/health",
    }


# Import and include routers
try:
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
    
    # Auth routes
    app.include_router(auth_router.router, prefix="/api/auth", tags=["Authentication"])
    
    # User routes
    app.include_router(users_router.router, prefix="/api/users", tags=["Users"])
    
    # Exam routes
    app.include_router(exams_router.router, prefix="/api/exams", tags=["Exams"])
    
    # Credit routes
    app.include_router(credits_router.router, prefix="/api/credits", tags=["Credits"])
    
    # Payment routes
    app.include_router(payments_router.router, prefix="/api/payments", tags=["Payments"])
    
    # AI routes
    app.include_router(ai_router.router, prefix="/api/ai", tags=["AI"])
    
    # Study routes
    app.include_router(study_router.router, prefix="/api/study", tags=["Study"])
    
    # Gamification routes
    app.include_router(gamification_router.router, prefix="/api/gamification", tags=["Gamification"])
    
    logger.info("All API routers loaded successfully")
    
except ImportError as e:
    logger.warning(f"Some API routers not loaded (this is normal during development): {e}")


# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on startup."""
    logger.info("Starting HintAI V2 API...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Database URL: {settings.DATABASE_URL}")
    
    # Initialize database (create tables if needed)
    # This is handled by Alembic migrations
    
    logger.info("HintAI V2 API started successfully")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Run on shutdown."""
    logger.info("Shutting down HintAI V2 API...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
