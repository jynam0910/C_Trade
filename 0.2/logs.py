import time
import os

time.strftime('%Y-%m-%d %I:%M:%S', time.localtime())
starttime = time.strftime('%Y-%m-%d %I:%M:%S', time.localtime(time.time()))
#starttime = time.ctime(time.time())
os.mkdir(starttime)

def start_log():
    log = time.time()
    logtime = time.strftime('%Y-%m-%d %I:%M:%S', time.localtime(log))
    #logtime = time.ctime(log)
    normal = open(starttime + "/[normal]" + logtime + ".txt", 'a')
    critical = open(starttime + "/[critical]" + logtime + ".txt", 'a')
    normal.close()
    critical.close()
    return log

def logger(log,level,message):
    logtime = time.strftime('%Y-%m-%d %I:%M:%S', time.localtime(log))
    #logtime = time.ctime(log)
    normal = open(starttime + "/[normal]" + logtime + ".txt", 'a')
    critical = open(starttime + "/[critical]" + logtime + ".txt", 'a')
    if time.time() - log > 3600*3:
        normal.close()
        critical.close()
        log = time.time()
        logtime = time.strftime('%Y-%m-%d %I:%M:%S', time.localtime(log))
        #logtime = time.ctime(log)
        normal = open(starttime + "/[normal]" + logtime + ".txt", 'a')
        critical = open(starttime + "/[critical]" + logtime + ".txt", 'a')
    if level == 'critical':
        critical.write(time.strftime('%Y-%m-%d %I:%M:%S', time.localtime(time.time())) + '  ' + str(message) + '\n')
        #critical.write(time.ctime(time.time()) + '  ' + str(message) + '\n')
    normal.write(time.strftime('%Y-%m-%d %I:%M:%S', time.localtime(time.time())) + '  ' + str(message) + '\n')
    print(time.strftime('%Y-%m-%d %I:%M:%S', time.localtime(time.time())) + '  ' + str(message))
    #normal.write(time.ctime(time.time()) + '  ' + str(message) + '\n')
    #print(time.ctime(time.time()) + '  ' + str(message))
    normal.close()
    critical.close()
    return log
