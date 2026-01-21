"""create schedules table

Revision ID: 40e5647cee92
Revises: 013dea2a4754
Create Date: 2026-01-16 09:28:32.275390

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '40e5647cee92'
down_revision: Union[str, Sequence[str], None] = '013dea2a4754'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
    CREATE TABLE IF NOT EXISTS schedules (
        id SERIAL PRIMARY KEY,
        barber_id INTEGER REFERENCES users (id),
        day_of_week SMALLINT NOT NULL,
        start_time TIME NOT NULL,
        end_time TIME NOT NULL,
        break_start TIME,
        break_end TIME,
        tolerance INTERVAL DEFAULT '00:00:00',
        UNIQUE (barber_id, day_of_week)
    )
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""DROP TABLE IF EXISTS schedules CASCADE""")
