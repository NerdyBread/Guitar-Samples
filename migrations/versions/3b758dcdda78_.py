"""empty message

Revision ID: 3b758dcdda78
Revises: 256a30ba3d0e
Create Date: 2021-07-27 12:14:25.679948

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b758dcdda78'
down_revision = '256a30ba3d0e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('image_file', sa.String(length=20), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'image_file')
    # ### end Alembic commands ###