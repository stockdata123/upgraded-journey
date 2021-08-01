import os

import pandas as pd
import numpy
import yfinance as yf
from datetime import datetime
import matplotlib.pyplot as plt
import json
import pickle

todaystr = datetime.now().strftime('%Y-%m-%d')

"""table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
df = table[0]
df.to_csv('/home/lan/Documents/py3ds/output/S&P500-Info.csv')
df.to_csv("/home/lan/Documents/py3ds/output/S&P500-Symbols.csv", columns=['Symbol'])"""

def yahooSP500download():
    #dfsymbol = pd.read_csv(r'/home/lan/Documents/py3ds/output/S&P500-Symbols.csv') 
    dfsymbol = pd.read_csv(r'/home/lan/Documents/py3ds/DownloadData/stockOver10_8_10years.csv')
    dfsymbol_removeB = dfsymbol[dfsymbol['Symbol'].str.contains('.B')==False]
    stocklist = dfsymbol_removeB.Symbol.values
    print(stocklist)
    cnt = 0
    for stocksymbol in stocklist:   
        if('.B' in stocksymbol):
                continue
        else:
            try: 
                #ahoodata = yf.download(stocksymbol,'2010-01-01', todaystr)
                yahoodata = yf.download(stocksymbol,'2010-01-01', '2020-10-18')
            except:
                print(stocksymbol)

        yahoocsv = '/home/lan/Documents/py3ds/DownloadData/stockcsv_20100101_20201018/' + stocksymbol +'.csv'  
        yahoodata.to_csv(yahoocsv)
        cnt +=1
        print(cnt) 

def yahooDownloadData(filePath, startDate, endDate):
    #path = '/home/lan/Documents/py3ds/DownloadData/stockcsv_'+startDate.replace('-', '')+'_'+endDate.replace('-', '')
    #path = '/home/lan/Documents/py3ds/output/downloadedStockcsv'
    #filePath = r"file:///home/lan/Documents/py3ds/output/stockList/topstocklist.csv"
    #filePath = r"file:///home/lan/Documents/py3ds/output/stockList/stockRateWeekly.csv"
    
    #dfsymbol = pd.read_csv(r'/home/lan/Documents/py3ds/output/S&P500-Symbols.csv') 
    dfsymbol = pd.read_csv(r'/home/lan/Documents/py3ds/output/stockList/nasdaqlisted.csv', delimiter=',')
    #dfsymbol_removeB = dfsymbol[dfsymbol['Symbol'].str.contains('.B')==False]
    stockList = dfsymbol.Symbol.values
    
    with open('./stocklist.data', 'rb') as filehandle:
        # read the data as binary data stream
        stockList = pickle.load(filehandle)

    path = '/home/lan/Documents/py3ds/output/downloadedStockcsv/'
    cnt = 0
    for stocksymbol in stockList:   
        if('.B' in stocksymbol):
                continue
        else:
            try: 
                #ahoodata = yf.download(stocksymbol,'2010-01-01', todaystr)
                yahoodata = yf.download(stocksymbol, startDate, endDate)
                yahoocsv = path +'/' + stocksymbol +'.csv' 
                print(yahoocsv) 
                yahoodata.to_csv(yahoocsv)
            except:
                print('fail to dl: ', stocksymbol)
                break
        
        cnt +=1
        print(cnt) 

def yahooDownloadSingleStock(stocksymbol, startDate, endDate):
    #path = r'/home/lan/Documents/py3ds/output/downloadedStockcsv'
    path = r'/home/lan/Documents/py3ds/output/stockPrice'
    '''
    try:
        os.mkdir(path)
    except:
        print('not able creat path for ', stocksymbol)
    '''
    try: 
        print(stocksymbol)
        yahoodata = yf.download(stocksymbol, startDate, endDate)
        
    except:
        print(stocksymbol)

    yahoocsv = path+'/' + stocksymbol +'.csv'  
    #print(yahoocsv)
    yahoodata.to_csv(yahoocsv)

