import httplib
import base64
import xmlParse
import datamanager
import time
#Group->Users (TBD???)
    #User->Device (allowances...???)
#Group->Devices
    #Devices -> Streams
    #Devices -> Files


class etheriosData:
    #username = "pgSatterlee" # enter your username
    #password = "Pgecs-2322" # enter your password
    username = "TestMe"
    password = "Password_123"
    auth = base64.encodestring("%s:%s"%(username,password))[:-1]

    def __init__(self):
        self.oneCall=0
        self.deviceListInfo = []
        self.streamListInfo = []
        self.streamDataList = {}
        self.firstCall = 1
    def initFromDB(self):
        if self.firstCall:
            self.firstCall = 0
            result = datamanager.getMostRecentTSDataPoint()
            print "Latest DB DataPoint: ",str(time.strftime('%B %d, %Y %H:%M:%S', time.localtime((float(result)/1000))))
            result = datamanager.getDeviceList()  #models.device.query.all()
            if len(result) ==0:
                print "No Devices in database"
                self.updateDeviceList()
                #other datatables should be empty if there are no devices
                    #Should they be deleted/emptied?
            else:
                for record in result:       #([connectID,lat,longit,group,connected,globID,disconnectTime ])
                    self.deviceListInfo.append([record.devConnectwareId,record.dpMapLat,record.dpMapLong,"",record.dpConnectionStatus,record.dpGlobalIp,record.dpLastDisconnectTime])
                #check for new devices if stale
                #self.printFormattedNestedArray(self.deviceListInfo)

            result = datamanager.getStreamList()
            if len(result) ==0:
                print "No Streams in database"
                self.updateLatestStreamValues()     #query for all streams
            else:
                for record in result:       #(devID,StreamID,TS,datapoint)
                    self.streamListInfo.append([record.devID,record.streamID,record.timeStamp,record.datapoint])
                #check for new streams
                #self.printFormattedNestedArray(self.streamListInfo)
        
            #check for any datapoints
            result = datamanager.getAnyDatapoint()
            if len(result) == 0:
                print "No datapoints exist"
                self.updateStreamListDataPoints()
                #get all data if db empty
            else:   #Just testing for existance of data points
                #datamanager.normalizeDataPointRecords()
                #should extend to recent datapoints, and get latest if stale (older than.. 1 day/hour??)
                #print "Len:",len(result),result[0].id, result[0].devID,result[0].datapoint,result[0].timeStamp
                pass
    def printFormattedNestedArray(self,ar,head=""):
        print 
        print "-"*100
        for rec in ar:
            outputString=""
            for item in rec:
                outputString += "{0:>37},".format(item)
            print outputString 
        print "-"*100
    
    def getNewDevices(self):
        pass
    def getNewStreams(self):
        pass
    def getNewDataPoints(self):
        pass

    def parseAllAccountData(self):
        #updateDeviceList()
        #for dev in devList:
            #get all streams
        #getSystemAlarms from above (event/alarm datastreams)
        pass

    def setUserNamePassword(self,usern,passw):
        username = usern
        password = passw

    def setDeviceLocation(self,deviceID,lat,longit):
        message = """<DeviceCore>
              <devConnectwareId>{0}</devConnectwareId> 
                <dpMapLat>{1}</dpMapLat>
                <dpMapLong>{2}</dpMapLong>
            </DeviceCore>
            """.format(self.deviceID,lat,longit)
        self.genericWebServiceCall("/DeviceCore","PUT",message)

    def updateDeviceList(self):
        response_body = self.genericWebServiceCall("/DeviceCore","GET")
        self.deviceListInfo = xmlParse.parseDeviceListing(response_body)
        #([connectID,lat,longit,group,connected,globID,disconnectTime ])
        for i in self.deviceListInfo:
            print i
            result = datamanager.getDeviceByID(i[0])
            if result is None:
                print "\tNEW Device","\t",i[2],i[3]
                if i[0][0] == "0":
                    i[0].upper()
                datamanager.addNewDevice(devConnectwareId=i[0],dpMapLat=i[1],dpMapLong=i[2],dpConnectionStatus=i[4],dpGlobalIp=i[5],dpLastDisconnectTime=i[6])
                #recordItem = models.device(devConnectwareId=i[0],dpMapLat=i[1],dpMapLong=i[2],dpConnectionStatus=i[4],dpGlobalIp=i[5],dpLastDisconnectTime=i[6])
                #db.session.add(recordItem)
            else:
                print "\tUPDATE Device","\t",result.devConnectwareId,result.dpConnectionStatus
                result.devConnectwareId=i[0]
                result.dpMapLat=i[1]
                result.pMapLong=i[2]
                result.dpConnectionStatus=i[4]
                result.dpGlobalIp=i[5]
                result.dpLastDisconnectTime=i[6]
        datamanager.commitDB()
        return self.deviceListInfo
    
    def getUserList(self):
        pass

    def updateStreamListDataPoints(self,lengthOfTime=0):
        for stream in self.streamListInfo:  #for every data stream, get list of points
            #get all in last week/day/hour (check database to figure out which?)
            #print stream
            streamPoints = self.getDataStreamPoints(stream[0],stream[1])
            #print streamPoints
            #store to database
            for p in streamPoints:
                #check if exists
                result = datamanager.getDataPoint(stream[0],stream[1],p[0],p[1])
                if result is None:
                    print "New Data Point Record: ",stream,p
                    datamanager.addDataPoint(devID=stream[0],streamID=stream[1],timeStamp = p[0],datapoint=p[1])
                else:
                    print "Record exists...",
                #recordItem = models.dataPointRecords(devID=stream[0],streamID=stream[1],timeStamp = p[0],datapoint=p[1])
                #db.session.add(recordItem)
        datamanager.commitDB()
            #devID,StreamID,TS,Data
            #with open("etheriosdatastore\ethStreamPoints_"+str(stream[0])+"_"+str(stream[1]),"w") as filewrt:
                #for p in streamPoints:
                    #filewrt.write(str(p[0])+","+str(p[1])+"\n")


