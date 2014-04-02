#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'salamander'
#взять средие(лушче медиану) от друзей пользователя по городу, возрасту и ВУЗу
import vkontakte
from pprint import pprint
from os.path import exists, isfile
import pickle, datetime
from copy import deepcopy

from handlers import logger, textViewer, auxMath


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
    researchFields='bdate,city,universities,exports,connections,contacts'
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
        #print(cmd)
        #return eval('self.vk.%s'%cmd)
        return self.evalWithCache(cmd)

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

    def birdReport(self,rankedListDates:list):
        start = min(auxMath.getMemberPair(rankedListDates))
        end = max(auxMath.getMemberPair(rankedListDates))
        top = rankedListDates[0][0]
        year = datetime.date.today().year
        age = year - int(top)
        report = 'премерное время рождения %s - %s гг., наиболее вероятно в %s г.\n' \
                 'Примерный возраст %s лет' % (start,end,top,age)
        return report

    def mainResearch(self, id: int):
        """
        пытается угадать возраст, пол и ВУЗ человека по его друзьям
        Используется метод максимума (среди друзей как правило, больше всего друзей с одного и того же ВУЗа, того же возраста и из того же города, что и сам человек
        @rtype: str
        """
        peopleList = self.eval("friends.get(user_id=%s,order='name', fields='%s')"%(str(id),self.researchFields))
        berd = {}
        univers = {}
        city = {}
        for people in peopleList:
            assert isinstance(people,dict)
            auxMath.addToDict(city,people.get('city'))
            bdate = people.get('bdate')
            if bdate is None:
                continue
            assert isinstance(bdate,str)
            if bdate.count('.') is 2:
                auxMath.addToDict(berd,bdate[-4:])
        hotbdate = auxMath.findTopFreq(berd)
        reportYers = auxMath.birthPeriodReport(hotbdate)
        hotcity = auxMath.findTopFreq(city)
        for i,v in enumerate(hotcity):
            t = self.evalWithCache('database.getCitiesById(city_ids=%s)'%str(hotcity[i][0]))[0]['name']
            hotcity[i] = list(v)
            hotcity[i][0] = t
        reportCity = auxMath.cityReport(hotcity)
        return (hotbdate,hotcity,reportYers,reportCity)

    def test(self, id):
        x = self.evalWithCache("friends.get(user_id=%s,order='name', fields='%s')"%(str(id),self.researchFields))
        pprint(x)


class mainController(object):
    def __init__(self,vk,tw=None):
        self.vk=vk
        self.tw=tw

    def vkApiInterpreter(self):
        print ('input you method')
        while True:
            x = input()
            x = self.vk.eval(x)
            print(x)

    def mainResearchInterpreter(self):
        print ('Enter the username(id or shortname) for the report')
        while True:
            x = input()
            x = self.vk.mainResearch(int(x))
            for line in x[2:]:
                print(line)


    def test1(self):
        print(self.vk.getServerTime())
        print(self.vk.friends.get(fields='uid, first_name, last_name, nickname, sex, bdate',uid='21229916'))
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
    mainClass = mainController(vk,tw)
    #research = vk.mainResearch(226723565)
    #print(research[2])
    #print(vk.mainResearch(72858365)[2])
    #print(vk.mainResearch(150798434)[2])
    x = vk.mainResearch(182541327)[2:4]
    pprint(x)

    #vk.test(3870390)
    #mainClass.vkApiInterpreter()
    mainClass.mainResearchInterpreter()
    return 0

if __name__ == '__main__':
    try:
        main()
    except EOFError:
        exit(0)


