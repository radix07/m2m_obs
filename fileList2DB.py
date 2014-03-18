from app import db, models
import os,sys
import StringIO
import csv

resultDir = "//etheriosdatastore//"
resultDir = os.getcwd()+resultDir
onlyfiles = [ f for f in os.listdir(resultDir) if os.path.isfile(os.path.join(resultDir,f)) ]

for i in onlyfiles:
    index = i.split("_")
    if len(index)>3:    #normalize for underscore in dev name
        index[1] = index[1]+"_"+index[2]
        index[2] = index[3]
        del index[3]
    deviceID = index[1]
    stream = index[2]
    print i
    print "\t",index
    mycsv = csv.reader(open(resultDir+i))
    for row in mycsv:
        print row[0],",",row[1]
        recordItem = models.dataPointRecords(devID=deviceID,streamID=stream,timeStamp = row[0],datapoint=row[1])
        db.session.add(recordItem)
db.session.commit()