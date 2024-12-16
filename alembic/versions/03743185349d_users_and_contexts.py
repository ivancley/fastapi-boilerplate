"""users and contexts

Revision ID: 03743185349d
Revises: 
Create Date: 2024-12-09 11:40:31.394002

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '03743185349d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contexts',
    sa.Column('name', sa.String(length=60), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name', name='uq_context_name'),
    schema='DEV'
    )
    op.create_index(op.f('ix_DEV_contexts_id'), 'contexts', ['id'], unique=True, schema='DEV')
    op.create_index(op.f('ix_DEV_contexts_name'), 'contexts', ['name'], unique=False, schema='DEV')
    op.create_index('ix_context_name', 'contexts', ['name'], unique=False, schema='DEV')
    op.create_table('users',
    sa.Column('name', sa.String(length=60), nullable=False),
    sa.Column('full_name', sa.String(length=120), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email', name='uq_user_email'),
    schema='DEV'
    )
    op.create_index(op.f('ix_DEV_users_email'), 'users', ['email'], unique=True, schema='DEV')
    op.create_index(op.f('ix_DEV_users_full_name'), 'users', ['full_name'], unique=False, schema='DEV')
    op.create_index(op.f('ix_DEV_users_id'), 'users', ['id'], unique=True, schema='DEV')
    op.create_index(op.f('ix_DEV_users_name'), 'users', ['name'], unique=False, schema='DEV')
    op.create_index('ix_user_email', 'users', ['email'], unique=False, schema='DEV')
    op.create_table('user_context',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('context_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['context_id'], ['DEV.contexts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['DEV.users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'context_id'),
    sa.UniqueConstraint('user_id', 'context_id', name='uq_user_context'),
    schema='DEV'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_context', schema='DEV')
    op.drop_index('ix_user_email', table_name='users', schema='DEV')
    op.drop_index(op.f('ix_DEV_users_name'), table_name='users', schema='DEV')
    op.drop_index(op.f('ix_DEV_users_id'), table_name='users', schema='DEV')
    op.drop_index(op.f('ix_DEV_users_full_name'), table_name='users', schema='DEV')
    op.drop_index(op.f('ix_DEV_users_email'), table_name='users', schema='DEV')
    op.drop_table('users', schema='DEV')
    op.drop_index('ix_context_name', table_name='contexts', schema='DEV')
    op.drop_index(op.f('ix_DEV_contexts_name'), table_name='contexts', schema='DEV')
    op.drop_index(op.f('ix_DEV_contexts_id'), table_name='contexts', schema='DEV')
    op.drop_table('contexts', schema='DEV')
    # ### end Alembic commands ###