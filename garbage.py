__author__ = 'salamander'
import  time

#kontakte.VKError: Error(code = '14', description = 'Captcha needed', params = '[{'key': 'oauth', 'value': '1'}, {'key': 'method', 'value': 'friends.get'}, {'key': 'fields', 'value': 'bdate,city,universities,exports,connections,contacts'}, {'key': 'access_token', 'value': '********'}, {'key': 'order', 'value': 'name'}, {'key': 'timestamp', 'value': '1396599294'}, {'key': 'user_id', 'value': '182541327'}]')

#cacheLog = open('casheLog1.txt','r+')
#for line in cacheLog:
#    print(line)
#cacheLog.write('1-2\n')
#cacheLog.write('2-3\n')

def main():
    class ex(object):
        def __del__(self):
            print('call dell!')

    a = ex()
    a = time.time()
    print(time.time())
    time.sleep(1)
    print(type(a-time.time()))

main()