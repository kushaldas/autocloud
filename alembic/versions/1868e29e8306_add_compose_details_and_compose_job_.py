"""add compose details and compose job details table

Revision ID: 1868e29e8306
Revises: 55932e5d6b3f
Create Date: 2016-04-26 18:28:54.865917

"""

# revision identifiers, used by Alembic.
revision = '1868e29e8306'
down_revision = '55932e5d6b3f'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'compose_details',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('compose_id', sa.String(length=255), nullable=False,
                  unique=True),
        sa.Column('respin', sa.String(length=255), nullable=False),
        sa.Column('type', sa.String(length=255), nullable=False),
        sa.Column('passed', sa.Integer(), nullable=True, default=0),
        sa.Column('failed', sa.Integer(), nullable=True, default=0),
        sa.Column('status', sa.String(length=255), nullable=True),
        sa.Column('created_on', sa.DateTime(), nullable=False),
        sa.Column('last_updated', sa.DateTime(), nullable=False),
        sa.Column('location', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'compose_job_details',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('arch', sa.String(length=255), nullable=True),
        sa.Column('compose_id', sa.String(length=255), nullable=False),
        sa.Column('created_on', sa.DateTime(), nullable=False),
        sa.Column('family', sa.String(length=255), nullable=True),
        sa.Column('image_url', sa.String(length=255), nullable=False),
        sa.Column('last_updated', sa.DateTime(), nullable=True),
        sa.Column('output', sa.Text(), nullable=False),
        sa.Column('release', sa.String(length=255), nullable=True),
        sa.Column('status', sa.String(length=255), nullable=False),
        sa.Column('subvariant', sa.String(length=255), nullable=False),
        sa.Column('user', sa.String(length=255), nullable=False),
        sa.Column('image_format', sa.String(length=255), nullable=False),
        sa.Column('image_type', sa.String(length=255), nullable=False),
        sa.Column('image_name', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    pass


def downgrade():
    op.drop_table('compose_details')
    op.drop_table('compose_job_details')
    pass
