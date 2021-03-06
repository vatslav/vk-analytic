# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect,request
from app import app
from app.forms import LoginForm
from app.core import vk_analytic
reporter = vk_analytic.simpleRunner()
import urllib
#@app.route('/')
#@app.route('/index')
#def index():
#    user = { 'nickname': 'Miguel' }
#    posts = [
#        {
#            'author': { 'nickname': 'John' },
#            'body': 'Beautiful day in Portland!'
#        },
#        {
#            'author': { 'nickname': 'Susan' },
#            'body': 'The Avengers movie was so cool!'
#        }
#    ]
#    return render_template("index.html",
#        title = 'Home',
#        user = user,
#        posts = posts)

@app.route(u'/index',methods=[u'GET',u'POST'])
@app.route(u'/',methods=[u'GET',u'POST'])
def main():
    form = LoginForm()
    #if form.validate_on_submit():
    #    flash('Login requeted for OpenId= %s , remember_me = %s '%( \
    #        form.openid.data,str(form.remember_me.data)))
    #    return redirect('/index')
    report =u'a'
    report = reporter.report(5859210)
    #a = str(vk_analytic.researcheOneMan(5859210))

    return  render_template(u'main.html',
                            title=u'Дипломный проект',
                            form = form,
                            report = report,
                            providers = app.config[u'OPENID_PROVIDERS'])

@app.route(u'/login/',methods=[u'GET',u'POST'])
def loginn():
    form = LoginForm()
    if form.validate_on_submit():
        flash(u'Login requeted for OpenId= %s , remember_me = %s '%( \
            form.openid.data,unicode(form.remember_me.data)))
        return redirect(u'/index')

    return  render_template(u'login.html',
                            title=u'Sign In',
                            form = form,
                            providers = app.config[u'OPENID_PROVIDERS'])
@app.route(u'/auth/')
def auth():
    appid = unicode(4365397)
    secret = vk_analytic.getCredent(u'app/core/credentials.txt')
    url = u'vk-analisys.com/auth'
    #print('1 %s' % request.method)
    #print('2 %s' %str(request.args.get('code')))
    #print('1 %s' %str(request.query_string))
    #dangder!

    code = request.args.get(u'code')
    if code is not None:
        req = u'https://oauth.vk.com/access_token?client_id=%s&client_secret=%s&code=%s&redirect_uri=%s' % (appid,secret,code,url)
        urllib2.urlopen(req)
        
    return u'auth'


