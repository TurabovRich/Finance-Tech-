"""initial schema

Revision ID: 5b7ad6e9fea5
Revises: 
Create Date: 2026-07-23 01:08:32.933583

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.db.base import Base


# revision identifiers, used by Alembic.
revision: str = '5b7ad6e9fea5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # This is the baseline migration (no prior schema to diff against), so it creates
    # every table straight from the ORM models via metadata rather than hand-written
    # op.create_table() calls. This is a deliberate one-time exception: every migration
    # after this one must use explicit op.* operations (generated via
    # `alembic revision --autogenerate` against a running database) so schema history
    # stays reviewable without executing code.
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)


def downgrade() -> None:
    bind = op.get_bind()
    Base.metadata.drop_all(bind=bind)
