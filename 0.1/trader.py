import pyupbit
import time
import sys
from detecter import *
from buyer import *
from seller import *
import traceback


access_key = "SXNutokqUGXkTDH5C4hbmRqNRsZjyfQ0eOyc31BK"
secret_key = "WlugojbqxP8V7RiZxpY1LrxN9fc6lh84iVxoP8PX"
upbit = pyupbit.Upbit(access_key, secret_key)
print(upbit.get_balances())
print(time.ctime((time.time())) + '  로그인 성공')

#sys.stdout = open(time.ctime((time.time()))+'.txt', 'w')

status = 0
mode = 'search'
detected = []
while status == 0:
    try:
        if mode == 'search':
            #sys.stdout.close()
            #sys.stdout = open(time.ctime((time.time()))+'.txt', 'w')
            print('####################[종목탐색]####################')
            detected = detect(15, 25)  # detecter.py
            mode = 'buy'
        elif mode == 'buy':
            print('####################[매수시도]####################')
            mode = buy(detected, upbit)  # buyer.py
        elif mode == 'sell':
            print('####################[매도시도]####################')
            mode = sell(upbit)
            detected = []
        elif mode == 'no money':
            print('no money')
            time.sleep(600)
        else:
            try:
                print('##모드 에러##')
                errc = 0
                print(time.ctime((time.time())) + '  ##강제매도##')
                while len(upbit.get_balances()) != 1:
                    ticker_KRW = 'KRW-' + upbit.get_balances()[1]['currency']
                    balance = upbit.get_balances()[1]['balance']
                    orderbook = pyupbit.get_orderbook(ticker_KRW)
                    bids_asks = orderbook['orderbook_units']
                    ret = upbit.sell_limit_order(ticker_KRW, bids_asks[0]['bid_price'], balance)
                    errc += 1
                    if errc == 10:
                        break
                mode = 'search'
            except:
                status = 1
    except:
        if KeyboardInterrupt:
            print('정상종료됨')
            print(upbit.get_balances())
            sys.exit(1)
        try:
            print(traceback.format_exc())
            print('##알수없는오류##회생절차시작##')
            errc = 0
            print(time.ctime((time.time())) + '  ##강제매도##')
            while len(upbit.get_balances()) != 1:
                ticker_KRW = 'KRW-' + upbit.get_balances()[1]['currency']
                balance = upbit.get_balances()[1]['balance']
                orderbook = pyupbit.get_orderbook(ticker_KRW)
                bids_asks = orderbook['orderbook_units']
                ret = upbit.sell_limit_order(ticker_KRW, bids_asks[0]['bid_price'], balance)
                time.sleep(10)
                errc += 1
                if errc == 10:
                    break
            mode = 'search'
            print('에러로 인해 강제매도함')
        except:
            status = 1
            print('에러로 인한 강제종료')
            print(upbit.get_balances())