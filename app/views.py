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

@app.route('/index.html')
@app.route('/')
def raw_index():
    app.logger.debug("raw index")
    return render_template('index.html',user= 'Ryan')
@app.route('/login')
@app.route('/login.html')
def login():
    return render_template('login.html')
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

@app.route('/maps.html')
def map():
    return render_template('maps.html',user= 'Ryan',)

@app.route('/controller/')
def controller():
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
