from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
data_stream = Table('data_stream', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
)

latest_data_stream_points = Table('latest_data_stream_points', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('devID', String(length=64)),
    Column('streamID', String(length=64)),
    Column('timeStamp', String(length=64)),
    Column('datapoint', String(length=64)),
)

device = Table('device', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('location', SmallInteger, default=ColumnDefault(0)),
    Column('devConnectwareId', String(length=64)),
    Column('devMac', String(length=64)),
    Column('dpConnectionStatus', String(length=64)),
    Column('dpGlobalIp', String(length=64)),
    Column('dpLastKnownIp', String(length=64)),
    Column('dpMapLat', String(length=64)),
    Column('dpMapLong', String(length=64)),
    Column('dpLastDisconnectTime', String(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['data_stream'].drop()
    post_meta.tables['latest_data_stream_points'].create()
    post_meta.tables['device'].columns['devConnectwareId'].create()
    post_meta.tables['device'].columns['devMac'].create()
    post_meta.tables['device'].columns['dpConnectionStatus'].create()
    post_meta.tables['device'].columns['dpGlobalIp'].create()
    post_meta.tables['device'].columns['dpLastDisconnectTime'].create()
    post_meta.tables['device'].columns['dpLastKnownIp'].create()
    post_meta.tables['device'].columns['dpMapLat'].create()
    post_meta.tables['device'].columns['dpMapLong'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['data_stream'].create()
    post_meta.tables['latest_data_stream_points'].drop()
    post_meta.tables['device'].columns['devConnectwareId'].drop()
    post_meta.tables['device'].columns['devMac'].drop()
    post_meta.tables['device'].columns['dpConnectionStatus'].drop()
    post_meta.tables['device'].columns['dpGlobalIp'].drop()
    post_meta.tables['device'].columns['dpLastDisconnectTime'].drop()
    post_meta.tables['device'].columns['dpLastKnownIp'].drop()
    post_meta.tables['device'].columns['dpMapLat'].drop()
    post_meta.tables['device'].columns['dpMapLong'].drop()
