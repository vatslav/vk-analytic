# -*- coding: utf-8 -*-
from cgi import logfile
from io import open

__author__ = u'django'
from app.core.vk_analytic import baseMind,analytic,vkontakte
import pickle,app.core.handlers, time, timeit
from pprint import pprint

class socialAnalyze(baseMind,analytic):

    #беру некоторый user id в Вконтакте например, http://vk.com/id200000000
    #в цикле пока переменную успешных опросов не достигнет 1000:
    #- смотрим указана на странице полная дата рождения, учебное заведение и город и открыты ли более 30 друзей
    #- если да то делаем анализ и сравниваем с данными из анкеты + записываем результаты в лог
    #- увеличиваем переменную успешных анализов на 1

    def __del__(self):
        self.logFile2str.close()
        self.logFile2.close()
        print u'del run'

    def analyzeManyPeople(self):
        self.logFile2= open(self.logBinPath,u'ab')
        self.logFile2str= open(self.logPath,u'a')
        #78340794 init user
        #id = 78395684
        successProfile = 0
        neededOpenFriends = 30
        bird = {}
        city = {}
        univers = {}
        ids = list(set(self.ut.getExistedId()))
        ids2 = list(set(self.ut.getIdFromTextLog()))
        for id in ids:
            if id in ids2:
                ids2.remove(id)
        print len(ids2)
        ids2.sort()
        print u'len=%s'%len(ids2)

        for id in ids2:
            try:
                print id
                realMan = self.usersGet(id,self.researchFields)
                if u'universities' in realMan and u'city' in realMan and u'bdate' in realMan and \
                len(realMan[u'universities'])>0  and realMan[u'city']>0 and realMan[u'bdate'].count(u'.') is 2:
                    analyzedMan = self.mainResearch(id,service=True)
                    if analyzedMan[0] is None:
                        id +=1
                        continue
                    out = ((realMan[u'bdate'],analyzedMan[0]), (realMan[u'universities'][0][u'name'],analyzedMan[1]),(self.api.getCitiesById(realMan[u'city']),analyzedMan[2]),id )
                    pickle.dump(out,self.logFile2)
                    self.logFile2str.write(unicode(out)+u'\n')
                    pprint(unicode(out))
                    successProfile +=1
                id +=1
            except vkontakte.VKError, e:
                if e.code==15:
                    id += 1
                elif e.code is 14: #captra need
                    print u'captra need'
                    #обработчик ошибки для капчи, но тут походу предется править обертку вокруг api
                    time.sleep(5)
                elif e.code is 6: #Too many requests per second
                    print u'sleep run!?!'


                else:
                    print e
                    exit(1)

    def analiz(self,x,y=None):
        cash = self.ut.getBinCashLog()
        res = []
        for line in cash:
            if y is None:
                res.append(line[x])
            else:
                res.append(line[x][y])
        return res

    def makeCsv(self):
        cash = self.ut.getBinCashLog()
        l = cash[0]
        res = u''
        for line in cash:
            for block in line:
                if not isinstance(block,unicode):
                    for elem in block:
                        if not isinstance(elem,unicode):
                            for subelem in elem:
                                res+=u'%s,'%subelem
                        else:res += u'%s,'%elem
                else:res += block
            line+=u'\n'
        #[] - rebase to 0,0
        #колонки с выводами
        #уникальность
    def logAnalysis(self):
        self.logFile2str= open(self.logPath,u'a')
        cash = self.ut.getBinCashLog()
        bitCash = cash[0:10]
            #for obj in cash:
            #    for  elem in
            #
            #a=1


