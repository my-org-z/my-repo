"""
${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# pgvector support
from pgvector.sqlalchemy import Vector


# Helper functions for pgvector

def upgrade():
    ${imports if imports else ""}
    ${upgrade_ops}


def downgrade():
    ${downgrade_ops}
