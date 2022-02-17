import pyupbit
import time

def detect(avgcount, maxcount):
    detecter_status = 0
    detected = []
    while detecter_status == 0:
        if (time.gmtime((time.time())).tm_min) % 5 >= 3:
            print(time.ctime((time.time())) + '  searching...')
            tickers_KRW = pyupbit.get_tickers(fiat="KRW")
            for ticker_KRW in tickers_KRW:
                try:
                    data = pyupbit.get_ohlcv(ticker=ticker_KRW, interval="minute5", count=avgcount + 1)
                    data_list = data.columns.values.tolist() + data.values.tolist()
                    volsum = 0
                    for i in range(6, 6 + avgcount):
                        volsum += data_list[i][4]
                    avgvol = volsum / avgcount
                    volnow = data_list[avgcount + 6][4]
                    pdifrate = (data_list[avgcount + 6][3] - data_list[avgcount + 6][0]) / data_list[avgcount + 6][0]
                    if volnow > avgvol * 5 and pdifrate > 0.002:
                        data = pyupbit.get_ohlcv(ticker=ticker_KRW, interval="minute5", count=maxcount + 1)
                        data_list = data.columns.values.tolist() + data.values.tolist()
                        vollist = []
                        for i in range(6, 6 + maxcount):
                            vollist.append(data_list[i][4])
                        if volnow > max(vollist):
                            orderbook = pyupbit.get_orderbook(ticker_KRW)
                            bids_asks = orderbook['orderbook_units']
                            if bids_asks[0]['bid_price']*1.01 > bids_asks[0]['ask_price']:
                                print('  ' + ticker_KRW + '  ' + str(avgvol) + '  ' + str(volnow) + '  ' + str(volnow / avgvol) + '  ' + str(pdifrate))
                                detected.append(ticker_KRW)
                                return detected
                except:
                    print(time.ctime((time.time())) + ticker_KRW + ' 종목 불러오기 실패 (*searching 중에는 종료하지마세요)')
                time.sleep(0.04)
            if len(detected) != 0:
                detecter_status = 1
        else:
            print(time.ctime((time.time())) + '  stanby...')
            slpt = 180 - (int((time.time()))%300) + 1
            time.sleep(slpt)
    return detected