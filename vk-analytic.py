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




class analytic(object):
    __allUserFields='sex,bdate,city,country,photo_50,photo_100,photo_200_orig,photo_200,photo_400_orig,photo_max,photo_max_orig,online,online_mobile,lists,domain,has_mobile,contacts,connections,site,education,universities,schools,can_post,can_see_all_posts,can_see_audio,can_write_private_message,status,last_seen,common_count,relation,relatives,counters'
    __kitUserFields='sex,bdate,city,country,online,lists,domain,contacts,connections,site,education,universities,schools,can_post,can_see_all_posts,can_see_audio,can_write_private_message,status,last_seen,common_count,relation,relatives,counters'
    __researchFields='bdate,city,education,nickname,universities'
    researchFields2='bdate,city,universities'
    baseFields = 'first_name,last_name,uid'
    baseFields2 = 'online,user_id'
    baseFieldsFinally = baseFields + baseFields2
    __researchCmd = "friends.get(user_id=78340794,order='name',fields='bdate,city,education,nickname,universities')"
    t1 = 'friends.getMutual(source_uid=78340794, target_uid=11538362)'
    logtxt = []
    cache = {}
    def __init__(self,tok,log=1,loggerObject=None):
        self.vk=vkontakte.API(token=tok)
        self.logtxt=log
        if loggerObject is None:
            loggerObject = logger()
        self.logger = loggerObject

    def log(self,cmd):
        pass
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
        print(cmd)
        return eval('self.vk.%s'%cmd)
    def evalWithCache(self,cmd):
        if cmd in self.cache:
            return self.cache[cmd]
        else:
            response = eval('self.vk.%s'%cmd)
            self.cache[cmd]=response
            return response

    def medianResearch(self, id):
        text = self.eval("friends.get(user_id=%s,order='name', fields='%s')"%(str(id),self.researchFields2))

        return text


class textViewer(object):
    replacedFields = {'city':'database.getCitiesById(city_ids=XX)','country':'database.getCountriesByIdv(country_ids=XX)'}
    def __init__(self,vk):
        assert(vk, analytic)
        self.vk=vk
    def print(self,docs,orderList):
        sortedDoc = []
        docs = self.baseReplacer(docs)
        for doc in docs:
            assert isinstance(doc,dict)
            sortedUser = []
            for entry in orderList:

                if entry in doc:
                    sortedUser.append('%s - %s' %(entry, str(doc[entry])))
            sortedDoc.append(sortedUser)
        pprint(sortedDoc)
        return  sortedDoc


    def baseReplacer(self,rawListOfDicts):
        for rawList in rawListOfDicts:
            assert  isinstance(rawList,dict)
            for field in self.replacedFields.keys():
                if field in rawList:
                    if rawList[field] is 0:
                        rawList[field]='Нет информации'
                    else:
                        #t1 = self.replacedFields[field]
                        #t2 = t1.replace('XX',str(rawList[field]))
                        #t3 = self.vk.eval(t2)[0]['name']

                        rawList[field] = self.vk.evalWithCache(self.replacedFields[field].replace('XX',str(rawList[field])))[0]['name']
                    #doc[field]=self.vk.eval(self.replacedFields[field].replace('XX',field))[0]['name']
        return rawListOfDicts




def test1():
    print(vk.getServerTime())
    print(vk.friends.get(fields='uid, first_name, last_name, nickname, sex, bdate',uid='21229916'))

def main():
    log = logger()

    #print (vk.getServerTime())
    vk = analytic(getCredent('credentials.txt'))
    tw = textViewer(vk)
    #vk = vkontakte.API(token=getCredent('credentials.txt'))
    #print "Hello vk API , server time is ",vk.getServerTime()
    #print unicode(vk.users.get(uids=146040808))
    #reader.read(vk.users.get(uids=233945283,fields='sex'))
    #log.responseLog(vk.usersGet(vk.eval(vk.t1)))
    #print(vk.researchFields2.split(','))
    tw.print(vk.medianResearch(226723565),(vk.baseFields+vk.researchFields2).split(','))#78340794
    print ('input you method')
    while True:
        x = input()
        #log.comandLog(x)
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

