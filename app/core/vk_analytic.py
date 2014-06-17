#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'salamander'
#взять средие(лушче медиану) от друзей пользователя по городу, возрасту и ВУЗу

from app.core import vkontakte
from pprint import pprint
from os.path import exists, isfile
import pickle, datetime, timeit,time
from copy import deepcopy
from app.core.handlers import logger, textViewer, auxMath
#import logging 5859210
import math
import base64

def getCredent(file):
    '''
    вытаскивает токен авторизации из файла credentials.txt
    @type param: file
    @rtype: str

    '''
    try:
        print(file)
        if not isfile(file):
            file = file.split('/')[2]
            if not isfile(file):
                raise FileNotFoundError('error cred path file')
        f = open(file,'r')
        line =  f.readline().strip()
        f.close()
        if line is '':
            print('secret app key is empty')
            exit(1)
    except FileNotFoundError:
        print("не найден файл с токеном авторизации")
        exit(1)
    return line


class baseMind():
    def __init__(self,*args,**kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        for arg in args:
            for key, value in arg.items():
                setattr(self, key, value)

class openFile():
    def __init__(self,file,mode):
        self.file = open(file,mode)
    def __del__(self):
        self.file.close()


class analytic(object):
    #def __new__(cls, *args, **kwargs):
    #    if not hasattr(cls, 'instance'):
    #         cls.instance = super(analytic, cls).__new__(cls)
    #    return cls.instance
    __allUserFields='sex,bdate,city,country,photo_50,photo_100,photo_200_orig,photo_200,photo_400_orig,photo_max,photo_max_orig,online,online_mobile,lists,domain,has_mobile,contacts,connections,site,education,universities,schools,can_post,can_see_all_posts,can_see_audio,can_write_private_message,status,last_seen,common_count,relation,relatives,counters'
    __kitUserFields='sex,bdate,city,country,online,lists,domain,contacts,connections,site,education,universities,schools,can_post,can_see_all_posts,can_see_audio,can_write_private_message,status,last_seen,common_count,relation,relatives,counters'
    __researchFields='bdate,city,education,nickname,universities'
    #researchFields='bdate,city,universities,exports,connections,contacts'
    researchFields='bdate,city,universities'
    baseFields = 'first_name,last_name,uid'
    baseFields2 = 'online,user_id'
    baseFieldsFinally = baseFields + baseFields2
    __researchCmd = "friends.get(user_id=78340794,order='name',fields='bdate,city,education,nickname,universities')"
    t1 = 'friends.getMutual(source_uid=78340794, target_uid=11538362)'
    logtxt = []
    cache = {}
    cachPath = 'cacheLog'
    logBinPath = 'socialLog3'
    logPath = 'socialLog3str'
    cacheLogFile = None
    timeForLastRequest=0
    reqNumber = 0



    #def logerLoader(self, path, file, uploadDict):
    #    try:
    #        file = open(file, 'rb+')
    #        while True:
    #            unpickleObj = pickle.load(file)



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
        self.logFile2= None
        self.logFile2str= None
        self.vk=vkontakte.API(token=tok)
        self.__warmingUpCache()
        self.logtxt=log
        if loggerObject is None:
            loggerObject = logger()
        self.logger = loggerObject
        from app.core.socialAnalyzer import socialAnalyze

        from app.core.myutilites import utilites
        args = {'vk':self.vk,'logtxt':self.logtxt,'logger':self.logger,'cacheLogFile':self.cacheLogFile,'logFile2':self.logFile2,'logFile2str':self.logFile2str}
        args['api']=vkapi(args)

        self.api = vkapi(args) #свои набор, для часто применяемых методов запросов к api vk
        self.social = socialAnalyze(args) #класс для социвального анализа в вк по теме
        self.ut = utilites()
        self.timeForLastRequest = time.time()
        self.social.ut = self.ut


    def __del__(self):
        self.cacheLogFile.close()


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
        t = self.vk.users.get(user_ids=ids, fields=kitFields)[0]
        return t
    def timeDelay(self):
        "вызывается перед обращением к серверам vk api и следит, за тем что бы система не превысила лимит запросов в секунду"
        curTime = time.time()
        delta =  curTime-self.timeForLastRequest
        if self.reqNumber>2 and delta<3:
            print(delta-3)
            self.reqNumber = -1
            self.timeForLastRequest = time.time()
            delta = 3-delta
            if delta>1:
                delta=1
            time.sleep(delta)
            return

        self.reqNumber += 1
        self.timeForLastRequest = curTime
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
            while True:
                try:
                    self.timeDelay()
                    response = eval('self.vk.%s'%cmd)
                    self.cache[cmd]=response
                    self.__logCache(cmd,response)
                    return response
                except vkontakte.VKError as e:
                    if e.code ==6:
                        time.sleep(1)
                        print('sleep!')
                        continue
                    else:
                        raise e

    def getCityName(self,id):
        return self.evalWithCache('database.getCitiesById(city_ids=%s)'%str(id))[0].get('name')


    def mainResearch(self, id: int, service=None, fields=researchFields):
        """
        пытается угадать возраст, пол и ВУЗ человека по его друзьям
        Используется метод максимума (среди друзей как правило, больше всего друзей с одного и того же ВУЗа, того же возраста и из того же города, что и сам человек
        @rtype: str
        """

        peopleList = self.evalWithCache("friends.get(user_id=%s,order='name', fields='%s')"%(str(id),fields))
        #частотные словари
        berd = {}
        univers = {}
        city = {}
        if peopleList is None:
            return (None, 'Слишком мало друзей, что бы провесьти анализ')
        friendsNumber = len(peopleList)
        if friendsNumber < 20:
            return (None, 'Слишком мало друзей, что бы провесьти анализ')

        #добавление данных в частотные словари
        for people in peopleList:
            assert isinstance(people,dict)
            auxMath.addToDict(city,people.get('city'))

            bdate = people.get('bdate')
            if bdate is None:
                continue
            assert isinstance(bdate,str)
            if bdate.count('.') is 2:
                auxMath.addToDict(berd,bdate[-4:])
            if 'universities' in people and len(people.get('universities')) > 0:
                t = people.get('universities')[0]
                auxMath.addToDict(univers,people.get('universities')[0].get('name'))
        #обработка частотных ловарей. Выделение наиболее встречаемых
        topbdate = auxMath.findTopFreq(berd)

        toptuniversity = auxMath.findTopFreq(univers)
        #работа с профайлом пользователя
        userData = self.evalWithCache("users.get(user_ids=%s,order='name', fields='%s')"%(str(id),fields) )[0]
        print(userData)
        profile = mydict()
        profile['year'] = None
        profile['city'] = userData.get('city')
        userBdate = userData.get('bdate')
        if userBdate.count('.') is 2:
            profile['year'] = userBdate[-4:]
        profile['un'] = userData.get('universities')[0].get('name')
        print(profile)





        topcity = auxMath.findTopFreq(city)
        for i,v in enumerate(topcity):
            if len(topcity[i]) is 0:
                temp = 0
            else:
                temp = topcity[i][0]

            t = self.evalWithCache('database.getCitiesById(city_ids=%s)'%str(temp))
            if t is None or len(t) is 0:
                t = "Не известно"
            else:
                t = t[0]['name']
                topcity[i] = list(v)
                topcity[i][0] = t

        eventName=('верефицирован',"найден")


        if service is not None:
            return (topbdate,toptuniversity, topcity)
        reportBirthDay = auxMath.birthPeriodReport(topbdate,profile,(74,86))
        reportCity = auxMath.cityReport(topcity,self.getCityName(profile.city),(76,94),eventName)
        reportUniversity = auxMath.universitiesReport(toptuniversity,friendsNumber, profile.un,eventName,(39,68))
        #bitReport = self.megaReport(topbdate,reportBirthDay, topcity,reportCity, toptuniversity,reportUniversity, profile)


        return (topbdate,reportBirthDay, topcity,reportCity, toptuniversity,reportUniversity)

    def megaReport(self,topbdate,reportBirthDay, topcity,reportCity, toptuniversity,reportUniversity, profile):
        obj = dict(vuz='университет',voz='возраст',gor='город')
        event = dict(ver='верефицирован', find='найден')
        opasity = 'точность'
        persent = dict(vuz='47',voz='57',gor='75')
        curEvent = ''
        report = ''

        if profile.city in topbdate:
            curEvent = event.ver
        else:curEvent = event.find
        report.join('%s %s %s %s'%('город',topbdate))


        bigReport = ''
        bigReport.join('')




    def test(self, id):
        x = self.evalWithCache("friends.get(user_id=%s,order='name', fields='%s')"%(str(id),self.researchFields))
        pprint(x)



class vkapi(baseMind,analytic):
    def getCitiesById(self, id):
        if id is 0 or id is '0' or id==['0'] or id is None:
            return 'Не определен'

        return self.evalWithCache('database.getCitiesById(city_ids=%s)'%str(id))[0]['name']


#нужен универсальный обработчик случаев отсутсвия инфы:
#когда не чего не вернулось, когда вернулся 0
class mainController(object):
    def __init__(self,vk=None,tw=None):
        #self.vk=analytic(getCredent('app/core/credentials.txt'))
        self.vk=analytic(vk)
        self.tw=tw

    def vkApiInterpreter(self,beautifulOut=None):
        print ('input you method')
        while True:
            x = input()
            x = self.vk.eval(x)
            if beautifulOut is not None:
                auxMath.beatifulOut(x)
            else:
                print(x)

    def mainResearchInterpreter(self,beautifulOut=None):
        print ('Enter the username(id or shortname) for the report')
        while True:
            x = input()
            x = self.vk.mainResearch(int(x))
            if beautifulOut is not None:
                auxMath.beatifulOut(x)
            else:
                print(x)


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

class mydict(dict):
    '''
    словарь,у которого доступ к элементам возможен как к методам, а в случае отсутсвии элемента возвращается None
    '''
    def __getattr__(self, key):
        try:
            return self[key]
        except AttributeError:
            return None
    def __setattr__(self, key, value):
        self[key] = value

class simpleRunner:
    #def __init__(self,cred=getCredent('app/core/credentials.txt')):
    def __init__(self,cred=None):
        #cred=getCredent('app/core/credentials.txt')
        cred=None
        self.vk = analytic(cred)
    def report(self,id):
        report = self.vk.mainResearch(id)
        report = auxMath.beatifulOut(report)
        #report = ''.join(report)
        f = open('resultLog.txt','a+')
        f.write(str(id)+'\n')
        #f.write(report)
        f.close()
        return report



def main():

        repoter = simpleRunner()#212835149
        x = repoter.report(5091268)#5859210

        print(x)
        a=1




if __name__ == '__main__':
    main()
