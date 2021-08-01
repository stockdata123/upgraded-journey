import shutil, os
import pandas as pd
import numpy as np
from datetime import datetime

from bokeh.plotting import figure
from bokeh.io import output_notebook, show
import pandas as pd
from bokeh.models import Range1d

from bokeh.models import LinearAxis
from bokeh.models import DatetimeTickFormatter
#from bokeh.models.sources import ColumnDataSource
from bokeh.models import ColumnDataSource, HoverTool, LinearColorMapper
from bokeh.palettes import brewer, plasma
from bokeh.transform import transform

colors = ['Red', 'Green','Blue','Purple','Brown','Magenta','Tan','Cyan','Olive','Maroon','Navy','Aquamarine',
'Turquoise','Silver','Lime','Teal','Indigo','Violet','Pink','Yellow','Gray']

def draw_stockFilePath(filePath, *ycolumns):    
    df = pd.read_csv(filePath, delimiter = ",", parse_dates=['Date'])
    draw_stockdf(df, *ycolumns)

def draw_mulStockClose(dictory, startDate, endDate):
    stockNameList = []   
    adjClosePriceList = []
    n=0
    for filename in os.listdir(dictory):
        n +=1
        if filename.endswith(".csv") :
            filePath = os.path.join(dictory, filename)
            stockSymbol =  str(filename)[0:-4]
            stockNameList.append(stockSymbol)
            rfilePath = filePath
            stockcsv = pd.read_csv(rfilePath, delimiter = ",", parse_dates=['Date'])
            try:
                df = stockcsv[(stockcsv['Date']>startDate)&(stockcsv['Date']<endDate)]
                df['AdjClose'] = df['Adj Close'].copy()
                trimColumnNames = ['Date', 'AdjClose', 'Close']
                new_data = pd.DataFrame(index=range(0, len(df)), columns=trimColumnNames)
                startIndex = df.index[0]
                for i in range(0,len(df)):
                    for cname in trimColumnNames:
                        new_data[cname][i] =  df[cname][i+startIndex]
                if ( n<2 ):
                    X= new_data.Date
                    adjClosePriceList.append(new_data.AdjClose)
                else:
                    adjClosePriceList.append(new_data.AdjClose)

            except:
                print(stockSymbol)
                continue
    p = figure(title='Price', 
            plot_width=1200, 
            plot_height=800,
            x_axis_label='Month-Year', y_axis_label='Price', 
            x_axis_type='datetime')

    
    for i in range(len(adjClosePriceList)):
        Y = adjClosePriceList[i]
        source = ColumnDataSource(data=dict(x=X, y=Y))
        p.line('x','y',  source=source, legend_label= stockNameList[i], 
        line_color = colors[i] )
        #hover = HoverTool(tooltips=[('desc', '@desc')])
        

    show(p)

def draw_fromMulFiles(dictory, columnNames):
    stockNameList = []   
    dataList = []
    n=0
    for filename in os.listdir(dictory):
        n +=1
        if filename.endswith(".csv") :
            filePath = os.path.join(dictory, filename)
            stockSymbol =  str(filename)[0:-4]
            stockNameList.append(stockSymbol)
            rfilePath = filePath
            stockcsv = pd.read_csv(rfilePath, delimiter = ",", parse_dates=['Date'])
            X = stockcsv.Date
            if ( n<2 ):                
                dataList.append(stockcsv[columnNames])
            else:
                dataList.append(stockcsv[columnNames])              
    X = stockcsv.Date
    desc = stockNameList    
    p = figure(title='std', 
            plot_width=1200, 
            plot_height=800,
            x_axis_label='Month-Year', y_axis_label='Price', 
            x_axis_type='datetime')

    
    for i in range(len(dataList)):
        Y = dataList[i]
        source = ColumnDataSource(data=dict(x=X, y=Y))
        p.line('x','y',  source=source, 
        legend_label= stockNameList[i],
        line_color = colors[i] 
        )
        # hover = HoverTool(tooltips=[('desc', '@desc')])
        

    show(p)

