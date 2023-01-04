import pandas as pd
import datetime as dt
import yfinance as yf
from pandas_datareader import data as pdr
import time
import smtplib
from datetime import date
# Import the email modules we'll need
from email.mime.text import MIMEText
import yagmail
import random

def sendemail(exportlist,runtime):

    Welcomelist = ["Did you sleep Well?","Are You Ready?","Hope this Helps:p"]
    greets = random.sample(Welcomelist, 1)[0]
    Greeting = 'Good Morning, '+greets+' This result took '+str(runtime)+' to generate today'+'\n'

    if len(exportlist) == 0:
        Greeting = "The Stock Screener has determined that there is no appropriate stock to buy"
        yagmail.SMTP('sender@gmail.com').send('receiver@gmail.com', str(date.today())+'Stock Screen 1: KDrise', Greeting)
    else:


        sendlist=[]
        sendlist.append(Greeting+'\n')
        for index, element in enumerate(exportlist):
            sendlist.append(str(index+1) + ". " + element +'\n')
        yagmail.SMTP('sender@gmail.com').send('receiver@gmail.com', str(date.today()) + 'Stock Screen 1: KDrise', sendlist)
        
        
        
        """with open("dTodayPicks.txt","w") as wp:
            for index, element in enumerate(exportlist):
                wp.writelines(str(index) + ". " + element)
            with open("dTodayPicks.txt", 'rb') as fp:
            # Create a text/plain message
            msg = MIMEText((fp.read()).hex())
            # me == the sender's email address
            # you == the recipient's email address"""
    """
    Alternative to Email Alert Sending
    
    msg['Subject'] = Greeting +'Here it is %s' % textfile
    msg['From'] = 'from@gmail.com'
    msg['To'] = ["to@gmail.com"]

        # Send the message via our own SMTP server, but don't include the
        # envelope header.
    s = smtplib.SMTP('localhost')
    s.sendmail('sender.com', ["receiver.com"], msg.as_string())
    s.quit()
"""





start_time = time.time()
yf.pdr_override()
start = dt.datetime(2022, 1, 1)
now = dt.datetime.now()

filepath="sp500.csv"
stocklist = pd.read_csv(filepath)
exportList = []
kdjgclist = []

for i in stocklist.index:
    stock=str(stocklist["Symbol"][i])
    try:
        df = pdr.get_data_yahoo(stock,start,now)
        low_list = df['Low'].rolling(30, min_periods=30).min()
        low_list.fillna(value=df['Low'].expanding().min(), inplace=True)
        high_list = df['High'].rolling(30, min_periods=30).max()
        high_list.fillna(value=df['High'].expanding().max(), inplace=True)
        rsv = round((df['Close'] - low_list) / (high_list - low_list) * 100, 2)

        df['K'] = round(rsv.ewm(com=2, adjust=False).mean(), 3)
        df['D'] = round(df['K'].ewm(com=2, adjust=False).mean(), 3)
        if (float(df['D'][-1]) < 25 and float(df['K'][-1]) >= float(df['D'][-1]) and float(df['K'][-2]) < float(df['D'][-2])):
            exportList.append(stock)
    except Exception:
        print("No data on " + stock)


sendemail(exportList,str(time.time()-start_time))

if len(exportList) == 0:
    print("No stock you can buy")
else:
    print("{buy}")
    index = 0

    for j in exportList:
        print(str(index) + ". "+ j)
        index+=1



print("KDrise took "+str(time.time()-start_time)+" to run")
