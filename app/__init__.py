import os
from flask import Flask, Blueprint
from flask.ext.sqlalchemy import SQLAlchemy

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from flask.ext.login import LoginManager
from momentjs import momentjs
from config import basedir

app = Flask(__name__)


app.config.from_object('config')
db = SQLAlchemy(app)


migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


try:
    os.environ['DATABASE_URL']
except:
    from localcontrolview import local_api
    print "local dev"
    app.register_blueprint(local_api)


lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'


#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
#SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

if not app.debug and os.environ.get('HEROKU') is None:  #release
    import logging
    from logging.handlers import RotatingFileHandler
    from logging.handlers import SMTPHandler
    try:
        if not os.path.exists("tmp/log.log"):
            os.makedirs("tmp/")
    except:
        pass
    file_handler = RotatingFileHandler('tmp/log.log', 'a+', 1 * 1024 * 1024, 10)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('microblog startup')

if os.environ.get('HEROKU') is not None:        #heroku
    import logging
    stream_handler = logging.StreamHandler()
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('system startup')

app.jinja_env.globals['momentjs'] = momentjs
app.jinja_env.add_extension('jinja2.ext.do')

from app import views, models 
