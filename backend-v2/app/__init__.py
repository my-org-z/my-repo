# HintAI V2 Backend
# FastAPI Application

from fastapi import FastAPI

# Create FastAPI app
app = FastAPI(
    title="HintAI V2 API",
    description="AI-Powered Educational Platform for K12 & High School Students",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Import and register routes after app creation
# This is done here to avoid circular imports


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