##Get stream data for system with latest data, store to database or update if item already exists
    def updateLatestStreamValues(self):
        response_body = self.genericWebServiceCall("/DataStream/","GET")
        self.streamListInfo = xmlParse.parseStreamListingXML(response_body)
        #(devID,StreamID,TS,datapoint)
        for i in self.streamListInfo:
            #result = models.latestDataStreamPoints.query.filter_by(streamID=i[1],devID=i[0]).first()
            result = datamanager.getStreamListByDeviceIDAndStreamID(i[0],i[1])
            if result is None:
                print "\tNEW RECORD","\t",i#[2],i[3]
                datamanager.addNewStream(devID=i[0],streamID=i[1],timeStamp = i[2],datapoint=i[3])
                #recordItem = models.latestDataStreamPoints(devID=i[0],streamID=i[1],timeStamp = i[2],datapoint=i[3])
                #db.session.add(recordItem)
            else:
                print "\tUPDATE RECORD","\t",result.datapoint,result.timeStamp
                result.timeStamp = i[2]
                result.datapoint=i[3]
        datamanager.commitDB()

        return self.streamListInfo

    def getDataStreamPoints(self,devID,dataStr,size=0,startTime=0,endTime=0):
        if startTime and endTime:
            # ws/DataPoint/device1/temp?startTime=2012-07-18T12:00:00.000Z&endTime=2012-07-18T12:30:00.000Z
            response_body = self.genericWebServiceCall("/DataPoint/{0}/{1}?startTime={2}".format(devID,dataStr,startTime),"GET")
        elif size:
            response_body = self.genericWebServiceCall("/DataPoint/{0}/{1}?size={2}".format(devID,dataStr,size),"GET")
        else:
            response_body = self.genericWebServiceCall("/DataPoint/{0}/{1}".format(devID,dataStr),"GET")
        #print response_body
        return xmlParse.parseDataStreamXML(response_body)

    def getDeviceSettings(self,devID):
        message = """<sci_request version="1.0"> 
          <send_message cache="false"> 
            <targets> 
              <device id="%s"/> 
            </targets> 
            <rci_request version="1.1"> 
              <query_setting/></rci_request>
          </send_message></sci_request>"""%devID

        webservice = httplib.HTTP("login.etherios.com",80)
        # to what URL to send the request with a given HTTP method
        webservice.putrequest("POST", "/ws/sci")

        # add the authorization string into the HTTP header
        webservice.putheader("Authorization", "Basic %s"%self.auth)
        webservice.putheader("Content-type", "text/xml; charset=\"UTF-8\"")
        webservice.putheader("Content-length", "%d" % len(message))
        webservice.endheaders()
        webservice.send(message)

    def genericWebServiceCall(self,request,getpost,message=""):
        print request
        webservice = httplib.HTTP("login.etherios.com",80)
        # to what URL to send the request with a given HTTP method
        webservice.putrequest(getpost, "/ws"+request)
        # add the authorization string into the HTTP header
        webservice.putheader("Authorization", "Basic %s"%self.auth)
        webservice.putheader("Content-type", "text/xml; charset=\"UTF-8\"")
        if len(message):
            webservice.putheader("Content-length", "%d" % len(message))
        webservice.endheaders()
        if len(message):
            webservice.send(message)
        statuscode, statusmessage, header = webservice.getreply()
        response_body = webservice.getfile().read()
        return response_body
