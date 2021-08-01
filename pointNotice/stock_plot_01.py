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

def draw_stockdf(df):
    startIndex = df.index[0]
    data = df.sort_index(ascending=True, axis=0)
    columnNames = df.columns
    #new_data = pd.DataFrame(index=range(0,len(df)),columns=['Date', 'AdjClose', 'Close', 'Volume'])
    trimColumnNames = []
    for cname in columnNames:
        trimColumnNames.append(cname.replace(' ', ''))
    
    data.columns = trimColumnNames
    data['PlotVolume'] = data.apply(lambda x: round(x['Volume']/1000000, 1), axis=1)
    
    new_data = pd.DataFrame(index=range(0, len(df)), columns=trimColumnNames)

    for i in range(0,len(data)):
        for cname in trimColumnNames:
            if cname != 'Volume' :
                new_data[cname][i] =  data[cname][i+startIndex]
            else :
                new_data[cname][i] =  data['PlotVolume'][i+startIndex]

    new_data['Date']=pd.to_datetime(new_data['Date'])

    p = figure(title='Price vs Volume trend', 
            plot_width=1200, 
            plot_height=800,
            x_axis_label='Month-Year', y_axis_label='Price', 
            x_axis_type='datetime')

    rgb = 101
    for cname in trimColumnNames:  
        if (rgb<50) :
            rgb += 17
        elif (rgb>200) :
            rgb -= 13
        else:
            pass
        rgbcolor = (rgb, rgb+25, rgb-25)
        if cname == 'Volume' :
            rgbcolor = (rgb, rgb, rgb)
            p.scatter(x = new_data.Date, y = new_data.Volume, color = 'green', size = 2)
        if cname == 'Close':
            rgbcolor = (rgb, rgb+50, rgb)
            p.scatter(x = new_data.Date, y = new_data.Close, color = 'blue', size = 5)
        if cname == 'AdjClose':
            rgbcolor = (rgb, rgb, rgb-50)
            p.scatter(x = new_data.Date, y = new_data.AdjClose, color = rgbcolor, size = 2)
        rgb += 5

    show(p)

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
                        dfcap[stocksymbol] = getMarketCapValue(stocksymbol, df)[stocksymbol]
                        dfcap['MarketCap'] = dfcap.apply(lambda x: (x['MarketCap']+x[stocksymbol]), axis=1)
                    else:
                        dfcap = getMarketCapValue(stocksymbol, df)
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

def getMarketCapValue(stocksymbol, df):
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
    p = figure(title='MarketCap', 
                plot_width=1200, 
                plot_height=800,
                x_axis_type='datetime')

    """    startIndex = df.index[0]
    data = df.sort_index(ascending=True, axis=0)
    newColumnNames = data.columns    
    new_data = pd.DataFrame(index=range(0, len(df)), columns=newColumnNames)

    for i in range(0,len(data)):
        for cname in newColumnNames:
            new_data[cname][i] =  data[cname][i+startIndex]
    """
  
    #new_data['Date']=pd.to_datetime(new_data['Date'])  
    X = df['Date']
    for stocksymbol in columnList:    
        df[stocksymbol] = df[stocksymbol].fillna(0)
        """"      
        data_source = ColumnDataSource(new_data)
        new_data['Date']=pd.to_datetime(new_data['Date']) 
        print(data_source)        """
        
        Y = df[stocksymbol]
        p.line(x=X, y=Y)
    
    """
    xlist = new_data.Date.to_list()
    for stocksymbol in columnList:  
        new_data[stocksymbol] = new_data[stocksymbol].fillna(0)
        ylist = new_data[stocksymbol].to_list() 
        #p.line(xlist, ylist)
        #p.line(x = new_data.Date, y = new_data[stocksymbol])
        p.line(x='Date', y='MarketCap', sources=data_source, line_width=1)
    """
    show(p)

def main():
    
    filePath = r"file:///home/lan/Documents/py3ds/output/MarketCapSum.csv"
    #filePath = r"file:///home/lan/Documents/py3ds/output/downloadedStockcsv/TD_Stock.csv"
    #stockcsv = pd.read_csv(filePath, delimiter = ",")
    stockcsv = pd.read_csv(filePath, delimiter = ",", parse_dates=['Date'])
    stockcsv['sp500MarketCap'] = stockcsv[['MarketCap']]
    df = stockcsv[['Date', 'sp500MarketCap', 'MMM']]
    draw_MarketCapSumLine(df, ['sp500MarketCap'])
    #df = stockcsv[(stockcsv.Date>'2019-01-01')]
    #draw_stockdf(df)
    #draw_MarketCap(df)
    #draw_MarketCapSum('2020-01-01', '2020-10-10')SS


if __name__ == '__main__':
    main()
   
