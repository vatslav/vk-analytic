#!flask/bin/python
from werkzeug.wrappers import Request, Response
from app import app
import sys

app.config.from_object('config')
if len(sys.argv)>1:
    app.run(host='0.0.0.0')
else:
    app.run(host='127.0.0.1', debug=True)
