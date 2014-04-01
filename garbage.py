__author__ = 'salamander'

cacheLog = open('casheLog1.txt','r+')
for line in cacheLog:
    print(line)
cacheLog.write('1-2\n')
cacheLog.write('2-3\n')

