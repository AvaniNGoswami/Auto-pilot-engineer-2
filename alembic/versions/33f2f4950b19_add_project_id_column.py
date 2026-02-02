"""add project id column

Revision ID: 33f2f4950b19
Revises: 199385a810b2
Create Date: 2026-02-02 16:02:02.759336

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '33f2f4950b19'
down_revision: Union[str, Sequence[str], None] = '199385a810b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Add project_id column to in_out table."""
    op.add_column(
        'in_out',
        sa.Column('project_id', sa.String(), nullable=True)  # nullable=True so existing rows work
    )


def downgrade() -> None:
    """Remove project_id column from in_out table."""
    op.drop_column('in_out', 'project_id')