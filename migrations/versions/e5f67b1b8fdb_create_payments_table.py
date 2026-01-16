"""create payments table

Revision ID: e5f67b1b8fdb
Revises: 24c587a14352
Create Date: 2026-01-16 10:34:25.503139

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e5f67b1b8fdb'
down_revision: Union[str, Sequence[str], None] = '24c587a14352'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        id SERIAL PRIMARY KEY,
        appointment_id INTEGER REFERENCES appointments (id),
        amount NUMERIC(10, 2) NOT NULL,
        method VARCHAR(30) NOT NULL CHECK (method in ('pix', 'debit', 'credit', 'cash')),
        paid_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""DROP TABLE IF EXISTS payments CASCADE""")