def draw_stockdf(df, *ycolumns):
    #df = pd.read_csv(filePath, delimiter = ",", parse_dates=['Date'])
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
        if ((cname == 'Volume') & (cname in ycolumns)):
            rgbcolor = (rgb, rgb, rgb)
            p.scatter(x = new_data.Date, y = new_data.Volume, color = 'green', size = 1)
        if ((cname == 'Close') & (cname in ycolumns)):
            rgbcolor = (rgb, rgb+50, rgb)
            p.scatter(x = new_data.Date, y = new_data.Close, color = 'blue', size = 2)
        if ((cname == 'AdjClose') & (cname in ycolumns)):
            rgbcolor = (rgb, rgb, rgb-50)
            p.scatter(x = new_data.Date, y = new_data.AdjClose, color = rgbcolor, size = 1)
        rgb += 5

    show(p)

def draw_csv_withDate(stockSymbol, filePath, *ycolumns):
    df = pd.read_csv(filePath, delimiter = ",", parse_dates=['Date'])
    df['buymkt'] = df.apply(lambda x: x['buy']*5+275.00, axis=1)

    p = figure(title=stockSymbol, 
            plot_width=1200, 
            plot_height=800,
            x_axis_label='Month-Year', y_axis_label='Price', 
            x_axis_type='datetime')

    rgb = 101
    i=5
    for cname in ycolumns:  
        if (rgb<50) :
            rgb += 17
        elif (rgb>200) :
            rgb -= 13
        else:
            pass
        rgbcolor = (rgb, rgb+50, rgb)
        X=df['Date']
        Y=df[cname]
       # p.scatter(x = X, y = Y, color = rgbcolor, size = 2)
        source = ColumnDataSource(data=dict(x=X, y=Y))
       # p.line('x','y',  source=source, legend_label= cname, 
        p.line('x','y',  source=source,
        line_color = colors[i] )
        rgb += 5
        i+=1

    show(p)

def draw_csv_withoutDate(stockSymbol, filePath, *ycolumns):
    df = pd.read_csv(filePath, delimiter = ",")

    p = figure(title=stockSymbol, 
            plot_width=1200, 
            plot_height=800,
            x_axis_label= ycolumns[0], y_axis_label= ycolumns[1], 
            x_axis_type='datetime')

    
    X=df[ycolumns[0]]
    for i in range(1, len(ycolumns)):
        Y=df[ycolumns[i]]
        source = ColumnDataSource(data=dict(x=X, y=Y))
        p.scatter(x = X, y = Y, color = colors[i], size = 10)   

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

