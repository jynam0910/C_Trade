import pyupbit
import time
from modules import *
from logs import *

def max_min_seller(upbit,log):
    wallet = get_coin_wallet(upbit)
    [coins, price, balance, order] = wallet
    if len(coins) == 0:
        log = logger(log, 'normal', '보유중인 코인이 없음')
        return [[], log]
    sold = []
    for coin in coins:
        avgbought = float(balance[coin]['avg_buy_price'])
        price = pyupbit.get_current_price('KRW-' + coin)
        amount_coin = upbit.get_balance(coin)
        min = avgbought * 0.98
        max = avgbought * 1.04
        if price > max or price < min:
            time.sleep(5)
            try:
                num_order = len(order[coin])
            except:
                num_order = -99
            time.sleep(5)
            if num_order == 1:
                uuid = order[coin][0]['uuid']
                side = order[coin][0]['side']
                ord_type = order[coin][0]['ord_type']
                if side == 'ask' and ord_type != 'limit':
                    ord = cancel_order(upbit, uuid)
                    time.sleep(0.3)
                else:
                    break
            elif num_order >= 2:
                log = logger(log, 'normal', '주문내역이 2개 이상임')
                break
            elif num_order == -99:
                log = logger(log, 'critical', '주문내역 불러오기 실패')
                break
            #TODO 매도 가격 적기
            log = logger(log, 'critical', '[매도주문]  ' + coin)
            [sell_order, log] = make_sell_market_order(upbit, log, coin, amount_coin)
            time.sleep(0.5)
            try:
                log = logger(log, 'critical', sell_order['uuid'])
                sold.append(coin)
            except:
                log = logger(log, 'critical', '주문오류, uuid 없음')
        time.sleep(0.3)
    return [sold, log]
