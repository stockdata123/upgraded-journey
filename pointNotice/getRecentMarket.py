import pandas as pd
import numpy as np
from datetime import datetime

from bokeh.plotting import figure
from bokeh.io import output_notebook, show
import pandas as pd
from bokeh.models import Range1d

from bokeh.models import LinearAxis
from bokeh.models import DatetimeTickFormatter
from bokeh.models.sources import ColumnDataSource

todaystr = datetime.now().strftime('%Y-%m-%d')

def draw_MarketCap(df):
    startIndex = df.index[0]
    data = df.sort_index(ascending=True, axis=0)

    data['AdjClose'] = data['Adj Close'] 
    data['PlotVolume'] = data.apply(lambda x: round(x['Volume']/(10**5), 1), axis=1)
    data['MarketCap'] = data.apply(lambda x: round(x['Volume']*x['Close']/(10**7), 1), axis=1)
    
    newColumnNames = data.columns
    
    new_data = pd.DataFrame(index=range(0, len(df)), columns=newColumnNames)

    for i in range(0,len(data)):
        for cname in newColumnNames:
            new_data[cname][i] =  data[cname][i+startIndex]

    new_data['Date']=pd.to_datetime(new_data['Date'])

    p = figure(title='Price vs Volume trend', 
            plot_width=1200, 
            plot_height=800,
            x_axis_label='Month-Year', y_axis_label='Price', 
            x_axis_type='datetime')

    p.scatter(x = new_data.Date, y = new_data.MarketCap, color='red', size = 2)
    p.scatter(x = new_data.Date, y = new_data.Close, color='blue', size = 2)
    p.scatter(x = new_data.Date, y = new_data.PlotVolume, color='green', size = 2)
    
    show(p)

def draw_MarketCapSum(startDate, endDate):
    dfsymbol = pd.read_csv(r'/home/lan/Documents/py3ds/output/S&P500-Symbols.csv')
    #dfsymbol['Symbol'] = dfsymbol.symbol
    dfsymbol_removeB = dfsymbol[dfsymbol['Symbol'].str.contains('.B')==False]
    stocklist = dfsymbol_removeB.Symbol.values
    #stocklist = ['VNT', 'TD']
    cnt = 0
    dfcap = pd.DataFrame()
    validStockSymbol = []
    for stocksymbol in stocklist:   
        if('.B' in stocksymbol):
            continue
        else:
            try: 
                filePath = r'file:///home/lan/Documents/py3ds/output/downloadedStockcsv/'+ stocksymbol +'_Stock.csv' 
                stockcsv = pd.read_csv(filePath, delimiter = ",")
                stockcsv['Date']=pd.to_datetime(stockcsv['Date'])
                if (stockcsv.Date[0]< pd.to_datetime(startDate)): 
                    df = stockcsv[(stockcsv.Date>startDate)&(stockcsv.Date<=endDate)]
                    if (len(dfcap)>0):
                        dfcap[stocksymbol] = getStockMarketCapValue(stocksymbol, df)[stocksymbol]
                        dfcap['MarketCap'] = dfcap.apply(lambda x: (x['MarketCap']+x[stocksymbol]), axis=1)
                    else:
                        dfcap = getStockMarketCapValue(stocksymbol, df)
                    validStockSymbol.append(stocksymbol)
            except:
                print("exception", stocksymbol)
        cnt +=1
    
    print('stockNum:', cnt)

    if(len(dfcap)>0):
        dfcap.to_csv(r'/home/lan/Documents/py3ds/output/MarketCapSum.csv')
        new_data = dfcap
        new_data['Date']=pd.to_datetime(new_data['Date'])
        p = figure(title='Price vs Volume trend', 
                plot_width=1200, 
                plot_height=800,
                x_axis_label='Month-Year', y_axis_label='Price', 
                x_axis_type='datetime')

        p.scatter(x = new_data.Date, y = new_data.MarketCap, color='red', size = 2)
        for stocksymbol in validStockSymbol:   
            p.scatter(x = new_data.Date, y = new_data[stocksymbol], size = 2)

        show(p)

def getStockMarketCapValue(stocksymbol, df):
    startIndex = df.index[0]
    data = df.sort_index(ascending=True, axis=0)
    data['MarketCap'] = data.apply(lambda x: round(x['Volume']*x['Close']/(10**6), 1), axis=1)
    
    newColumnNames = ['Date', 'MarketCap']    
    new_data = pd.DataFrame(index=range(0, len(df)), columns=newColumnNames)

    for i in range(0,len(data)):
        for cname in newColumnNames:
            new_data[cname][i] =  data[cname][i+startIndex]
    new_data['Date'] = pd.to_datetime(new_data['Date'])
    new_data[stocksymbol] = new_data['MarketCap']
    return new_data

