#!flask/bin/python
import os
import unittest
import time

from config import basedir
from app import app, db

from app.models import device,User,dataPointRecords,latestDataStreamPoints,localControllerDataItems
from app import etheriosmanager
from app import datamanager

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        db.create_all()
        
    def tearDown(self):
        #db.drop_all()
        pass

    def test_datamanager(self):        
        assert datamanager.fixDevID("00000000-00000000-00042DFF-FF0418FB")[0] == "00000000-00000000-00042DFF-FF0418FB"
        assert datamanager.fixDevID("0000000-00000000-00042DFF-FF0418FB")[0] == "00000000-00000000-00042DFF-FF0418FB"
        assert datamanager.fixDevID("000000-00000000-00042DFF-FF0418FB")[0] != "00000000-00000000-00042DFF-FF0418FB"
        assert datamanager.fixDevID("00080003-00000000-030001F1-E056EE95")[0] == "00080003-00000000-030001F1-E056EE95"
        assert datamanager.fixDevID("PYTHONPC1_RYAN")[0] == "0PYTHONPC1_RYAN"
        assert datamanager.fixDevID("pythonPC1_Ryan")[0] == "pythonPC1_Ryan"
        
    def test_user_db_init_etherios(self):
        # create a user
        app.logger.debug("TEST")
        
        u = User(username = 'TestMe', password ="123_password",email = 'john@example.com')
        etherios = etheriosmanager.etheriosData()

        #test bad
        userRe = etherios.tryLogin(u.username,u.password)                
        assert userRe == None
        
        #test good
        u.password = 'Password_123'
        userRe = etherios.tryLogin(u.username,u.password)                
        assert userRe != None                

        #validate database
        #device list                
        dList = datamanager.getDeviceList()         
        print "Device Count:",len(dList)
        for d in dList:
            print d.id,d.devConnectwareId,d.dpConnectionStatus,d.dpGlobalIp,d.dpLastDisconnectTime,d.dpMapLat,d.dpMapLong
            #invalid devConnectorID,dups (sql model)?
            assert d.id > 0
            assert len(d.devConnectwareId)==35    # or d.devConnectwareId == "python
        
        #data streams
        minTS=99999999999999
        maxTS=0
        strList = datamanager.getStreamList()
        print "data stream count:",len(strList)
        for s in strList:
            assert s.id > 0            
            assert (len(s.devID) == 35 or s.devID == "pythonPC1_Ryan" )      #invalid devID                            
            #dups   (model, how to verify?)
            
            if int(s.timeStamp) < int(minTS):     #timestamp warnings, range report??
                minTS = s.timeStamp
            if int(s.timeStamp) > int(maxTS):
                maxTS = s.timeStamp
            #datapoint length? warn
            #units

        print "\tStream Min TS:",minTS,"\t\t",str(time.strftime('%B %d, %Y %H:%M:%S', time.localtime((float(minTS)/1000))))
        print "\tStream Max TS:",maxTS,"\t\t",str(time.strftime('%B %d, %Y %H:%M:%S', time.localtime((float(maxTS)/1000))))
        '''
        #takes long time to load entire data point list into RAM
        #data points
        minTS=99999999999999
        maxTS=0
        dpList = datamanager.getAllDatapoints()
        print "data points count:",len(dpList)
        for dp in dpList:
            assert dp.id > 0
            assert (len(dp.devID) == 35 or dp.devID == "pythonPC1_Ryan" )      #invalid devID                            
            if int(dp.timeStamp) < int(minTS):     #timestamp warnings, range report??
                minTS = dp.timeStamp
            if int(dp.timeStamp) > int(maxTS):
                maxTS = dp.timeStamp
            #dups?? select * where devID/StreamID/tiemstamp/datapoint match
            #timestamp validate
            #datapoint len?
            #1395079462299
            #1397487951620
        print "\tPoint Min TS:",minTS,"\t\t",str(time.strftime('%B %d, %Y %H:%M:%S', time.localtime((float(minTS)/1000))))
        print "\tPoint Max TS:",maxTS,"\t\t",str(time.strftime('%B %d, %Y %H:%M:%S', time.localtime((float(maxTS)/1000))))
        '''
        #users
            #check for user in db?
        #periodic check for new data test
        etherios.updateLatestStreamValues()
        etherios.updateStreamListDataPoints()

    #def test_ViewsNavForExceptions(self)
    #def test_LocalXMLRpcInterface(self)
    #def test_databaseModels(self)
    #def test_forms(self)
    #def test_periodicUpdate(self)
    #def test_reportGenerator

if __name__ == '__main__':
    unittest.main()