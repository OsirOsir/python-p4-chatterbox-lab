"""your message

Revision ID: 9a87a263706c
Revises: 72a15dfc0258
Create Date: 2024-10-30 14:00:47.523312

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a87a263706c'
down_revision = '72a15dfc0258'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('messages', 'body',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('messages', 'username',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('messages', 'created_at',
               existing_type=sa.DATETIME(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('messages', 'created_at',
               existing_type=sa.DATETIME(),
               nullable=False)
    op.alter_column('messages', 'username',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('messages', 'body',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
