import xmlrpclib
import cPickle as pickle
import os.path
import socket
import fileManager

def getIPAddress():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com",80))
    listen_interface = s.getsockname()[0]
    print listen_interface
    s.close()
    return listen_interface

xmlrpc_port = 8077
sysIP = getIPAddress()

class xmlServerProc():
    def __init__(self,address='http://localhost:8077/'):
        print "Connecting to ",address
        #initLocalHostXMLRPC(self):
        self.connect(address) 
        #self.x=xmlrpclib.ServerProxy(address)
        #scan for backend servers???.. check localhost and scan local base network
        #x=xmlrpclib.ServerProxy('http://192.168.1.53:8077/')
    def connect(self,address):
        try:
            self.x=xmlrpclib.ServerProxy(address)
        except Exception, e:
            print e
    def CheckConnect(self):
        return self.x.CheckConnect()

    def GetControllerCal(self):
        controllerCal = self.x.GetControllerCal()
        #for i in controllerCal:
            #print i 
        return controllerCal

    def SetControllerCal(self,cal):
        result = self.x.SetControllerCal(cal)
        print result
        if result:
            print "Cal Set"
        else:
            print "Cal Failed"
        return result

    def GetDB(self,dev_id,type=0,force=0,index=0):
        #if table doesnt exist or force
        #check if exists
        print "Get Database" 
        localDatabase = "db_"+dev_id+"_"+str(index)
        if not force and os.path.isfile(localDatabase):
            #verify connection!
            try:
                with open(localDatabase, 'rb') as handle:
                    return pickle.loads(handle.read())
            except:
                print "Failed to run remote function"
                return 0

        datab = self.x.GetDB()    #pickle format
        print "Writing new database control file:",localDatabase
        with open(localDatabase, 'wb') as handle:
            handle.write(datab)
        return pickle.loads(datab)

    def GetDBVarValues(self):
        print "Get Database Values"
        try:
            dataV = self.x.GetDBVarValues()
        except Exception, e:
            print e
            print dataV
        return dataV 

    def GetItem(self,id):
        return self.x.GetItem(id)

    def SetItem(self,id,value,save=0):
        return self.x.SetItem(id,value)

    def GetGOCoMSettings(self):
        settingsBinary = self.x.GetGOCoMSettings().data
        fileManager.writeSettings(settingsBinary,1)
        return pickle.loads(settingsBinary)

    def SetGOCoMSettings(self, configPick):
        self.x.SetGOCoMSettings(pickle.dumps(settings))

    def GetLiveData(self):
         try:
            liveStream,recordData = self.x.GetLiveData()
            print "Live Stream Def:"
            for i in liveStream:
                print i
            print "Record Data"        
            for i in recordData:
                print i
            return liveStream,recordData
         except Exception, e:
            print self.x.GetLiveData()
            print e

    def GetOperationStatus(self):
        status = self.x.GetOperationStatus()
        return status

    def UpdateDataFiles(self, database,event,statusDict):
        pass

    def ConvertDatabase(self, sqlFile,overwrite=0):
        pass

########################################################################################################################
########################################################################################################################
    def getDatabase(self,index=0,force=0):
        #if table doesnt exist or force
        #check if exists
        localDatabase = "db_"+str(index)
        if not force and os.path.isfile(localDatabase):
            #verify connection!
            try:
                if self.x.pow(2,2) == 4:
                    with open(localDatabase, 'rb') as handle:
                        return pickle.loads(handle.read())
                else:
                    print "Remote function return invalid"
                    return 0
            except:
                print "Failed to run remote function"
                return 0

        datab = self.x.get_data()    #pickle format
        print "Writing new database control file:",localDatabase
        with open(localDatabase, 'wb') as handle:
            handle.write(datab)
        return pickle.loads(datab)
    
if __name__ == '__main__':    
    #test 
    s = xmlServerProc("http://192.168.1.54:8077/")
    #s = xmlServerProc()
    #s.initLocalHostXMLRPC()
    #s.test()
    print s.CheckConnect()
    
    test = s.GetOperationStatus()
    print test

    cal = s.GetControllerCal()
    print cal
    #s.SetControllerCal(cal)
    depicDB = s.GetDB("123")
    print depicDB
    config = s.GetGOCoMSettings()
    print config
    s.SetGOCoMSettings(config)

    #s.SetItem([3685,3954,3963],[1,1,0.131])
    listID = []
    dbList =[]
    for i in depicDB:
        listID.append(i[0])
        dbList.append(i)
        if len(listID)>125:
            for j in dbList:print j 
            val = s.GetItem(listID)
            print "\t",val
            print "\t",s.SetItem(listID,val)
            listID = []
            dbList = []
    #data = s.GetDBVarValues()

    #settings
