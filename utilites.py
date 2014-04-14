__author__ = 'salamander'
import webbrowser, pickle,re
from handlers import *
from vk_analytic import analytic,baseMind

class utilites(baseMind,analytic):

    def openurl(url):
        webbrowser.open(url)

    def getBinCashLog(self):
        cashFile = open(self.cachPath,'rb+')
        res = []
        try:
            line = pickle.load(cashFile)
            assert isinstance(line,dict)
            for k,v in line.items():
                for l2 in v:
                    res.append(l2)
        except (FileNotFoundError, EOFError):
            pass
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

    def getExistedId(self):
        cash = self.getBinCashLog()
        res = []
        for line in cash:
            res.append(line['uid'])
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


if __name__ == '__main__':

    x = input()
    if x.isalnum():
        utilites.openurl('https://vk.com/id%s'%x)


