import xmlrpclib
import cPickle as pickle
import os.path

#x=xmlrpclib.ServerProxy('http://localhost:8077/')
x=xmlrpclib.ServerProxy('http://192.168.1.53:8077/')

class xmlServerProc():
    def getSettings(self):
        settingsBinary = x.settings().data
        config = pickle.loads(settingsBinary)

    def getDatabase(self,index=0,force=0):
        #if table doesnt exist or force
        #check if exists
        localDatabase = "db_"+str(index)
        if not force and os.path.isfile(localDatabase):
            with open(localDatabase, 'rb') as handle:
                return pickle.loads(handle.read())

        datab = x.get_data()    #pickle format
        print "Writing new database control file:",localDatabase
        with open(localDatabase, 'wb') as handle:
            handle.write(datab)
        return pickle.loads(datab)

#parse menu filter listings


    def getFilteredDataValues(self):
        pass
    def setDataItem(self,ID,value):
        pass