def main():
    #data = yf.download('TSLA','2008-01-01', todaystr)
    #data.to_csv(r'/home/lan/Documents/py3ds/output/downloadedStockcsv/'+'TSLA'+'_Stock.csv')
    #filePath = r"file:///home/lan/Documents/py3ds/output/stockList/topstocklist.csv"
    #filePath = r"file:///home/lan/Documents/py3ds/output/stockList/stockRateWeekly.csv"
    
    dfsymbol = pd.read_csv(r'/home/lan/Documents/py3ds/output/stockList/mylist.csv')  
    #dfsymbol = pd.read_csv(r'/home/lan/Documents/py3ds/output/stockList/Snp500Plus.csv', delimiter=',')
    dfsymbol_removeB = dfsymbol[dfsymbol['Symbol'].str.contains('.B')==False]
    stockList = dfsymbol_removeB.Symbol.values
    #stockList = ['CNQ.TO']
    """
    with open('stocklist.data', 'rb') as filehandle:
        # read the data as binary data stream
        stockList = pickle.load(filehandle)

    #df = stockcsv[(stockcsv['increaseCounts']== 22 ) & (stockcsv['increaseSubBuyMean']==7.63)].copy()
    
    stockList = ['AAPL', 'ABBV', 'ABT', 'ACN', 'ADBE', 'ADI', 'ADP', 'ADSK', 'AEP', 'AIG', 'ALGN', 'ALXN', 'AMAT', 'AMD', 'AMGN', 'AMT', 'AMZN', 'ANSS', 'ASML', 'ATVI', 'AVGO', 'AXP', 'BA', 'BAC', 'BIDU', 'BIIB', 'BK', 'BKNG', 'BLK', 'BMY', 'BRK.B', 'C', 'CAT', 'CDNS', 'CDW', 'CERN', 'CHKP', 'CHTR', 'CL', 'CMCSA', 'COF', 'COP', 'COST', 'CPRT', 'CRM', 'CSCO', 'CSX', 'CTAS', 'CTSH', 'CVS', 'CVX', 'DD', 'DHR', 'DIS', 'DLTR', 'DOCU', 'DOW', 'DUK', 'DXCM', 'EA', 'EBAY', 'EMR', 'EXC', 'F', 'FAST', 'FB', 'FDX', 'FISV', 'FOX', 'FOXA', 'GD', 'GE', 'GILD', 'GM', 'GOOG', 'GOOGL', 'GS', 'HD', 'HON', 'IBM', 'IDXX', 'ILMN', 'INCY', 'INTC', 'INTU', 'ISRG', 'JD', 'JNJ', 'JPM', 'KDP', 'KHC', 'KLAC', 'KO', 'LIN', 'LLY', 'LMT', 'LOW', 'LRCX', 'LULU', 'MA', 'MAR', 'MCD', 'MCHP', 'MDLZ', 'MDT', 'MELI', 'MET', 'MMM', 'MNST', 'MO', 'MRK', 'MRNA', 'MRVL', 'MS', 'MSFT', 'MTCH', 'MU', 'MXIM', 'NEE', 'NFLX', 'NKE', 'NTES', 'NVDA', 'NXPI', 'OKTA', 'ORCL', 'ORLY', 'PAYX', 'PCAR', 'PDD', 'PEP', 'PFE', 'PG', 'PM', 'PTON', 'PYPL', 'QCOM', 'REGN', 'ROST', 'RTX', 'SBUX', 'SGEN', 'SIRI', 'SNPS', 'SO', 'SPG', 'SPLK', 'SWKS', 'T', 'TCOM', 'TEAM', 'TGT', 'TMO', 'TMUS', 'TSLA', 'TXN', 'UNH', 'UNP', 'UPS', 'USB', 'V', 'VRSK', 'VRSN', 'VRTX', 'VZ', 'WBA', 'WDAY', 'WFC', 'WMT', 'XEL', 'XLNX', 'XOM', 'ZM']
    stockList = ['ARKG', 'JPM', 'AAPL', 'ENPH', 'INTC', 'GPN', 'ADSK', 'SLV', 'NEM', 'TD', 'TSLA', 'CNQ', 'MSFT', 'GOOG', 'WMT', 'CP', 'CNQ', 'TD', 'AC', 'PHM', 'HD', 'BTI', 'PM', 'SPY', 'NDX']
    
    csv_file = r'optionlist.csv'
    df = pd.read_csv(csv_file, delimiter=',')
    stockList = df.columns"""

    n = 0
    for stocksymbol in stockList:
        yahooDownloadSingleStock(stocksymbol, '2000-01-01', todaystr)
        n = n + 1
        print(n)
    
    #yahooDownloadData(filePath, '2004-01-01', todaystr)

if __name__ == "__main__":
    main()