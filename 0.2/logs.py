import time
import os

#TODO level 'fetal' 추가
#TODO level별 글씨색 다르게 설정

time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
starttime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
os.mkdir(starttime)

def start_log():
    log = time.time()
    logtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(log))
    normal = open(starttime + "/[normal]" + logtime + ".txt", 'a')
    critical = open(starttime + "/[critical]" + logtime + ".txt", 'a')
    normal.close()
    critical.close()
    return log

def logger(log,level,message):
    logtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(log))
    normal = open(starttime + "/[normal]" + logtime + ".txt", 'a')
    critical = open(starttime + "/[critical]" + logtime + ".txt", 'a')
    if time.time() - log > 3600*3:
        normal.close()
        critical.close()
        log = time.time()
        logtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(log))
        normal = open(starttime + "/[normal]" + logtime + ".txt", 'a')
        critical = open(starttime + "/[critical]" + logtime + ".txt", 'a')
    if level == 'critical':
        critical.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + '  ' + str(message) + '\n')
    normal.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + '  ' + str(message) + '\n')
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + '  ' + str(message))
    normal.close()
    critical.close()
    return log
