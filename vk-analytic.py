#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'salamander'

import vk_auth
import vkontakte
from handlers import reader

def getCredent(file):
    '''
    @type param: file
    '''
    f = open(file,'r')
    return [lines.strip() for lines in f]
def razor(req):
    '''
    @rtype: dict
    '''
    return req[0]


def main():
    login, pas, appid, appkey = getCredent('credentials.txt')

    (token,user_id) = vk_auth.auth(login, pas, appid, appkey)
    vk = vkontakte.API(token=token)
    #print "Hello vk API , server time is ",vk.getServerTime()
    #print unicode(vk.users.get(uids=146040808))
    reader.read(vk.users.get(uids=233945283,fields='sex'))
    print 'input you method'
    while True:
        x = raw_input()
        x = 'vk.%s'%x

        x = eval(x)
        reader.read(x)
    return 0

if __name__ == '__main__':
    while True:
        try:
            main()
        except (SyntaxError, RuntimeError) as s:
            print s
            continue