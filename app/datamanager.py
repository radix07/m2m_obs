from app import db, models
from models import User, ROLE_USER, ROLE_ADMIN
from sqlalchemy import func
import sqlalchemy
import time

#######################GET################################

##Device
def removeAllDevices():
    print "Deleting All Devices"
    devices = models.device.query.all()
    for dev  in devices:
        db.session.delete(dev)
    db.session.commit()

def getDeviceList():
    return models.device.query.all()

def getDeviceByID(id):
    return models.device.query.filter_by(devConnectwareId=id).first()

def getStreamListByDeviceID(id):
    if id[:4] == "0000":    #truncate zeros to account for missing ones if they exist
        id = id[4:len(id)]
    #return models.latestDataStreamPoints.query.filter_by(devID=id).all()
    return models.latestDataStreamPoints.query.filter(models.latestDataStreamPoints.devID.ilike("%"+id.lower()+"%")).all()
    #return models.latestDataStreamPoints.query.filter(func.lower(models.latestDataStreamPoints.devID) == func.lower(id)).all()
    #user = models.User.                   query.filter(func.lower(User.username                      ) == func.lower("GaNyE")).first()
def addOrGetUser(username,password):
    user = User.query.filter_by(username=username).first()
    if user is None:        
        user = models.User(username = username, password = "")
        db.session.add(user)
    return user

##Stream
def getStreamListByDeviceIDAndStreamID(did,sid):
    return models.latestDataStreamPoints.query.filter_by(streamID=sid,devID=did).first()
def getStreamList():
    return models.latestDataStreamPoints.query.all()
def getStreamListByStreamID(id):
    return models.latestDataStreamPoints.query.filter_by(streamID=id).all()

##DataPoints
def getDataPoint(devID,streamID,timeStamp,datapoint):
    return models.dataPointRecords.query.filter_by(devID=devID,streamID=streamID,timeStamp=timeStamp,datapoint=datapoint).first()

def getMostRecentTSDataPoint(devID=0,streamID=0):
    if devID and streamID:
        try:
            lastrecord = db.session.query(models.dataPointRecords).filter(models.dataPointRecords.devID==devID.strip().upper(),models.dataPointRecords.streamID==streamID).order_by(models.dataPointRecords.timeStamp.desc()).first()
            print devID,streamID,":",lastrecord.timeStamp
            return lastrecord.timeStamp            
        except Exception, e:
            print "None exist return 0, e:",e
            return 0
    else:
        return db.session.query(func.max(models.dataPointRecords.timeStamp)).all()[0][0]

def getAnyDatapoint():
    return models.dataPointRecords.query.limit(1).all()

def getAllDatapoints(devID,streamID):
    if devID[:4] == "0000":    #truncate zeros to account for missing ones if they exist
        devID = devID[4:len(devID)]
    return models.dataPointRecords.query.filter(models.dataPointRecords.devID.ilike("%"+devID.lower()+"%"),
                                                models.dataPointRecords.streamID==streamID).all()
    #return models.dataPointRecords.query.filter_by(streamID=streamID,devID=devID).all()
def getAllEventOccurances(count=10):
    print "Get Event Occurances"
    return formatEpochTimeofList(models.dataPointRecords.query.filter( models.dataPointRecords.streamID=="EventList").order_by(models.dataPointRecords.timeStamp.desc()).limit(10))


####################ADD#############################
def addNewDevice(devConnectwareId,dpMapLat,dpMapLong,dpConnectionStatus,dpGlobalIp,dpLastDisconnectTime):
    #query if exists, then if doesnt
    recordItem = models.device(devConnectwareId=str(devConnectwareId),
                               dpMapLat=str(dpMapLat),dpMapLong=str(dpMapLong),
                               dpConnectionStatus=str(dpConnectionStatus),
                               dpGlobalIp=str(dpGlobalIp),
                               dpLastDisconnectTime=str(dpLastDisconnectTime))
    try:
        db.session.save(recordItem) #was add()
    except:
        db.session.add(recordItem)
    print "Pre Commit Changes"
    db.session.commit()
    print "Commit Change"
    return recordItem
def addNewStream(devID,streamID,timeStamp,datapoint,commit=0):
    recordItem = models.latestDataStreamPoints(devID=devID,streamID=streamID,timeStamp =timeStamp ,datapoint=datapoint)
    try:
        db.session.save(recordItem)
    except:
        db.session.add(recordItem)
    if commit:
        db.session.commit()
def addDataPoint(devID,streamID,timeStamp,datapoint,commit=0):
    devID,set = fixDevID(devID)
    recordItem = models.dataPointRecords(devID=devID, streamID=streamID, timeStamp = timeStamp, datapoint=datapoint)
    try:
        db.session.save(recordItem)
    except:
        db.session.add(recordItem)
    if commit:
        db.session.commit()

########################DATA MANAGE##################
def normalizeDataStreamRecords():
    query = db.session.query(models.latestDataStreamPoints)
    comFlag=0
    for row in query:
        row.devID,comFlag = fixDevID(row.devID)
    if comFlag:        
        print "Commit Changes"
        commitDB()

def normalizeDataPointRecords():
    query = db.session.query(models.dataPointRecords)
    #rows = query.statement.execute().fetchall()
    comFlag=0
    for row in query:        
        row.devID,comFlag = fixDevID(row.devID)
    if comFlag:        
        print "Commit Changes"
        commitDB()

def commitDB():
    db.session.commit()
##############Utility#################
def formatEpochTimeofList(list):
    print "Format Epoch"
    for st in list:
        print st.timeStamp
        try:
            if st.timeStamp.isdigit():
                st.timeStamp = time.strftime('%B %d, %Y %H:%M:%S', time.localtime((float(st.timeStamp)/1000)))
        except:
            st.timeStamp = time.strftime('%B %d, %Y %H:%M:%S', time.localtime((float(st.timeStamp)/1000)))
    return list

def fixDevID(devID):
    set=0
    devID = devID.upper()

    if "PYTHON" in devID:
        devID = "PYTHONPC1_RYAN"
        set=1
    elif devID.find("-") >8:        
        while devID.find("-") >7:
            print devID.find("-")
            devID= devID[1:len(devID)]
    elif devID[8] != "-": #fix missing 0 prefix in device
        print devID
        devID = "0"+devID
        set=1

    if devID[0] == "0" and devID[len(devID)-1].islower():     #fix lowercase device id
        print devID
        devID = devID.upper()
        set=1
    return devID,set

#def normalizeLatestDataStreamDeviceID():
    #make all items same case and length for similar
    #remove inherint potential duplicates


