import os
from flask import flash, session, request, g
from flask import Flask,render_template,abort, redirect, url_for
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.sqlalchemy import SQLAlchemy
from forms import LoginForm
from models import User, ROLE_USER, ROLE_ADMIN
from random import choice
import datamanager
import etheriosmanager
from app import app, db, lm, oid

basedir = os.path.abspath(os.path.dirname(__file__))

eth = etheriosmanager.etheriosData()
#eth.listDevices()
#eth.getStreamListData()


@app.route('/index.html')
@app.route('/')
def raw_index():
    #app.logger.debug("raw index")
    app.logger.debug(eth.deviceListInfo)
    return render_template('index.html',user= 'Ryan',devList=eth.deviceListInfo)

@app.route('/login')
@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/controllers.html')
def controllers():
    return render_template('controllers.html',user= 'Ryan',devList=eth.deviceListInfo)


@app.route('/controller/<deviceID>')
def controller():
    return render_template('device.html',user= 'Ryan',streamList=eth.streamListInfo,device=deviceID)
    pass

@app.route('/flot.html')
def flot():
    app.logger.debug("float")
    salutation = choice(testStringData)
    return render_template('flot.html', salutation=testStringData[0])

testStringData = [
    'TEST PG SICOM',]


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    if port == 5000:
        app.debug = True

    app.run(host='0.0.0.0', port=port)


    '''
@app.route('/getEtheriosStreams.xml')
def etheriosStreams():
    app.logger.debug("Etherios Call")
    return ", ".join(str(x) for x in eth.getStreamListData())


@app.route('/getEtheriosEnginePoints.xml')
def etheriosPoints():
    deviceID = "pythonPC1_Ryan" #"0000000-00000000-00042dFF-FF0418fb"
    dataStr = "EngineSpeedFloat"
    app.logger.debug("Etherios Call")
    
    return dataStr+":"+", ".join(str(x) for x in eth.listDevices())
    return dataStr+":"+", ".join(str(x) for x in eth.getDataStream(deviceID,dataStr))
    '''