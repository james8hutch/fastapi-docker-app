"""Add Dummy TaskType row

Revision ID: cdb8f9dfece1
Revises: 62ae3ce6ab05
Create Date: 2025-01-22 11:33:36.997592

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column

# revision identifiers, used by Alembic.
revision = 'cdb8f9dfece1'
down_revision = '62ae3ce6ab05'
branch_labels = None
depends_on = None

# Recreate the `task_types` table schema
task_types_table = table(
    'task_types',
    column('id', sa.Integer),
    column('name', sa.String),
)

def upgrade() -> None:
    # Insert a row into the task_types table, let the database handle the ID
    op.bulk_insert(task_types_table, [{'name': 'Dummy'}])


def downgrade() -> None:
    # Remove the row added during the upgrade
    op.execute("DELETE FROM task_types WHERE name = 'Dummy'")
