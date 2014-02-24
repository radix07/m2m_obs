from flask import Flask,render_template,abort, redirect, url_for
import os
from random import choice
import httplib
import base64
import psycopg2
import urlparse

username = "pgSatterlee" # enter your username
password = "Pgecs-2322" # enter your password



#Datbase information for Heroku postgres
#username: leqslquceprcjb
#password: bTO0DubrLXbT7fdVjIf-c-nDvI
#port: 5432
#database: d9rfmhttltdj9c
#host: ec2-54-197-227-238.compute-1.amazonaws.com
#postgres://leqslquceprcjb:bTO0DubrLXbT7fdVjIf-c-nDvI@ec2-54-197-227-238.compute-1.amazonaws.com:5432/d9rfmhttltdj9c

app = Flask(__name__)
try:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
except:
    print "local dev"
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgres://test.db')

##Postgres
'''
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])
conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
'''
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


@app.route('/')
def raw_index():
    app.logger.debug("raw index")
    return redirect(url_for('index'))

@app.route('/testEtherios.xml')
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
    #salutation = choice(salutations)
    return render_template('index.html', salutation=testStringData, resp="TEST")

@app.route('/flot.html')
def flot():
    app.logger.debug("float")
    salutation = choice(salutations)
    return render_template('flot.html', salutation=testStringData)

testStringData = [
    'TEST PG SICOM',]


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    if port == 5000:
        app.debug = True

    app.run(host='0.0.0.0', port=port)
