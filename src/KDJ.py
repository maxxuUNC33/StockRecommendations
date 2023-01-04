import pandas as pd
import datetime as dt
import yfinance as yf
from pandas_datareader import data as pdr

import time
from datetime import date
import random,yagmail


def sendemail(exportlist, runtime):
    Welcomelist = ["Did you sleep Well?", "Are You Ready?", "Hope this Helps:p"]
    greets = random.sample(Welcomelist, 1)[0]
    Greeting = 'Good Morning, ' + greets + ' This result took ' + str(runtime) + ' to generate today' + '\n'

    if len(exportlist) == 0:
        Greeting = "The Stock Screener strategy determined that there is no appropriate stock to buy."
        yagmail.SMTP('sender@gmail.com').send('receiver@gmail.com', str(date.today()) + 'Stock Screen 2:KDJ corss', Greeting)
    else:

        sendlist = []
        sendlist.append(Greeting + '\n')
        for index, element in enumerate(exportlist):
            sendlist.append(str(index + 1) + ". " + element + '\n')
        yagmail.SMTP('sender@gmail.com').send('receiver@gmail.com', str(date.today()) + 'Stock Screen 2:KDJ corss', sendlist)


start_time = time.time()


yf.pdr_override()
start = dt.datetime(2022, 1, 1)  #date should be within 2 years, script takes too long otherwise
now = dt.datetime.now()

filepath="sp500.csv"
stocklist = pd.read_csv(filepath)
exportList = []
kdjgclist = []

for i in stocklist.index:
    stock=str(stocklist["Symbol"][i])
    try:
        df = pdr.get_data_yahoo(stock,start,now)
        low_list = df['Low'].rolling(27, min_periods=27).min()
        low_list.fillna(value=df['Low'].expanding().min(), inplace=True)
        high_list = df['High'].rolling(27, min_periods=27).max()
        high_list.fillna(value=df['High'].expanding().max(), inplace=True)
        rsv = round((df['Close'] - low_list) / (high_list - low_list) * 100, 2)

        df['K'] = round(rsv.ewm(com=2, adjust=False).mean(), 3)               # get K line data of given day given stock
        df['D'] = round(df['K'].ewm(com=2, adjust=False).mean(), 3)           # get D line data of given day given stock
        df['J'] = 3 * df['K'] - 2 * df['D']                                   # get J line data of given day given stock
        df['P'] = round(df['D'].ewm(com=2, adjust=False).mean(), 3)           # get P line data of given day given stock
        if (float(df['P'][-1]) < 30 and float(df['D'][-1]) >= float(df['P'][-1]) and float(df['D'][-2]) < float(df['P'][-2])):
            exportList.append(stock)
        if (df['J'][-1] < 65 and df['J'][-1] > df['D'][-1] and df['J'][-1] > df['K'][-1]) and (df['J'][-2] <= df['D'][-1] or df['J'][-2] <= df['K'][-2]):
            kdjgclist.append(stock)
    except Exception:
        print("No data on " + stock)

if len(exportList) == 0:
    print("No stock can buy")
else:
    print("{buy}")
    index = 0
    for j in exportList:
        print(str(index) + ". "+ j)
        index+=1

if len(kdjgclist) == 0:
    print("No stock has KDJ cross")
else:
    print("\n")
    print("{KDJ cross}")
    index = 0
    for j in kdjgclist:
        print(str(index) + ". "+ j)
        index+=1

sendemail(exportList,str(time.time()-start_time))

print("Stock Screen: KDJ cross took"+str(time.time()-start_time)+"to run")
