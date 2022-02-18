import pickle

with open('data/data_pkl/minute30/KRW-BTC.pkl','rb') as f:
    data_list = pickle.load(f)

print(data_list)