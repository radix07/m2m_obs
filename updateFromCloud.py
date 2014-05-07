from app import db,etheriosmanager,datamanager
import time

etherios = etheriosmanager.etheriosData()
#etherios.tryLogin("TestMe","Password_123")
etherios.tryLogin("pgengineering","Pgecs-2322")
time1 = time.time()
etherios.updateLatestStreamValues()
etherios.updateStreamListDataPoints()    
#datamanager.cleanOldDataForDBThreshold(9700)        #how to ensure actually only oldest records removed?

time2 = time.time()
print 'Import function took %0.3f ms' % ((time2-time1)*1000.0)

