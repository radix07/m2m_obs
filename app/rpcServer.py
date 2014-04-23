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
    #initLocalHostXMLRPC(self):
    def __init__(self,address='http://localhost:8077/'):
        print "Connecting to ",address
        self.x=xmlrpclib.ServerProxy(address)
        
        #scan for backend servers???.. check localhost and scan local base network
        #x=xmlrpclib.ServerProxy('http://192.168.1.53:8077/')

    def getSettings(self):
        settingsBinary = self.x.settings().data
        fileManager.writeSettings(settingsBinary,1)
        return pickle.loads(settingsBinary)
    def getLiveStreams(self):
        liveStream,recordData = self.x.get_live_streams()
        print "Live Stream Def:"
        for i in liveStream:
            print i
        print "Record Data"        
        for i in recordData:
            print i
        return liveStream,recordData

    def writeSettings(self,settings):
        self.x.write_settings(pickle.dumps(settings))

    def getStatus(self):
        status = self.x.get_system_status()
        print status
        return status

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
    #def getItem(self)
    #def writeItem(self)
    #def getLiveSampleList(self)


#parse menu filter listings

    def getFilteredDataValues(self):
        pass
    
if __name__ == '__main__':    
    #test 
    s = xmlServerProc()
    #s.initLocalHostXMLRPC()
    s.getLiveStreams()
        
    #print s.getStatus()
    '''
    db  = s.getDatabase()
    set = s.getSettings()
    '''

