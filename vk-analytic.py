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
    allUserFields='sex, bdate, city, country, photo_50, photo_100, photo_200_orig, photo_200, photo_400_orig, photo_max, photo_max_orig, online, online_mobile, lists, domain, has_mobile, contacts, connections, site, education, universities, schools, can_post, can_see_all_posts, can_see_audio, can_write_private_message, status, last_seen, common_count, relation, relatives, counters'
    t1 = 'friends.getMutual(source_uid=78340794, target_uid=11538362)'
    def __init__(self,tok):
        self.vk=vkontakte.API(token=tok)
    def getMutal(self,id1, id2):
        res = self.vk.getMutual(source_uid=id1, target_uid=id2)
        return res
    def usersGet(self,ids):
        info = []
        self.vk.users.get(user_ids=ids, fields=self.allUserFields)
    def eval(self,cmd):
        return eval('self.vk.%s'%cmd)




def test1():
    print(vk.getServerTime())
    print(vk.friends.get(fields='uid, first_name, last_name, nickname, sex, bdate',uid='21229916'))

def main():
    #vk = vkontakte.API('4264030', 'TMqwtjQP3D1YXMlKmBva')
    #print (vk.getServerTime())
    vk = anyk(getCredent('credentials.txt'))
    #vk = vkontakte.API(token=getCredent('credentials.txt'))
    #print "Hello vk API , server time is ",vk.getServerTime()
    #print unicode(vk.users.get(uids=146040808))
    #reader.read(vk.users.get(uids=233945283,fields='sex'))
    t = vk.usersGet(vk.eval(vk.t1))
    print(t)
    print ('input you method')
    while True:
        x = input()
        log (x)
        x = vk.eval(x)
        print(x)
    return 0

if __name__ == '__main__':
    while True:
        try:
            main()
        except (SyntaxError, RuntimeError, NameError,vkontakte.api.VKError) as s:
            print (s)
            continue