def draw_stockcsv(filePath):
    df = pd.read_csv(filePath, delimiter = ",")
    xColumnName = df.columns[0]
    yColumnName = df.columns[1]

    if ( 'Date' in cname for cname in df.columns):
        df = pd.read_csv(filePath, delimiter = ",", parse_dates=['Date'])

        startIndex = df.index[0]
        data = df.sort_index(ascending=True, axis=0)
        newColumnNames = data.columns    
        new_data = pd.DataFrame(index=range(0, len(df)), columns=newColumnNames)

        for i in range(0,len(data)):
            for cname in newColumnNames:
                new_data[cname][i] =  data[cname][i+startIndex]

        p = figure(title=filePath, 
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

def draw_anycsvWithDesc(filePath):
    df = pd.read_csv(filePath, delimiter = ",")
    list_x = df['corr'].to_list()
    list_y = df['cov'].to_list()
    desc = df['stockSymbol2'].to_list()

    source = ColumnDataSource(data=dict(x=list_x, y=list_y, desc=desc))
    hover = HoverTool(tooltips=[
    #   ("index", "$index"),
    #  ("(x,y)", "(@x, @y)"),
        ('desc', '@desc'),
    ])
    mapper = LinearColorMapper(palette=plasma(256), low=min(list_y), high=max(list_y))

    p = figure(plot_width=1200, plot_height=800, tools=[hover], title=filePath)
    p.circle('x', 'y', size=10, source=source,
            fill_color=transform('y', mapper))

    #output_file('test.html')
    show(p)

def csvdescribe(csvFilePath):
    csvdf = pd.read_csv(csvFilePath, delimiter = ',')    
    print(csvdf[csvdf.RSI>90]['Symbol'])

def draw_df_withoutDate(df, stockName, xColumnName, yColumnName):
    #df['strIndicator'] = df['indicator'].apply(str)
    p = figure(title=stockName, 
        plot_width=1200, 
        plot_height=800)    

    X = df[xColumnName]
    Y = df[yColumnName]

    colormap =  {'-1':'red', '1':'blue'}
    #colormap = {i: colors[i] for i in df.indicator.unique()}
    colors = [colormap[str(x)] for x in df.strIndicator]
    p.scatter(X, Y, color=colors )
    show(p)


def draw_listStock(stockList, filePath, *ycolumns):
    i = 0
    p = figure(title=str(stockList), 
                plot_width=1200, 
                plot_height=800,
                x_axis_label='Month-Year', y_axis_label=ycolumns[0], 
                x_axis_type='datetime')
    rgb = 1
    for stockSymbol in stockList:      
        filePath1 = filePath + stockSymbol+"_obs.csv" 
        df = pd.read_csv(filePath1, delimiter = ",", parse_dates=['Date'])
        df['buymkt'] = df.apply(lambda x: x['buy']*5+275.00, axis=1)
        j = 0
        
        for cname in ycolumns:  
            if (rgb>=20) :
                rgb -= 7
            else:
                pass
            rgbcolor = []
            X=df['Date']
            Y=df[cname]
        # p.scatter(x = X, y = Y, color = rgbcolor, size = 2)
            source = ColumnDataSource(data=dict(x=X, y=Y))
        # p.line('x','y',  source=source, legend_label= cname, 
            p.line('x','y',  source=source, legend_label=stockSymbol,
            line_color = colors[rgb] )
        rgb = rgb + 3

    show(p)

def draw_csv_definedField(stockSymbol, filePath, *ycolumns):
    filePath = filePath + stockSymbol + '_obs.csv'
    df = pd.read_csv(filePath, delimiter = ",", parse_dates=['Date'])
    df['zmean'] = df.apply(lambda x: int(x['buy']*x['meanPrice']/3.0), axis=1)

    p = figure(title=stockSymbol, 
            plot_width=1200, 
            plot_height=800,
            x_axis_label='Month-Year', y_axis_label='Price', 
            x_axis_type='datetime')

    
    c = 5
    for cname in ycolumns:  
        if (c<20) :
            c += 1
        elif (c>20) :
            c -= 3
        else:
            pass
        X=df['Date']
        Y=df[cname]
       # p.scatter(x = X, y = Y, color = rgbcolor, size = 2)
        source = ColumnDataSource(data=dict(x=X, y=Y))
       # p.line('x','y',  source=source, legend_label= cname, 
        p.line('x','y',  source=source,
        line_color = colors[c] )
      

    show(p)


def main():
    todayStr = datetime.now().strftime('%Y-%m-%d')
    stockSymbol= 'AAPL Z 60 value'
    #filePath = r"file:///home/lan/Documents/py3ds/output/stockRpt/correlation/"+stockSymbol+"_777_StdCorr.csv" 
    filePath = r"file:///home/lan/Documents/py3ds/output/stockRpt/AAPL/AAPL_ana_1999_60_real.csv"  
    #draw_csv_withDate(stockSymbol, filePath, 'corr', 'cov')
    draw_csv_withoutDate(stockSymbol, filePath, 'zdiffmean', 'zdaysmean')
    filePath = r"file:///home/lan/Documents/py3ds/output/stockRpt/save/"
    #draw_csv_definedField(stockSymbol, filePath, 'zmean', 'marketPrice')

    stockList = ['NVDA', 'MCHP', 'AAPL']
    filePath = r"file:///home/lan/Documents/py3ds/output/stockRpt/save2013-2021/"
    #draw_listStock(stockList, filePath, 'buy')


    #filePath = r"file:///home/lan/Documents/py3ds/output/dataWatch/datawatch_RSI_2020-10-26.csv"
    #csvdescribe(filePath)

    #filePath = r"/home/lan/Documents/py3ds/DownloadData/testData/CAN"
    #draw_mulStockClose(filePath, '2000-01-01', '2021-03-10')

    #filePath = r"/home/lan/Documents/py3ds/output/stockRpt/correlation/AAPL_500_roibuy.csv"
    #draw_anycsv(filePath)
    #draw_anycsvWithDesc(filePath)

    #filePath = r"/home/lan/Documents/py3ds/output/stockRpt/save/test"    
    #draw_fromMulFiles(filePath, 'buy')
    #draw_stockFilePath(filePath, 'Close', 'AdjClose')
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
   
