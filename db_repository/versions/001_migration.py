from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
data_stream = Table('data_stream', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
)

device = Table('device', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('location', SmallInteger, default=ColumnDefault(0)),
)

post = Table('post', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('body', String(length=140)),
    Column('timestamp', DateTime),
    Column('user_id', Integer),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('nickname', String(length=64)),
    Column('email', String(length=120)),
    Column('role', SmallInteger, default=ColumnDefault(0)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['data_stream'].create()
    post_meta.tables['device'].create()
    post_meta.tables['post'].create()
    post_meta.tables['user'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['data_stream'].drop()
    post_meta.tables['device'].drop()
    post_meta.tables['post'].drop()
    post_meta.tables['user'].drop()
