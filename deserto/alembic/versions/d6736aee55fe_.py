"""empty message

Revision ID: d6736aee55fe
Revises: 
Create Date: 2020-10-05 22:39:13.850939

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6736aee55fe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('person',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('login', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('gender', sa.String(length=1), nullable=True),
    sa.Column('user_agent', sa.String(), nullable=True),
    sa.Column('cookies', sa.ARRAY(sa.JSON()), nullable=True),
    sa.Column('last_activity', sa.DateTime(), nullable=True),
    sa.Column('is_fake', sa.Boolean(), nullable=True),
    sa.Column('is_dribbble_user', sa.Boolean(), nullable=True),
    sa.Column('is_dribbble_email_confirm', sa.Boolean(), nullable=True),
    sa.Column('is_dribbble_set_pic', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=100), nullable=True),
    sa.Column('counter', sa.Integer(), nullable=True),
    sa.Column('is_liked_task', sa.Boolean(), nullable=True),
    sa.Column('is_comment_task', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('association',
    sa.Column('person_id', sa.Integer(), nullable=True),
    sa.Column('task_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['person_id'], ['person.id'], ),
    sa.ForeignKeyConstraint(['task_id'], ['task.id'], )
    )
    op.create_table('dribbble_queue',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('person_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['person_id'], ['person.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dribbble_queue')
    op.drop_table('association')
    op.drop_table('task')
    op.drop_table('person')
    # ### end Alembic commands ###
