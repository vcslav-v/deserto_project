"""empty message

Revision ID: 18df191fbe08
Revises: 4575b0c0fb58
Create Date: 2020-10-07 08:45:07.155885

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18df191fbe08'
down_revision = '4575b0c0fb58'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tasks_queue',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['task_id'], ['task.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tasks_queue')
    # ### end Alembic commands ###
