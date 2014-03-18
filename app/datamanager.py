from app import db, models
from sqlalchemy import func

#######################GET################################
def getDeviceList():
    return models.device.query.all()

def getStreamList():
    return models.latestDataStreamPoints.query.all()

def getStreamListByDeviceIDAndStreamID(did,sid):
    return models.latestDataStreamPoints.query.filter_by(streamID=sid,devID=did).first()

def getStreamListByDeviceID(id):
    if id[:4] == "0000":    #truncate zeros to account for missing ones if they exist
        id = id[4:len(id)]
    #return models.latestDataStreamPoints.query.filter_by(devID=id).all()

    return models.latestDataStreamPoints.query.filter(models.latestDataStreamPoints.devID.ilike("%"+id.lower()+"%")).all()
    #return models.latestDataStreamPoints.query.filter(func.lower(models.latestDataStreamPoints.devID) == func.lower(id)).all()
    #user = models.User.                   query.filter(func.lower(User.username                      ) == func.lower("GaNyE")).first()

def getStreamListByStreamID(id):
    return models.latestDataStreamPoints.query.filter_by(streamID=id).all()

def getDeviceByID(id):
    return models.device.query.filter_by(devConnectwareId=id).first()

def getAllDatapoints(devID,streamID):
    if devID[:4] == "0000":    #truncate zeros to account for missing ones if they exist
        devID = devID[4:len(devID)]
    return models.dataPointRecords.query.filter(models.dataPointRecords.devID.ilike("%"+devID.lower()+"%"),
                                                models.dataPointRecords.streamID==streamID).all()
    #return models.dataPointRecords.query.filter_by(streamID=streamID,devID=devID).all()

####################ADD#############################
def addNewDevice(devConnectwareId,dpMapLat,dpMapLong,dpConnectionStatus,dpGlobalIp,dpLastDisconnectTime):
    recordItem = models.device(devConnectwareId=devConnectwareId,dpMapLat=dpMapLat,dpMapLong=dpMapLong,dpConnectionStatus=dpConnectionStatus,dpGlobalIp=dpGlobalIp,dpLastDisconnectTime=dpLastDisconnectTime)
    db.session.add(recordItem)
    return recordItem
def addNewStream(devID,streamID,timeStamp,datapoint):
    recordItem = models.latestDataStreamPoints(devID=devID,streamID=streamID,timeStamp =timeStamp ,datapoint=datapoint)
    db.session.add(recordItem)
def addDataPoint(devID,streamID,timeStamp,datapoint):
    recordItem = models.dataPointRecords(devID=devID, streamID=streamID, timeStamp = timeStamp, datapoint=datapoint)
    db.session.add(recordItem)

########################DATA MANAGE##################
def commitDB():
    db.session.commit()

#def normalizeLatestDataStreamDeviceID():
    #make all items same case and length for similar
    #remove inherint potential duplicates
















































#Datbase information for Heroku postgres
#username: leqslquceprcjb
#password: bTO0DubrLXbT7fdVjIf-c-nDvI
#port: 5432
#database: d9rfmhttltdj9c
#host: ec2-54-197-227-238.compute-1.amazonaws.com
#postgres://leqslquceprcjb:bTO0DubrLXbT7fdVjIf-c-nDvI@ec2-54-197-227-238.compute-1.amazonaws.com:5432/d9rfmhttltdj9c

##Postgres
'''

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])
conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
'''

