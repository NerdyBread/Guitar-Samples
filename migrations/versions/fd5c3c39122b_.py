"""empty message

Revision ID: fd5c3c39122b
Revises: 3b758dcdda78
Create Date: 2021-07-27 14:30:45.866139

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd5c3c39122b'
down_revision = '3b758dcdda78'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('user_desc', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'user_desc')
    # ### end Alembic commands ###
