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
        list.append([q.dev_connectware_id,q.dp_map_lat,q.dp_map_long,"",q.dp_connection_status,q.dp_global_ip,q.dp_last_disconnect_time])
    return list


def getDeviceList():
    return models.device.query.all()

def getDeviceByID(id):
    return models.device.query.filter_by(dev_connectware_id=id).first()

def getStreamListByDeviceID(dev_id):
    print dev_id
    dev_id,set = fixDevID(dev_id)
    return models.latestDataStreamPoints.query.filter(models.latestDataStreamPoints.dev_id.ilike("%"+dev_id.lower()+"%")).all()

def addOrGetUser(username,password):
    user = User.query.filter_by(username=username).first()
    if user is None:        
        user = models.User(username = username, password = "")
        db.session.add(user)
    return user

##Stream
def getStreamListByDeviceIDAndstream_id(did,sid):
    did,set = fixDevID(did)
    return models.latestDataStreamPoints.query.filter_by(stream_id=sid,dev_id=did).first()
def getStreamListByDeviceID(did):
    return models.latestDataStreamPoints.query.filter_by(dev_id=did)
def getStreamList():
    return models.latestDataStreamPoints.query.all()
def getStreamListBystream_id(id):
    return models.latestDataStreamPoints.query.filter_by(stream_id=id).all()

##DataPoints
def getDataPoint(dev_id,stream_id,timestamp,datapoint):
    dev_id,set = fixDevID(dev_id)
    return models.dataPointRecords.query.filter_by(dev_id=dev_id,stream_id=stream_id,timestamp=timestamp,datapoint=datapoint).first()

def getMostRecentTSDataPoint(dev_id=0,stream_id=0):        
    if dev_id and stream_id:
        dev_id,set = fixDevID(dev_id)
        try:
            lastrecord = db.session.query(models.dataPointRecords).filter(models.dataPointRecords.dev_id==dev_id.strip(),models.dataPointRecords.stream_id==stream_id).order_by(models.dataPointRecords.timestamp.desc()).first()
            print dev_id,stream_id,":",lastrecord.timestamp,str(time.strftime('%B %d, %Y %H:%M:%S', time.localtime((float(lastrecord.timestamp)/1000))))
            return lastrecord.timestamp            
        except Exception, e:
            print "Exception, None exist returning 0 TS, e:",e
            return 0
    else:
        return db.session.query(func.max(models.dataPointRecords.timestamp)).all()[0][0]

def getAnyDatapoint():
    return models.dataPointRecords.query.limit(1).all()

def getAllDatapoints():
    return models.dataPointRecords.query.order_by(models.dataPointRecords.timestamp.desc()).all()

def getAllDatapointsFiltered(dev_id,sinceTS,stream=None):
    if stream is None:
        return models.dataPointRecords.query.filter(models.dataPointRecords.dev_id==dev_id,models.dataPointRecords.timestamp >= sinceTS).order_by(models.dataPointRecords.timestamp.asc()).all()
    else:
        return models.dataPointRecords.query.filter(models.dataPointRecords.dev_id==dev_id,models.dataPointRecords.timestamp >= sinceTS,models.dataPointRecords.stream_id==stream).order_by(models.dataPointRecords.timestamp.asc()).all()

def getDecimatedDatapointsByID(dev_id,stream_id,interval):
    data = db.engine.execute("SELECT ROW_NUMBER() FROM data_point_records WHERE stream_id LIKE 'PowerInputVoltage'")
    #data = db.engine.execute("SELECT id,timestamp,datapoint,stream_id, ROW_NUMBER() OVER (ORDER BY id) AS rownum FROM data_point_records WHERE stream_id LIKE 'PowerInputVoltage'")
    #data = db.engine.execute("SELECT id,timestamp,datapoint,stream_id FROM (SELECT id,timestamp,datapoint,stream_id, ROW_NUMBER() OVER (ORDER BY id) AS rownum FROM data_point_records WHERE stream_id LIKE 'PowerInputVoltage') AS t WHERE t.rownum % 30 = 0 ORDER BY t.id")
    
        
    for i in data:
        print i

def getAllDatapointsByIDRaw(dev_id,stream_id):
    return db.engine.execute("SELECT \"timestamp\",datapoint FROM data_point_records WHERE \"stream_id\" LIKE '"+stream_id+"' AND \"dev_id\" LIKE '"+dev_id+"'")
    #q = "SELECT timestamp,datapoint FROM data_point_records WHERE stream_id LIKE '{}' AND dev_id LIKE '{}'".format(dev_id,stream_id)
    #print q
    #data = db.engine.execute(q)
    #data = db.engine.execute("SELECT timestamp,datapoint FROM data_point_records WHERE stream_id LIKE 'PowerInputVoltage' AND dev_id LIKE '00000000-00000000-00042DFF-FF0418FB'")
        
def getAllDatapointsByID(dev_id,stream_id):
    dev_id,set = fixDevID(dev_id)
    return models.dataPointRecords.query.filter(models.dataPointRecords.dev_id.ilike("%"+dev_id.lower()+"%"),
                                                models.dataPointRecords.stream_id==stream_id).all()
    #return models.dataPointRecords.query.filter_by(stream_id=stream_id,dev_id=dev_id).all()
