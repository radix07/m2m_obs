#!flask/bin/python
import os
import unittest
import time

from config import basedir
from app import app, db

from app.models import device,User,dataPointRecords,latestDataStreamPoints,device
from app import etheriosmanager
from app import datamanager

from sqlalchemy import func
import sqlalchemy
import time


class Test_testDB(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
    def tearDown(self):
        #db.drop_all()
        pass

    def test_A_Count(self):        
        try:
            dID = "00000000-00000000-00042DFF-FF051018"
            stList = datamanager.getStreamListByDeviceID(dID)
            datapoints = datamanager.getAllDatapointsByID(str(dID),stList[int(0)].streamID)


            print "Device Count:",db.session.query(device).filter(device.id.like('%')).count() 
            print "Data Stream Count:",db.session.query(latestDataStreamPoints).filter(latestDataStreamPoints.id.like('%')).count() 
            print "Data Point Count:",db.session.query(dataPointRecords).filter(dataPointRecords.id.like('%')).count() 
            print "Latest DataPoint:",time.strftime('%B %d, %Y %H:%M:%S', time.localtime((float(datamanager.getMostRecentTSDataPoint())/1000)))

            print "WR21 Specific Data Point Count:",db.session.query(dataPointRecords).filter(dataPointRecords.devID.like('%fb%')).count() 
            assert 1==1            
        except Exception,e:
            print e
            self.fail("Counter query fail")
    def test_B_BreakdownDevice2Streams(self):
        #per device
            #get streams
                #validate timestamps, ordering
                #check for duplicates
                #find last

        assert 1==1

    def test_C_BreakdownStreams2Points(self):
        #per stream
            #get points (lots of data...)
        #minThresh = 35
        #maxThresh = 55
        minThresh = 10
        maxThresh = 25
        #devID = "00000000-00000000-00042DFF-FF0418FB"

        devID = "00080003-00000000-030001F1-90D17C44"
        #timeSince = 1399533532000
        timeSince = 1399992866000  #when fix for time comp added

        print "Device:",devID
        print "Start Time:",time.strftime('%B %d, %Y %H:%M:%S', time.localtime((timeSince/1000)))
        strList = datamanager.getStreamListByDeviceID(devID)
        for st in strList:
            print st.streamID
            if st.streamID == 'EventList':
                pass
            else:
                fist=0
                dp = datamanager.getAllDatapointsFiltered(devID,timeSince,st.streamID)
                try:
                    lastRecord = dp[0]
                    for i in dp:
                        #should be close to 44
                        if fist > 0:
                            delta = (i.timeStamp - lastRecord.timeStamp)/1000 
                            if delta < minThresh or delta >maxThresh:
                                print "Delta:",delta ,"\t",
                                print "Time:",time.strftime('%B %d, %Y %H:%M:%S', time.localtime((i.timeStamp/1000))),
                                print i.id,i.timeStamp,i.datapoint,i.created_on
                        fist=1
                        lastRecord = i

                        #validate timestamps, ordering
                        #interval range analyzer
                        #check for duplicates
                        #find last
                        #catch drastic value changes for event occurance?

                except Exception,e:
                    print "Bad Query? :  ",e

    
if __name__ == '__main__':
    unittest.main()
