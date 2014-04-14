from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
local_controller_data_items = Table('local_controller_data_items', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('controlId', Integer),
    Column('baseID', String(length=64)),
    Column('CID', String(length=64)),
    Column('label', String(length=64)),
    Column('value', String(length=64)),
    Column('units', String(length=64)),
    Column('data_size', String(length=64)),
    Column('min', String(length=64)),
    Column('max', String(length=64)),
    Column('scaling', String(length=64)),
    Column('isfloat', String(length=64)),
    Column('issigned', String(length=64)),
    Column('update', String(length=64)),
    Column('menu', String(length=64)),
    Column('parent', String(length=64)),
)

device = Table('device', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('location', SmallInteger, default=ColumnDefault(0)),
    Column('devConnectwareId', String(length=64)),
    Column('devMac', String(length=64)),
    Column('dpConnectionStatus', String(length=64)),
    Column('dpGlobalIp', String(length=64)),
    Column('dpLastDisconnectTime', String(length=64)),
    Column('dpLastKnownIp', String(length=64)),
    Column('dpMapLat', String(length=64)),
    Column('dpMapLong', String(length=64)),
    Column('localIp', String(length=64)),
    Column('localController', String(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['local_controller_data_items'].create()
    post_meta.tables['device'].columns['localController'].create()
    post_meta.tables['device'].columns['localIp'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['local_controller_data_items'].drop()
    post_meta.tables['device'].columns['localController'].drop()
    post_meta.tables['device'].columns['localIp'].drop()
