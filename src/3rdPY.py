import pandas as pd
import datetime as dt
import yfinance as yf
from pandas_datareader import data as pdr
import time
from datetime import date
import random, yagmail


def sendemail(exportlist, runtime):
    Welcomelist = ["Did you sleep Well?", "Are You Ready?", "Hope this Helps:p"]
    greets = random.sample(Welcomelist, 1)[0]
    Greeting = 'Good Morning, ' + greets + ' This result took ' + str(runtime) + ' to generate today' + '\n'

    if len(exportlist) == 0:
        Greeting = "Stock Screener did not provide any quality stock pick for today."
        yagmail.SMTP('bigbullets133@gmail.com').send('alexxu98@gmail.com', str(date.today()) + '选股指标公式：操盘顾问',
                                                     Greeting)
    else:

        sendlist = []
        sendlist.append(Greeting + '\n')
        for index, element in enumerate(exportlist):
            sendlist.append(str(index + 1) + ". " + element + '\n')
        yagmail.SMTP('bigbullets133@gmail.com').send('alexxu98@gmail.com', str(date.today()) + '选股指标公式：操盘顾问',
                                                     sendlist)


start_time = time.time()
yf.pdr_override()
start = dt.datetime(2022, 3, 28)
now = dt.datetime.now()

filepath="sp500.csv"
stocklist = pd.read_csv(filepath)
exportList = []
kdjgclist = []

for i in stocklist.index:
    stock=str(stocklist["Symbol"][i])
    try:
        df = pdr.get_data_yahoo(stock,start,now)
        low_list = df['Low'].rolling(34, min_periods=34).min()
        low_list.fillna(value=df['Low'].expanding().min(), inplace=True)
        high_list = df['High'].rolling(34, min_periods=34).max()
        high_list.fillna(value=df['High'].expanding().max(), inplace=True)
        wr = round((high_list-df['Close']) / (high_list - low_list) * (-100), 3)

        df['long_mm']=round(wr.rolling(window=19).mean(),3)
        df['mm']=round(wr.ewm(com=3,adjust=True,min_periods=4).mean(),3)
        if (float(df['long_mm'][-1]) < 50 and float(df['mm'][-1]) >= float(df['long_mm'][-1]) and float(df['mm'][-2]) < float(df['long_mm'][-2])):
            exportList.append(stock)
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

sendemail(exportList,str(time.time()-start_time))
print("DavidStock P3 选股指标公式：操盘顾问 花费了"+str(time.time()-start_time)+"运行")
