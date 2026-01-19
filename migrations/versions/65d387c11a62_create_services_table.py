"""create services table

Revision ID: 65d387c11a62
Revises: 40e5647cee92
Create Date: 2026-01-16 09:49:16.548932

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '65d387c11a62'
down_revision: Union[str, Sequence[str], None] = '40e5647cee92'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
    CREATE TABLE IF NOT EXISTS catalog_items (
        id SERIAL PRIMARY KEY,
        barber_id INTEGER REFERENCES users (id),
        name VARCHAR(100) NOT NULL,
        description TEXT,
        price NUMERIC(10, 2) NOT NULL,
        duration INTERVAL NOT NULL
    )
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""DROP TABLE IF EXISTS catalog_items CASCADE""")
