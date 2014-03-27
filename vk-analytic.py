#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'salamander'

import vkontakte
from handlers import reader


def getCredent(file):
    '''
    @type param: file
    '''
    f = open(file,'r')
    line =  f.readline().strip()
    f.close()
    return line

def log(cmd):
    flog=open('log1','a')
    flog.writelines(cmd+'\n')
    print(cmd)
    flog.close()

class anyk(object):
    def __init__(self,tok):
        self.vk=vkontakte.API(token=tok)
    def getMutal(self,id1, id2):
        res = self.vk.getMutual(source_uid=id1, target_uid=id2)
        return res




def test1():
    print(vk.getServerTime())
    print(vk.friends.get(fields='uid, first_name, last_name, nickname, sex, bdate',uid='21229916'))

def main():
    #vk = vkontakte.API('4264030', 'TMqwtjQP3D1YXMlKmBva')
    #print (vk.getServerTime())

    vk = vkontakte.API(token=getCredent('credentials.txt'))
    #print "Hello vk API , server time is ",vk.getServerTime()
    #print unicode(vk.users.get(uids=146040808))
    #reader.read(vk.users.get(uids=233945283,fields='sex'))

    print ('input you method')
    while True:
        x = input()
        x = 'vk.%s'%x
        log (x)
        x = eval(x)
        reader.read(x)
    return 0

if __name__ == '__main__':
    while True:
        try:
            main()
        except (SyntaxError, RuntimeError, NameError,vkontakte.api.VKError) as s:
            print (s)
            continue

