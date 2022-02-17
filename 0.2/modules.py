import pyupbit
import time
import traceback
from logs import *

def get_wallet(upbit):
    balances = upbit.get_balances()
    coin = []
    balance = {}
    for balan in balances:
        bal = balan['currency']
        coin.append(bal)
        if bal != 'KRW':
            balance[bal] = float(balan['balance'])
            orders = upbit.get_order('KRW-'+bal)
            for order in orders:
                if order['side'] == 'ask':
                    balance[bal] += float(order['remaining_volume'])
        else:
            balance[bal] = float(balan['balance'])
    wallet = [coin, balance]
    return wallet

def print_wallet(upbit,log):
    wallet = get_wallet(upbit)
    all_orders = get_orders(upbit)
    log = logger(log, 'normal', '#####현재보유자산#####')
    for coin in wallet[0]:
        if coin != 'KRW':
            price = pyupbit.get_current_price('KRW-' + coin)
            log = logger(log, 'normal', coin + ': ' + str(wallet[1][coin]) + ' (' + str(wallet[1][coin] * price) + ')')
            orders = all_orders[coin]
            for order in orders:
                index_list = ['uuid', 'side', 'ord_type', 'state', 'created_at', 'volume', 'remaining_volume']
                for index in index_list:
                    log = logger(log, 'normal', '  ' + index + ': ' + str(order[index]))
        else:
            log = logger(log, 'normal', coin + ': ' + str(wallet[1][coin]))
    log = logger(log, 'normal', '###################')
    return log

def get_coin_wallet(upbit):
    balances = upbit.get_balances()
    coins = []
    price = {}
    balance = {}
    order = {}
    for balan in balances:
        coin = balan['currency']
        if coin != 'KRW':
            coins.append(coin)
            balance[coin] = balan
            price[coin] = float(balan['balance'])
            orders = upbit.get_order('KRW-' + coin)
            order[coin] = orders
            for ord in orders:
                if ord['side'] == 'ask':
                    price[coin] += float(ord['remaining_volume'])
    wallet = [coins, price, balance, order]
    return wallet

def get_orders(upbit):
    all_orders = {}
    coins = get_wallet(upbit)[0][1:]
    for coin in coins:
        all_orders[coin] = upbit.get_order('KRW-' + coin)
        time.sleep(0.03)
    return all_orders

def make_buy_market_order(upbit,log,coin,amount_KRW):
    if amount_KRW > 5050:
        try:
            order = upbit.buy_market_order('KRW-' + coin, amount_KRW)
        except:
            log = logger(log, 'critical', '시장가매수 오류발생')
            log = logger(log, 'critical', traceback.format_exc())
    else:
        log = logger(log, 'critical', '최소주문금액 부족')
    return log

def make_sell_market_order(upbit,log,coin,amount_coin):
    orderbook = pyupbit.get_orderbook('KRW-' + coin)
    bids_asks = orderbook['orderbook_units']
    if upbit.get_balance(coin) >= amount_coin and amount_coin*bids_asks[0]['bid_price'] > 5050:
        try:
            sell_order = upbit.sell_market_order('KRW-' + coin, amount_coin)
            return [sell_order, log]
        except:
            log = logger(log, 'critical', coin + '  시장가매수 오류발생')
            log = logger(log, 'critical', traceback.format_exc())
    else:
        log = logger(log, 'critical', coin + '  보유코인 부족')
    return [[], log]

def make_buy_limit_order(upbit,log,coin,amount_KRW,buyat):
    if amount_KRW > 5050:
        try:
            order = upbit.buy_limit_order('KRW-' + coin, buyat, amount_KRW/buyat)
        except:
            log = logger(log, 'critical', '지정가매수 오류발생')
            log = logger(log, 'critical', traceback.format_exc())
    else:
        log = logger(log, 'critical', '최소주문금액 부족')
    return log

def make_sell_limit_order(upbit,log,coin,amount_coin,sellat):
    if upbit.get_balance(coin) >= amount_coin and amount_coin*sellat > 5050:
        try:
            order = upbit.sell_limit_order('KRW-' + coin, sellat, amount_coin)
        except:
            log = logger(log, 'critical', '지정가매수 오류발생')
            log = logger(log, 'critical', traceback.format_exc())
    else:
        log = logger(log, 'critical', '보유코인 부족')
    return log

def cancel_order(upbit,uuid):
    order = upbit.cancel_order(uuid)

def get_history(tickers,length,timeunit):
    data_list = {}
    for ticker in tickers:
        data = pyupbit.get_ohlcv(ticker=ticker, interval=timeunit, count=length)
        data_list[ticker] =data.values.tolist()
        time.sleep(0.05)
    return data_list

def get_tickers(excluded_tickers):
    tickers = pyupbit.get_tickers(fiat="KRW")
    for ticker in excluded_tickers:
        try:
            tickers.remove(ticker)
        except:
            print(ticker + ' 티커 제외 실패(또는 중복)')
    return tickers

def exclude_tickers_owned(upbit,exclude):
    wallet = get_wallet(upbit)
    excluded_tickers = exclude
    for coin in wallet[0]:
        if coin != 'KRW':
            ticker = 'KRW-' + coin
            if (ticker in excluded_tickers) == False:
                excluded_tickers.append(ticker)
    return excluded_tickers

def get_tickers_prices(tickers,indicator,length,timeunit):
    data_list = get_history(tickers, length, timeunit)
    indicators = {'open': 0, 'high': 1, 'low': 2, 'close': 3, 'volume': 4}
    indicate = indicators[indicator]
    prices = {}
    for ticker in tickers:
        price = []
        for i in range(0, length):
            try:
                price.append(data_list[ticker][i][indicate])
            except:
                price.append(0)
        prices[ticker] = price
    return prices

def get_tickers_average(tickers,indicator,length,timeunit):
    data_list = get_history(tickers,length,timeunit)
    indicators = {'open': 0, 'high': 1, 'low': 2, 'close': 3, 'volume': 4}
    indicate = indicators[indicator]
    averages = {}
    for ticker in tickers:
        average = 0
        for i in range(0, length):
            try:
                average += data_list[ticker][i][indicate]
            except:
                length -= 1
        average = average/length
        averages[ticker] = average
    return averages

def get_tickers_moving_average(tickers,indicator,length,count,timeunit):
    data_list = get_history(tickers,200,timeunit)
    indicators = {'open': 0, 'high': 1, 'low': 2, 'close': 3, 'volume': 4}
    indicate = indicators[indicator]
    moving_averages = {}
    for ticker in tickers:
        moving_average = []
        for i in range(1, count+1):
            average = 0
            for j in range(0, length):
                try:
                    average += data_list[ticker][200-count-length+i+j][indicate]
                except:
                    length -= 1
            average = average/length
            moving_average.append(average)
        moving_averages[ticker] = moving_average
    return moving_averages
