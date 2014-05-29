__author__ = 'salamander'
import webbrowser, pickle

import sys
import re
#from app.core.handlers import *
#from app.core.vk_analytic import analytic,baseMind

class utilites():
    path = 'logArhive/socialLogPurgePro.csv'
    def openurl(url):
        webbrowser.open(url)

    def getBinCashLog(self):
        cashFile = open(self.logBinPath,'rb')
        res = []
        try:
            while True:
                line = pickle.load(cashFile)
                #assert isinstance(line,tuple)
                res.append(line)
        except (FileNotFoundError, EOFError):
            pass
        cashFile.close()
        return res

    def getReadableBinCashLog(self):
        cash = self.getBinCashLog()
        res = ''
        for elem in cash:
            res += (str(elem)+'\n')
        return res
    def getReadableCashLog(self):
        cash = open('socialLog3str','r')
        res = ''
        for line in cash:
            res += line
        return res

    def getCashLog(self):
        cash = open('socialLog3str','r')
        res = []
        for line in cash:
            res.append(line)
        return res

    def getIdFromTextLog(self):
        cash = self.getCashLog()
        res = []
        p = re.compile(r'((\d+)\))$')
        for line in cash:
            res.append(int(re.findall(p,line)[0][0][:-1]))
        res = set(res)
        res = list(res)
        res.sort()

        return res
    def createStandaloneToken(self):
        url = 'https://oauth.vk.com/authorize?client_id=4365397&scope=friends&redirect_uri=https://oauth.vk.com/blank.html&display=popup&v=5.21&response_type=token'
        webbrowser.open(url)


    def getExistedId(self):
        cash = self.getBinCashLog()
        res = []
        for line in cash:
            res.append(line[3])
        return res



    def readLog(self):
        lofFile2= open('socialLog3','rb')
        try:
            line = pickle.load(lofFile2)
            for v in line:
                print(line)
        except (FileNotFoundError, EOFError):
            pass

        lofFile2.close()

    def cleanSocialLog(self):
        '''
        убирает плохие логи из лог-файла
        '''
        import fileinput
        path = self.path
        p = '\w;;;;$'
        def replaceAll(file):
            for line in fileinput.input(file, inplace=1):
                if len(re.findall(p,line))>0:
                    sys.stdout.write(line)
        replaceAll(path)
    def separateYears(self):
        """
        добовляет столбцы - день, месяц, год из реала
        """
        import fileinput


        for line in fileinput.input(self.path, inplace=1):
            if 'RealDate;aDate;score;' not in line:
                line = ''.join((line[:11], ';'.join(line[:10].split('.')),';',line[11:]))
            sys.stdout.write(line)


    def analisysLog(self):
        f = open(self.path,'r')
        fResult = open(self.path+'.result','w')
        fieldSet = 'RealDate,rDay,rMouth,rYear,aDate,aDateScore,bDate,bDateScore,cDate,cDateScore,rUniversity,aUniversity,\
aUniversityScore,bUniversity,bUniversityScore,cUniversity,cUniversityScore,\
rCity,aCity,aCityScore,bCity,bCityScore,cCity,cCityScore,id'.split(',')
        temp = [[''.join((x,word)) for x in 'abcf'] for word in ('Date','TruncDate','TrancDateTwo', 'University','City','AllFound' )]
        nameStatisticField  = []
        for l1 in temp:
            for l2 in l1:nameStatisticField.append(l2)
        statistic = mydictTwo.fromkeys(nameStatisticField,0)

        import datetime
        def trancDate(yar,moth, otherYear,delta=100):
            moth = int(moth)
            yar = int(yar)
            otherYear = int(otherYear)
            delta = datetime.timedelta(days=100)
            return datetime.date(yar,moth,1)-delta < datetime.date(otherYear,1,1) < datetime.date(yar,moth,1)+delta

        for line in f:
            if 'RealDate;aDate;score;' in line:
                continue
            line = line[:-5]
            namedLine = mydict(zip(fieldSet, line.split(';')))
            foundInAnyDate = False
            foundInAnyDateTwo = False
            foundAllInA = 0
            foundAllInB = 0
            foundAllInC = 0

            if namedLine.aDate in namedLine.rYear:
                statistic.aDate+=1
                foundAllInA += 1
            if namedLine.bDate in namedLine.rYear:
                statistic.bDate+=1
                foundAllInB += 1
            if namedLine.cDate in namedLine.rYear:
                statistic.cDate+=1
                foundAllInC += 1
            if namedLine.rYear in (namedLine.cDate,namedLine.bDate,namedLine.aDate):statistic.fDate+=1

            if namedLine.aCity in namedLine.rCity:
                statistic.aCity+=1
                foundAllInA += 1
            if namedLine.bCity in namedLine.rCity:
                statistic.bCity+=1
                foundAllInB += 1
            if namedLine.cCity in namedLine.rCity:
                statistic.cCity+=1
                foundAllInC += 1
            if namedLine.rCity in (namedLine.cCity,namedLine.bCity,namedLine.aCity):statistic.fCity+=1

            if namedLine.aUniversity in namedLine.rUniversity:
                statistic.aUniversity+=1
                foundAllInA += 1
            if namedLine.bUniversity in namedLine.rUniversity:
                statistic.bUniversity+=1
                foundAllInB += 1
            if namedLine.cUniversity in namedLine.rUniversity:
                statistic.cUniversity+=1
                foundAllInC += 1
            if namedLine.rUniversity in (namedLine.cUniversity,namedLine.bUniversity,namedLine.aUniversity):statistic.fUniversity+=1

            if trancDate(namedLine.rYear,namedLine.rMouth,namedLine.aDate):
                statistic.aTruncDate+=1
                foundInAnyDate = 1
            if trancDate(namedLine.rYear,namedLine.rMouth,namedLine.bDate):
                statistic.bTruncDate+=1
                foundInAnyDate=1
            if trancDate(namedLine.rYear,namedLine.rMouth,namedLine.cDate):
                statistic.cTruncDate+=1
                foundInAnyDate=1
            if foundInAnyDate:statistic.fTruncDate+=1

            #trancTwo
            if trancDate(namedLine.rYear,namedLine.rMouth,namedLine.aDate,delta=730):
                statistic.aTrancDateTwo+=1
                foundInAnyDateTwo = 1
            if trancDate(namedLine.rYear,namedLine.rMouth,namedLine.bDate,delta=730):
                statistic.bTrancDateTwo+=1
                foundInAnyDateTwo=1
            if trancDate(namedLine.rYear,namedLine.rMouth,namedLine.cDate,delta=730):
                statistic.cTrancDateTwo+=1
                foundInAnyDateTwo=1
            if foundInAnyDate:statistic.fTrancDateTwo+=1

            #allFound
            if foundAllInA is 3: statistic.aAllFound+=1
            if foundAllInB is 3: statistic.bAllFound+=1
            if foundAllInC is 3: statistic.cAllFound+=1
            if 3 in (foundAllInA, foundAllInB, foundAllInC):statistic.fAllFound+=1

        statistic
        print(statistic)
        print(['%s - %s'%(name,statistic[name]) for name in nameStatisticField])


class mydict(dict):
    def __getattr__(self, key):
        return self[key]
    def __setattr__(self, key, value):
        self[key] = value

class mydictTwo(dict):
    def __getattr__(self, key):
        return self[key]
    def __setattr__(self, key, value):
        self[key] = value


if __name__ == '__main__':
    ut = utilites()
    ut.analisysLog()