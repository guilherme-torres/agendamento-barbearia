"""create appointments table

Revision ID: 24c587a14352
Revises: 65d387c11a62
Create Date: 2026-01-16 10:07:42.724122

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '24c587a14352'
down_revision: Union[str, Sequence[str], None] = '65d387c11a62'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id SERIAL PRIMARY KEY,
        client_id INTEGER REFERENCES users (id),
        barber_id INTEGER REFERENCES users (id),
        catalog_item_id INTEGER REFERENCES catalog_items (id),
        appointment_date DATE NOT NULL,
        appointment_time TIME NOT NULL,
        status VARCHAR(10) CHECK (status in ('scheduled', 'finished', 'canceled')) DEFAULT 'scheduled',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""DROP TABLE IF EXISTS appointments CASCADE""")
