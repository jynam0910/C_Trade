from modules import *

#탐색전략 여러개 저장 가능 (ex. search1, search2 ...)

def search1(upbit, excluded_tickers):
    found = []
    tickers = get_tickers(excluded_tickers)
    averages_close_50_day = get_tickers_average(tickers,'close',50,'day') #1,3,5,10,30,60m day week month
    averages_close_15_day = get_tickers_average(tickers,'close',15,'day')
    for ticker in tickers:
        if averages_close_15_day[ticker] > averages_close_50_day[ticker]:
            found.append(ticker)
    return found

def search2(upbit, excluded_tickers):
    #TODO 가격이 평균선에서 와리가리치는 경우 걸러내야함
    day =100
    timeunit = 'minute30'
    found = []
    tickers = get_tickers(excluded_tickers)
    prices = get_tickers_prices(tickers,'close',day,timeunit)
    moving_average_20 = get_tickers_moving_average(tickers,'close',20,day,timeunit)
    moving_average_60 = get_tickers_moving_average(tickers,'close',60,day,timeunit)
    for ticker in tickers:
        if moving_average_20[ticker][day - 2] > prices[ticker][day - 2] and moving_average_20[ticker][day - 1] < \
                prices[ticker][day - 1] \
                and moving_average_60[ticker][day - 2] - moving_average_20[ticker][day - 2] > moving_average_60[ticker][
            day - 1] - moving_average_20[ticker][day - 1] \
                and moving_average_60[ticker][day - 1] - moving_average_20[ticker][day - 1] > 0:
            found.append(ticker)
    return found

def search3(upbit, excluded_tickers):
    day = 100
    timeunit = 'minute30'
    found = []
    tickers = get_tickers(excluded_tickers)
    prices = get_tickers_prices(tickers, 'close', day, timeunit)
    moving_average_20 = get_tickers_moving_average(tickers, 'close', 20, day, timeunit)
    #만들다 말았음