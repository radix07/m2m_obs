from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
latest_data_stream_points = Table('latest_data_stream_points', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('devID', String(length=64)),
    Column('streamID', String(length=64)),
    Column('timeStamp', String(length=64)),
    Column('datapoint', String(length=64)),
    Column('units', String(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['latest_data_stream_points'].columns['units'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['latest_data_stream_points'].columns['units'].drop()
