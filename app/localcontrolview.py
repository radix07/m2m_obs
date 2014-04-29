import os
import datetime
from flask import Blueprint,redirect
from flask import render_template, flash, session, request, g, jsonify
from forms import LocalControllerForm

import jinja2
env = jinja2.Environment()
env.globals.update(zip=zip)

local_api = Blueprint('local_api', __name__)
rpc =0
forceDB = 1

if os.environ.get('DATABASE_URL') is None:
    localFrontEnd = 1
    import rpcServer
    import webbrowser
    new = 2
    url = "http://127.0.0.1:5000"
    webbrowser.open(url,new=new)
def resetLocalControlInterface():
    global rpc
    global forceDB
    rpc =0
    forceDB = 1

@local_api.route("/local",methods = ['GET', 'POST'])
def enterControllerLocation():
    global rpc
    print "Get Local Controller Location Page"
    if isinstance(rpc, int):
        form = LocalControllerForm(request.form)
        if form.validate_on_submit():            
            xmlIP = form.ipRpcXML.data
            print xmlIP
            rpc = rpcServer.xmlServerProc("http://"+xmlIP+":8077/")
            print xmlIP
            return redirect('/local/Dash.html')
        resetLocalControlInterface()
        return render_template('local_device/enterLocalAddress.html',user= 'Ryan',form = form)
    else:
        return redirect('/local/Dash.html')

@local_api.route("/local/logout")
def logoutLocalDevice():
    resetLocalControlInterface()
    return redirect('/local/Dash.html')

@local_api.route("/local/Dash.html")
def controlDash():
    print "Local Dash"
    if isinstance(rpc, int):
        return redirect('/local')

    systemStatus = rpc.getStatus()
    liveStreams,recordData = rpc.getLiveStreams()

    if not systemStatus:
        resetLocalControlInterface()
        return render_template('local_device/localControllerError.html',user= 'Local')
    else:
        #str(datetime.timedelta(seconds=666))
        systemStatus["StoreTimeLeft"] = str(datetime.timedelta(seconds=systemStatus["StoreTimeLeft"]))
        systemStatus["ExportTimeLeft"]= str(datetime.timedelta(seconds=systemStatus["ExportTimeLeft"]))

        #print sorted(systemStatus, key=systemStatus.get)
        return render_template('local_device/localDash.html',user= 'Local',
                               status = systemStatus,
                               streams = liveStreams,
                               records = recordData[1],
                               timestamp = recordData[0][0],
                               location = recordData[0][1])

@local_api.route("/local/datatable.html")
def controlDataTable():
    global rpc
    global forceDB
    print "Local DataTable"
    if isinstance(rpc, int):
        return redirect('/local')

    db = rpc.getDatabase(force=forceDB)
    if not db:
        resetLocalControlInterface()
        return render_template('local_device/localControllerError.html',user= 'Ryan')
    else:
        forceDB = 0
        return render_template('local_device/localDataTable.html',user= 'Ryan',db=db,datatable=1)

@local_api.route("/local/settings")
@local_api.route("/local/Settings.html")
def settings():
    try:
        set = rpc.getSettings()
        return render_template('local_device/settings.html',user= 'Ryan',settings=set)
    except Exception, e:
        print e
        resetLocalControlInterface()
        return render_template('local_device/localControllerError.html',user= 'Ryan')

@local_api.route("/local/settings/<subSet>")
def subSettings(subSet):
    try:
        set = rpc.getSettings()
        return render_template('local_device/settings.html',user= 'Ryan',settings=set[subSet])
    except Exception, e:
        print e
        resetLocalControlInterface()
        return render_template('local_device/localControllerError.html',user= 'Ryan')
