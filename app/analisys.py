# -*- coding: utf-8 -*-

import urllib
import json
import sys
import re
from app.core import vk_analytic
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, make_response, Markup
from flask import request
from app.core.vkontakte import VKError
from urllib.error import HTTPError

app = Flask(__name__)
app.config.from_object(__name__)
debug=True

# хранить в конфигурационном файле
# хранить в конфигурационном файле
VK_CODE = {
    "scope":"email,nohttps",
    "client_id":"4365397",
    "redirect_uri":"http://vk-analisys.com/oauth2/vk/code",
    "response_type":"code",
    "v":"5.21"
}

# хранить в конфигурационном файле
VK_TOKEN = {
    "client_id":"4365397",
    "client_secret":"LwIi4TTmzvCUTH4qzpoU",
    "redirect_uri":"http://vk-analisys.com/oauth2/vk/code",
    #"grant_type":"client_credentials" # с этой опцией пользователь авторизуется навсегда
}



def get_url_vk_code(config=VK_CODE):
    u"""
        url на запрос кода (code) для авторизации через OAuth vk.com
    """
    params = urllib.parse.urlencode(config)
    url = "https://oauth.vk.com/authorize?{}".format(params)
    return url


def get_url_vk_token(config=VK_TOKEN, code=""):
    u"""
        url на запрос access_token vk.com
    """
    config.update({"code": code})
    params = urllib.parse.urlencode(config)
    url = "https://oauth.vk.com/access_token?{}".format(params)
    return url




@app.route('/oauth2/vk/code')
def vklogin():
    u"""
        К этому url vk обращается для передачи запросов
        это часть redirect_uri, менять только совместно с изменением в конфиге
    """
    code = request.args.get('code')
    if code:
       return redirect('/oauth2/vk/token?code={}'.format(code))
    return "Success"

@app.route('/secret/')
def secret():
    id = request.args.get('id')
    if id and str(id).isalnum():
        id = int(id)
        try:
            return test(id=id)
        except VKError as e:
            return render_template('report.html',error=str(e.description))
        except HTTPError:
            return render_template('report.html',error='мы записали вас в свои логи...')
    return 404



@app.route('/test/')
def testRoute():
    return test()

@app.route('/test2/')
def testRoute2():
    return test(id=12928646)

def test(id=78340794):#78340794
        userid = id #12928646
        reporter = vk_analytic.simpleRunner()
        report = reporter.report(int(userid))
        report = report.replace('\n','<br>')
        report = Markup(report)
        return  render_template('report.html',report = report)

@app.route('/oauth2/vk/token')
def token():
    code = request.args.get('code')
    if code:
        url = get_url_vk_token(VK_TOKEN, code)
        try:
            req = urllib.request.urlopen(url)

            data = req.read().decode('utf8')
            resp = json.loads(data)

            userid= re.findall('user_id":\d+',data)[0].split(':')[1]
            tok = re.findall('token":"\w+',data)[0].split('"')[2]

            reporter = vk_analytic.simpleRunner(cred=tok)
            report = reporter.report(int(userid))
        except VKError as e:
            return render_template('report.html',error=str(e.description))
        except HTTPError:
            return render_template('report.html',error='Не верный формат code, мы записали вас в свои логи...')
        #except:
        #    return render_template('report.html',error='Вы сделали нечто странное, мы записали вас в свои логи...')

        report = report.replace('\n','<br>')
        report = Markup(report)
        return  render_template('report.html',report = report)
        #if resp and resp.get("access_token", None):
        #
        #
        #
        #    max_age = resp.get("expires_in", None)
        #    response = make_response(redirect('/'))
        #    response.set_cookie('email', resp.get("email", None), max_age=max_age)
        #    response.set_cookie('access_token', resp.get("access_token", None), max_age=max_age)
        #
        #    return response
        #
        #return redirect('/')
    else:
        return render_template('error.html',error = 'Не верный формат code, мы записали вас в свои логи...')

@app.route('/034fcfa2b4acc7c9f08ae55593a5f23b5a17db9b249a546a1cd711b79b0d197f.html')
def yaMeTrica():
    return 'postoffice-034fcfa2b4acc7c9f08ae55593a5f23b5a17db9b249a546a1cd711b79b0d197f'

@app.route('/анализ/')
@app.route('/analisys.html')
@app.route('/analisys/')
def about(text=''):
    vk_login_url=get_url_vk_code(VK_CODE)
    return render_template('analisys.html', vk_login_url=vk_login_url,text=text)
    return render_template('analisys.html')

@app.route('/index.html')
@app.route('/index/')
@app.route('/')
def ind():
    return render_template('index.html', vk_login_url=get_url_vk_code(VK_CODE))


@app.route('/о_проекте/')
@app.route('/blog.html')
@app.route('/blog/')
def blog():
    return render_template('blog.html')

@app.route('/контакты/')
@app.route('/contact.html')
@app.route('/contact/')
def contact():
    return render_template('contact.html')

def run(args):
    global debug
    host='127.0.0.1'
    if len(args)>1:
        host='0.0.0.0'
        debug=False

    app._static_folder= 'templates'
    app.static_url_path=''
    app.run(host=host,debug=debug)


if __name__ == '__main__':
    #host='127.0.0.1'
    #if len(sys.argv)>1:
    #    host='0.0.0.0'
    #    app.run(host=host)
    #    exit(0)
    app.run(host='127.0.0.1',debug=debug)
