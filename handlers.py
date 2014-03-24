__author__ = 'salamander'


class reader(object):
    debug=1
    @staticmethod
    def rawHandler(req):
        '''
        @rtype: dict
        '''
        return req[0]
    @staticmethod
    def getKeys(req):
        return reader.rawHandler(req).keys()
    @staticmethod
    def getValues(req):
        return reader.rawHandler(req).values()
    @staticmethod
    def read(req):
        if isinstance(req,str):
            print req
        elif isinstance(req,list):
            #print req
            arr = [(str(i[0]),i[1]) for i in reader.rawHandler(req).items()]
            for x,y in arr:
                print x,y
        else:raise RuntimeError('unknow type of requst')
    @staticmethod
    def r():
        return 1



