"""
Database configuration for HintAI V2 using SQLAlchemy with async support.
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.declarative import declarative_base
from backend_v2.app.core.config import settings
import logging

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600,
)

# Create async session factory
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base class for models
Base = declarative_base()


# Dependency to get DB session
async def get_db():
    """
    Dependency function to get a database session.
    Use with FastAPI's Depends().
    """
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logging.error(f"Database error: {e}")
            raise
        finally:
            await session.close()


# Sync version for migrations (Alembic)
def get_sync_engine():
    """
    Get a synchronous engine for migrations.
    """
    from sqlalchemy import create_engine
    sync_url = settings.DATABASE_URL.replace("postgresql+asyncpg", "postgresql")
    return create_engine(sync_url)
