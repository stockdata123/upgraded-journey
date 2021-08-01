#import pandas_datareader.data as web
import os
import pandas as pd
import numpy as np
#from talib import RSI, BBANDS
import matplotlib.pyplot as plt
import yfinance as yf
import datetime as dt
import math
from collections import deque

today = dt.date.today().strftime('%Y-%m-%d')
startdate = (dt.date.today() - dt.timedelta(days=30)).strftime('%Y-%m-%d')

def getRSIList(rsiStartDate, stocksymbol, timespandays):
    startdate = (rsiStartDate- dt.timedelta(days=timespandays)).strftime('%Y-%m-%d')
    #startdate = (dt.date.today() - dt.timedelta(days=30)).strftime('%Y-%m-%d'
    df0 = yf.download(stocksymbol, startdate,today)
    timespan = timespandays

    data = df0.sort_index(ascending=True, axis=0)
    data['Date'] = data.index
    new_data = pd.DataFrame(index=range(0,len(df0)),columns=['Date', 'Close', 'Loss', 'Gain'])
    #print('27/n', new_data[:3])
    for i in range(0,len(data)):
        new_data['Date'][i] = data['Date'][i]
        new_data['Close'][i] = data['Adj Close'][i]
        if i > 0:
            if (data['Adj Close'][i-1]>data['Adj Close'][i]):
                new_data['Loss'][i] = data['Adj Close'][i-1]-data['Adj Close'][i]
                new_data['Gain'][i] = 0
            if (data['Adj Close'][i]>data['Adj Close'][i-1]):
                new_data['Gain'][i] = data['Adj Close'][i]-data['Adj Close'][i-1]
                new_data['Loss'][i] = 0
        else:
            new_data['Gain'][0] = 0
            new_data['Loss'][0] = 0

    new_data['avgGain'] = new_data['Gain'].rolling(min_periods=1, window=13).mean()
    new_data['avgLoss'] = new_data['Loss'].rolling(min_periods=1, window=13).mean()
    RSI_data = new_data[new_data['avgLoss']>0].copy()
    RSI_data['RS'] = RSI_data.apply(lambda x: (x['avgGain']/x['avgLoss']), axis=1)
    RSI_data['RSI'] = RSI_data.apply(lambda x: (100-(100/(1+x['RS']))), axis=1)
    RSI_return = RSI_data[RSI_data['Date']>=rsiStartDate].copy()

    return RSI_return

def getTodayRSI(stocksymbol, timespandays):
    startdate = (dt.date.today() - dt.timedelta(days=30)).strftime('%Y-%m-%d')
    df0 = yf.download(stocksymbol, startdate,today)
    timespan = timespandays

    data = df0.sort_index(ascending=True, axis=0)
    data['Date'] = data.index
    new_data = pd.DataFrame(index=range(0,len(df0)),columns=['Date', 'Close', 'Loss', 'Gain'])
    #print('27/n', new_data[:3])
    for i in range(0,len(data)):
        new_data['Date'][i] = data['Date'][i]
        new_data['Close'][i] = data['Adj Close'][i]
        if i > 0:
            if (data['Adj Close'][i-1]>data['Adj Close'][i]):
                new_data['Loss'][i] = data['Adj Close'][i-1]-data['Adj Close'][i]
                new_data['Gain'][i] = 0
            if (data['Adj Close'][i]>data['Adj Close'][i-1]):
                new_data['Gain'][i] = data['Adj Close'][i]-data['Adj Close'][i-1]
                new_data['Loss'][i] = 0
        else:
            new_data['Gain'][0] = 0
            new_data['Loss'][0] = 0

    new_data['avgGain'] = new_data['Gain'].rolling(min_periods=1, window=13).mean()
    new_data['avgLoss'] = new_data['Loss'].rolling(min_periods=1, window=13).mean()
    RSI_data = new_data[new_data['avgLoss']>0].copy()
    RSI_data['RS'] = RSI_data.apply(lambda x: (x['avgGain']/x['avgLoss']), axis=1)
    RSI_data['RSI'] = RSI_data.apply(lambda x: (100-(100/(1+x['RS']))), axis=1)

    todayRSI = RSI_data.RSI.tail(1).values[0]
    todayprice = data.Close.tail(1).values[0]
    yesterdayRSI = RSI_data.RSI.tail(2).values[0]
    yesterdayprice = data.Close.tail(2).values[0]
    #print(stocksymbol, todayRSI)
    todayRSI_list=[stocksymbol, yesterdayprice, todayprice, yesterdayRSI, todayRSI]

    return todayRSI_list

def main():
    '''
    stocklist = ['CNI', 'PPL', 'PBA', 'BB', 'PFE', 'AMZN', 'MSFT', 'GOOG', 'FB', 'TD', 'ALXN', 
    'TSLA', 'GLD', 'BAC', 'SLV', 'NTDOY', 'REI', 'OXY', 'WMT', 'HD', 'FANG', 'AAPL', 'CNQ', 'AEM', 
    'UVV', 'NEM', 'HD', 'WMT', 'ORG', 'SPY', 'NUGT', 'MMM']
    
    #stocklist = ['MMM'] #'MRU', 'IFC', 'LSPD', 'ELF', 'CJT']
    '''
    #dfsymbol = pd.read_csv(r'/home/lan/Documents/py3ds/output/nyse_left.csv')
    dfsymbol = pd.read_csv(r'/home/lan/Documents/py3ds/output/stockList/topstocklist.csv')
    dfsymbol['Symbol'] = dfsymbol.Symbol
    dfsymbol_removeB = dfsymbol[dfsymbol['Symbol'].str.contains('.B')==False]
    stocklist = dfsymbol_removeB.Symbol.values
  

    all_list = []
    for stock in stocklist:
        #rsi_list = []
        #rsi_list.append(stock)
        try:
            rsi = getTodayRSI(stock, 30)
            #rsi_list.append(rsi)
            all_list.append(rsi)
        except:
            continue

    df = pd.DataFrame(all_list, columns=['Symbol', 'yesterdayClosePrice', 'ClosePrice', 'yesterdayRSI', 'RSI'])
    print(df)
    savefilename = '/home/lan/Documents/py3ds/output/dataWatch/datawatch_RSI_'+today+'.csv'
    df.to_csv(savefilename)    


if __name__=='__main__':
    main()
    
    
