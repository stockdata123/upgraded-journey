import pandas as pd
import numpy as np
from datetime import datetime

from bokeh.plotting import figure
from bokeh.io import output_notebook, show
from bokeh.models import Range1d
from bokeh.models import LinearAxis
from bokeh.models import DatetimeTickFormatter
from bokeh.models.sources import ColumnDataSource

import simpleTools


def resetIndex(df):
    startIndex =  df.index[0]
    data = df.sort_index(ascending=True, axis=0)
    columnNames = df.columns
    #new_data = pd.DataFrame(index=range(0,len(df)),columns=['Date', 'AdjClose', 'Close', 'Volume'])
    trimColumnNames = []
    for cname in columnNames:
        trimColumnNames.append(cname.replace(' ', ''))
    
    data.columns = trimColumnNames
    
    trimColumnNames.append('PreviousClose')
    trimColumnNames.append('Increased')
    new_data = pd.DataFrame(index=range(0, len(df)), columns=trimColumnNames)
        
    for i in range(0,len(data)):
        for cname in trimColumnNames:            
            if (cname == 'PreviousClose') :
                if i==0 :
                    new_data['PreviousClose'] = 0.00
                    new_data['Increased'] = 0
                else :
                    previousClose = data['Close'][i+startIndex-1].round(3)
                    currentClose = data['Close'][i+startIndex].round(3)
                    new_data['PreviousClose'][i] =  previousClose
                    priceChange = currentClose - previousClose

                    if priceChange > 0:
                        new_data['Increased'][i]=1
                    elif priceChange < 0:
                        new_data['Increased'][i]=-1
                    else:
                        new_data['Increased'][i]=0
            elif (cname != 'Increased'):
                new_data[cname][i] =  data[cname][i+startIndex]


    new_data['Date']=pd.to_datetime(new_data['Date'])
    return new_data

def getList1(df):
    newdf = resetIndex(df)
    """    newdf['day1'] = newdf.Increased + newdf.Increased.shift(1)
    newdf['day2'] = newdf.Increased + newdf.Increased.shift(1)+newdf.Increased.shift(2)
    newdf['day3'] = newdf.Increased + newdf.Increased.shift(1)+newdf.Increased.shift(2)+newdf.Increased.shift(3)
    newdf['day4'] = newdf.Increased + newdf.Increased.shift(1)+newdf.Increased.shift(2)+newdf.Increased.shift(3) + newdf.Increased.shift(4)
    """
    newdf['day5'] = newdf.Increased + newdf.Increased.shift(1)+newdf.Increased.shift(2)+newdf.Increased.shift(3) + newdf.Increased.shift(4)+newdf.Increased.shift(5)
    """    newdf['day6'] = newdf.Increased + newdf.Increased.shift(1)+newdf.Increased.shift(2)+newdf.Increased.shift(3) + newdf.Increased.shift(4) + newdf.Increased.shift(5)+newdf.Increased.shift(6)
    newdf['day7'] = newdf.Increased + newdf.Increased.shift(1)+newdf.Increased.shift(2)+newdf.Increased.shift(3) + newdf.Increased.shift(4) + newdf.Increased.shift(5)+newdf.Increased.shift(6)+newdf.Increased.shift(7)
    newdf['day8'] = newdf.Increased + newdf.Increased.shift(1)+newdf.Increased.shift(2)+newdf.Increased.shift(3) + newdf.Increased.shift(4) + newdf.Increased.shift(5)+newdf.Increased.shift(6)+newdf.Increased.shift(7)  + newdf.Increased.shift(8)
    newdf['day9'] = newdf.Increased + newdf.Increased.shift(1)+newdf.Increased.shift(2)+newdf.Increased.shift(3)+ newdf.Increased.shift(4)  + newdf.Increased.shift(5)+newdf.Increased.shift(6)+newdf.Increased.shift(7)+ newdf.Increased.shift(8)+newdf.Increased.shift(9)
    newdf['day10'] = newdf.Increased + newdf.Increased.shift(1)+newdf.Increased.shift(2)+newdf.Increased.shift(3)+ newdf.Increased.shift(4) + newdf.Increased.shift(5)+newdf.Increased.shift(6)+newdf.Increased.shift(7)+ newdf.Increased.shift(8)+newdf.Increased.shift(9)+newdf.Increased.shift(10)
    newdata = newdf[['Date', 'Close', 'day5', 'day6', 'day7', 'day8', 'day9', 'day10']]"""
    print(newdf.head(10))

def getList(df, numberOfDays):
    n =  numberOfDays
    ratio_n = 'ration_'+str(n)
    IncreasedSum_n = 'Sum_' + str(n)
    newdf = resetIndex(df)
    newlist = newdf.Increased
    if n>0 :
        for j in range(1, n+1):
            newdf['IncreasedSum'] = newlist + newdf.Increased.shift(j)        
            newlist = newdf.IncreasedSum
        
        newdf['ratio']= ( newdf.Close - newdf.Close.shift(n) )/newdf.Close
    else :       
        newdf['IncreasedSum'] = newdf.Increased
        newdf['ratio'] = 1

    #scatterdf(newdf)
    returndata = newdf[['Date', 'Close', 'ratio', 'IncreasedSum']].copy()
    returndata.rename(columns = {'ratio': ratio_n, 'IncreasedSum': IncreasedSum_n}, inplace = True)
    
    return returndata


def scatterdf(df):
    new_data = df
    p = figure(title='IncreasedTimes vs ratio', 
            plot_width=1200, 
            plot_height=800)
    p.scatter(x = new_data.ratio, y = new_data.IncreasedSum, color='green', size = 2)
    
    show(p)

def getListIncreasedSum(df):
    newdf = pd.DataFrame()
    newdf1 = pd.DataFrame()
    for i in range(10):
        if i == 0:
            newdf = getList(df, i)
        else:
            newdf1 = getList(df, i)
            newdf = pd.concat([newdf, newdf1[newdf1.columns[-2:]].copy()], axis=1)

    sumCnameList = []
    cnames = newdf.columns
    for cname in cnames:
        if 'Sum' in cname:
            sumCnameList.append(cname)
    
    rstdata = newdf.groupby(sumCnameList).count()
    print(rstdata)


def main():

    filePath = r"file:///home/lan/Documents/py3ds/DownloadData/stockcsv_20100101_20201018/TD.csv"
    #filePath = r"file:///home/lan/Documents/py3ds/DownloadData/stockcsv_19800101_20091230/UPS.csv"
    stockcsv = pd.read_csv(filePath, delimiter = ",")
    df = stockcsv[(stockcsv.Date>'2018-01-01') & (stockcsv.Date<'2020-01-01')]
    getListIncreasedSum(df)


   


if __name__ == '__main__':
    main()

        


