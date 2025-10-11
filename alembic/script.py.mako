##
# Migration script template for Alembic (Mako)
##
"""
Revision ID: ${up_revision}
Revises: ${down_revision | none}
Create Date: ${create_date}
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '${up_revision}'
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade():
${upgrades | indent(4) if upgrades else '    pass'}


def downgrade():
${downgrades | indent(4) if downgrades else '    pass'}
