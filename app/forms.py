__author__ = u'django'
from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import  Required

class LoginForm(Form):
    openid = TextField(u'openid',validators=[Required()])
    remember_me = BooleanField(u'remember_me',default=False)
