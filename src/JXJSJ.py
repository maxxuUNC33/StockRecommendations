import pandas as pd
import datetime as dt
import yfinance as yf
from pandas_datareader import data as pdr
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from datetime import datetime
import requests
import csv
import time
from dateutil.relativedelta import relativedelta
from datetime import date
import random, yagmail


def sendemail(exportlist, runtime):
    Welcomelist = ["Did you sleep Well?", "Are You Ready?", "Hope this Helps:p"]
    greets = random.sample(Welcomelist, 1)[0]
    Greeting = 'Good Morning, ' + greets + ' This result took ' + str(runtime) + ' to generate today'

    if len(exportlist) == 0:
        Greeting = "No Stock You can Buy"
        yagmail.SMTP('bigbullets133@gmail.com').send('alexxu98@gmail.com', str(date.today()) + '均线金三角',
                                                     Greeting)
    else:

        sendlist = []
        sendlist.append(Greeting)
        print(str(len(exportlist)))
        for index, element in enumerate(exportlist,start=1):
            sendlist.append(str(index) + ". " + element )
            print (str(index))
       # yagmail.SMTP('bigbullets133@gmail.com').send('alexxu98@gmail.com', str(date.today()) + '均线金三角',
                                                     #sendlist)
        print(sendlist)




def getCsv ():
    

    """url = 'https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=3296&exchange=nyse'
    headers = { "user-agent":"Mozilla"}

    r = requests.get(url, headers=headers)

    open('NYSEstock3296Picks.csv', 'wb').write(r.content)
"""

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
    }

    url = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=3296&exchange=nasdaq"
    r = requests.get(url, headers=headers)
    j = r.json()

    table = j['data']['table']
    table_headers = table['headers']

    with open('Stocks.csv', 'w', newline='') as f_output:
        csv_output = csv.DictWriter(f_output, fieldnames=table_headers.values(), extrasaction='ignore')
        csv_output.writeheader()

        for table_row in table['rows']:
            csv_row = {table_headers.get(key, None): value for key, value in table_row.items()}
            csv_output.writerow(csv_row)


start_time = time.time()
#--print "%(id)s" > sometext.txt
getCsv()

one_yr_ago_date=datetime.now()-relativedelta(years=1)
print(one_yr_ago_date)

yf.pdr_override()
start = dt.datetime(2021,7,9)
now = dt.datetime.now()

#filepath="NYSEstock3296Picks.csv"
filepath="NYSE_screener.csv"
stocklist = pd.read_csv(filepath)
exportList = pd.DataFrame(columns=["Stock"])

for i in stocklist.index:
    stock=str(stocklist["Symbol"][i])
    try:
        df = pdr.get_data_yahoo(stock,start,now)
        smaUsed=[5,10,20]
        for x in smaUsed:
            sma=x
            df["SMA_"+str(sma)]=round(df.iloc[:,4].rolling(window=sma).mean(),3)
        moving_average_5=df["SMA_5"][-1]
        moving_average_10=df["SMA_10"][-1]
        moving_average_20=df["SMA_20"][-1]
        try:
            moving_average_10_1past=df["SMA_10"][-2]
            moving_average_20_1past=df["SMA_20"][-2]
        except Exception:
            moving_average_10_1past=0
            moving_average_20_1past=0

        if(moving_average_5>moving_average_10):
            cond1=True
        else:
            cond1=False

        if(moving_average_10>moving_average_20):
            cond2=True
        else:
            cond2=False

        if(moving_average_10_1past<moving_average_20_1past):
            cond3=True
        else:
            cond3=False
        if(cond1 and cond2 and cond3):
            exportList = exportList.append({"Stock":stock},ignore_index=True)
    except Exception:
        print("No data on " + stock)

print(exportList)
sendemail(exportList,str(time.time()-start_time))

print("DavidStock 选股指标公式 均线金三角 花费了"+str(time.time()-start_time)+"运行")