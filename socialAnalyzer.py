__author__ = 'django'
from vk_analytic import analytic
import vkontakte, pickle, handlers, time, timeit
from pprint import pprint

class socialAnalyze(analytic):
    def __init__(self,vk,logtxt,logger,cacheLogFile,api):
        self.vk, self.logtxt, self.logger,self.cacheLogFile,self.api = vk,logtxt,logger,cacheLogFile,api

    #беру некоторый user id в Вконтакте например, http://vk.com/id200000000
    #в цикле пока переменную успешных опросов не достигнет 1000:
    #- смотрим указана на странице полная дата рождения, учебное заведение и город и открыты ли более 30 друзей
    #- если да то делаем анализ и сравниваем с данными из анкеты + записываем результаты в лог
    #- увеличиваем переменную успешных анализов на 1

    def analyzeManyPeople(self):
        id = 78341048
        successProfile = 0
        neededOpenFriends = 30
        bird = {}
        city = {}
        univers = {}
        lofFile2= open('socialLog2','wb+')

        while True:
            try:
                print(id)
                realMan = self.usersGet(id,self.researchFields)
                if 'universities' in realMan and 'city' in realMan and 'bdate' in realMan and \
                len(realMan['universities'])>0  and realMan['city']>0 and realMan['bdate'].count('.') is 2:
                    analyzedMan = self.mainResearch(id,service=True)
                    if analyzedMan[0] is None:
                        id +=1
                        continue

                    t = (realMan['universities'][0]['name'],analyzedMan[1][0])
                    t2 = (self.api.getCitiesById(realMan['city']),analyzedMan[2])
                    t0 = (realMan['bdate'],analyzedMan[0])
                    out = ((realMan['bdate'],analyzedMan[0]), (realMan['universities'][0]['name'],analyzedMan[1][0]),(self.api.getCitiesById(realMan['city']),analyzedMan[2]) )
                    pickle.dump(out,lofFile2)
                    pprint(out)
                id +=1
                successProfile +=1
                if successProfile>1000:
                    break
            except vkontakte.VKError as e:
                if e.code==15:
                    id += 1
                elif e.code is 14: #captra need
                    #обработчик ошибки для капчи, но тут походу предется править обертку вокруг api
                    exit(1)
                elif e.code is 6: #Too many requests per second
                    time.sleep(1)

                else:
                    print(e)
                    exit(1)



