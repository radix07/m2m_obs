import os
from flask import render_template, flash, session, request, g, jsonify
from flask import Flask,abort, redirect, url_for
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.sqlalchemy import SQLAlchemy
from functools import wraps
from datetime import datetime,timedelta
from app import app, db, lm
from models import User, ROLE_USER, ROLE_ADMIN
from forms import LoginForm,pecosConfigForm
from random import choice
import time
import etheriosmanager
import datamanager
import string
import math
app.permanent_session_lifetime = timedelta(minutes=30)
app.last_time = 0
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
        print "USER",registered_user
        if registered_user == "Invalid Key":
            flash('Valid Login, Invalid Dash/Cloud Key' , 'error')
            return redirect(url_for('login'))
        elif registered_user is None:
            flash('Username or Password is invalid' , 'error')
            return redirect(url_for('login'))

        #add if new user/
        login_user(registered_user, remember = form.remember_me.data)
        flash('You were successfully logged in')
        return redirect('/index')

    return render_template('login.html',
                            title = 'Sign In',
                            form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    #if localFrontEnd:
    flash("User logged out")
    return redirect('index')


@app.route('/index.html')
@app.route('/index')
@app.route('/')
@login_required
def index_page():
    if etherios.updateDeviceList() is None:
        flash("Bad Credentials",'message')
        redirect('/logout')

    ed = datamanager.getAllEventOccurances()
    #for e in ed:
        #print e.devID,e.streamID,e.datapoint,e.timeStamp

    return render_template('index.html',user= g.user.get_username(),
                           devList=etherios.deviceListInfo,
                           eventData=ed,
                           local=localFrontEnd,
                           datatable=1)
@app.route('/clean')
@login_required
def cleanDB():
    flash('Clean Database Run')
    etherios.initFromDB()
    datamanager.removeAllDevices()
    return render_template('index.html',user= g.user.get_username(),devList=etherios.deviceListInfo)

@app.route('/force')
@login_required
def forceUpdate():
    etherios.initFromDB()
    return render_template('index.html',user= g.user.get_username(),devList=etherios.deviceListInfo)

@app.route('/controllers.html')
@login_required
def controllers():
    return render_template('controllers.html',user= g.user.get_username(),
                           devList=etherios.deviceListInfo,
                           eventData=datamanager.getAllEventOccurances(),
                           datatable=1)
@app.route('/details/<deviceID>')
@login_required
def controllersDetail(deviceID):    
    detailListing=[]    
    resp = etherios.deviceCLIRequest(deviceID,"pycfg scripts")
    #print resp
    if "Invalid target" in resp:        #if device is connected
        detailListing.append("Device Not Found")
    else:
        resp = string.split(resp, '\n')
        for i in resp:
            if "Uptime" in i:
                detailListing.append( string.split(i, ':') )
                break
        resp = etherios.deviceCLIRequest(deviceID,"pycfg mem")
        resp = string.split(resp, '\n')
        for i in resp:
            if "heap left" in i:
                detailListing.append( string.split(i, ':') )            
                break
    #etherios parse set1 file
    #get 
    return render_template('controlDetails.html',user= g.user.get_username(),                           
                           deviceID=deviceID,
                           devDetailList = detailListing,                     
                           datatable=1)

@app.route('/controller/<deviceID>/configuration',methods = ['GET', 'POST'])
@login_required
def deviceConfigView(deviceID):
    if request.method == 'POST':
        if request.form['submit'] == 'Submit Battery Charge':
            if form.validate_on_submit():
                print "Form Response:"  #package data items
                stringConfig = str(form.item0.label.text)+","+str(form.item0.data)+"\n"+\
                                str(form.item1.label.text)+","+str(form.item1.data)
                print stringConfig
                etherios.sendFile(stringConfig,deviceID+"/config.txt")  #send to (deviceID group)/config
                #emit RCI request
                flash('PECoS Configuration Sent')
                #spawn process to wait/poll for update verify?
                    #notify user of update with flash message
        elif request.form['submit'] == 'Submit Device Settings':
            print "Form Response:"

        elif request.form['submit'] == 'TestButton':
            print "Test Button Pressed" 
            curr_time = int(time.time())        #put blocking timer to prevent over sending/running etherios/device
            if curr_time - app.last_time > 30:
                app.last_time = curr_time
                flash(etherios.RCIRequest(deviceID,"START"))
            else:
                flash("request already sent...")

    form = pecosConfigForm(request.form)    
    return render_template('deviceConfiguration.html',   #dataPoint
                           user= g.user.get_username(),
                           devID = deviceID,
                           form = form,
                           datatable=1)

@app.route('/controller/<deviceID>/<streamID>')
@login_required
def dataPointView(deviceID,streamID):
    #dataPointList = datamanager.getAllDatapointsByID(deviceID,streamID)
    dataPointList = datamanager.getAllDatapointsByIDRaw(str(deviceID),streamID)
    count=0
    list =[]
    for st in dataPointList:
        #st.timeStamp = str(time.strftime('%B %d, %Y %H:%M:%S', time.localtime(float(st[0])/1000)))
        #list.append([str(time.strftime('%B %d, %Y %H:%M:%S', time.localtime(float(st[0])/1000))),st[1]])
        list.append([st[0],st[1]])
        count+=1        
    max =750    
    decimateInterval = int(math.ceil(count//max))    
    #dataPointList = dataPointList[1::decimateInterval] 
    list = list[1::decimateInterval] 

    streamList = datamanager.getStreamListByDeviceID(deviceID)

    return render_template('dataPointList.html',   #dataPoint
                           user= g.user.get_username(),
                           dataPointList=list,
                           streamList=streamList,
                           devID = deviceID,
                           stID = streamID,
                           eventData=datamanager.getAllEventOccurances(),
                           datatable=1)

@app.route('/controller/<deviceID>')
@login_required
def controller(deviceID):
    #get config list from database
    #get all data from db with deviceID
    streamList = datamanager.getStreamListByDeviceID(deviceID)

    return render_template('device.html',
                           user= g.user.get_username(),
                           streamList=streamList,
                           devID = deviceID,
                           eventData=datamanager.getAllEventOccurances(devID=deviceID),
                           datatable=1,
                           )
@app.route('/t')
def highChartTestPage():
    dataPointList=[]
    #get max length
    maxPoints =350
    x=120
    x=5
    dID = "00000000-00000000-00042DFF-FF051018"   
    stList = datamanager.getStreamListByDeviceID(dID)

    #return render_template('highchart.htm')
    return render_template('highchart.htm',devID = dID,streamList=stList)

########################TEST/UTILITY
@app.route('/test.html')
def testPage():
    dID = "00000000-00000000-00042DFF-FF051018"
    stList = datamanager.getStreamListByDeviceID(dID)
    '''
    if stList.count():
        recordCount = len(datamanager.getAllDatapointsByID(dID,stList[0].streamID))
        decimateCount = int(round(recordCount/maxPoints))
        print "DecInterval:",decimateCount,"  Record Count:",recordCount
        for stream in stList:        
            temp = datamanager.getAllDatapointsByID(dID,stream.streamID)[1::decimateCount]
            if len(temp) > 0 and stream.streamID != "EventList":
                print stream.streamID
                dataPointList.append(temp)
            else:
                print "No Data:",stream.streamID
                '''
    return render_template('flot-demo.html',devID = dID,streamList=stList)
    

@app.route('/ctest.html')
def chartTest():
    dID = "00000000-00000000-00042DFF-FF051018"
    stList = datamanager.getStreamListByDeviceID(dID)
    chartCount=0
    for i in stList:
        chartCount+=1
    return render_template('chartTester.html',devID=dID,streamList=stList,chartCount=chartCount)


@app.route('/get_data/<devID>/<streamIndex>')
def get_data(devID,streamIndex):
    print "Get_Data",devID,streamIndex
    #need date filter...
    stList = datamanager.getStreamListByDeviceID(devID)
    datapoints = datamanager.getAllDatapointsByIDRaw(str(devID),stList[int(streamIndex)].streamID)

    list=[]
    count=0
    for i in datapoints:
        #list.append([i[0],i[1]])
        list.append([i[0],float(i[1])])
        count+=1

    max =750    
    decimateInterval = int(math.ceil(count//max))
    list = list[1::decimateInterval]

    return jsonify(label =stList[int(streamIndex)].streamID , data=list)

@app.route('/get_data_highchart/<devID>/<streamIndex>')
def get_data_highchart(devID,streamIndex):
    print "Get_Data_Highcharts",devID,streamIndex
    #need date filter...
    stList = datamanager.getStreamListByDeviceID(devID)
    datapoints = datamanager.getAllDatapointsByIDRaw(str(devID),stList[int(streamIndex)].streamID)

    list=[]
    count=0
    for i in datapoints:
        list.append([i[0],float(i[1])])
        count+=1
    
    max =750    
    decimateInterval = int(math.ceil(count//max))
    list = list[1::decimateInterval]
    print "List Items:",len(list), "\t",list[0] 
    return jsonify(data=list)


@app.route('/get_data')
def test_get_data():
    print ":TEST"
    return '''{"cols": [
                    {"id":"","label":"Topping","pattern":"","type":"string"},
                    {"id":"","label":"Slices","pattern":"","type":"number"}
                  ],
              "rows": [
                    {"c":[{"v":"Mushrooms","f":null},{"v":3,"f":null}]},
                    {"c":[{"v":"Onions","f":null},{"v":1,"f":null}]},
                    {"c":[{"v":"Olives","f":null},{"v":1,"f":null}]},
                    {"c":[{"v":"Zucchini","f":null},{"v":1,"f":null}]},
                    {"c":[{"v":"Pepperoni","f":null},{"v":2,"f":null}]}
                  ]
            }'''

if __name__ == '__main__':
    print "VIEW IS MAIN"
    port = int(os.environ.get('PORT', 5000))
    if port == 5000:
        app.debug = True
    app.run(host='0.0.0.0', port=port)
