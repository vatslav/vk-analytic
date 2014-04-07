__author__ = 'salamander'
import webbrowser, pickle
from handlers import *
from vk_analytic import analytic

class utilites(analytic):
    def __init__(self,vk,logtxt,logger,cacheLogFile,api):
        self.vk, self.logtxt, self.logger,self.cacheLogFile,self.api = vk,logtxt,logger,cacheLogFile,api

    def openurl(url):
        webbrowser.open(url)

    def readCashLog(self):
        cashFile = open(self.cachPath,'rb+')
        try:
            line = pickle.load(cashFile)
            assert isinstance(line,dict)
            for k,v in line.items():
                for l2 in v:
                    print(l2,end='\n')
        except (FileNotFoundError, EOFError):
            pass

    def readLog(self):
        lofFile2= open('socialLog2','rb')
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


