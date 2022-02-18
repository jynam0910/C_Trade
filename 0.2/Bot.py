import pyupbit
import time
import sys
import traceback
from modules import *
from search import *
from sell import *
from buy import *
from logs import *

access_key = "SXNutokqUGXkTDH5C4hbmRqNRsZjyfQ0eOyc31BK"
secret_key = "WlugojbqxP8V7RiZxpY1LrxN9fc6lh84iVxoP8PX"
upbit = pyupbit.Upbit(access_key, secret_key)

# 초기설정
exclude = ['KRW-BTT','KRW-IQ']
status = 0
mode = 'sell'

#로깅시작
log = start_log()
log = logger(log, 'critical', '{로깅시작}')

# 로그인 (+지갑확인)
try:
    log = print_wallet(upbit,log)
    log = logger(log, 'critical', '{로그인 성공}')
except:
    log = logger(log, 'critical', '{로그인 실패}')
    log = logger(log, 'critical', traceback.format_exc())
    sys.exit(1)

# BOT
found = []
#TODO 에러타임 구현 오류 있음
error_time = time.time() #5분안에 사소한 에러 두번 발생 시 강제종료
while status == 0:
    if mode == 'search':
        found = []
        try:
            log = logger(log, 'normal', '{탐색} 전략2')
            excluded_tickers = exclude_tickers_owned(upbit, exclude)
            found = search2(upbit, excluded_tickers)
            if len(found) != 0:
                log = logger(log, 'critical', '탐색된 코인: ' + str(found))
                log = logger(log, 'normal', '{탐색종료}')
                time.sleep(1)
                mode = 'buy'
            else:
                log = logger(log, 'normal', '탐색된 코인이 없음')
                log = logger(log, 'normal', '{탐색종료}')
                time.sleep(10)
                mode = 'sell'
        except:
            log = logger(log, 'critical', '탐색 오류 발생')
            log = logger(log, 'critical', traceback.format_exc())
            error_time = time.time() - error_time
            time.sleep(3)
            mode = 'search'
    elif mode == 'buy':
        try:
            log = logger(log, 'normal', '{매수}')
            log = buy1(upbit,log,found)
        except:
            log = logger(log, 'critical', '매수 오류 발생')
            log = logger(log, 'critical', traceback.format_exc())
            error_time = time.time() - error_time
        log = logger(log, 'normal', '{매수종료}')
        time.sleep(10)
        mode = 'sell'
    elif mode == 'sell':
        try:
            log = logger(log, 'normal', '{매도}')
            [sold, log] = max_min_seller(upbit,log)
            if len(sold) == 0:
                log = logger(log, 'normal', '매도한 종목 없음')
            else:
                log = logger(log, 'critical', str(sold) + ' 매도완료')
        except:
            log = logger(log, 'critical', '매도 오류 발생')
            log = logger(log, 'critical', traceback.format_exc())
            error_time = time.time() - error_time
        log = logger(log, 'normal', '{매도종료}')
        time.sleep(30)
        mode = 'search'
    else:
        log = logger(log, 'critical', '모드 설정 오류')
        sys.exit(90)
    if error_time < 300:
        log = logger(log, 'critical', '5분 이내에 에러 2번 이상 발생')
        sys.exit(91)
