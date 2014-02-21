from flask import Flask
from flask import render_template
from flask import abort, redirect, url_for
import os
from random import choice
import httplib
import base64

username = "pgSatterlee" # enter your username
password = "Pgecs-2322" # enter your password 


app = Flask(__name__)

@app.route('/')
def raw_index():
    app.logger.debug("raw index")
    return redirect(url_for('index'))

@app.route('/testEtherios')
def etherios():
    auth = base64.encodestring("%s:%s"%(username,password))[:-1]
    webservice = httplib.HTTP("login.etherios.com",80)
    webservice.putrequest("GET", "/ws/DataPoint/0000000-00000000-00042dFF-FF0418fb/EngineSpeedFloat")
    webservice.putheader("Authorization", "Basic %s"%auth)
    webservice.putheader("Content-type", "text/xml; charset=\"UTF-8\"")
    webservice.endheaders()
    statuscode, statusmessage, header = webservice.getreply()
    response_body = webservice.getfile().read()
    return response_body

@app.route('/index.html')
def index():
    app.logger.debug("index")
    salutation = choice(salutations)
    return render_template('index.html', salutation=salutation, resp="TEST")

@app.route('/flot.html')
def flot():
    app.logger.debug("float")
    salutation = choice(salutations)
    return render_template('flot.html', salutation=salutation)

salutations = [
    'TEST PG SICOM',]


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    if port == 5000:
        app.debug = True

    app.run(host='0.0.0.0', port=port)
