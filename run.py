#!flask/bin/python
from app import app
#app.run(debug = False)
app.run(host='0.0.0.0',debug = True)
