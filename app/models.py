from app import db
import sqlalchemy
from sqlalchemy import func

ROLE_USER = 0
ROLE_ADMIN = 1

#Users are mostly handled by Etherios login currently
class User(db.Model):
    '''
        Etherios Users
    '''
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
    '''
        Etherios based devices
    '''
    id                      = db.Column(db.Integer, primary_key = True)
    location                = db.Column(db.SmallInteger, default = ROLE_USER)
    dev_connectware_id      = db.Column(db.String(64))  #unique??
    dev_mac                 = db.Column(db.String(64))
    dp_connection_status    = db.Column(db.String(64))
    dp_global_ip            = db.Column(db.String(64))
    dp_last_disconnect_time = db.Column(db.String(64))
    dp_last_known_ip        = db.Column(db.String(64))
    dp_map_lat              = db.Column(db.String(64))
    dp_map_long             = db.Column(db.String(64))
    local_ip                = db.Column(db.String(64))
    local_controller        = db.Column(db.String(64))
    created_on              = db.Column(db.DateTime, default=db.func.now())
    updated_on              = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    app_id                  = db.Column(db.String(64)) 
    #firmware
    #grpID
    #cstID
    #startDate
    #grpPath
    #contact
    #description

class latestDataStreamPoints(db.Model):
    '''
        Latest data stream values and information  
    ''' 
    id          = db.Column(db.Integer, primary_key = True)

    dev_id       = db.Column(db.String(64), unique = False)      #foreign key constraint to device
    stream_id    = db.Column(db.String(64), unique = False)
    timestamp   = db.Column(db.BigInteger, unique = False)
    datapoint   = db.Column(db.String(64), unique = False)
    units       = db.Column(db.String(64), unique = False)
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    #test= db.Column(db.String(64), unique = False)

class gocomSettingsTable(db.Model):
    '''
        GOCoM settings parsed from (or used to generate) settings.py 
    '''
    id           = db.Column(db.Integer, primary_key = True)
    dev_id        = db.Column(db.String(64), unique = False)
    label        = db.Column(db.String(64), unique = True)
    value        = db.Column(db.Numeric)
    min          = db.Column(db.Numeric)
    max          = db.Column(db.Numeric)
    res          = db.Column(db.Numeric)
    group        = db.Column(db.String(64))

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

#PECoS data specific
class applicationTable(db.Model):
    '''
        Application detail table in regards to PECoS firmware/hardware/software/application
        Critical for tracking when multiple variants/controllers/models are released
    '''
    id           = db.Column(db.Integer, primary_key = True)
    app_id        = db.Column(db.String(64), unique = False)
    app_ver       = db.Column(db.BigInteger)
    label        = db.Column(db.String(64),unique = True)
    controller   = db.Column(db.String(64),unique = True)
    hardwarer_rev= db.Column(db.String(64))
    software_rev = db.Column(db.String(64))
    firmware_file= db.Column(db.String(64))
    group        = db.Column(db.String(64))
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

class dataListingsTable(db.Model):
    '''
        Will hold database data from GOCoM for higher level data access to the controller
        May not be used for base useage to start
    '''
    id           = db.Column(db.Integer, primary_key = True)
    app_id        = db.Column(db.String(64), unique = False)
    app_ver       = db.Column(db.BigInteger)
    label        = db.Column(db.String(64),unique = True)
    value        = db.Column(db.Numeric)
    min          = db.Column(db.Numeric)
    max          = db.Column(db.Numeric)
    res          = db.Column(db.Numeric)
    level        = db.Column(db.Numeric)
    group        = db.Column(db.String(64))
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())


class calibrationTable(db.Model):
    '''
        Used to generate/parse pecos configuration file to be sent to/from Etherios and processed by GOCoM device
    '''
    id           = db.Column(db.Integer, primary_key = True)
    dev_id        = db.Column(db.String(64), unique = False)
    cid          = db.Column(db.BigInteger)
    label        = db.Column(db.String(64), unique = True)
    value        = db.Column(db.Numeric)
    min          = db.Column(db.Numeric)
    max          = db.Column(db.Numeric)
    res          = db.Column(db.Numeric)

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

#Data Point Tables
class dataPointRecords(db.Model):
    '''
        Individual data points stream from various GOCoM devices
    '''
    #typically has resolution down to ~1-20 minutes, contains all raw datapoint stream data
    id = db.Column(db.Integer, primary_key = True)
    dev_id = db.Column(db.String(64), unique = False)
    stream_id = db.Column(db.String(64), unique = False) #foreign key constraint to streamTable
    timestamp   = db.Column(db.BigInteger, unique = False)
    datapoint = db.Column(db.String(64), unique = False)    #would like this to be numeric, but strings are possible...
    #Need unique constraint amongst streamID, timestamp, and datapoint to prevent duplicate inserts
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
#    db.UniqueConstraint(

#could do a daily/weekly/monthly update of base datapoint model to the longer interval tables, data will start to stretch
#need data broken out to allow for quicker queries with appropriate resolution for display purposes (small/spefic windows) at 1million->500,000->250,000 (large/wide windows)
#http://www.highcharts.com/component/content/article/2-articles/news/48-loading-millions-of-points-in-highcharts

class dataPointRecordsWeek(db.Model):
    #Updates daily, contains new day of data from base data points
    #break down from minute resolution to (0.5-2) hour resolution (168 hours/week)
    id = db.Column(db.Integer, primary_key = True)
    dev_id = db.Column(db.String(64), unique = False)
    stream_id = db.Column(db.String(64), unique = False) #foreign key constraint to streamTable
    timestamp   = db.Column(db.BigInteger, unique = False)
    datapoint = db.Column(db.String(64), unique = False)
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
class dataPointRecordsMonth(db.Model):
    #Update weekly? contains new week based data to be view over an entire month
    #break down from hour range to 1/4-1 day range (5208 hours/month) (@ .25 days ~ 120pts)
    id = db.Column(db.Integer, primary_key = True)
    dev_id = db.Column(db.String(64), unique = False)
    stream_id = db.Column(db.String(64), unique = False) #foreign key constraint to streamTable
    timestamp   = db.Column(db.BigInteger, unique = False)
    datapoint = db.Column(db.String(64), unique = False)
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
class dataPointRecordsYear(db.Model):
    #break months down to years 
    # may not be needed, wont be needed for at least 1-2 years... (@120/month, 1440/year reasonable?)
    id = db.Column(db.Integer, primary_key = True)
    dev_id = db.Column(db.String(64), unique = False)
    stream_id = db.Column(db.String(64), unique = False) #foreign key constraint to streamTable
    timestamp   = db.Column(db.BigInteger, unique = False)
    datapoint = db.Column(db.String(64), unique = False)
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

###Local data table (TBD)
class localControllerDataItems(db.Model):
    id           = db.Column(db.Integer, primary_key = True)
    control_id    = db.Column(db.Integer)
    base_id       = db.Column(db.String(64))
    cid          = db.Column(db.String(64))
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

