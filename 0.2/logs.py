import time
import os

starttime = time.ctime(time.time())
os.mkdir(starttime)

def start_log():
    log = time.time()
    logtime = time.ctime(log)
    normal = open(starttime + "/[normal]" + logtime + ".txt", 'a')
    critical = open(starttime + "/[critical]" + logtime + ".txt", 'a')
    normal.close()
    critical.close()
    return log

def logger(log,level,message):
    logtime = time.ctime(log)
    normal = open(starttime + "/[normal]" + logtime + ".txt", 'a')
    critical = open(starttime + "/[critical]" + logtime + ".txt", 'a')
    if time.time() - log > 3600*3:
        normal.close()
        critical.close()
        log = time.time()
        logtime = time.ctime(log)
        normal = open(starttime + "/[normal]" + logtime + ".txt", 'a')
        critical = open(starttime + "/[critical]" + logtime + ".txt", 'a')
    if level == 'critical':
        critical.write(time.ctime(time.time()) + '  ' + str(message) + '\n')
    normal.write(time.ctime(time.time()) + '  ' + str(message) + '\n')
    print(time.ctime(time.time()) + '  ' + str(message))
    normal.close()
    critical.close()
    return log
