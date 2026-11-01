"""
Alembic environment configuration for HintAI V2.
"""

import sys
sys.path.insert(0, '/workspace/github__my-org-z__my-repo/backend-v2')

from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from app.core.config import settings
from app.models import Base
import os

# This is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# Skip if no logging config
try:
    if config.config_file_name is not None:
        fileConfig(config.config_file_name)
except Exception:
    pass

# Add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# Override the database URL from environment variable
config.set_main_option(
    "sqlalchemy.url",
    settings.DATABASE_URL.replace("postgresql+asyncpg", "postgresql")
)


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        user_module_prefix="sa.",
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            user_module_prefix="sa.",
            # Enable pgvector extension
            process_revision_directives=process_revision_directives,
        )

        with context.begin_transaction():
            context.run_migrations()


def process_revision_directives(context, revision):
    """
    Process revision directives for pgvector and other extensions.
    """
    migration_context = context
    
    # Check if we're creating the pgvector extension
    if revision.rev == "initial":
        # Add pgvector extension
        migration_context.run_sql("CREATE EXTENSION IF NOT EXISTS vector")
        
    return []


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