def draw_MarketCapSumLine(df, columnList):
    p = figure(title=columnList[0], 
                plot_width=1200, 
                plot_height=800,
                x_axis_type='datetime')

    X = df['Date']
    for stocksymbol in columnList: 
        if (stocksymbol!='Date'):  
        #df[stocksymbol] = df[stocksymbol].fillna(0)
            Y = df[stocksymbol]
        #p.line(x=X, y=Y)
            #p.line(x = X, y = Y)
            p.scatter(x = X, y = Y, size = 2)
    show(p)

def getAllStockMarketCapSumcsv(startDate, endDate):
    dfsymbol = pd.read_csv(r'/home/lan/Documents/py3ds/DownloadData/stocklist.csv')
    dfsymbol_removeB = dfsymbol[dfsymbol['Symbol'].str.contains('.B')==False]
    stocklist = dfsymbol_removeB.Symbol.values
    cnt = 0
    dfcap = pd.DataFrame()
    validStockSymbol = []
    for stocksymbol in stocklist:   
        try: 
            filePath = r'file:///home/lan/Documents/py3ds/DownloadData/stockcsv_20100101_20201018/'+ stocksymbol +'.csv' 
            stockcsv = pd.read_csv(filePath, delimiter = ",")
            stockcsv['Date']=pd.to_datetime(stockcsv['Date'])
            if (stockcsv.Date[0]< pd.to_datetime(startDate)): 
                df = stockcsv[(stockcsv.Date>startDate)&(stockcsv.Date<=endDate)]
                if (len(dfcap)>0):
                    dfcap[stocksymbol] = getStockMarketCapValue(stocksymbol, df)[stocksymbol]
                    dfcap['MarketCap'] = dfcap.apply(lambda x: (x['MarketCap']+x[stocksymbol]), axis=1)
                else:
                    dfcap = getStockMarketCapValue(stocksymbol, df)
                    
            validStockSymbol.append(stocksymbol)
        except:
                print("exception", stocksymbol)

        cnt +=1 
        print(cnt)

    dfcap.to_csv(r'/home/lan/Documents/py3ds/output/allStockMarketCapSum.csv')
    print('compelete!')

def getTopMarketCapTopList(stockMarketCapCsvPath, topnum):
    #filePath = r"file:///home/lan/Documents/py3ds/output/allStockMarketCapSum.csv"
    stockcsv = pd.read_csv(stockMarketCapCsvPath, delimiter = ",", parse_dates=['Date'])
    stockcsv.fillna(0)
    marketCapList = []
    cnt = 0
    for label, content in stockcsv.items():
        if (cnt>1):
            if (label!='Date' and label!='MarketCap'):
                if content[-1:].values>1 :
                    marketCapList.append([label, content[-1:].values[0]])                    
        cnt +=1

       
    sortMarketCapList = sorted(marketCapList, key=lambda x: x[1], reverse=True)
    topMarketCapStocks = pd.DataFrame(sortMarketCapList[:topnum])
    topMarketCapStocks.columns = ['Symbol', 'MarketCap']
    topMarketCapStocks.to_csv(r'/home/lan/Documents/py3ds/output/topMarketCapStocks.csv')  
        


def main():
    
    #getAllStockMarketCapSumcsv('2020-01-01', '2020-10-10')
    #filePath = r"file:///home/lan/Documents/py3ds/output/500MarketCapSum.csv"
    marketCapSumfilePath = r"file:///home/lan/Documents/py3ds/output/allStockMarketCapSum.csv"
    marketCapdf = pd.read_csv(marketCapSumfilePath, delimiter = ",", parse_dates=['Date'])
    stocklistPath = r"file:///home/lan/Documents/py3ds/output/topMarketCapStocks.csv"
    
    stocklistdf = pd.read_csv(stocklistPath, delimiter = ",")[['Symbol']].values[:50]
    stocklist = []
    for stock in stocklistdf:
        stocklist.append(stock[0])
    print(stocklist)
    stocklist.append('Date')
    #stocklist.append('MarketCap')
    df = marketCapdf.loc[:, marketCapdf.columns.isin(stocklist)]

    draw_MarketCapSumLine(df, stocklist)

    """filePath = r"file:///home/lan/Documents/py3ds/output/500MarketCapSum.csv"
    #filePath = r"file:///home/lan/Documents/py3ds/output/downloadedStockcsv/TD_Stock.csv"
    #stockcsv = pd.read_csv(filePath, delimiter = ",")
    stockcsv = pd.read_csv(filePath, delimiter = ",", parse_dates=['Date'])
    stockcsv['sp500MarketCap'] = stockcsv[['MarketCap']]
    df = stockcsv[['Date', 'sp500MarketCap', 'MMM']]
    draw_MarketCapSumLine(df, ['sp500MarketCap'])
   
    #draw_stockdf(df)
    #draw_MarketCap(df)
    #draw_MarketCapSum('2020-01-01', '2020-10-10')"""
    #getTopMarketCapTopList(filePath, 100)


if __name__ == '__main__':
    main()
   
