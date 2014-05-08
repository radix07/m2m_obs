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
            print "Device Count:",db.session.query(device).filter(device.id.like('%')).count() 
            print "Data Stream Count:",db.session.query(latestDataStreamPoints).filter(latestDataStreamPoints.id.like('%')).count() 
            print "Data Point Count:",db.session.query(dataPointRecords).filter(dataPointRecords.id.like('%')).count() 
            print "Latest DataPoint:",time.strftime('%B %d, %Y %H:%M:%S', time.localtime((float(datamanager.getMostRecentTSDataPoint())/1000)))
            assert 1==1            
        except:
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
                #validate timestamps, ordering
                #check for duplicates
                #find last
                #catch drastic value changes for event occurance?

        pass

if __name__ == '__main__':
    unittest.main()
