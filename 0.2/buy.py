import pyupbit
from modules import *
from logs import *

def buy1(upbit,log,tickers):
    for ticker in tickers:
        coin = ticker[4:]
        money = upbit.get_balance('KRW')
        if money > 680000:
            log = make_buy_market_order(upbit,log,coin,10000)
            time.sleep(2)
            #TODO 매수 가격 적기
            log = logger(log, 'critical', coin + ' 매수함')
        else:
            log = logger(log, 'critical', coin + ' 매수 보유원화부족')
            break
        time.sleep(0.3)
    return log