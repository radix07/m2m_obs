from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
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
    def __repr__(self):
        return '<User %r>' % (self.nickname)    

class device(db.Model):
    id                      = db.Column(db.Integer, primary_key = True)
    location                = db.Column(db.SmallInteger, default = ROLE_USER)
    devConnectwareId        = db.Column(db.String(64), unique = true)
    devMac                  = db.Column(db.String(64), unique = false)
    dpGlobalIp              = db.Column(db.String(64), unique = false)
    dpConnectionStatus      = db.Column(db.String(64), unique = false)
    dpGlobalIp              = db.Column(db.String(64), unique = false)
    dpLastKnownIp           = db.Column(db.String(64), unique = false)
    dpMapLat                = db.Column(db.String(64), unique = false)
    dpMapLong               = db.Column(db.String(64), unique = false)
    dpLastDisconnectTime    = db.Column(db.String(64), unique = false)
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
    devID = db.Column(db.String(64), unique = false)
    streamID = db.Column(db.String(64), unique = false)
    timeStamp = db.Column(db.String(64), unique = false)
    datapoint = db.Column(db.String(64), unique = false)

class latestDataStreamPoints(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    devID = db.Column(db.String(64), unique = false)
    streamID = db.Column(db.String(64), unique = false)
    timeStamp = db.Column(db.String(64), unique = false)
    datapoint = db.Column(db.String(64), unique = false)
    units = db.Column(db.String(64), unique = false)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)