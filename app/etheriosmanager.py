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
    def __init__(self):
        self.username = "" #"TestMe"
        self.password = "" #"Password_123"
        self.auth = base64.encodestring("%s:%s"%(self.username,self.password))[:-1]
        self.oneCall=0
        self.deviceListInfo = []
        self.streamListInfo = []
        self.streamDataList = {}        
        self.ethUser =None

    def tryLogin(self,un,pw):
        self.auth = base64.encodestring("%s:%s"%(un,pw))[:-1]        
        #response_body = self.genericWebServiceCall("/DeviceCore","GET")
        response_body = self.initFromDB()
        print "UserName:",un," Password:",pw,"  AutKey:", self.auth
        print "Result:",response_body
        if "Bad credentials" in response_body:
            self.auth = base64.encodestring("%s:%s"%(self.username,self.password))[:-1]
            print self.username,self.password, self.auth
            return None
        else:
            username = un
            password = pw
            user = datamanager.addOrGetUser(username,password)                        
            self.ethUser = user
            
            return user
    
    def initFromDB(self):
        #result = datamanager.getDeviceList()
        if self.getNewDevices() is None:
            return "Bad credentials"
        '''
        if len(result) ==0:
            print "No Devices in database"
            self.updateDeviceList()
            #other datatables should be empty if there are no devices
                #Should they be deleted/emptied?
        else:
            self.deviceListInfo =[]
            for record in result:       #([connectID,lat,longit,group,connected,globID,disconnectTime ])
                self.deviceListInfo.append([record.devConnectwareId,record.dpMapLat,record.dpMapLong,"",record.dpConnectionStatus,record.dpGlobalIp,record.dpLastDisconnectTime])
            #check for new devices if stale
            #self.printFormattedNestedArray(self.deviceListInfo)
        '''

        result = datamanager.getStreamList()
        if len(result) ==0:
            print "No Streams in database"
            self.updateLatestStreamValues()     #query for all streams
        else:
            self.streamListInfo =[]
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
            #print "Latest DB DataPoint: ",str(time.strftime('%B %d, %Y %H:%M:%S', time.localtime((float(result)/1000))))
            #datamanager.normalizeDataPointRecords()
            #should extend to recent datapoints, and get latest if stale (older than.. 1 day/hour??)
            #print "Len:",len(result),result[0].id, result[0].devID,result[0].datapoint,result[0].timeStamp
            pass
        return "Data Initialzed!"

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
        return self.updateDeviceList()

    def getNewStreams(self):
        self.updateLatestStreamValues()

    def getRecentDataPoints(self):
        '''
            Will be run periodically as scheduled task or on-demad (force update/refresh) to update new Etherios data points
            could be incorporated into a live mode possibly? Or maybe handle seperately... (JS on user machine direct to cloud)
            (Typically a daily run should suffice, and only ~12 minutes/day allowed with free heroku tier)
        '''
        #find latest data point
        lastPointTS = datamanager.getMostRecentTSDataPoint()
        print "LastSampleDate:",str(time.strftime('%B %d, %Y %H:%M:%S', time.localtime((float(lastPointTS)/1000))))
        print "LastSampleDate:",lastPointTS
                
        #query etherios for all since
        #self.updateStreamListDataPoints(fromDate=lastPointTS)
        self.updateStreamListDataPoints()
        #add to database

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
                
        try:
            if "Bad credentials" in response_body:
                return None
        except:
            return None

        self.deviceListInfo = xmlParse.parseDeviceListing(response_body)    #gets only from Etherios
        #local

        #([connectID,lat,longit,group,connected,globID,disconnectTime ])
        for i in self.deviceListInfo:
            print i
            try:
                result = datamanager.getDeviceByID(i[0])
            except:
                pass
            if result is None:
                print "\tNEW Device","\t",i[1],i[3]
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
        print "Committing Device List..."
        datamanager.commitDB()
        
        self.deviceListInfo  = datamanager.getDeviceListFormatted()

        return self.deviceListInfo
    
    def updateStreamListDataPoints(self,fromDate=0):
        #get data
        #store data
        endTimer=0     
        newDataPointCounter=0
        for stream in self.streamListInfo:  #for every data stream, get list of points                
            if not fromDate:
                lastPointTS = datamanager.getMostRecentTSDataPoint(stream[0],stream[1])
            else:
                lastPointTS = fromDate
            
            startTimer = time.time()        #prevent oversampling Etherios
            if startTimer - endTimer < 1:#print "Fast Sample, Add Delay...",startTimer - endTimer
                time.sleep(.8)
            else:pass#print "Sample Time Delta:", str(startTimer - endTimer)

            if lastPointTS:
                streamPoints = self.getDataStreamPoints(stream[0],stream[1],startTime=lastPointTS)
            else:
                streamPoints = self.getDataStreamPoints(stream[0],stream[1])
            commitFlag=0
            if len(streamPoints) == 0:
                print "\tNo Etherios data"
                #Stream exists, but no data points! Should this stream be deleted from Etherios????
                #OR.....Zero results depending responses data

            else: #print "Processing ",len(streamPoints)," Data Points"
                for p in streamPoints:                   
                    result = datamanager.getDataPoint(stream[0],stream[1],p[0],p[1])
                    if result is None:
                        commitFlag = 1
                        datamanager.addDataPoint(devID=stream[0],streamID=stream[1],timeStamp = p[0],datapoint=p[1])
                        newDataPointCounter+=1
                        #app.logger.debug("New Data Point Record: ",stream,p)
            if commitFlag:
                datamanager.commitDB()
            else:
                print "\tNo new data"
            endTimer = startTimer
        print "Data Points Added:",newDataPointCounter

