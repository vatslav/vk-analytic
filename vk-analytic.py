#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'salamander'

import vk_auth
import vkontakte

def getCredent(file):
    '''
    @type param: file
    '''
    f = open(file,'r')
    return [lines.strip() for lines in f]



def main():
    login, pas, appid, appkey = getCredent('credentials.txt')

    (token,user_id) = vk_auth.auth(login, pas, appid, appkey)
    vk = vkontakte.API(token=token)
    print "Hello vk API , server time is ",vk.getServerTime()
    return 0

if __name__ == '__main__':
    pass
    main()