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


def findRate(df, timeSpan):
    priceRate = getPriceRateList(df, timeSpan)
    npPriceRate = np.array(priceRate)
    #increaseRate = np.transpose(priceRate)
    #draw_dataArray(priceRate)
    
    try:
        increaseFilter =  np.asarray([1])
        increaseMask = np.in1d(npPriceRate[:, 0], increaseFilter)
        increasenp = npPriceRate[increaseMask]
        increaseSub = np.transpose(increasenp)

        decreaseFilter =  np.asarray([-1])
        decreaseMask = np.in1d(npPriceRate[:, 0], decreaseFilter)
        decreasenp = npPriceRate[decreaseMask]
        decreaseSub = np.transpose(decreasenp)    
        
        increaseRateAvg = round(increaseSub[1].mean(), 2)
        increaseCounts = len(increasenp)
        increaseSubBuyMean = round(increaseSub[2].mean(), 2)
        increaseSubBuyMin = round(increaseSub[2].min(), 2)
        increaseSubBuyMax = round(increaseSub[2].max(), 2)
        increaseSubSellMean = round(increaseSub[4].mean(), 2)
        increaseSubSellMin = round(increaseSub[4].min(), 2)
        increaseSubSellMax = round(increaseSub[4].max(), 2)
        
        decreaseRateAvg = round(decreaseSub[1].mean(), 2)
        decreaseCounts = len(decreasenp)
        decreaseSubSellMean = round(decreaseSub[2].mean(), 2)
        decreaseSubSellMin = round(decreaseSub[2].min(), 2)
        decreaseSubSellMax = round(decreaseSub[2].max(), 2)
        decreaseSubBuyMean = round(decreaseSub[4].mean(), 2)
        decreaseSubBuyMin = round(decreaseSub[4].min(), 2)
        decreaseSubBuyMax = round(decreaseSub[4].max(), 2)

        rateDict = {'increaseCounts': increaseCounts,  'increaseRateAvg': increaseRateAvg, 
        'increaseSubBuyMean': increaseSubBuyMean, 'increaseSubSellMean': increaseSubSellMean, 
        'increaseSubBuyMin': increaseSubBuyMin, 'increaseSubBuyMax': increaseSubBuyMax,  
        'increaseSubSellMin': increaseSubSellMin, 'increaseSubSellMax': increaseSubSellMax, 
        'decreaseCounts': decreaseCounts, 'decreaseRateAvg': decreaseRateAvg, 
        'decreaseSubBuyMean': decreaseSubBuyMean, 'decreaseSubSellMean': decreaseSubSellMean,
        'decreaseSubSellMin': decreaseSubSellMin, 'decreaseSubSellMax': decreaseSubSellMax, 
        'decreaseSubBuyMin': decreaseSubBuyMin, 'decreaseSubBuyMax': decreaseSubBuyMax}
    except:
        print('error')
        rateDict = {}

    print(rateDict)
    return rateDict


def getPriceRateList(df, timeSpan):
    startIndex =  df.index[0]
    data = df.sort_index(ascending=True, axis=0)
    columnNames = df.columns
    #new_data = pd.DataFrame(index=range(0,len(df)),columns=['Date', 'AdjClose', 'Close', 'Volume'])
    trimColumnNames = []
    for cname in columnNames:
        trimColumnNames.append(cname.replace(' ', ''))
    
    data.columns = trimColumnNames
    data['PlotVolume'] = data.apply(lambda x: round(x['Volume']/100000, 1), axis=1)
    
    new_data = pd.DataFrame(index=range(0, len(df)), columns=trimColumnNames)
        
    for i in range(0,len(data)):
        for cname in trimColumnNames:
            if cname != 'Volume' :
                new_data[cname][i] =  data[cname][i+startIndex]
            else :
                new_data[cname][i] =  data['PlotVolume'][i+startIndex]

    new_data['Date']=pd.to_datetime(new_data['Date'])

    priceRateList = []
    if timeSpan == 'Day':
        n = 2
        #print("Daily")
    if timeSpan == 'Week':
        n = 5
        #print("Weekly")
    if timeSpan == 'Month':
        n = 20
        #print("Monthly")
    if timeSpan == 'Year':
        n = 250
        #print("Yearly")
    for i in range(0,len(new_data)):
        dataChunk = new_data[i:i+n]
        newRate =  getRate(dataChunk)
        priceRateList.append(newRate)

    return priceRateList


