__author__ = u'salamander'
import webbrowser, pickle,re
from app.core.handlers import *
from app.core.vk_analytic import analytic,baseMind
from io import open

class utilites(baseMind,analytic):

    def openurl(url):
        webbrowser.open(url)

    def getBinCashLog(self):
        cashFile = open(self.logBinPath,u'rb')
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
        res = u''
        for elem in cash:
            res += (unicode(elem)+u'\n')
        return res
    def getReadableCashLog(self):
        cash = open(u'socialLog3str',u'r')
        res = u''
        for line in cash:
            res += line
        return res

    def getCashLog(self):
        cash = open(u'socialLog3str',u'r')
        res = []
        for line in cash:
            res.append(line)
        return res

    def getIdFromTextLog(self):
        cash = self.getCashLog()
        res = []
        p = re.compile(ur'((\d+)\))$')
        for line in cash:
            res.append(int(re.findall(p,line)[0][0][:-1]))
        res = set(res)
        res = list(res)
        res.sort()

        return res

    def getExistedId(self):
        cash = self.getBinCashLog()
        res = []
        for line in cash:
            res.append(line[3])
        return res



    def readLog(self):
        lofFile2= open(u'socialLog3',u'rb')
        try:
            line = pickle.load(lofFile2)
            for v in line:
                print line
        except (FileNotFoundError, EOFError):
            pass

        lofFile2.close()



if __name__ == u'__main__':

    x = raw_input()
    if x.isalnum():
        utilites.openurl(u'https://vk.com/id%s'%x)


