# -*- coding: utf-8 -*-
import cookielib
import urllib2
import urllib
from urlparse import urlparse
from HTMLParser import HTMLParser
#
class FormParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.url = None
        self.params = {}
        self.in_form = False
        self.form_parsed = False
        self.method = u"GET"

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag == u"form":
            if self.form_parsed:
                raise RuntimeError(u"Second form on page")
            if self.in_form:
                raise RuntimeError(u"Already in form")
            self.in_form = True 
        if not self.in_form:
            return
        attrs = dict((name.lower(), value) for name, value in attrs)
        if tag == u"form":
            self.url = attrs[u"action"] 
            if u"method" in attrs:
                self.method = attrs[u"method"]
        elif tag == u"input" and u"type" in attrs and u"name" in attrs:
            if attrs[u"type"] in [u"hidden", u"text", u"password"]:
                self.params[attrs[u"name"]] = attrs[u"value"] if u"value" in attrs else u""

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == u"form":
            if not self.in_form:
                raise RuntimeError(u"Unexpected end of <form>")
            self.in_form = False
            self.form_parsed = True

def auth_user(email, password, client_id, scope, opener):
    response = opener.open(
        u"http://oauth.vk.com/oauth/authorize?" + \
        u"redirect_uri=http://oauth.vk.com/blank.html&response_type=token&" + \
        u"client_id=%s&scope=%s&display=wap" % (client_id, u",".join(scope))
        )
    doc = response.read()
    parser = FormParser()
    parser.feed(doc)
    parser.close()
    if not parser.form_parsed or parser.url is None or u"pass" not in parser.params or \
      u"email" not in parser.params:
          raise RuntimeError(u"Something wrong")
    parser.params[u"email"] = email
    parser.params[u"pass"] = password
    if parser.method == u"post":
        response = opener.open(parser.url, urllib.urlencode(parser.params))
    else:
        raise NotImplementedError(u"Method '%s'" % parser.method)
    return response.read(), response.geturl()

def give_access(doc, opener):
    parser = FormParser()
    parser.feed(doc)
    parser.close()
    if not parser.form_parsed or parser.url is None:
          raise RuntimeError(u"Something wrong")
    if parser.method == u"post":
        response = opener.open(parser.url, urllib.urlencode(parser.params))
    else:
        raise NotImplementedError(u"Method '%s'" % parser.method)
    return response.geturl()


def auth(email, password, client_id, scope):
    if not isinstance(scope, list):
        scope = [scope]
    opener = urllib2.build_opener(
        urllib2.HTTPCookieProcessor(cookielib.CookieJar()),
        urllib2.HTTPRedirectHandler())
    doc, url = auth_user(email, password, client_id, scope, opener)
    if urlparse(url).path != u"/blank.html":
        # Need to give access to requested scope
        url = give_access(doc, opener)
    if urlparse(url).path != u"/blank.html":
        raise RuntimeError(u"Expected success here "+urlparse(url).path)

    def split_key_value(kv_pair):
        kv = kv_pair.split(u"=")
        return kv[0], kv[1]

    answer = dict(split_key_value(kv_pair) for kv_pair in urlparse(url).fragment.split(u"&"))
    if u"access_token" not in answer or u"user_id" not in answer:
        raise RuntimeError(u"Missing some values in answer")
    return answer[u"access_token"], answer[u"user_id"] 

