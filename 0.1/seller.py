import pyupbit
import time

def sell(upbit):
    time.sleep(3)
    ticker_KRW = 'KRW-' + upbit.get_balances()[1]['currency']
    balance = upbit.get_balances()[1]['balance']
    boughtat = float(upbit.get_balances()[1]['avg_buy_price'])
    minline = boughtat*0.996
    starttime = time.time()
    while time.time() - starttime < 180:
        orderbook = pyupbit.get_orderbook(ticker_KRW)
        bids_asks = orderbook['orderbook_units']
        if float(bids_asks[0]['bid_price']) > boughtat*1.011 or float(bids_asks[0]['bid_price']) < minline:
            ret = upbit.sell_limit_order(ticker_KRW, bids_asks[0]['bid_price'], balance)
            print(time.ctime((time.time())) + '  [매도주문]  ' + ticker_KRW + '  ' + str(bids_asks[0]['bid_price']))
            time.sleep(10)
            errc = 0
            while len(upbit.get_order(ticker_KRW)) != 0:
                for order in upbit.get_order(ticker_KRW):
                    order_num = order['uuid']
                    cancel = upbit.cancel_order(str(order_num))
                    print(time.ctime((time.time())) + '  [미체결주문취소]  '+str(errc))
                    time.sleep(2)
                    orderbook = pyupbit.get_orderbook(ticker_KRW)
                    bids_asks = orderbook['orderbook_units']
                    ret = upbit.sell_limit_order(ticker_KRW, bids_asks[0]['bid_price'], balance)
                    print(time.ctime((time.time())) + '  [매도주문]  ' + ticker_KRW + '  ' + str(bids_asks[0]['bid_price']))
                    time.sleep(10)
                errc += 1
                if errc == 10:
                    return 'error'
            else:
                print(time.ctime((time.time())) + '  [매도완료]  '+ticker_KRW)
                return 'search'
        else:
            print(time.ctime((time.time())) + '  [매도대기]  ' + ticker_KRW + '  구매가:' +
                  upbit.get_balances()[1]['avg_buy_price'] + '  현재가:' + str(pyupbit.get_current_price(ticker_KRW)) +
                  '(' + str(float(pyupbit.get_current_price(ticker_KRW))/float(upbit.get_balances()[1]['avg_buy_price'])) + ')' +
                  '  호가1호:' + str(bids_asks[0]['ask_price']) + ',' + str(bids_asks[0]['bid_price']))
            time.sleep(10)
    print(time.ctime((time.time())) + '  [시간초과로인한 매도]')
    orderbook = pyupbit.get_orderbook(ticker_KRW)
    bids_asks = orderbook['orderbook_units']
    ret = upbit.sell_limit_order(ticker_KRW, bids_asks[0]['bid_price'], balance)
    print(time.ctime((time.time())) + '  [매도주문]  ' + ticker_KRW + '  ' + str(bids_asks[0]['bid_price']))
    time.sleep(10)
    errc = 0
    while len(upbit.get_order(ticker_KRW)) != 0:
        for order in upbit.get_order(ticker_KRW):
            order_num = order['uuid']
            cancel = upbit.cancel_order(str(order_num))
            print(time.ctime((time.time())) + '  [미체결주문취소]  '+str(errc))
            time.sleep(2)
            orderbook = pyupbit.get_orderbook(ticker_KRW)
            bids_asks = orderbook['orderbook_units']
            ret = upbit.sell_limit_order(ticker_KRW, bids_asks[0]['bid_price'], balance)
            print(time.ctime((time.time())) + '  [매도주문]  ' + ticker_KRW + '  ' + str(bids_asks[0]['bid_price']))
            time.sleep(10)
        errc += 1
        if errc == 10:
            return 'error'
    else:
        print(time.ctime((time.time())) + '  [매도완료]  '+ticker_KRW)
    return 'search'


