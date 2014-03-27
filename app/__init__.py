import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

#from flask.ext.openid import OpenID
from config import basedir


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

#lm.login_message = lazy_gettext('Please log in to access this page.')
#oid = OpenID(app, os.path.join(basedir, 'tmp'))

try:
    #app.config['SQLALCHEMY_DATABASE_URI'] = 
    os.environ['DATABASE_URL']
    
except:
    print "local dev"

    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    #SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

if not app.debug and os.environ.get('HEROKU') is None:
    import logging
    from logging.handlers import RotatingFileHandler
    if not os.path.exists("tmp/microblog.log"):
        os.makedirs("tmp/")
    file_handler = RotatingFileHandler('tmp/microblog.log', 'a+', 1 * 1024 * 1024, 10)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('microblog startup')

if os.environ.get('HEROKU') is not None:
    import logging
    stream_handler = logging.StreamHandler()
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('system startup')


from app import views, models 