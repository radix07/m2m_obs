'''
Called periodically from extenal process on server 

Will update all new devices, streams, data points
'''

from app import db,etheriosmanager,datamanager
import time

#datamanager.getDecimatedDatapointsByID("00000000-00000000-00042DFF-FF0418FB","PowerInputVoltage",1)
#datamanager.getAllDatapointsByIDRaw('00000000-00000000-00042DFF-FF0418FB','PowerInputVoltage')

etherios = etheriosmanager.etheriosData()
#etherios.tryLogin("TestMe","Password_123")
etherios.tryLogin("pgengineering","Pgecs-2322")
time1 = time.time()
etherios.updateLatestStreamValues()

etherios.updateStreamListDataPoints(limit=1000) 
#while etherios.updateStreamListDataPoints(limit=1000) >50:pass   #dont run on actual server!!!! May never stop...

#datamanager.cleanOldDataForDBThreshold(9800)        #how to ensure actually only oldest records removed?
#cant remove last item of a particular stream or latest record lost

time2 = time.time()
print 'Import function took %0.3f ms' % ((time2-time1)*1000.0)

