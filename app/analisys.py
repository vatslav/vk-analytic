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


@app.route('/')
def main():
    access_token = request.cookies.get('access_token')
    email = request.cookies.get('email')
    if not access_token:
        if debug:
            vk_login_url=get_url_vk_code(VK_CODE)
        else:
            vk_login_url='http://www.bit.ly/1oOBPkI'
        return render_template('login.html', vk_login_url=vk_login_url)
    else:
        return render_template('main.html', email=email)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error, social_url=get_url_vk_code(VK_CODE))


@app.route('/logout')
def logout():
    response = make_response(redirect('/?logout'))
    response.set_cookie('email', '', expires=0)
    response.set_cookie('access_token', '', expires=0)
    return response


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

@app.route('/test/')
def test():#78340794
        userid = 78340794
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
            return render_template('error.html',error=str(e.code))
        except HTTPError:
            return render_template('error.html',error='Не верный формат code, мы записали вас в свои логи...')
        except:
            return render_template('error.html',error='Вы сделали нечто странное, мы записали вас в свои логи...')

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

def run(args):
    global debug
    host='127.0.0.1'
    if len(args)>1:
        host='0.0.0.0'
        debug=False

    app.run(host=host,debug=debug)


if __name__ == '__main__':
    #host='127.0.0.1'
    #if len(sys.argv)>1:
    #    host='0.0.0.0'
    #    app.run(host=host)
    #    exit(0)
    app.run(host='127.0.0.1',debug=debug)
