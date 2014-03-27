import os
from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask import Flask,render_template,abort, redirect, url_for

from flask.ext.login import login_user, logout_user, current_user, login_required
from functools import wraps
from flask import g, request, redirect, url_for

from flask.ext.sqlalchemy import SQLAlchemy
from forms import LoginForm
from models import User, ROLE_USER, ROLE_ADMIN
from random import choice
import time
from datetime import datetime
import datamanager
import etheriosmanager
from app import app, db, lm
import datamanager


if os.environ.get('DATABASE_URL') is None:
    localFrontEnd = 1
    import rpcServer
    rpc = rpcServer.xmlServerProc()
    import webbrowser
    new = 2
    url = "http://127.0.0.1:5000"
    webbrowser.open(url,new=new)
else:
    localFrontEnd = 0

basedir = os.path.abspath(os.path.dirname(__file__))
etherios = etheriosmanager.etheriosData()

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

@app.route('/login',methods = ['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm(request.form)

    if form.validate_on_submit():
        registered_user = User.query.filter_by(username=form.openid.data,password=form.password.data).first()
        if registered_user is None:
            flash('Username or Password is invalid' , 'error')
            return redirect(url_for('login'))
        login_user(registered_user, remember = form.remember_me.data)
        return redirect('/index')

    return render_template('login.html', 
        title = 'Sign In',
        form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('index')


@app.route('/index.html')
@app.route('/index')
@app.route('/')
@login_required
def raw_index():
    app.logger.debug(etherios.deviceListInfo)
    return render_template('index.html',user= 'Ryan',devList=etherios.deviceListInfo,local=localFrontEnd)

@app.route('/clean')
@login_required
def cleanDB():
    etherios.initFromDB()
    datamanager.removeAllDevices()
    return render_template('index.html',user= 'Ryan',devList=etherios.deviceListInfo)

@app.route('/force')
@login_required
def forceUpdate():
    etherios.initFromDB()
    return render_template('index.html',user= 'Ryan',devList=etherios.deviceListInfo)

@app.route('/test.html')
@login_required
def testPage():
    print "TEST"
    app.logger.debug(etherios.updateDeviceList())
    #app.logger.debug(etherios.updateLatestStreamValues())    
    #app.logger.debug(etherios.updateStreamListDataPoints())
    #return render_template(temp)
    return render_template('login.html')


@app.route('/controllers.html')
@login_required
def controllers():
    return render_template('controllers.html',user= 'Ryan',devList=etherios.deviceListInfo)

@app.route('/controller/<deviceID>/<streamID>')
@login_required
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
@login_required
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
@login_required
def flot():
    app.logger.debug("float")
    salutation = choice(testStringData)
    return render_template('flot.html', salutation=testStringData[0])

@app.route('/tables.html')
@login_required
def tablesTest():
    app.logger.debug("float")
    salutation = choice(testStringData)
    return render_template('tables.html', salutation=testStringData[0])


##########################LocalControlViews############################
@app.route('/localDash.html')
@login_required
def localController():
    #seperate base template
    db = rpc.getDatabase()

    return render_template('localDash.html',user= 'Ryan',db=db,datatable=1)
#onInit
    #getSettings
    #getDatabase

#getMenuDirectorData()
    #request all menus
#getChartData()
    #request all data
#build plot window
#plotDataItem
    #return plot window with JS
#_getNewPlotPoints
    #return JSONify of data points
#displaySettings()

#get/build local database?



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