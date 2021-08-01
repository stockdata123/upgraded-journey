import os
from os import path
import pandas as pd
import numpy as np

import yfinance as yf
import datetime as dt

def main():
    todaystr = dt.date.today().strftime('%Y-%m-%d')
    daynum = 5
    '''
    stockSymbolList = ['SPY', 'TD', 'GLD',  'UGXD', 'VIXY', 'TSLA', 'QQQ', 'DIA', 'CNI', 'PPL', 'PBA', 'BB', 'PFE', 'AMZN', 'MSFT', 'GOOG', 'FB', 'TD', 'ALXN', 
    'TSLA', 'GLD', 'BAC', 'SLV', 'NTDOY', 'REI', 'OXY', 'WMT', 'HD', 'FANG', 'AAPL', 'CNQ', 'AEM', 'UVV', 'NEM', 'HD', 'WMT', 'ORG', 'SPY', 'NUGT', 'MMM']
    #'VIXY', 'TSLA', , 'QQQ', 'DIA'
    '''
    stockSymbolList = ['SPY', 'CP']#,'DAL','MSFT','CNI','AC','BAC','TD','ALXN','CNQ','BABA','AMZN','TSLA','GOOG', 'NUGT', 'GLD']

    
    startDateStr = (dt.date.today() - dt.timedelta(days=1597)).strftime('%Y-%m-%d')    
    endDateStr = todaystr
    timeSpan = 'month'
    beta = getBetaList(stockSymbolList, startDateStr, endDateStr, timeSpan)
    #beta = getBetaList(stockSymbolList, '2004-02-01', '2004-08-30', timeSpan)
    dfbeta = pd.DataFrame(beta)
    dfbeta.columns = ['timespan', 'symbol', 'Roi0', 'stderr0', 'beta', 'stderr', 'ROImean', 'ROImax']
    dfbeta.to_csv(r'/home/lan/Documents/py3ds/output/dataWatch/beta_Stock_'+todaystr+'.csv')

def getBetaList(stockSymbolList, startDateStr, endDateStr, timeSpan): 
    stockSymbolList = stockSymbolList
    startDateStr = startDateStr
    endDateStr = endDateStr
    timeSpan = timeSpan

    changeRateList = []
    betalist = []

    for stockSymbol in stockSymbolList:
        startDate = pd.to_datetime(startDateStr)
        endDate = pd.to_datetime(endDateStr)

        downloadedStockFileName = '/home/lan/Documents/py3ds/output/downloadedStockcsv/'+stockSymbol+'_Stock.csv'
        downloadNew = 1
        
        if(path.exists(downloadedStockFileName)):
            try:
                df0 = pd.read_csv('/home/lan/Documents/py3ds/output/downloadedStockcsv/'+stockSymbol+'_Stock.csv')
                df0['Date'] = pd.to_datetime(df0['Date'], format='%Y-%m-%d')
                if((df0['Date'].values[0]<=startDate) and (df0['Date'].values[-1]>=endDate)):
                    df = df0[((df0['Date']>=startDate) & (df0['Date']<=endDate))].copy()
                    downloadNew = 0
            #else if ((df0['Date'].values[0]<=startDate) and (df0['Date'].values[-1]< endDate))
            except:
                print('download data')

        if (downloadNew):            
            df = pd.DataFrame(yf.download(stockSymbol, startDateStr,endDateStr))
            df.to_csv(r'/home/lan/Documents/py3ds/output/downloadedStockcsv/'+stockSymbol+'_Stock.csv')
            df['Date'] = df.index
   
        timespan = 'month'
        try:
            rateChange = getChangeRate(stockSymbol, df, timespan)
            changeRateList.append(rateChange)
        except:
            pass        
        
    for i in range(1, len(changeRateList)):
        print(changeRateList[i][0])
        try:
            beta = []
            cov = np.cov(changeRateList[0][1], changeRateList[i][1])        
            beta = [timespan, changeRateList[i][0], cov[0][0], changeRateList[0][2],  cov[0][1]/cov[0][0], cov[1][1], changeRateList[i][2], changeRateList[i][3]]
            if len(beta)!=0:
                betalist.append(beta)
        except:
            pass

    return betalist

