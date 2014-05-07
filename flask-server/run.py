#!flask/bin/python
from app import app
app.config.from_object('config')
app.run(debug = True)
