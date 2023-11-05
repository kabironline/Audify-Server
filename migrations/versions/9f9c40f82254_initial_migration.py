"""Initial migration.

Revision ID: 9f9c40f82254
Revises: 
Create Date: 2023-11-05 17:14:15.047083

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f9c40f82254'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('User',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('nickname', sa.String(length=50), nullable=False),
    sa.Column('bio', sa.String(length=200), nullable=True),
    sa.Column('password', sa.String(length=50), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('last_modified_by', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('last_modified_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['User.id'], ),
    sa.ForeignKeyConstraint(['last_modified_by'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('User', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_User_nickname'), ['nickname'], unique=True)
        batch_op.create_index(batch_op.f('ix_User_username'), ['username'], unique=True)

    op.create_table('Channel',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('last_modified_by', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('last_modified_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['User.id'], ),
    sa.ForeignKeyConstraint(['last_modified_by'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('Channel', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_Channel_name'), ['name'], unique=True)

    op.create_table('Member',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.Column('channel_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('last_modified_by', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('last_modified_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['channel_id'], ['Channel.id'], ),
    sa.ForeignKeyConstraint(['created_by'], ['User.id'], ),
    sa.ForeignKeyConstraint(['last_modified_by'], ['User.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Member')
    with op.batch_alter_table('Channel', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_Channel_name'))

    op.drop_table('Channel')
    with op.batch_alter_table('User', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_User_username'))
        batch_op.drop_index(batch_op.f('ix_User_nickname'))

    op.drop_table('User')
    # ### end Alembic commands ###
