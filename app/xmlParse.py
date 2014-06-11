#XML Parser for Etherios Web Calls
from xml.dom import minidom
'''
<result>
   <resultTotalRows>3</resultTotalRows>
   <requestedStartRow>0</requestedStartRow>
   <resultSize>3</resultSize>
   <requestedSize>1000</requestedSize>
   <remainingSize>0</remainingSize>
   <DeviceCore>
      <id>
         <devId>1094434</devId>
         <devVersion>12</devVersion> 
      </id>
      <devRecordStartDate>2013-12-23T21:47:00.000Z</devRecordStartDate>
      <devMac>00:0c:29:ad:9c:49</devMac>
      <devConnectwareId>00000000-00000000-000C29FF-FFAD9C49</devConnectwareId>
      <cstId>6163</cstId>
      <grpId>9881</grpId>
      <devEffectiveStartDate>2013-12-09T20:59:00.000Z</devEffectiveStartDate>
      <devTerminated>false</devTerminated>
      <dvVendorId>50332145</dvVendorId> 
      <dpDeviceType>SICoM Sample</dpDeviceType>
      <dpFirmwareLevel>16777216</dpFirmwareLevel>
      <dpFirmwareLevelDesc>1.0.0.0</dpFirmwareLevelDesc>
      <dpRestrictedStatus>0</dpRestrictedStatus>
      <dpLastKnownIp>192.168.1.190</dpLastKnownIp>
      <dpGlobalIp>69.128.109.62</dpGlobalIp>
      <dpConnectionStatus>0</dpConnectionStatus>
      <dpLastConnectTime>2014-01-30T20:57:20.627Z</dpLastConnectTime>
      <dpContact/>
      <dpDescription/>
      <dpLocation/>
      <dpMapLat>44.932017</dpMapLat>
      <dpMapLong>-93.461594</dpMapLong>
      <dpServerId/>
      <dpZigbeeCapabilities>0</dpZigbeeCapabilities>
      <dpCapabilities>68210</dpCapabilities>
      <grpPath>PG Controllers</grpPath>
      <dpLastDisconnectTime>2014-01-30T20:58:15.400Z</dpLastDisconnectTime>
   </DeviceCore>
'''
def parseDeviceListing(ds):
    #print ds
    xmldoc = minidom.parseString(ds)
    itemlist = xmldoc.getElementsByTagName('DeviceCore') 
    valueList=[]
    for s in itemlist:
        lat=0
        longit=0
        connectID=0
        disconnectTime=0
        group=""
        if len(s.getElementsByTagName("devConnectwareId")):
            connectID = s.getElementsByTagName("devConnectwareId")[0].firstChild.nodeValue
        if len(s.getElementsByTagName("dpGlobalIp")):
            globID = s.getElementsByTagName("dpGlobalIp")[0].firstChild.nodeValue
        if len(s.getElementsByTagName("dpLastDisconnectTime")):
            disconnectTime = s.getElementsByTagName("dpLastDisconnectTime")[0].firstChild.nodeValue

        if len(s.getElementsByTagName("dpMapLat")):
            lat = s.getElementsByTagName("dpMapLat")[0].firstChild.nodeValue
        if len(s.getElementsByTagName("dpMapLong")):
            longit = s.getElementsByTagName("dpMapLong")[0].firstChild.nodeValue
        try:
            if len(s.getElementsByTagName("grpPath")):
                group = s.getElementsByTagName("grpPath")[0].firstChild.nodeValue
        except:
            group="root"
        if len(s.getElementsByTagName("dpConnectionStatus")):
            connected = s.getElementsByTagName("dpConnectionStatus")[0].firstChild.nodeValue

        valueList.append([connectID,lat,longit,group,connected,globID,disconnectTime ])
    
    return valueList

'''<result>
       <resultSize>26</resultSize>
       <requestedSize>1000</requestedSize>
       <pageCursor>8dd271e1-9b13-11e3-8159-bc764e10597d</pageCursor>
       <requestedStartTime>-1</requestedStartTime>
       <requestedEndTime>-1</requestedEndTime>
       <DataPoint>
          <id>c476f277-9981-11e3-a944-bc764e105279</id>
          <cstId>6163</cstId>
          <streamId>0000000-00000000-00042dFF-FF0418fb/EngineSpeedFloat</streamId>
          <timestamp>1392826837720</timestamp>
          <serverTimestamp>1392848449874</serverTimestamp>
          <data>367.309125115</data>
          <description/>
          <quality>0</quality>
          <location>42.259636,-89.058205,223.0</location>
       </DataPoint>'''

def parseDataStreamXML(ds):
    if len(ds) > 300:
        print "\tDataStreamParserXML Len :",len(ds)
    elif "<resultSize>0</resultSize>" in ds:
        return None
    else:
        print "\tDataStreamParserXML Len :",len(ds)
        print ds
    
    xmldoc = minidom.parseString(ds)
    node = xmldoc.documentElement
    resLen = xmldoc.getElementsByTagName('resultedSize') 
    itemlist = xmldoc.getElementsByTagName('DataPoint') 
    valueList=[]
    for s in itemlist:
        ts = s.getElementsByTagName("timestamp")
        val = s.getElementsByTagName("data")
        valueList.append([ts[0].firstChild.nodeValue,val[0].firstChild.nodeValue])
    return valueList


'''
<result>
   <resultSize>40</resultSize>
   <requestedSize>1000</requestedSize>
   <pageCursor>5fdfa7e6-28-13ee9978</pageCursor>
   <DataStream>
      <cstId>6163</cstId>
      <streamId>0000000-00000000-00042dFF-FF0418fb/ActuatorCurrent</streamId>
      <dataType>FLOAT</dataType>
      <forwardTo/>
      <currentValue>
         <id>f72820d4-8da7-11e3-8dad-bc764e113426</id>
         <timestamp>1391523829690</timestamp>
         <serverTimestamp>1391523850522</serverTimestamp>
         <data>0.0128481784797</data>
         <description/>
         <quality>0</quality>
      </currentValue>
      <description/>
      <units>amps</units>
      <dataTtl>2678400</dataTtl>
      <rollupTtl>2678400</rollupTtl>
   </DataStream>
'''
def parseStreamListingXML(ds):
    #print ds
    xmldoc = minidom.parseString(ds)
    itemlist = xmldoc.getElementsByTagName('DataStream') 
    valueList=[]
    for s in itemlist:
        units=""
        test = s.getElementsByTagName("streamId")[0].firstChild.nodeValue.split("/")
        sublist = s.getElementsByTagName('currentValue')
        if len(s.getElementsByTagName("units")):
            try:units = s.getElementsByTagName("units")[0].firstChild.nodeValue
            except: pass
        for b in sublist:
            test.append(b.getElementsByTagName("timestamp")[0].firstChild.nodeValue)
            test.append(b.getElementsByTagName("data")[0].firstChild.nodeValue)
        #test.append(s.getElementsByTagName("data")[0].firstChild.nodeValue)
            #get sub value
        test.append(units)
        valueList.append(test)    ##dev_id,dataItem

    return valueList

