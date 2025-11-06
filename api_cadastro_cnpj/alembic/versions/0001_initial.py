"""
Initial migration: create usuarios, empresas, estabelecimentos, socios, tags and empresa_tags
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'usuarios',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String, nullable=False, unique=True),
        sa.Column('hashed_password', sa.String, nullable=False),
        sa.Column('is_admin', sa.Boolean, nullable=False, server_default=sa.text('0')),
    )

    op.create_table(
        'empresas',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('nome', sa.String, nullable=False),
        sa.Column('cnpj', sa.String, nullable=True),
    )

    op.create_table(
        'estabelecimentos',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('nome', sa.String, nullable=False),
        sa.Column('empresa_id', sa.Integer, sa.ForeignKey('empresas.id')),
    )

    op.create_table(
        'socios',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('nome', sa.String, nullable=False),
        sa.Column('estabelecimento_id', sa.Integer, sa.ForeignKey('estabelecimentos.id')),
    )

    op.create_table(
        'tags',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False, unique=True),
    )

    op.create_table(
        'empresa_tags',
        sa.Column('empresa_id', sa.Integer, sa.ForeignKey('empresas.id'), primary_key=True),
        sa.Column('tag_id', sa.Integer, sa.ForeignKey('tags.id'), primary_key=True),
    )


def downgrade():
    op.drop_table('empresa_tags')
    op.drop_table('tags')
    op.drop_table('socios')
    op.drop_table('estabelecimentos')
    op.drop_table('empresas')
    op.drop_table('usuarios')