def getChangeRate(stockSymbol, dfstockSymbol, timespan):
    if(timespan):
        timespan =  timespan
    else: 
        timespan = 'day'
    
    df = dfstockSymbol
    df['year'] = df.apply(lambda x: x['Date'].year, axis=1)
    df['month'] = df.apply(lambda x: x['Date'].month, axis=1)
    df['day'] = df.apply(lambda x: x['Date'].day, axis=1)
    df['weekofyear'] = df.apply(lambda x: (dt.date(x['year'], x['month'], x['day']).isocalendar()[1]), axis=1)
    df['weekday'] = df.apply(lambda x: (dt.date(x['year'], x['month'], x['day']).isocalendar()[2]), axis=1)
    df['yearweek'] = df.apply(lambda x: (str(x['year'])+'_'+str(x['weekofyear'])),axis=1)
    df['yearmonth'] = df.apply(lambda x: (str(x['year'])+'_'+str(x['month'])),axis=1)
    df['pClose'] = df['Close'].shift(1)
    df['change'] = df.apply(lambda x: ((x['Close']-x['pClose'])/x['pClose']), axis=1)
    df = df.dropna()
    df = df.reset_index(drop=True)    
    roi = df['change'].mean()
    maxroi =  ((df['Close'].max()-df['Close'].min())/(df['Close'].min()).round(2)
    #df.to_csv(r'/home/lan/Documents/py3ds/output/downloadedStockcsv/000_Stock.csv')
    
    #***weekly***
    new_data = pd.DataFrame(index=range(0,len(df)),columns=['yearweek', 'Close'])
    
    for i in range(0,len(df)):
        new_data['yearweek'][i] = df['yearweek'][i]
        new_data['Close'][i] = (df['Close'][i]).round(2)  
    #week_data = new_data.groupby(['yearweek'])['Close'].mean()
    week_data = pd.DataFrame(pd.to_numeric(new_data['Close']).groupby(new_data['yearweek']).mean())
    week_data['pClose'] = week_data['Close'].shift(1)
    week_data = week_data.dropna()
    week_data = week_data.reset_index(drop=True)
    week_data['change'] = week_data.apply(lambda x: (x['Close']-x['pClose'])/x['pClose'] if x['pClose']!='pClose' else 1, axis=1)
    week_roi = week_data['change'].mean()        
    week_maxroi = ((week_data['Close'].max()-week_data['Close'].min())/(week_data['Close'].min())).round(2)            
    
    #***monthly***
    m_new_data = pd.DataFrame(index=range(0,len(df)),columns=['yearmonth', 'Close'])
    for i in range(0,len(df)):
        m_new_data['yearmonth'][i] = df['yearmonth'][i]
        m_new_data['Close'][i] = (df['Close'][i]).round(2)  
    #print(m_new_data.head())
    month_data = pd.DataFrame(pd.to_numeric(m_new_data['Close']).groupby(m_new_data['yearmonth']).mean())
    month_data['pClose'] = month_data['Close'].shift(1)
    month_data = month_data.dropna()
    month_data = month_data.reset_index(drop=True)
    month_data['change'] = month_data.apply(lambda x: (x['Close']-x['pClose'])/x['pClose'] if x['pClose']!='pClose' else 1, axis=1)
    month_roi = month_data['change'].mean()
    month_maxroi = ((month_data['Close'].max()-month_data['Close'].min())/(month_data['Close'].min())).round(2) 
    maxVauleIndex = month_data.index[month_data['Close']==month_data['Close'].max()]         
    print(maxVauleIndex)
        
    if (timespan=='day'):
        stockChangeRate = [stockSymbol, df.change.values, roi, maxroi]
    if (timespan=='week'):
        stockChangeRate = [stockSymbol, week_data.change.values, week_roi, week_maxroi]
    if (timespan=='month'):
        stockChangeRate = [stockSymbol, month_data.change.values, month_roi, month_maxroi]

    return stockChangeRate
    #changeRateList.append(stockChangeRate)
'''
def getBetaList(stockSymbol, startdate, endDate, timeSpan)
    betalist = []
    for i in range(1, len(changeRateList)):
        cov = np.cov(changeRateList[0][1], changeRateList[i][1])
        beta = [changeRateList[i][0], cov[0][1]/cov[0][0], changeRateList[i][2]]
        betalist.append(beta)

    print(betalist)
'''


if __name__=='__main__':
    main()
    