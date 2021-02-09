"""empty message

Revision ID: dfa51f885702
Revises: 
Create Date: 2021-02-09 03:30:02.291202

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dfa51f885702'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('aluno',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=50), nullable=False),
    sa.Column('dre', sa.Integer(), nullable=True),
    sa.Column('cpf', sa.Integer(), nullable=True),
    sa.Column('dataNascimento', sa.String(length=8), nullable=False),
    sa.Column('sexo', sa.String(length=10), nullable=False),
    sa.Column('periodoIngresso', sa.Integer(), nullable=True),
    sa.Column('curso', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cpf'),
    sa.UniqueConstraint('dre')
    )
    op.create_table('materia',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=50), nullable=False),
    sa.Column('codigo', sa.String(length=15), nullable=False),
    sa.Column('creditos', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('association',
    sa.Column('materia_id', sa.Integer(), nullable=True),
    sa.Column('aluno_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['aluno_id'], ['aluno.id'], ),
    sa.ForeignKeyConstraint(['materia_id'], ['materia.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('association')
    op.drop_table('materia')
    op.drop_table('aluno')
    # ### end Alembic commands ###
