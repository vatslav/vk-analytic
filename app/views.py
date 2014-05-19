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

@app.route('/index',methods=['GET','POST'])
@app.route('/',methods=['GET','POST'])
def main():
    form = LoginForm()
    #if form.validate_on_submit():
    #    flash('Login requeted for OpenId= %s , remember_me = %s '%( \
    #        form.openid.data,str(form.remember_me.data)))
    #    return redirect('/index')
    report ='a'
    report = reporter.report(5859210)
    #a = str(vk_analytic.researcheOneMan(5859210))

    return  render_template('main.html',
                            title='Дипломный проект',
                            form = form,
                            report = report,
                            providers = app.config['OPENID_PROVIDERS'])

@app.route('/login/',methods=['GET','POST'])
def loginn():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requeted for OpenId= %s , remember_me = %s '%( \
            form.openid.data,str(form.remember_me.data)))
        return redirect('/index')

    return  render_template('login.html',
                            title='Sign In',
                            form = form,
                            providers = app.config['OPENID_PROVIDERS'])
@app.route('/auth/')
def auth():
    appid = str(4365397)
    secret = ''
    url = 'vk-analisys.com/auth'
    #print('1 %s' % request.method)
    #print('2 %s' %str(request.args.get('code')))
    #print('1 %s' %str(request.query_string))
    #dangder!
    code = request.args.get('code')
    req = 'https://oauth.vk.com/access_token?client_id=%s&client_secret=%s&code=%s&redirect_uri=%s' % (appid,secret,code,url)
    return request.args.get('code')


