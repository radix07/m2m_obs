import os
from flask import Flask,render_template,abort, redirect, url_for
from random import choice
import psycopg2
from flask.ext.sqlalchemy import SQLAlchemy
import datamanager
import etheriosmanager

#app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

try:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
except:
    print "local dev"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    

db = SQLAlchemy(app)
db.create_all()
@app.route('/')
def raw_index():
    app.logger.debug("raw index")
    return redirect(url_for('index'))

@app.route('/testEtherios.xml')
def etherios():
    app.logger.debug("Etherios Call")
    return etheriosmanager.getDataStream()

@app.route('/index.html')
def index():
    app.logger.debug("index")
    salutation = choice(testStringData)
    return render_template('index.html', salutation=testStringData, resp="TEST")

@app.route('/flot.html')
def flot():
    app.logger.debug("float")
    salutation = choice(testStringData)
    return render_template('flot.html', salutation=testStringData)

testStringData = [
    'TEST PG SICOM',]


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    if port == 5000:
        app.debug = True

    app.run(host='0.0.0.0', port=port)
