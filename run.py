#!flask/bin/python
from werkzeug.wrappers import Request, Response
from app import analisys
import sys

#app.config.from_object('config')
analisys.run(sys.argv)