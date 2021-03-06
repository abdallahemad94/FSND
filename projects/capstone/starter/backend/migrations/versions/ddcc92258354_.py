"""empty message

Revision ID: ddcc92258354
Revises: 
Create Date: 2020-09-13 02:30:49.540779

"""
from alembic import op
import sqlalchemy as sa
from datetime import date

# revision identifiers, used by Alembic.
revision = 'ddcc92258354'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    artists_table = op.create_table('Artists',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('gender', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    movies_table = op.create_table('Movies',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('release_date', sa.Date(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    roles_table = op.create_table('Roles',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('movie_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('character', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['Artists.id'], ),
    sa.ForeignKeyConstraint(['movie_id'], ['Movies.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Roles')
    op.drop_table('Movies')
    op.drop_table('Artists')
    # ### end Alembic commands ###