def getRateDays(df, timeSpan):
    priceRate = getPriceRateList(df, timeSpan)
    rateDays = []
    for rowitm in priceRate:
        dfrow = {'indicator': rowitm[0], 'changeRate': rowitm[1], 'price1': rowitm[2], 
        'day1': rowitm[3], 'price2': rowitm[4], 'day2': rowitm[5]}
        rateDays.append(dfrow)
    
    dfRateDays = pd.DataFrame(rateDays)
    dfRateDays['day1'] = pd.to_datetime(dfRateDays['day1'])
    dfRateDays['day2'] = pd.to_datetime(dfRateDays['day2'])
    dfRateDays['dateDiff'] = (dfRateDays['day1']-dfRateDays['day2'])/pd.Timedelta(1, unit='d')
    dfRateDays['absdays']= dfRateDays.apply(lambda x: abs(x['dateDiff']), axis=1)
    dfRateDays['days']= dfRateDays.apply(lambda x: x['indicator']*abs(x['dateDiff']), axis=1)
    dfRateDays['realRate']= dfRateDays.apply(lambda x: x['indicator']*x['changeRate'], axis=1)
    
    dfgrpRateDays = dfRateDays.groupby(['indicator', 'changeRate', 'absdays']).size().reset_index()   
 
    #print(dfgrpRateDays)
    return dfgrpRateDays


def draw_dataArray(dataArray):
    trimColumnNames =  ['increase', 'absRate', 'minPrice', 'minDate', 'maxPrice', 'maxDate']
    new_data = pd.DataFrame(index=range(0, len(dataArray)), columns=trimColumnNames)
    

    for i in range(0,len(dataArray)-1):
        j = 0
        for cname in trimColumnNames:
            if ('Date' in cname):
                #print(i, j, dataArray[i][j])
                #new_data[cname][i] =  datetime.fromtimestamp(dataArray[i][j])
                new_data[cname][i] =  dataArray[i][j]#.strftime('%Y-%m-%D')
            else :
                #print(i, j, dataArray[i][j])
                new_data[cname][i] =  dataArray[i][j]
            j +=1

    new_data['minDate']=pd.to_datetime(new_data['minDate'])
    new_data['maxDate']=pd.to_datetime(new_data['maxDate'])


    p = figure(title='Price vs Volume trend', 
            plot_width=1200, 
            plot_height=800,
            x_axis_label='Month-Year', y_axis_label='Price', 
            x_axis_type='datetime')

    p.scatter(x = new_data.minDate, y = new_data.minPrice, color = 'green', size = 2)
    p.scatter(x = new_data.maxDate, y = new_data.maxPrice, color = 'red', size = 5)
 
    show(p)
  


def getRate(df):

    dataList =  df[['Date', 'Close']].values.tolist()
    dataListT = np.transpose(dataList)
    closeList =  dataListT[1]
    maxPrice = max(closeList)
    maxIndex = np.argmax(closeList)
    maxDate = dataList[maxIndex][0]
    minPrice = min(closeList)
    minIndex = np.argmin(closeList)
    minDate = dataList[minIndex][0]

    absRate = round(((maxPrice-minPrice)/minPrice), 4)
    increase = -1
    if (minIndex < maxIndex):
        increase = 1
    #print(increase, absRate, minPrice, minDate, maxPrice, maxDate)
    return [increase, absRate, minPrice, minDate, maxPrice, maxDate]


    """ ##use dataframe 
    minValue = df.Close.min()
    minIndex = df[df['Close']==minValue].index
    minDate = df['Date'][minIndex]
    maxValue = df.Close.max()
    maxIndex = df[df['Close']==maxValue].index
    maxDate = df['Date'][maxIndex]
    
    absRate = round(((maxPrice-minPrice)/minPrice), 4)
    increase = -1
    if (minIndex.values[0]<maxIndex.values[0]):
        increase = 1
    """


def main():

    #filePath = r"file:///home/lan/Documents/DownloadData/CNQ.csv"
    #filePath = r"file:///home/lan/Documents/py3ds/output/downloadedStockcsv/AMZN_Stock.csv"
    filePath = r"file:///home/lan/Documents/py3ds/DownloadData/stockcsv_20100101_20201018/UPS.csv"
    #filePath = r"file:///home/lan/Documents/py3ds/DownloadData/stockcsv_19800101_20091230/UPS.csv"
    stockcsv = pd.read_csv(filePath, delimiter = ",")
    #df = stockcsv[(stockcsv.Date>'2012-06-01') & (stockcsv.Date<'2013-06-01')]
    #print(df.index[0])
    #df = stockcsv[(stockcsv.Date>'2019-03-01')&(stockcsv.Date<'2020-03-01')]
    startDate='1980-05-01'
    endDate = '2021-01-01'
    df = stockcsv[(stockcsv.Date>startDate)&(stockcsv.Date<endDate)]
    stockName = filePath[-8: -4]
    print(stockName)
    #findRate(df, 'Day')
    #findRate(df, 'Week')
    #findRate(df, 'Month')
    #findRate(df, 'Year')
    timeSpan = 'Year'
    dfdays = getRateDays(df, timeSpan) 
    simpleTools.draw_df_withoutDate(dfdays, stockName+'_'+timeSpan+'_'+startDate+'-'+endDate, 'absdays', 'changeRate')




if __name__ == '__main__':
    main()

        


