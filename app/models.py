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
    devConnectwareId        = db.Column(db.String(64), unique = True)
    devMac                  = db.Column(db.String(64), unique = False)
    dpGlobalIp              = db.Column(db.String(64), unique = False)
    dpConnectionStatus      = db.Column(db.String(64), unique = False)
    dpGlobalIp              = db.Column(db.String(64), unique = False)
    dpLastKnownIp           = db.Column(db.String(64), unique = False)
    dpMapLat                = db.Column(db.String(64), unique = False)
    dpMapLong               = db.Column(db.String(64), unique = False)
    dpLastDisconnectTime    = db.Column(db.String(64), unique = False)
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
    timeStamp = db.Column(db.String(64), unique = False)
    datapoint = db.Column(db.String(64), unique = False)

class latestDataStreamPoints(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    devID = db.Column(db.String(64), unique = False)
    streamID = db.Column(db.String(64), unique = False)
    timeStamp = db.Column(db.String(64), unique = False)
    datapoint = db.Column(db.String(64), unique = False)
    units = db.Column(db.String(64), unique = False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)