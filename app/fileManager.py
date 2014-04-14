import cPickle as pickle
import os
import xmlrpclib

settingsFileName = "set1"   #seems to be issue where file stays persistant after deletion in digi...

def validateSettings(config):
    print "Validate Settings file: ",
    valFail = 0
    fileConfig = restoreSettings()
    for key,value in config.iteritems():
        if value !=fileConfig[key]:
            valFail = 1
            print "-"*40,"\n",value
            print fileConfig[key],"\n","-"*40
    if valFail:
        writeSettings(config)

def restoreSettings(file=0):
    #if specific new settings file name found, use that and rename to overwrite default, store new config??....
    if os.path.isfile(settingsFileName) and not file:         #load settings file if it exists
        print "loading settings from file..."
        with open(settingsFileName, 'rb') as handle:
            config = pickle.loads(handle.read())
    else:                               #if settings file not available load default settings and save
        print "loading default settings and storing to file..."
        settingsFile={}
        execfile("settings.py",settingsFile)    #have to handle local python scope issues with execfile by passing to dict and accessing key value
        config = settingsFile["config"]
        with open(settingsFileName, 'wb') as handle:
            pickle.dump(config, handle,pickle.HIGHEST_PROTOCOL)
    #print config['Operation']
    return config

def getXMLRPCSettingsFile():
        print "\nretrieving settings XMLRPC file..."
        with open(settingsFileName, "rb") as f:
            return xmlrpclib.Binary(f.read())


def writeSettings(config,pickled = 0):
    with open(settingsFileName, 'wb') as handle:
        if pickled:
            handle.write(config)
        else:   #raw dict
            pickle.dump(config, handle,pickle.HIGHEST_PROTOCOL)
    print "Saved settings to file"

def restoreDatabase():
    #parse from py for inital loading if required, restoring via pickle to/from external file to speed up read/write of database
    listData=[]
    if os.path.isfile("database"):         #load database file if exists
        print "loading database file..."
        with open('database', 'rb') as handle:
            listData = pickle.loads(handle.read())
    else:                               #if 
        print "loading default database from database.py..."
        with open("database.py") as infile: #iterate through database.py is pickle isnt available
            for line in infile:
                exec(line.strip())
        print "storing to file..."
        with open('database', 'wb') as handle:
            pickle.dump(listData, handle,pickle.HIGHEST_PROTOCOL)
    #else prompt or search for cloud based, or parse an xml/sqlite based file
    return listData

def getXMLRPCDatabase():
    print "\nretrieving database XMLRPC file..."
    with open("database", "rb") as f:
        return xmlrpclib.Binary(f.read())


def writeDatabase(listData):
    with open('database', 'wb') as handle:
        pickle.dump(listData, handle,pickle.HIGHEST_PROTOCOL)   
    print "Saved database to file"


def restoreEventDictonary():
    if os.path.isfile("evntDct"):         #load database file if exists
        print "loading event file..."
        with open('evntDct', 'rb') as handle:
            listData = pickle.loads(handle.read())
    else:
        print "Event Lookup file missing"
    return listData

def restoreStatusDictonary():
    if os.path.isfile("statDsDc"):         #load database file if exists
        print "loading bit status file..."
        with open('statDsDc', 'rb') as handle:
            listData = pickle.loads(handle.read())
    else:
        print "Status Lookup file missing"
    return listData

def append2DataStore(index,record,new=0):
    if new:
        mode='w'
    else:
        mode='a'
    with open('x'+str(index), mode) as handle:
        handle.write(record)

def readDataStore(index):
    if os.path.isfile("x"+str(index)):         #load database file if exists
        with open("x"+str(index), 'r') as handle:
            listData = handle.read()
