import os
from flask import flash, session, request, g
from flask import Flask,render_template,abort, redirect, url_for
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.sqlalchemy import SQLAlchemy
from forms import LoginForm
from models import User, ROLE_USER, ROLE_ADMIN
from random import choice
import time
import datamanager
import etheriosmanager
from app import app, db, lm, oid

import datamanager

basedir = os.path.abspath(os.path.dirname(__file__))

etherios = etheriosmanager.etheriosData()


@app.route('/index.html')
@app.route('/')
def raw_index():
    #etherios.initFromDB()
        
    app.logger.debug(etherios.deviceListInfo)
    return render_template('index.html',user= 'Ryan',devList=etherios.deviceListInfo)

@app.route('/clean')
def cleanDB():
    datamanager.removeAllDevices()
    return render_template('index.html',user= 'Ryan',devList=etherios.deviceListInfo)

@app.route('/force')
def forceUpdate():
    etherios.initFromDB(1)
    return render_template('index.html',user= 'Ryan',devList=etherios.deviceListInfo)

@app.route('/test.html')
def testPage():
    print "TEST"
    app.logger.debug(etherios.updateDeviceList())
    #app.logger.debug(etherios.updateLatestStreamValues())    
    #app.logger.debug(etherios.updateStreamListDataPoints())
    #return render_template(temp)
    return render_template('login.html')

@app.route('/login')
@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/controllers.html')
def controllers():
    return render_template('controllers.html',user= 'Ryan',devList=etherios.deviceListInfo)

@app.route('/controller/<deviceID>/<streamID>')
def dataPointView(deviceID,streamID):
    print "DATA POINT VIEW"
    streamList = datamanager.getAllDatapoints(deviceID,streamID)
    
    for st in streamList:
        if st.timeStamp.isdigit():
            st.timeStamp = str(time.strftime('%B %d, %Y %H:%M:%S', time.localtime((float(st.timeStamp)/1000))))
        else:
            st.timeStamp = "--"
            st.datapoint = "--"

    return render_template('dataPointList.html',   #dataPoint
                           user= 'Ryan',
                           streamList=streamList,
                           devID = deviceID,
                           stID = streamID)


@app.route('/controller/<deviceID>')
def controller(deviceID):
    #get all data from db with deviceID
    streamList = datamanager.getStreamListByDeviceID(deviceID)
    for st in streamList:
        print st.timeStamp
        if st.timeStamp.isdigit():
            st.timeStamp = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime((float(st.timeStamp)/1000))))
        else:
            st.timeStamp = "--"
            st.datapoint = "--"
    #app.logger.debug(streamList)
    return render_template('device.html',
                           user= 'Ryan',
                           streamList=streamList,
                           devID = deviceID)

@app.route('/flot.html')
def flot():
    app.logger.debug("float")
    salutation = choice(testStringData)
    return render_template('flot.html', salutation=testStringData[0])



testStringData = [
    'TEST PG SICOM',]


if __name__ == '__main__':
    print "VIEW IS MAIN"
    port = int(os.environ.get('PORT', 5000))
    if port == 5000:
        app.debug = True
    app.run(host='0.0.0.0', port=port)


    '''
@app.route('/getEtheriosStreams.xml')
def etheriosStreams():
    app.logger.debug("Etherios Call")
    return ", ".join(str(x) for x in etherios.updateStreamListDataPoints())


@app.route('/getEtheriosEnginePoints.xml')
def etheriosPoints():
    deviceID = "pythonPC1_Ryan" #"0000000-00000000-00042dFF-FF0418fb"
    dataStr = "EngineSpeedFloat"
    app.logger.debug("Etherios Call")
    
    return dataStr+":"+", ".join(str(x) for x in etherios.updateDeviceList())
    return dataStr+":"+", ".join(str(x) for x in etherios.getDataStreamPoints(deviceID,dataStr))
    '''