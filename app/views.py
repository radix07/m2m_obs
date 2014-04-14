import os
from flask import render_template, flash, session, request, g, jsonify
from flask import Flask,abort, redirect, url_for
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.sqlalchemy import SQLAlchemy
from functools import wraps
from datetime import datetime,timedelta

from app import app, db, lm

from models import User, ROLE_USER, ROLE_ADMIN
from forms import LoginForm
from random import choice
import time
import etheriosmanager
import datamanager

app.permanent_session_lifetime = timedelta(minutes=30)

if not os.environ.get('DATABASE_URL') is None:
    localFrontEnd = 0
else:
    localFrontEnd = 1


basedir = os.path.abspath(os.path.dirname(__file__))

#need to skip this init if migrating database...
etherios = etheriosmanager.etheriosData()

@lm.user_loader
def load_user(id):    
    return etherios.ethUser
    #return User.query.get(int(id))

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
        registered_user = etherios.tryLogin(form.openid.data,form.password.data)
        #registered_user = User.query.filter_by(username=form.openid.data,password=form.password.data).first()
        if registered_user is None:        
            flash('Username or Password is invalid' , 'error')
            return redirect(url_for('login'))
        
        #add if new user/
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
def index_page():
    app.logger.debug(etherios.deviceListInfo)
    return render_template('index.html',user= 'Ryan',
                           devList=etherios.deviceListInfo,
                           eventData=datamanager.getAllEventOccurances(),
                           local=localFrontEnd,
                           datatable=1)

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
def testPage():
    #app.logger.debug(datamanager.getAllEventOccurances())
    #events = datamanager.getAllEventOccurances()
    #for e in events:
        #print e.datapoint,e.timeStamp
    #etherios.getNewDevices()
    #etherios.getNewStreams()
    
    #etherios.getRecentDataPoints()
    #datamanager.normalizeDataStreamRecords()
    #datamanager.normalizeDataPointRecords()
    etherios.updateStreamListDataPoints()
                                              
    #datamanager.getMostRecentTSDataPoint("00080003-00000000-030001F1-E056EE95","Hours")
    
    #app.logger.debug(etherios.updateLatestStreamValues())    
    #app.logger.debug(etherios.updateStreamListDataPoints())
    #return render_template(temp)
    return redirect('index')

@app.route('/controllers.html')
@login_required
def controllers():
    return render_template('controllers.html',user= 'Ryan',devList=etherios.deviceListInfo,datatable=1)

@app.route('/controller/<deviceID>/<streamID>')
@login_required
def dataPointView(deviceID,streamID):
    streamList = datamanager.getAllDatapoints(deviceID,streamID)    
    for st in streamList:
        st.timeStamp = str(time.strftime('%B %d, %Y %H:%M:%S', time.localtime((float(st.timeStamp)/1000))))

    return render_template('dataPointList.html',   #dataPoint
                           user= 'Ryan',
                           streamList=streamList,
                           devID = deviceID,
                           stID = streamID,
                           eventData=datamanager.getAllEventOccurances(),
                           datatable=1)


@app.route('/controller/<deviceID>')
@login_required
def controller(deviceID):
    #get all data from db with deviceID
    streamList = datamanager.getStreamListByDeviceID(deviceID)
    for st in streamList:
        print st.timeStamp
        st.timeStamp = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime((float(st.timeStamp)/1000))))

    #app.logger.debug(streamList)
    return render_template('device.html',
                           user= 'Ryan',
                           streamList=streamList,
                           devID = deviceID,
                           eventData=datamanager.getAllEventOccurances(),
                           datatable=1)


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


if __name__ == '__main__':
    print "VIEW IS MAIN"
    port = int(os.environ.get('PORT', 5000))
    if port == 5000:
        app.debug = True
    app.run(host='0.0.0.0', port=port)
