import pyupbit
import time

def buy(detected, upbit):
    for ticker_KRW in detected:
        orderbook = pyupbit.get_orderbook(ticker_KRW)
        bids_asks = orderbook['orderbook_units']
        buyat = bids_asks[0]['bid_price']
        result = makebuyorder(ticker_KRW, buyat, upbit)
        if result == 'BOUGHT':
            return 'sell'
    return 'search'

def makebuyorder(ticker_KRW, buyat, upbit):
    balance = upbit.get_balance('KRW')*0.999
    buy = upbit.buy_limit_order(ticker_KRW, buyat, balance/buyat)
    print(time.ctime((time.time())) + '  [매수시도]  '+ticker_KRW+'  '+str(buyat))
    tcount = 1
    time.sleep(4)
    orderbook = pyupbit.get_orderbook(ticker_KRW)
    bids_asks = orderbook['orderbook_units']
    while len(upbit.get_order(ticker_KRW)) != 0 and tcount < 4 and bids_asks[0]['ask_price'] > buyat*0.999 and bids_asks[0]['ask_price'] < buyat*1.05:
        if tcount == 1:
            print(time.ctime((time.time())) + '  [매수실패]  ' + ticker_KRW + '  ' + str(buyat))
        else:
            print(time.ctime((time.time())) + '  [매수실패]  ' + ticker_KRW + str(bids_asks[0]['ask_price']))
        try:
            order_num = buy['uuid']
            cancel = upbit.cancel_order(str(order_num))
            print(time.ctime((time.time())) + '  [미체결주문취소]')
            time.sleep(2)
        except:
            if len(upbit.get_order(ticker_KRW)) != 0:
                for order in upbit.get_order(ticker_KRW):
                    order_num = order['uuid']
                    cancel = upbit.cancel_order(str(order_num))
                    print(time.ctime((time.time())) + '  [미체결주문취소]')
                    time.sleep(2)
        buy = upbit.buy_limit_order(ticker_KRW, bids_asks[0]['ask_price'], balance/bids_asks[0]['ask_price'])
        print(time.ctime((time.time())) + '  [매수시도]  ' + ticker_KRW + '  ' + str(bids_asks[0]['ask_price']))
        tcount += 1
        time.sleep(4)
    if len(upbit.get_order(ticker_KRW)) == 0:
        if upbit.get_balance(ticker_KRW) == 0:
            print(time.ctime((time.time())) + '  [매수포기]  ' + ticker_KRW)
            return 'DID NOT BUY'
        else:
            print(time.ctime((time.time())) + '  [매수성공]')
            return 'BOUGHT'
    else:
        if len(upbit.get_order(ticker_KRW)) != 0:
            for order in upbit.get_order(ticker_KRW):
                order_num = order['uuid']
                cancel = upbit.cancel_order(str(order_num))
                print(time.ctime((time.time())) + '  [미체결주문취소]')
        print(time.ctime((time.time())) + '  [매수실패]  ' + ticker_KRW + '  ' + str(bids_asks[0]['ask_price']))
        print(time.ctime((time.time())) + '  [매수포기]  ' + ticker_KRW)
        return 'DID NOT BUY'


