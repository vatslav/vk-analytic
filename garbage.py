__author__ = 'salamander'

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