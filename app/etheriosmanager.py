import httplib
import base64
import xmlParse
import datamanager
import time
from config import DASH_ETHERIOS_KEY
import json
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
        
        response_body = self.validateKeyFile()
        print "UserName:",un," Password:",pw,"  AutKey:", self.auth
        print "Result:",response_body
        if response_body != 1:
            if "Bad credentials" in response_body:
                self.auth = base64.encodestring("%s:%s"%(self.username,self.password))[:-1]
                print "Bad Credentials"
                #print self.username,self.password, self.auth
                return None
            else:
                print "valid user credentials, invalid cloud/dash association keys"
                return "Invalid Key"
        else:
            username = un
            password = pw
            user = datamanager.addOrGetUser(username,password)                        
            self.ethUser = user
            response_body = self.initFromDB()
            return user
    def validateKeyFile(self):
        response = self.genericWebServiceCall("/FileData/~/dashKeyfile","GET")
        if response == DASH_ETHERIOS_KEY:
            return 1
        else:
            return response


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
                self.deviceListInfo.append([record.devConnectwareId,record.dp_map_lat,record.dp_map_long,"",record.dp_connection_status,record.dpGlobalIp,record.dp_last_disconnect_time])
            #check for new devices if stale
            #self.printFormattedNestedArray(self.deviceListInfo)
        '''

        result = datamanager.getStreamList()
        if len(result) ==0:
            print "No Streams in database"
            self.updateLatestStreamValues()     #query for all streams
        else:
            self.streamListInfo =[]
            for record in result:       #(dev_id,stream_id,TS,datapoint)
                self.streamListInfo.append([record.dev_id,record.stream_id,record.timestamp,record.datapoint])
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
            #print "Len:",len(result),result[0].id, result[0].dev_id,result[0].datapoint,result[0].timestamp
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

    def deviceCLIRequest(self,deviceID,CLI):
        message = """<sci_request version="1.0"> 
                      <send_message> 
                        <targets> <device id="{0}"/> </targets> 
                        <rci_request version="1.1"> 
                          <do_command target="cli">
                            <cli>{1}</cli></do_command>
                        </rci_request></send_message>
                    </sci_request>""".format(deviceID,CLI)
        return self.genericWebServiceCall("/sci","POST",message)

    def setDeviceLocation(self,deviceID,lat,longit):
        message = """<DeviceCore>
              <devConnectwareId>{0}</devConnectwareId> 
                <dpMapLat>{1}</dpMapLat>
                <dpMapLong>{2}</dpMapLong>
            </DeviceCore>
            """.format(deviceID,lat,longit)
        self.genericWebServiceCall("/DeviceCore","PUT",message)

    def updateDeviceList(self):
        response_body = self.genericWebServiceCall("/DeviceCore","GET")
        result = None
                
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
                datamanager.addNewDevice(dev_connectware_id=i[0],dp_map_lat=i[1],dp_map_long=i[2],dp_connection_status=i[4],dp_global_ip=i[5],dp_last_disconnect_time=i[6])
                #recordItem = models.device(dev_connectware_id=i[0],dp_map_lat=i[1],dp_map_long=i[2],dp_connection_status=i[4],dp_global_ip=i[5],dp_last_disconnect_time=i[6])
                #db.session.add(recordItem)
            else:
                print "\tUPDATE Device","\t",result.dev_connectware_id,result.dp_connection_status
                result.dev_connectware_id=i[0]
                result.dp_map_lat=i[1]
                result.dp_map_long=i[2]
                result.dp_connection_status=i[4]
                result.dp_global_ip=i[5]
                result.dp_last_disconnect_time=i[6]
        print "Committing Device List..."
        datamanager.commitDB()
        
        self.deviceListInfo  = datamanager.getDeviceListFormatted()

        return self.deviceListInfo
    
    def updateStreamListDataPoints(self,fromDate=0,limit=10):
        '''
        May want to allow for getting more than 1000 points per stream, Etherios Limited by default... Adjust request size or ask for more if available if limit hit...
        This module however should not miss any datapoints as it retrieves data since latest point sampled
        Even though it may not bring all data in at once, calling multiple times will eventually get all data if it isnt coming in faster than the call rate
        Ex. if calling daily, would need to verify that no more than 1000 points/day per stream would typically be generated
            Requires an export rate faster than 1 point every ~1.5 minutes per stream to need multiple calls per day
        '''
        '''May need to optimize insert method to use SQLAlchemy core method to speed up bulk inserts... potential to be 25 times faster.. 12 minute run time with maxed point counts and 15 streams'''
        endTimer=0     
        newDataPointCounter=0
        commitFlag=0
        for stream in self.streamListInfo:  #for every data stream, get list of points                
            if fromDate <= 0:
                lastPointTS = datamanager.getMostRecentTSDataPoint(stream[0],stream[1])+1   #add ms as to not query same data again
            else:
                lastPointTS = fromDate
            
            startTimer = time.time()        #prevent oversampling Etherios
            if startTimer - endTimer < 1:#print "Fast Sample, Add Delay...",startTimer - endTimer
                print "Delay Added:",startTimer - endTimer
                time.sleep(1.2)
            else:pass#print "Sample Time Delta:", str(startTimer - endTimer)

            if lastPointTS:
                streamPoints = self.getDataStreamPoints(stream[0],stream[1],startTime=lastPointTS,limit=limit)
            else:
                print "Last data point not found!"
                streamPoints = self.getDataStreamPoints(stream[0],stream[1],limit=limit)
            
            if streamPoints is None:
                print "\tNo New Etherios data"
                #Stream exists, but no data points! Should this stream be deleted from Etherios????
                #OR.....Zero results depending responses data
            elif len(streamPoints) == 0:    #shouldnt happen
                print "\tNo New Etherios data"
            else: 
                print "Processing ",len(streamPoints)," Data Points..."
                newDataPointCounter+=len(streamPoints)
                if datamanager.fastaddDataPoints(dev_id=stream[0],stream_id=stream[1],pointList = streamPoints):
                    commitFlag = 1
                '''
                for p in streamPoints:                   
                    result = datamanager.getDataPoint(stream[0],stream[1],p[0],p[1])
                    if result is None:
                        commitFlag = 1
                        datamanager.addDataPoint(dev_id=stream[0],stream_id=stream[1],timestamp = p[0],datapoint=p[1])
                        newDataPointCounter+=1
                        #app.logger.debug("New Data Point Record: ",stream,p)
                        '''
            if commitFlag:
                datamanager.commitDB()
        else:
            print "\tNo new data"
            endTimer = startTimer
        print "Data Points Added:",newDataPointCounter
        return newDataPointCounter

##Get stream data for system with latest data, store to database or update if item already exists
    def updateLatestStreamValues(self):
        result = None
        response_body = self.genericWebServiceCall("/DataStream/","GET")
        if "Bad credentials" in response_body:
            return None

        self.streamListInfo = xmlParse.parseStreamListingXML(response_body)
        #(dev_id,stream_id,TS,datapoint)
        for i in self.streamListInfo:
            #result = models.latestDataStreamPoints.query.filter_by(stream_id=i[1],dev_id=i[0]).first()
            result = datamanager.getStreamListByDeviceIDAndstream_id(i[0],i[1])
            if result is None:
                print "\tNEW RECORD","\t",i#[2],i[3]
                datamanager.addNewStream(dev_id=i[0],stream_id=i[1],timestamp = i[2],datapoint=i[3])
                #recordItem = models.latestDataStreamPoints(dev_id=i[0],stream_id=i[1],timestamp = i[2],datapoint=i[3])
                #db.session.add(recordItem)
            else:
                print "\tUPDATE RECORD","\t",result.dev_id,result.stream_id,result.datapoint,str(time.strftime('%B %d, %Y %H:%M:%S', time.localtime((float(result.timestamp)/1000))))
                result.timestamp = i[2]
                result.datapoint=i[3]
        datamanager.commitDB()

        return self.streamListInfo

    def getDataStreamPoints(self,dev_id,dataStr,size=0,startTime=0,endTime=0,limit=0):        
        #if dev_id == "00000000-00000000-00042DFF-FF0418FB":
            #dev_id = "0000000-00000000-00042DFF-FF0418FB"    #temp fix for embedded id error

        if startTime and endTime:
            # ws/DataPoint/device1/temp?startTime=2012-07-18T12:00:00.000Z&endTime=2012-07-18T12:30:00.000Z            
            if limit<=0:
                call = "/DataPoint/{0}/{1}?startTime={2}&endTime={3}".format(dev_id,dataStr,startTime,endTime)
            else:
                call = "/DataPoint/{0}/{1}?startTime={2}&endTime={3}&size={4}".format(dev_id,dataStr,startTime,endTime,limit)
            print "\tStart/End time thresh",call            
            response_body = self.genericWebServiceCall(call,"GET")
        elif startTime:
            if limit<=0:
                call = "/DataPoint/{0}/{1}?startTime={2}&endTime={3}".format(dev_id,dataStr,startTime,str(int(time.time()*1000)))
            else:
                call = "/DataPoint/{0}/{1}?startTime={2}&endTime={3}&size={4}".format(dev_id,dataStr,startTime,str(int(time.time()*1000)),limit)
            print "\tStart time thresh:",call
            response_body = self.genericWebServiceCall(call,"GET")            
        elif size:
            response_body = self.genericWebServiceCall("/DataPoint/{0}/{1}?size={2}".format(dev_id,dataStr,size),"GET")
        else:
            response_body = self.genericWebServiceCall("/DataPoint/{0}/{1}".format(dev_id,dataStr),"GET")                     
        if "Bad credentials" in response_body:
            return None            
        print "Response Recieved"    
        #print "RE Body:",response_body
        re = xmlParse.parseDataStreamXML(response_body)
        return re

    def getDeviceSettings(self,dev_id):
        message = """<sci_request version="1.0"> 
          <send_message cache="false"> 
            <targets> 
              <device id="%s"/> 
            </targets> 
            <rci_request version="1.1"> 
              <query_setting/></rci_request>
          </send_message></sci_request>"""%dev_id
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
        jsonMode=1
        if jsonMode:
            data = base64.encodestring(json.dumps(data))
            message = """<sci_request version="1.0"><file_system><targets><device id="%s"/>
                        </targets><commands><put_file path="jq_0"><data>%s</data></put_file>
                        </commands></file_system></sci_request>"""%(deviceID,data)
            temp = self.genericWebServiceCall("/sci","POST",message)

            return temp
        if 0:
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
    
    def getApplicationFiles(self):
        pass
    def getFolderContents(self,directory):
        "/ws/FileData?condition=fdPath='~/Applications/'"

    def genericWebServiceCall(self,request,getpost,message=""):
        try:
            webservice = self.getHTTPWebService()
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