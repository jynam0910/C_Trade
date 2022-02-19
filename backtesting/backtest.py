import pickle
import numpy
import matplotlib.pyplot as plt

timeunit = 'minute30'
tickers = ['KRW-XRP']
for ticker in tickers:
    do_test = 0
    mean_errors = []
    while do_test != 21:
        with open('data/data_pkl/' + timeunit + '/' + ticker + '.pkl', 'rb') as f:
            data_list = pickle.load(f)
        counts = 0
        real = []
        for i in range(7, len(data_list)):
            price_dif = float(data_list[i][4]) - float(data_list[i - 1][4])
            real.append(price_dif)
            counts += 1
        mean = numpy.mean(real)
        std = numpy.std(real)
        rand_norm = numpy.random.normal(mean, std, size=counts)
        error = 0
        counts = 0
        for estimate in rand_norm:
            error += abs(real[counts] - estimate)
            counts += 1
        mean_error = error / counts
        mean_errors.append(mean_error)
        do_test += 1
    mean_mean_error = numpy.mean(mean_errors)

    with open('data/data_pkl/' + timeunit + '/' + ticker + '.pkl', 'rb') as f:
        data_list = pickle.load(f)
    errors = []
    for i in range(8, len(data_list)):
        price_dif = float(data_list[i][4]) - float(data_list[i - 1][4])
        estimate = float(data_list[i - 1][4]) - float(data_list[i - 2][4])
        error = abs(price_dif - estimate)
        errors.append(error)
    mean_error = numpy.mean(errors)

    score = (mean_mean_error - mean_error)/mean_mean_error*100
    print(timeunit, ticker)
    print('점수: ' + str(score))