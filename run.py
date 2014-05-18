#!flask/bin/python
from werkzeug.wrappers import Request, Response
from app import app
#
app.config.from_object('config')
app.run(host='0.0.0.0')
