"""recreating db

Revision ID: 055397ba9bfa
Revises: 
Create Date: 2025-03-31 15:26:42.962495

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '055397ba9bfa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('password_hash', sa.String(length=120), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('trusted_email', sa.String(length=120), nullable=False),
    sa.Column('phone', sa.String(length=15), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone'),
    sa.UniqueConstraint('username')
    )
    op.create_table('academic',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('sgpa', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['username'], ['user.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('mood',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('mood', sa.Integer(), nullable=False),
    sa.Column('diary_entry', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['username'], ['user.username'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username', 'date', name='unique_user_date')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('mood')
    op.drop_table('academic')
    op.drop_table('user')
    # ### end Alembic commands ###
