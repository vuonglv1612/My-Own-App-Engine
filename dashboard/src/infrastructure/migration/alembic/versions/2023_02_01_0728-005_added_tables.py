"""Added tables

Revision ID: 005
Revises: 004
Create Date: 2023-02-01 07:28:05.358358

"""
import sqlalchemy as sa
from alembic import op

import src.infrastructure.postgres.models.base

# revision identifiers, used by Alembic.
revision = '005'
down_revision = '004'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('units',
                    sa.Column('id', sa.String(length=32), nullable=False),
                    sa.Column('cpu', sa.Integer(), nullable=True),
                    sa.Column('memory', sa.Integer(), nullable=True),
                    sa.Column('plan_name', sa.String(length=255), nullable=True),
                    sa.Column('price_id', sa.String(length=255), nullable=True),
                    sa.Column('active', sa.Boolean(), nullable=True),
                    sa.Column('created_at', src.infrastructure.postgres.models.base.TimeStamp(), nullable=True),
                    sa.Column('deleted_at', src.infrastructure.postgres.models.base.TimeStamp(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_units_created_at'), 'units', ['created_at'], unique=False)
    op.create_index(op.f('ix_units_deleted_at'), 'units', ['deleted_at'], unique=False)
    op.create_index(op.f('ix_units_price_id'), 'units', ['price_id'], unique=False)
    op.create_table('activities',
                    sa.Column('id', sa.String(length=32), nullable=False),
                    sa.Column('app_id', sa.String(length=32), nullable=True),
                    sa.Column('actor', sa.JSON(), nullable=True),
                    sa.Column('event_type', sa.String(length=255), nullable=True),
                    sa.Column('event', sa.String(length=255), nullable=True),
                    sa.Column('created_at', src.infrastructure.postgres.models.base.TimeStamp(), nullable=True),
                    sa.ForeignKeyConstraint(['app_id'], ['apps.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_activities_app_id'), 'activities', ['app_id'], unique=False)
    op.create_index(op.f('ix_activities_created_at'), 'activities', ['created_at'], unique=False)
    op.create_table('environments',
                    sa.Column('id', sa.String(length=32), nullable=False),
                    sa.Column('app_id', sa.String(length=32), nullable=True),
                    sa.Column('name', sa.String(length=255), nullable=True),
                    sa.Column('value', sa.Text(), nullable=True),
                    sa.ForeignKeyConstraint(['app_id'], ['apps.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_environments_app_id'), 'environments', ['app_id'], unique=False)
    op.create_table('scales',
                    sa.Column('id', sa.String(length=32), nullable=False),
                    sa.Column('app_id', sa.String(length=32), nullable=True),
                    sa.Column('unit_id', sa.String(length=32), nullable=True),
                    sa.Column('replicas', sa.Integer(), nullable=True),
                    sa.Column('created_at', src.infrastructure.postgres.models.base.TimeStamp(), nullable=True),
                    sa.Column('deleted_at', src.infrastructure.postgres.models.base.TimeStamp(), nullable=True),
                    sa.Column('start_time', src.infrastructure.postgres.models.base.TimeStamp(), nullable=True),
                    sa.Column('end_time', src.infrastructure.postgres.models.base.TimeStamp(), nullable=True),
                    sa.Column('active', sa.Boolean(), nullable=True),
                    sa.ForeignKeyConstraint(['app_id'], ['apps.id'], ),
                    sa.ForeignKeyConstraint(['unit_id'], ['units.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_scales_app_id'), 'scales', ['app_id'], unique=False)
    op.create_index(op.f('ix_scales_created_at'), 'scales', ['created_at'], unique=False)
    op.create_index(op.f('ix_scales_deleted_at'), 'scales', ['deleted_at'], unique=False)
    op.create_index(op.f('ix_scales_end_time'), 'scales', ['end_time'], unique=False)
    op.create_index(op.f('ix_scales_start_time'), 'scales', ['start_time'], unique=False)
    op.create_index(op.f('ix_scales_unit_id'), 'scales', ['unit_id'], unique=False)
    op.create_table('deployments',
                    sa.Column('id', sa.String(length=32), nullable=False),
                    sa.Column('app_id', sa.String(length=32), nullable=True),
                    sa.Column('scale_id', sa.String(length=32), nullable=True),
                    sa.Column('created_at', src.infrastructure.postgres.models.base.TimeStamp(), nullable=True),
                    sa.Column('deleted_at', src.infrastructure.postgres.models.base.TimeStamp(), nullable=True),
                    sa.Column('deployment_source', sa.String(length=255), nullable=True),
                    sa.Column('deployment_type', sa.String(length=255), nullable=True),
                    sa.Column('status', sa.String(length=255), nullable=True),
                    sa.Column('version_number', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['app_id'], ['apps.id'], ),
                    sa.ForeignKeyConstraint(['scale_id'], ['scales.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_deployments_app_id'), 'deployments', ['app_id'], unique=False)
    op.create_index(op.f('ix_deployments_created_at'), 'deployments', ['created_at'], unique=False)
    op.create_index(op.f('ix_deployments_deleted_at'), 'deployments', ['deleted_at'], unique=False)
    op.create_index(op.f('ix_deployments_scale_id'), 'deployments', ['scale_id'], unique=False)
    op.drop_index('ix_apps_plan_id', table_name='apps')
    op.drop_constraint('apps_plan_id_fkey', 'apps', type_='foreignkey')
    op.drop_column('apps', 'plan_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('apps', sa.Column('plan_id', sa.VARCHAR(length=32), autoincrement=False, nullable=True))
    op.create_foreign_key('apps_plan_id_fkey', 'apps', 'plans', ['plan_id'], ['id'])
    op.create_index('ix_apps_plan_id', 'apps', ['plan_id'], unique=False)
    op.drop_index(op.f('ix_deployments_scale_id'), table_name='deployments')
    op.drop_index(op.f('ix_deployments_deleted_at'), table_name='deployments')
    op.drop_index(op.f('ix_deployments_created_at'), table_name='deployments')
    op.drop_index(op.f('ix_deployments_app_id'), table_name='deployments')
    op.drop_table('deployments')
    op.drop_index(op.f('ix_scales_unit_id'), table_name='scales')
    op.drop_index(op.f('ix_scales_start_time'), table_name='scales')
    op.drop_index(op.f('ix_scales_end_time'), table_name='scales')
    op.drop_index(op.f('ix_scales_deleted_at'), table_name='scales')
    op.drop_index(op.f('ix_scales_created_at'), table_name='scales')
    op.drop_index(op.f('ix_scales_app_id'), table_name='scales')
    op.drop_table('scales')
    op.drop_index(op.f('ix_environments_app_id'), table_name='environments')
    op.drop_table('environments')
    op.drop_index(op.f('ix_activities_created_at'), table_name='activities')
    op.drop_index(op.f('ix_activities_app_id'), table_name='activities')
    op.drop_table('activities')
    op.drop_index(op.f('ix_units_price_id'), table_name='units')
    op.drop_index(op.f('ix_units_deleted_at'), table_name='units')
    op.drop_index(op.f('ix_units_created_at'), table_name='units')
    op.drop_table('units')
    # ### end Alembic commands ###