##Get stream data for system with latest data, store to database or update if item already exists
    def updateLatestStreamValues(self):
        response_body = self.genericWebServiceCall("/DataStream/","GET")
        if "Bad credentials" in response_body:
            return None

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
                print "\tUPDATE RECORD","\t",result.devID,result.streamID,result.datapoint,str(time.strftime('%B %d, %Y %H:%M:%S', time.localtime((float(result.timeStamp)/1000))))
                result.timeStamp = i[2]
                result.datapoint=i[3]
        datamanager.commitDB()

        return self.streamListInfo

    def getDataStreamPoints(self,devID,dataStr,size=0,startTime=0,endTime=0):        
        #if devID == "00000000-00000000-00042DFF-FF0418FB":
            #devID = "0000000-00000000-00042DFF-FF0418FB"    #temp fix for embedded id error

        if startTime and endTime:
            # ws/DataPoint/device1/temp?startTime=2012-07-18T12:00:00.000Z&endTime=2012-07-18T12:30:00.000Z            
            call = "/DataPoint/{0}/{1}?startTime={2}&endTime={3}".format(devID,dataStr,startTime,endTime)
            print "\tStart/End time thresh",call            
            response_body = self.genericWebServiceCall(call,"GET")
        elif startTime:
            call = "/DataPoint/{0}/{1}?startTime={2}&endTime={3}".format(devID,dataStr,startTime,str(int(time.time()*1000)))
            print "\tStart time thresh:",call
            response_body = self.genericWebServiceCall(call,"GET")            
        elif size:
            response_body = self.genericWebServiceCall("/DataPoint/{0}/{1}?size={2}".format(devID,dataStr,size),"GET")
        else:
            response_body = self.genericWebServiceCall("/DataPoint/{0}/{1}".format(devID,dataStr),"GET")                     
        if "Bad credentials" in response_body:
            return None            
            
        #print "RE Body:",response_body
        re = xmlParse.parseDataStreamXML(response_body)
        return re

    def getDeviceSettings(self,devID):
        message = """<sci_request version="1.0"> 
          <send_message cache="false"> 
            <targets> 
              <device id="%s"/> 
            </targets> 
            <rci_request version="1.1"> 
              <query_setting/></rci_request>
          </send_message></sci_request>"""%devID
        try:
            webservice = self.getHTTPWebService()
            # to what URL to send the request with a given HTTP method
            webservice.putrequest("POST", "/ws/sci")

            # add the authorization string into the HTTP header
            webservice.putheader("Authorization", "Basic %s"%self.auth)
            webservice.putheader("Content-type", "text/xml; charset=\"UTF-8\"")
            webservice.putheader("Content-length", "%d" % len(message))
            webservice.endheaders()
            webservice.send(message)
            statuscode, statusmessage, header = webservice.getreply()
            response_body = webservice.getfile().read()
            return response_body
        except Exception, e:
            print e
        statuscode, statusmessage, header = webservice.getreply()

    def RCIRequest(self,deviceID,data,action="action_callback"):
        message ="""<sci_request version="1.0"> 
                    <send_message cache="false"><targets><device id="%s"/>
                    </targets> <rci_request version="1.1"><do_command target="%s">
                    <data>%s</data></do_command></rci_request></send_message></sci_request>"""%(deviceID,action,data)
        temp = self.genericWebServiceCall("/sci","POST",message)
        print temp
        return temp

    def sendFile(self,data,destination):
        #webservice.putrequest("PUT", "/ws/FileData/~/test_folder/test.xml?type=file")
        request = "/FileData/~/"+destination+"?type=file"
        print request
        print self.genericWebServiceCall(request,"PUT",data)

    def genericWebServiceCall(self,request,getpost,message=""):
        try:
            webservice = self.getHTTPWebService()
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
            #if statuscode != 201:
            response_body = webservice.getfile().read()
            return response_body
        except Exception, e:
            print e

    def getHTTPWebService(self):
        return httplib.HTTP("login.etherios.com",80)