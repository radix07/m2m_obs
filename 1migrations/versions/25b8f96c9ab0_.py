"""empty message

Revision ID: 25b8f96c9ab0
Revises: None
Create Date: 2014-06-10 16:27:59.776000

"""

# revision identifiers, used by Alembic.
revision = '25b8f96c9ab0'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table(u'migrate_version')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table(u'migrate_version',
    sa.Column(u'repository_id', sa.VARCHAR(length=250), autoincrement=False, nullable=False),
    sa.Column(u'repository_path', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column(u'version', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint(u'repository_id', name=u'migrate_version_pkey')
    )
    ### end Alembic commands ###
