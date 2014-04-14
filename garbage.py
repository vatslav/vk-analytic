__author__ = 'salamander'
import  time
import pickle

#kontakte.VKError: Error(code = '14', description = 'Captcha needed', params = '[{'key': 'oauth', 'value': '1'}, {'key': 'method', 'value': 'friends.get'}, {'key': 'fields', 'value': 'bdate,city,universities,exports,connections,contacts'}, {'key': 'access_token', 'value': '********'}, {'key': 'order', 'value': 'name'}, {'key': 'timestamp', 'value': '1396599294'}, {'key': 'user_id', 'value': '182541327'}]')

#cacheLog = open('casheLog1.txt','r+')
#for line in cacheLog:
#    print(line)
#cacheLog.write('1-2\n')
#cacheLog.write('2-3\n')
class tester():
    pach = 'test'
    file = None
    d = [list(range(10)) for x in range(3)]
    def write(self):
        self.file = open(self.pach,'ab+')
        for x in self.d:
            pickle.dump(x,self.file)
        self.file.close()

    def read(self):
        while True:

            self.file = open(self.pach,'rb')
            self.d2 = []
            try:
                while True:
                        obj = pickle.load(self.file)
                        #assert isinstance(obj,dict)
                        self.d2.append(obj)
            except EOFError:
                pass
            print(self.d2)

t = tester()
t.write()
t.read()