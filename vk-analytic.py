#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'salamander'
#взять средие(лушче медиану) от друзей пользователя по городу, возрасту и ВУЗу
import vkontakte
from pprint import pprint
from os.path import exists, isfile

from handlers import logger


def getCredent(file):
    '''
    @type param: file
    '''
    f = open(file,'r')
    line =  f.readline().strip()
    f.close()
    return line




class anyk(object):
    __allUserFields='sex, bdate, city, country, photo_50, photo_100, photo_200_orig, photo_200, photo_400_orig, photo_max, photo_max_orig, online, online_mobile, lists, domain, has_mobile, contacts, connections, site, education, universities, schools, can_post, can_see_all_posts, can_see_audio, can_write_private_message, status, last_seen, common_count, relation, relatives, counters'
    __kitUserFields='sex, bdate, city, country, online, lists, domain, contacts, connections, site, education, universities, schools, can_post, can_see_all_posts, can_see_audio, can_write_private_message, status, last_seen, common_count, relation, relatives, counters'
    __researchFields='bdate, city, education, nickname, universities'
    __researchCmd = "friends.get(user_id=78340794,order='name', fields='bdate, city, education, nickname, universities')"
    t1 = 'friends.getMutual(source_uid=78340794, target_uid=11538362)'
    def __init__(self,tok):
        self.vk=vkontakte.API(token=tok)
    def getMutal(self,id1, id2):
        res = self.vk.getMutual(source_uid=id1, target_uid=id2)
        return res
    def usersGet(self,ids, kitFields=__kitUserFields):
        """
        получение информации о некотором человеке
        """
        if isinstance(ids,list):
            ids=str(ids)[1:-1]
        info = []
        print(ids)
        print(self.__allUserFields)
        return self.vk.users.get(user_ids=ids, fields=kitFields)

    def eval(self,cmd):
        """
        выполняет произвольную команду к api vk
        """
        return eval('self.vk.%s'%cmd)
    def medianResearch(self, id):
        self.eval("friends.get(user_id=%s,order='name', fields='%s')"%(str(id),self.__researchFields))





def test1():
    print(vk.getServerTime())
    print(vk.friends.get(fields='uid, first_name, last_name, nickname, sex, bdate',uid='21229916'))

def main():
    log = logger()
    #vk = vkontakte.API('4264030', 'TMqwtjQP3D1YXMlKmBva')
    #print (vk.getServerTime())
    vk = anyk(getCredent('credentials.txt'))
    #vk = vkontakte.API(token=getCredent('credentials.txt'))
    #print "Hello vk API , server time is ",vk.getServerTime()
    #print unicode(vk.users.get(uids=146040808))
    #reader.read(vk.users.get(uids=233945283,fields='sex'))
    #log.responseLog(vk.usersGet(vk.eval(vk.t1)))
    log.responseLog(vk.medianResearch(78340794))
    print ('input you method')
    while True:
        x = input()
        log.comandLog(x)
        x = vk.eval(x)
        print(x)
    return 0

if __name__ == '__main__':
    while True:
        try:
            main()
            #SyntaxError, RuntimeError
        except (NameError,vkontakte.api.VKError) as s:
            print (s)
            continue

