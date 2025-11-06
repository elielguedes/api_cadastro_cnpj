"""add unique constraint on empresas.cnpj

Revision ID: 0002_add_unique_cnpj
Revises: 0001_initial
Create Date: 2025-10-11 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0002_add_unique_cnpj'
down_revision = '0001_initial'
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    dialect = bind.dialect.name
    if dialect == 'sqlite':
        # sqlite: create unique index (no ALTER TABLE ADD CONSTRAINT)
        op.create_index('ux_empresas_cnpj', 'empresas', ['cnpj'], unique=True)
    else:
        # for postgres and others, create unique constraint
        op.create_unique_constraint('uq_empresas_cnpj', 'empresas', ['cnpj'])


def downgrade() -> None:
    bind = op.get_bind()
    dialect = bind.dialect.name
    if dialect == 'sqlite':
        op.drop_index('ux_empresas_cnpj', table_name='empresas')
    else:
        op.drop_constraint('uq_empresas_cnpj', 'empresas', type_='unique')
