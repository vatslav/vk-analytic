__author__ = 'salamander'


#kontakte.VKError: Error(code = '14', description = 'Captcha needed', params = '[{'key': 'oauth', 'value': '1'}, {'key': 'method', 'value': 'friends.get'}, {'key': 'fields', 'value': 'bdate,city,universities,exports,connections,contacts'}, {'key': 'access_token', 'value': '********'}, {'key': 'order', 'value': 'name'}, {'key': 'timestamp', 'value': '1396599294'}, {'key': 'user_id', 'value': '182541327'}]')

#cacheLog = open('casheLog1.txt','r+')
#for line in cacheLog:
#    print(line)
#cacheLog.write('1-2\n')
#cacheLog.write('2-3\n')

a = {}
for x in range(9):
    a[x]=x

for i,v in enumerate(a):
    if v==4:
        del a[2:]
print(a)