__author__ = 'salamander'
import webbrowser, pickle,re
#from app.core.handlers import *
#from app.core.vk_analytic import analytic,baseMind

class utilites():

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
        import fileinput
        import sys
        import re
        
        path = 'logArhive/socialLog.csv'
        p = '\w;;;;$'
        def replaceAll(file):
            for line in fileinput.input(file, inplace=1):
                if len(re.findall(p,line))>0:
                    sys.stdout.write(line)
        replaceAll(path)

if __name__ == '__main__':
    ut = utilites()
    ut.cleanSocialLog()