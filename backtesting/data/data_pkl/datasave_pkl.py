import pyupbit
import time
import os
import pickle

#과거데이터 조회
count = 2000
timeunit = 'minute30' #1,3,5,10,30,60m day week month
timesec = 30*60
os.mkdir(timeunit)

tickers = pyupbit.get_tickers(fiat="KRW")
number = len(tickers)
done = 0
for ticker in tickers:
    try:
        data = pyupbit.get_ohlcv(ticker=ticker, interval=timeunit, count=count, to=None, period=0.1)
        now = time.time() - count * timesec
        data_list = data.columns.values.tolist() + data.values.tolist()
        for i in range(6, 6 + count):
            data_list[i] = [time.strftime('%Y-%m-%d %H:%M', time.localtime(now + timesec * (i - 5)))] + data_list[i]
        with open(timeunit + '/' + ticker + '.pkl', 'wb') as f:
            pickle.dump(data_list, f)
        done += 1
        print(str(done) + '/' + str(number) + ' 완료')
    except:
        done += 1
        print(ticker + ' 저장실패')
        print(str(done) + '/' + str(number) + ' 완료')

'''with open('data_dict.pkl','rb') as f:
    mydict = pickle.load(f)'''