def getAllEventOccurances(count=10, dev_id=None):
    #print "Get Event Occurances"
    if dev_id is None:
        return formatEpochTimeofList(models.dataPointRecords.query.filter( models.dataPointRecords.stream_id=="EventList").order_by(models.dataPointRecords.timestamp.desc()).limit(10))
    else:
        return formatEpochTimeofList(models.dataPointRecords.query.filter( models.dataPointRecords.stream_id=="EventList",models.dataPointRecords.dev_id==dev_id).order_by(models.dataPointRecords.timestamp.desc()).limit(10))


####################ADD#############################
def addNewDevice(dev_connectware_id,dp_map_lat,dp_map_long,dp_connection_status,dp_global_ip,dp_last_disconnect_time):
    #query if exists, then if doesnt
    recordItem = models.device(dev_connectware_id=str(dev_connectware_id),
                               dp_map_lat=str(dp_map_lat),dp_map_long=str(dp_map_long),
                               dp_connection_status=str(dp_connection_status),
                               dp_global_ip=str(dp_global_ip),
                               dp_last_disconnect_time=str(dp_last_disconnect_time))
    try:
        db.session.save(recordItem) #was add()
    except:
        db.session.add(recordItem)
    print "Pre Commit Changes"
    db.session.commit()
    print "Commit Change"
    return recordItem

def addNewStream(dev_id,stream_id,timestamp,datapoint,commit=0):    
    dev_id,set = fixDevID(dev_id)
    recordItem = models.latestDataStreamPoints(dev_id=dev_id,stream_id=stream_id,timestamp =timestamp ,datapoint=datapoint)

    try:
        db.session.save(recordItem)
    except:
        db.session.add(recordItem)
    if commit:
        db.session.commit()
def fastaddDataPoints(dev_id,stream_id,pointList,commit=0):
    temp = [{"dev_id":dev_id,"stream_id":stream_id,"timestamp":i[0],"datapoint":i[1]} for i in pointList]        
    db.engine.execute(
        models.dataPointRecords.__table__.insert(),
        temp
        #[{"dev_id":dev_id,"stream_id":stream_id,"timestamp":i[0],"datapoint":i[1]} for i in pointList]        
        )
    return 1
    #print "SqlAlchemy Core: Total time for " + str(n) + " records " + str(time.time() - t0) + " secs"

    pass
def addDataPoint(dev_id,stream_id,timestamp,datapoint,commit=0):
    #Bottle neck here...
    dev_id,set = fixDevID(dev_id)
    recordItem = models.dataPointRecords(dev_id=dev_id, stream_id=stream_id, timestamp = timestamp, datapoint=datapoint)
    try:
        db.session.save(recordItem)
    except:
        db.session.add(recordItem)
    if commit:
        db.session.commit()

########################DATA MANAGE##################
def cleanOldDataForDBThreshold(limit):
    #NEED TO ENSURE SOMEHOW THAT LAST DATA POINT IN STREAM IS NOT REMOVED!!!!!!!!!!!!!!

    #recordCount = db.session.execute('select count(*) from data_point_records')
    recordCount = db.session.query(models.dataPointRecords).count()
    #print "Datapoint Record Count:",recordCount

    #group by stream, delete record count per group down to limit/(stream count)
    if recordCount > limit:
        result = db.session.execute('DELETE FROM data_point_records WHERE id IN (select id from data_point_records ORDER BY id ASC LIMIT '+str(long(recordCount) - limit)+")")
    #while recordCount > limit:
        #result = db.session.execute("DELETE FROM data_point_records WHERE id IN(SELECT MIN(id) FROM data_point_records GROUP BY 'stream_id')")
        #recordCount = db.session.query(models.dataPointRecords).count()
    

    print "Rec Count:",recordCount, "\tRemoved:",str(recordCount - limit),"\tLimit:",limit
    db.session.commit()

def normalizeDataStreamRecords():
    query = db.session.query(models.latestDataStreamPoints)
    comFlag=0
    for row in query:
        row.dev_id,comFlag = fixDevID(row.dev_id)
    if comFlag:        
        print "Commit Changes"
        commitDB()

def normalizeDataPointRecords():
    query = db.session.query(models.dataPointRecords)
    #rows = query.statement.execute().fetchall()
    comFlag=0
    for row in query:        
        row.dev_id,comFlag = fixDevID(row.dev_id)
    if comFlag:        
        print "Commit Changes"
        commitDB()

def commitDB():
    db.session.commit()
##############Utility#################
def formatEpochTimeofList(list):
    for st in list:
        try:
            if st.timestamp.isdigit():
                st.timestamp = time.strftime('%B %d, %Y %H:%M:%S', time.localtime((float(st.timestamp)/1000)))
        except:
            st.timestamp = time.strftime('%B %d, %Y %H:%M:%S', time.localtime((float(st.timestamp)/1000)))
    return list

def fixDevID(dev_id):
    set=0    
    if "python" in dev_id:       #special test case
        return dev_id,set    
    dev_id = dev_id.upper()

    if dev_id.find("-") >8:        
        while dev_id.find("-") >7:
            #print dev_id.find("-")
            dev_id= dev_id[1:len(dev_id)]
    elif dev_id[8] != "-": #fix missing 0 prefix in device
        #print dev_id
        dev_id = "0"+dev_id
        set=1

    if dev_id[0] == "0" and dev_id[len(dev_id)-1].islower():     #fix lowercase device id
        #print dev_id
        dev_id = dev_id.upper()
        set=1
    return dev_id,set

#def normalizeLatestDataStreamDeviceID():
    #make all items same case and length for similar
    #remove inherint potential duplicates



if __name__ == '__main__':
    datapoints = getAllDatapointsByID(str(dev_id),stList[int(streamIndex)].stream_id)