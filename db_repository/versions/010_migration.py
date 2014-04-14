from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
post = Table('post', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('body', String),
    Column('timestamp', DateTime),
    Column('user_id', Integer),
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
    Column('created_on', DateTime, default=ColumnDefault(<sqlalchemy.sql.functions.now at 0x31a0850; now>)),
    Column('updated_on', DateTime, onupdate=ColumnDefault(<sqlalchemy.sql.functions.now at 0x31a09d0; now>), default=ColumnDefault(<sqlalchemy.sql.functions.now at 0x31a0950; now>)),
)

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
    Column('created_on', DateTime, default=ColumnDefault(<sqlalchemy.sql.functions.now at 0x31b9370; now>)),
    Column('updated_on', DateTime, onupdate=ColumnDefault(<sqlalchemy.sql.functions.now at 0x31b9510; now>), default=ColumnDefault(<sqlalchemy.sql.functions.now at 0x31b9490; now>)),
)

data_point_records = Table('data_point_records', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('devID', String(length=64)),
    Column('streamID', String(length=64)),
    Column('timeStamp', Integer),
    Column('datapoint', String(length=64)),
    Column('created_on', DateTime, default=ColumnDefault(<sqlalchemy.sql.functions.now at 0x31ab7b0; now>)),
    Column('updated_on', DateTime, onupdate=ColumnDefault(<sqlalchemy.sql.functions.now at 0x31ab950; now>), default=ColumnDefault(<sqlalchemy.sql.functions.now at 0x31ab8d0; now>)),
)

latest_data_stream_points = Table('latest_data_stream_points', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('devID', String(length=64)),
    Column('streamID', String(length=64)),
    Column('timeStamp', Integer),
    Column('datapoint', String(length=64)),
    Column('units', String(length=64)),
    Column('created_on', DateTime, default=ColumnDefault(<sqlalchemy.sql.functions.now at 0x31b1610; now>)),
    Column('updated_on', DateTime, onupdate=ColumnDefault(<sqlalchemy.sql.functions.now at 0x31b17b0; now>), default=ColumnDefault(<sqlalchemy.sql.functions.now at 0x31b1730; now>)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['post'].drop()
    post_meta.tables['device'].columns['created_on'].create()
    post_meta.tables['device'].columns['updated_on'].create()
    post_meta.tables['local_controller_data_items'].columns['created_on'].create()
    post_meta.tables['local_controller_data_items'].columns['updated_on'].create()
    post_meta.tables['data_point_records'].columns['created_on'].create()
    post_meta.tables['data_point_records'].columns['updated_on'].create()
    post_meta.tables['latest_data_stream_points'].columns['created_on'].create()
    post_meta.tables['latest_data_stream_points'].columns['updated_on'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['post'].create()
    post_meta.tables['device'].columns['created_on'].drop()
    post_meta.tables['device'].columns['updated_on'].drop()
    post_meta.tables['local_controller_data_items'].columns['created_on'].drop()
    post_meta.tables['local_controller_data_items'].columns['updated_on'].drop()
    post_meta.tables['data_point_records'].columns['created_on'].drop()
    post_meta.tables['data_point_records'].columns['updated_on'].drop()
    post_meta.tables['latest_data_stream_points'].columns['created_on'].drop()
    post_meta.tables['latest_data_stream_points'].columns['updated_on'].drop()
