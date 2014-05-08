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

def getDeviceListFormatted():
    #valueList.append([connectID,lat,longit,group,connected,globID,disconnectTime ])
    query = models.device.query.all()
    list =[]
    for q in query:
        list.append([q.devConnectwareId,q.dpMapLat,q.dpMapLong,"",q.dpConnectionStatus,q.dpGlobalIp,q.dpLastDisconnectTime])
    return list


def getDeviceList():
    return models.device.query.all()

def getDeviceByID(id):
    return models.device.query.filter_by(devConnectwareId=id).first()

def getStreamListByDeviceID(devID):
    devID,set = fixDevID(devID)
    #return models.latestDataStreamPoints.query.filter_by(devID=id).all()
    return models.latestDataStreamPoints.query.filter(models.latestDataStreamPoints.devID.ilike("%"+devID.lower()+"%")).all()
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
    did,set = fixDevID(did)
    return models.latestDataStreamPoints.query.filter_by(streamID=sid,devID=did).first()
def getStreamList():
    return models.latestDataStreamPoints.query.all()
def getStreamListByStreamID(id):
    return models.latestDataStreamPoints.query.filter_by(streamID=id).all()

##DataPoints
def getDataPoint(devID,streamID,timeStamp,datapoint):
    devID,set = fixDevID(devID)
    return models.dataPointRecords.query.filter_by(devID=devID,streamID=streamID,timeStamp=timeStamp,datapoint=datapoint).first()

def getMostRecentTSDataPoint(devID=0,streamID=0):        
    if devID and streamID:
        devID,set = fixDevID(devID)
        try:
            lastrecord = db.session.query(models.dataPointRecords).filter(models.dataPointRecords.devID==devID.strip(),models.dataPointRecords.streamID==streamID).order_by(models.dataPointRecords.timeStamp.desc()).first()
            print devID,streamID,":",lastrecord.timeStamp,str(time.strftime('%B %d, %Y %H:%M:%S', time.localtime((float(lastrecord.timeStamp)/1000))))
            return lastrecord.timeStamp            
        except Exception, e:
            #print "None exist returning 0 TS, e:",e
            return 0
    else:
        return db.session.query(func.max(models.dataPointRecords.timeStamp)).all()[0][0]

def getAnyDatapoint():
    return models.dataPointRecords.query.limit(1).all()

def getAllDatapoints():
    return models.dataPointRecords.query.order_by(models.dataPointRecords.timeStamp.desc()).all()

def getAllDatapointsByID(devID,streamID):
    devID,set = fixDevID(devID)
    return models.dataPointRecords.query.filter(models.dataPointRecords.devID.ilike("%"+devID.lower()+"%"),
                                                models.dataPointRecords.streamID==streamID).all()
    #return models.dataPointRecords.query.filter_by(streamID=streamID,devID=devID).all()
def getAllEventOccurances(count=10, devID=None):
    #print "Get Event Occurances"
    if devID is None:
        return formatEpochTimeofList(models.dataPointRecords.query.filter( models.dataPointRecords.streamID=="EventList").order_by(models.dataPointRecords.timeStamp.desc()).limit(10))
    else:
        return formatEpochTimeofList(models.dataPointRecords.query.filter( models.dataPointRecords.streamID=="EventList",models.dataPointRecords.devID==devID).order_by(models.dataPointRecords.timeStamp.desc()).limit(10))


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
    devID,set = fixDevID(devID)
    recordItem = models.latestDataStreamPoints(devID=devID,streamID=streamID,timeStamp =timeStamp ,datapoint=datapoint)

    try:
        db.session.save(recordItem)
    except:
        db.session.add(recordItem)
    if commit:
        db.session.commit()
def fastaddDataPoints(devID,streamID,pointList,commit=0):
    temp = [{"devID":devID,"streamID":streamID,"timeStamp":i[0],"datapoint":i[1]} for i in pointList]        
    db.engine.execute(
        models.dataPointRecords.__table__.insert(),
        temp
        #[{"devID":devID,"streamID":streamID,"timeStamp":i[0],"datapoint":i[1]} for i in pointList]        
        )
    return 1
    #print "SqlAlchemy Core: Total time for " + str(n) + " records " + str(time.time() - t0) + " secs"

    pass
def addDataPoint(devID,streamID,timeStamp,datapoint,commit=0):
    #Bottle neck here...
    devID,set = fixDevID(devID)
    recordItem = models.dataPointRecords(devID=devID, streamID=streamID, timeStamp = timeStamp, datapoint=datapoint)
    try:
        db.session.save(recordItem)
    except:
        db.session.add(recordItem)
    if commit:
        db.session.commit()

########################DATA MANAGE##################
def cleanOldDataForDBThreshold(limit):
    recordCount = db.session.execute('select count(*) from data_point_records')
    print recordCount
    for i in recordCount:
        recordCount = i[0]
    if recordCount > limit:
        result = db.session.execute('DELETE FROM data_point_records WHERE id IN (select id from data_point_records ORDER BY id ASC LIMIT '+str(long(recordCount) - limit)+")")

    print "Rec Count:",recordCount, "\tRemoved:",str(recordCount - limit),"\tLimit:",limit
    db.session.commit()

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
    for st in list:
        try:
            if st.timeStamp.isdigit():
                st.timeStamp = time.strftime('%B %d, %Y %H:%M:%S', time.localtime((float(st.timeStamp)/1000)))
        except:
            st.timeStamp = time.strftime('%B %d, %Y %H:%M:%S', time.localtime((float(st.timeStamp)/1000)))
    return list

def fixDevID(devID):
    set=0    
    if "python" in devID:       #special test case
        return devID,set    
    devID = devID.upper()

    if devID.find("-") >8:        
        while devID.find("-") >7:
            #print devID.find("-")
            devID= devID[1:len(devID)]
    elif devID[8] != "-": #fix missing 0 prefix in device
        #print devID
        devID = "0"+devID
        set=1

    if devID[0] == "0" and devID[len(devID)-1].islower():     #fix lowercase device id
        #print devID
        devID = devID.upper()
        set=1
    return devID,set

#def normalizeLatestDataStreamDeviceID():
    #make all items same case and length for similar
    #remove inherint potential duplicates


