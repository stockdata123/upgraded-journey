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

from simpleTools import draw_stockdf

def mergeStockFilesTodf(*filepaths):
    dfs = []
    for filePath in filepaths:
        stockcsv = pd.read_csv(filePath, delimiter = ",")
        if (('Date' in stockcsv.columns) & ('Close' in stockcsv.columns)):
            stockcsv = pd.read_csv(filePath, delimiter = ",", parse_dates=['Date'])
            dfs.append(stockcsv)
        else:
            print(filePath,  'is not a stock csv file, it must have "Date" and "Close" columns')
            pass
        
    dfDateList = []
    if (len(dfs)>0):
        
        for df in dfs:
            df['Date']=pd.to_datetime(df['Date']) 
            dfDateList.append([df.Date.min(), df.Date.max()])
        
    firstStart = dfDateList[0][0]
    firstEnd = dfDateList[0][1]
    lastStart = dfDateList[-1][0]
    lastEnd = dfDateList[-1][1]

    dfmerged =  pd.DataFrame()    
    if ((min(dfDateList[0])== firstStart) & (max(dfDateList[1])==lastEnd) &
        (firstEnd < lastStart) & (len(dfDateList)==2)):
        dfmerged = pd.concat(dfs)


    print(dfmerged['Date'][0])
    return dfmerged

def drawdfs(dflist):
    for df in dflist:
        xColumnName = 'Date'
        yColumnName = 'Close'
        if ( 'Date' in cname for cname in df.columns) :
            #df = pd.read_csv(filePath, delimiter = ",", parse_dates=['Date'])
            startIndex = df.index[0]
            data = df.sort_index(ascending=True, axis=0)
            newColumnNames = data.columns   
            new_data = pd.DataFrame(index=range(0, len(data)), columns=newColumnNames)
            #print(newColumnNames)
            #print( df.columns)
            break
            for i in range(0,len(data)):
                for cname in newColumnNames:
                    new_data[cname][i] =  data[cname][i+startIndex]
                    

            p = figure(title='Price', 
                    plot_width=1200, 
                    plot_height=800,
                    x_axis_type='datetime')
            new_data['Date']=pd.to_datetime(new_data['Date'])  
            X = new_data['Date']
            for cName in newColumnNames:  
                if cname !='Date' :  
                    yColumnName = cName
                    df[cName] = df[cName].fillna(0)
        
            Y = df[yColumnName]
            p.line(x=X, y=Y)
        
        else:
            data_source = ColumnDataSource(df)              
            p.line(x=xColumnName, y=yColumnName, sources=data_source, line_width=1)
    
        show(p)
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
def csvdescribe(csvFilePath):
    csvdf = pd.read_csv(csvFilePath, delimiter = ',')
    
    print(csvdf[csvdf.RSI>90]['Symbol'])

def main():
    
    #filePath = r"file:///home/lan/Documents/py3ds/output/dataWatch/datawatch_RSI_2020-10-26.csv"
    #csvdescribe(filePath)
    filePath1 = r"file:///home/lan/Documents/py3ds/DownloadData/stockcsv_19800101_20091230/TD.csv"
    filePath2 = r"file:///home/lan/Documents/py3ds/DownloadData/stockcsv_20100101_20201018/TD.csv"
    df = mergeStockFilesTodf(filePath1, filePath2)
    drawdfs([df])
    #stockcsv = pd.read_csv(filePath, delimiter = ",")
    #stockcsv = pd.read_csv(filePath, delimiter = ",", parse_dates=['Date'])
    #df = stockcsv[['Date', 'MarketCap', 'MMM']]
    #df['sp500MarketCap'] = stockcsv[['MarketCap']].copy()
    #draw_MarketCapSumLine(df, ['MarketCap', 'MMM'])
    #df = stockcsv[(stockcsv.Date>'2019-01-01')]
    #draw_stockdf(df)
    #draw_MarketCap(df)
    #draw_MarketCapSum('2020-01-01', '2020-10-10')SS


if __name__ == '__main__':
    main()
   
