#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'salamander'
#взять средие(лушче медиану) от друзей пользователя по городу, возрасту и ВУЗу
import vkontakte
from pprint import pprint
from os.path import exists, isfile
import pickle
from copy import deepcopy

from handlers import logger


def getCredent(file):
    '''
    вытаскивает токен авторизации из файла credentials.txt
    @type param: file
    @rtype: str
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
    cachPath = 'cacheLog'
    cacheLogFile = None

    def __warmingUpCache(self):
        """
        прогрев кеша из файла. Используется при инициализации экземпляра класса
        """
        try:
            self.cacheLogFile = open(self.cachPath,'rb+')
            while True:
                unpickleObj = pickle.load(self.cacheLogFile)
                unpickleObj = unpickleObj.popitem()
                self.cache[unpickleObj[0]]=unpickleObj[1]

        except FileNotFoundError:
            self.cacheLogFile = open(self.cachPath,'wb')
        except EOFError:
            pass

    def __logCache(self,cmd, response):
        pickle.dump({cmd:response},self.cacheLogFile)




    def __init__(self,tok,log=1,loggerObject=None):
        self.vk=vkontakte.API(token=tok)
        self.__warmingUpCache()
        self.logtxt=log
        if loggerObject is None:
            loggerObject = logger()
        self.logger = loggerObject

    def log(self,cmd):
        pass
    def getMutal(self,id1, id2):
        """
        возвращает общих друзей двух людей
        @rtype: list
        """
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
        @rtype: list
        """
        print(cmd)
        return eval('self.vk.%s'%cmd)
    def evalWithCache(self,cmd):
        """
        выполняет запрос к серверу vk с кешированием в оперативной памяти. (Кеш не обновляется со временем)
        @rtype: list
        """
        if cmd is '':
            return ''
        if cmd in self.cache:
            return self.cache[cmd]
        else:
            response = eval('self.vk.%s'%cmd)
            self.cache[cmd]=response
            self.__logCache(cmd,response)
            return response

    def mainResearch(self, id: int):
        """
        пытается угадать возраст, пол и ВУЗ человека по его друзьям
        Используется метод максимума (среди друзей как правило, больше всего друзей с одного и того же ВУЗа, того же возраста и из того же города, что и сам человек
        @rtype: str
        """
        text = self.eval("friends.get(user_id=%s,order='name', fields='%s')"%(str(id),self.researchFields2))

        return text


class textViewer(object):
    replacedFields = {'city':'database.getCitiesById(city_ids=XX)',
                      'country':'database.getCountriesById(country_ids=XX)',
                      'universities':{'id':'','faculty':'','chair':'',
                                      'country':'database.getCountriesById(country_ids=XX)',
                                      'city':'database.getCitiesById(city_ids=XX)'},
                      'education':{'university':'', 'faculty':''}
                    }
    #universities - http://vk.com/dev/database.getFaculties
    #обработка отдельно
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
             cls.instance = super(textViewer, cls).__new__(cls)
        return cls.instance

    def __init__(self,vk):
        assert(vk, analytic)
        self.vk=vk
        self.log = logger()
    def print(self,docs:list,orderList:list):
        """
        печатает ответ сервера в удобном виде, с заменой id объектов на их человеческие названия, порядок полей определяется orderList
        возвращает обработанный ответ
        @rtype:list
        """
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


    def baseReplacer(self,rawListOfDicts:list):
        '''
        замена идентификаторов объектов по базе vk на их человеческие названия
        @rtype: list
        '''
        for rawList in rawListOfDicts:
            x = self.vk.evalWithCache('database.getCitiesById(city_ids=1)')
            assert  isinstance(rawList,dict)
            for field in self.replacedFields.keys():
                if field in rawList:
                    if rawList[field] is 0:
                        rawList[field]='Нет информации'
                    else:
                        t1 = self.replacedFields[field]
                        x = self.replacedFields
                        x2= deepcopy(self.replacedFields[field])

                        #если tuple, то для каждого элемента из tuple делаем замену
                        if isinstance(t1,dict):
                            a=1
                            t2 = rawList[field]
                            if len(t2)>0:
                                t2=t2[0]
                            else:
                                continue
                            assert isinstance(t2,dict)

                            for key,value in t1.items():
                                if key in t2:
                                    tt=value.replace('XX',str(t2[key]))
                                    self.log.responseLog(tt)


                                    try:
                                        ttt=self.vk.evalWithCache(tt)
                                    except AttributeError:
                                        a=1
                                    t2[key]=ttt
                            rawList[field]=t2


                            a=1



                        else:
                            t2 = t1.replace('XX',str(rawList[field]))
                            t3 = self.vk.evalWithCache(t2)
                            t4 = t3[0]['name']
                            rawList[field] = t4
        return rawListOfDicts





def test1():
    print(vk.getServerTime())
    print(vk.friends.get(fields='uid, first_name, last_name, nickname, sex, bdate',uid='21229916'))
    #vk = vkontakte.API(token=getCredent('credentials.txt'))
    #print "Hello vk API , server time is ",vk.getServerTime()
    #print unicode(vk.users.get(uids=146040808))
    #reader.read(vk.users.get(uids=233945283,fields='sex'))
    #log.responseLog(vk.usersGet(vk.eval(vk.t1)))
    #print(vk.researchFields2.split(','))
    #print (vk.getServerTime())

def main():
    log = logger()


    vk = analytic(getCredent('credentials.txt'))
    tw = textViewer(vk)

    tw.print(vk.mainResearch(226723565),(vk.baseFields+vk.researchFields2).split(','))#78340794
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

