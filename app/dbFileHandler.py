import datamanager
import etheriosmanager


class genericDB2FileHandler():
    def __init__():
        pass
    #database getter/setter
    #file getter/setter


class calibrationFiles():
    '''
        Handle parsing calFiles in and out
        Deal with merging in and out of dataListing Table
        Pulls cal file from appriopriate source
    '''
    def __init__(deviceID):
        pass

class settingsFiles():
    def __init__(deviceID):
        pass

class databaseFiles():
    def __init__(etherios,deviceID):
        #get inherint application association from device table
        #
        pass

    def updateDeviceDataRecords(forceDeviceSource=0):
        #query for any existing
        #get file source
            #retrieve from cloud source (forceDeviceSource=0)
                #else retrieve from device if connected (or forceDeviceSource=1 force)
                    #store back on etherios cloud for later use???

        #iterate update
        pass

    def getDeviceDataTable():
        #query table for all device specific data
            #if not updatedevicedatarecords from cloud file
        #
        pass

    def queryDeviceData():
        #device optimize query function???
        pass



if __name__ == '__main__':
    

    pass
