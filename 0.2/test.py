from logs import *

log = start_log()

log = logger(log,'critical','테스트중입니다1')
time.sleep(10)
log = logger(log,'critical','테스트중입니다2')