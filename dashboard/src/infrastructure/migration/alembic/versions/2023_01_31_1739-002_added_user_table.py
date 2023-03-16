"""Added user table

Revision ID: 002
Revises: 001
Create Date: 2023-01-31 17:39:43.231479

"""
import sqlalchemy as sa
from alembic import op

import src.infrastructure.postgres.models.base

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
                    sa.Column('id', sa.String(length=32), nullable=False),
                    sa.Column('name', sa.String(length=255), nullable=True),
                    sa.Column('email', sa.String(length=255), nullable=True),
                    sa.Column('created_at', src.infrastructure.postgres.models.base.TimeStamp(), nullable=True),
                    sa.Column('deleted_at', src.infrastructure.postgres.models.base.TimeStamp(), nullable=True),
                    sa.Column('deleted', sa.Boolean(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_users_created_at'), 'users', ['created_at'], unique=False)
    op.create_index(op.f('ix_users_deleted_at'), 'users', ['deleted_at'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_deleted_at'), table_name='users')
    op.drop_index(op.f('ix_users_created_at'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
