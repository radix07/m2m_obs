from app import db
import sqlalchemy
from sqlalchemy import func

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    username    = db.Column(db.String(64), unique = True)
    password    = db.Column(db.String(10))
    email       = db.Column(db.String(120), index = True, unique = True)
    role        = db.Column(db.SmallInteger, default = ROLE_USER)
    #posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
    #device = db.relationship('Device', backref = 'author', lazy = 'dynamic')
    #allowedDevices?
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return unicode(self.id)
    def get_username(self):
        return unicode(self.username)
    def __repr__(self):
        return '<User %r>' % (self.username)    

class device(db.Model):
    id                      = db.Column(db.Integer, primary_key = True)
    location                = db.Column(db.SmallInteger, default = ROLE_USER)
    devConnectwareId        = db.Column(db.String(64))  #unique??
    devMac                  = db.Column(db.String(64))
    dpConnectionStatus      = db.Column(db.String(64))
    dpGlobalIp              = db.Column(db.String(64))
    dpLastDisconnectTime    = db.Column(db.String(64))
    dpLastKnownIp           = db.Column(db.String(64))
    dpMapLat                = db.Column(db.String(64))
    dpMapLong               = db.Column(db.String(64))
    localIp                 = db.Column(db.String(64))
    localController         = db.Column(db.String(64))
    created_on              = db.Column(db.DateTime, default=db.func.now())
    updated_on              = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    

    #firmware
    #grpID
    #cstID
    #startDate
    #grpPath
    #contact
    #description

#class dataStream(db.Model):
    #id = db.Column(db.Integer, primary_key = True)
    #type - event,processed,raw

class dataPointRecords(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    devID = db.Column(db.String(64), unique = False)
    streamID = db.Column(db.String(64), unique = False)
    #timeStamp = db.Column(db.String(64), unique = False)
    timeStamp   = db.Column(db.BigInteger, unique = False)
    datapoint = db.Column(db.String(64), unique = False)
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

class latestDataStreamPoints(db.Model):
    
    id          = db.Column(db.Integer, primary_key = True)

    devID       = db.Column(db.String(64), unique = False)
    streamID    = db.Column(db.String(64), unique = False)
    #timeStamp   = db.Column(db.String(64), unique = False)
    timeStamp   = db.Column(db.BigInteger, unique = False)
    datapoint   = db.Column(db.String(64), unique = False)
    units       = db.Column(db.String(64), unique = False)
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())


class localControllerDataItems(db.Model):
    id           = db.Column(db.Integer, primary_key = True)
    controlId    = db.Column(db.Integer)
    baseID       = db.Column(db.String(64))
    CID          = db.Column(db.String(64))
    label        = db.Column(db.String(64))
    value        = db.Column(db.String(64))
    units        = db.Column(db.String(64))
    data_size    = db.Column(db.String(64))
    min          = db.Column(db.String(64))
    max          = db.Column(db.String(64))
    scaling      = db.Column(db.String(64))
    isfloat      = db.Column(db.String(64))
    issigned     = db.Column(db.String(64))
    update       = db.Column(db.String(64))
    menu         = db.Column(db.String(64))
    parent       = db.Column(db.String(64))
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

class pecosConfig(db.Model):
    '''Used to generate pecos configuration file to be sent to Etherios and processed by SICoM device
    '''
    id           = db.Column(db.Integer, primary_key = True)
    devID        = db.Column(db.String(64), unique = False)
    CID          = db.Column(db.BigInteger)
    label        = db.Column(db.String(64))
    value        = db.Column(db.Numeric)
    min          = db.Column(db.Numeric)
    max          = db.Column(db.Numeric)
    res          = db.Column(db.Numeric)

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
