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

def main():
    
    #filePath = r"file:///home/lan/Documents/DownloadData/CNQ.csv"
    filePath = r"file:///home/lan/Documents/py3ds/output/downloadedStockcsv/TSLA_Stock.csv"
    stockcsv = pd.read_csv(filePath, delimiter = ",")
    df = stockcsv[(stockcsv.Date>'2019-01-01')]
    draw_stockdf(df)



if __name__ == '__main__':
    main()
   



"""new_data = pd.DataFrame(index=range(0,len(df)),columns=['Date', 'AdjClose', 'Close', 'Volume'])

for i in range(0,len(data)):
    new_data['Date'][i] = data['Date'][i+startIndex]
    new_data['Close'][i] = data['Close'][i+startIndex]
    new_data['AdjClose'][i] = data['Adj Close'][i+startIndex]
    new_data['Volume'][i] = round(data['Volume'][i+startIndex]/100000, 1)

#print(new_data.head())
new_data['Date']=pd.to_datetime(new_data['Date'])
#print(new_data.head())
#data_source = ColumnDataSource(new_data)

p = figure(title='Price vs Volume trend', 
           plot_width=1200, 
           plot_height=800,
           x_axis_label='Month-Year', y_axis_label='Price', 
          x_axis_type='datetime')

p.scatter(x = new_data.Date, y = new_data.Close, color = 'blue', size = 1)
p.scatter(x = new_data.Date, y = new_data.AdjClose, color = 'cyan' , size = 1)
p.line(x = new_data.Date, y = new_data.Volume, color = 'navy' )
show(p)
"""
