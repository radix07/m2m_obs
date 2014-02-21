from flask import Flask
from flask import render_template
from flask import abort, redirect, url_for
import os
from random import choice


app = Flask(__name__)

@app.route('/')
def raw_index():
    app.logger.debug("raw index")
    return redirect(url_for('index'))

@app.route('/index.html')
def index():
    app.logger.debug("index")
    salutation = choice(salutations)
    return render_template('index.html', salutation=salutation)

@app.route('/flot.html')
def flot():
    app.logger.debug("chart")
    salutation = choice(salutations)
    return render_template('flot.html', salutation=salutation)

salutations = [
    'TEST PG SICOM',]


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    if port == 5000:
        app.debug = True

    app.run(host='0.0.0.0', port=port)
