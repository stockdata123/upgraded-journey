import glob
import os
import yfinance as yf
import pandas as pd
import math
from datetime import datetime, timedelta
import decimal

todaystr = datetime.now().strftime('%Y-%m-%d')

def smartRound(orgNum, numGap):
    minint = math.floor(orgNum/numGap)
    maxint = math.ceil(orgNum/numGap)

    if (orgNum - minint*numGap) > (maxint*numGap - orgNum):
        return maxint*numGap
    else:
        return minint*numGap

def drange(x, y, jump):
      while x < y:
        yield x
        x += jump

def getStockInfo(dfseleced):
    df = dfseleced
    data={}
    try:
        stockPrice1week = df.tail(5)           
        stockPrice1mon = df.tail(7*4)       
        stockPrice3mon = df.tail(7*12)
        stockPrice12mon = df.tail(7*53)
        stockPrice144 = df.tail(144) ##
        pastCloseAvg = round(stockPrice1mon.Close.mean(), 2)
        pastCloseAvg = round(stockPrice144.Close.mean(), 2)##
        pastMin = round(stockPrice1mon.Low.min(), 2)
        pastMax = round(stockPrice1mon.High.max(), 2)
        pastCloseStd1week = round(stockPrice1week.Close.std(), 4)
        pastCloseStd = round(stockPrice1mon.Close.std(), 4)
        pastCloseStd = round(stockPrice144.Close.std(), 4)##
        pastCloseStd3mon = round(stockPrice3mon.Close.std(), 2)
        pastCloseStd12mon = round(stockPrice12mon.Close.std(), 2)
        if(pastCloseStd1week>0):
            stdMonthtoWeek = round((pastCloseStd/pastCloseStd1week), 2)
        else:
            stdMonthtoWeek = 999.99
        
        latestDate = df.tail(1).Date.values[0]
        marketPrice = round(df.tail(1).Close.values[0], 2)
        marketHigh = round(df.tail(1).High.values[0], 2)
        marketLow = round(df.tail(1).Low.values[0], 2)
        pricegap = round((marketHigh-marketLow), 2)
        data = {
            'latestDateinCsv': latestDate,
            'stockSymbol': stockSymbol, 
            'marketPrice': marketPrice, 
            'marketHigh': marketHigh,
            'marketLow': marketLow,
            'closeMean': pastCloseAvg, 
            'closeMin': pastMin,
            'closeMax': pastMax, 
            '12monStd': pastCloseStd12mon, 
            '3monStd': pastCloseStd3mon, 
            'stdm': pastCloseStd,
            'stdw': pastCloseStd1week,
            'stdr': stdMonthtoWeek,
            'gap': pricegap

            }
        
        #print(data)                  
              
    except:
        print('outStockCSV', stockSymbol)
    return data  

def pointIndicator(marketRef, meanPrice, std):
    rst = smartRound(((marketRef-meanPrice)/std), 0.5)
    return rst


def stockStdMethod(stockSymbol, stockCsvPath, savetofile, researchFullList):
    data = []
    dataadd = 1
    rptlst = []
    try:
        df0 = pd.read_csv(stockCsvPath, delimiter = ",")
        if(len(df0)>1000):
            if researchFullList:
                df = df0.tail(2000)
            else :
                df = df0.tail(200)
            marketPrice0 = round(df['Close'].iloc[-1], 2)
            marketHigh0 = round(df['High'].iloc[-1], 2)
            marketLow0 = round(df['Low'].iloc[-1], 2)
            ##in case std too low, use minstd
            ##minstd0 = math.ceil(marketPrice0*0.02)
            ## remove minstd0, see how market behaviour 2020/02/15
            minstd0 = 0

            
            for i in range(1, len(df)):
                startPoint = -i-5*53
                
                if i==1:
                    dfs = df[startPoint:]
                    stockinfo = getStockInfo(dfs)
                    meanPrice0 = stockinfo.get('closeMean')
                    std0 = stockinfo.get('std')
                else:
                    dfs = df[startPoint:-i+1]
                    stockinfo = getStockInfo(dfs)
                    
                datatemp = [stockSymbol, stockinfo.get('latestDateinCsv'), stockinfo.get('marketPrice'), 
                max(minstd0, stockinfo.get('stdm')),  stockinfo.get('stdw'), stockinfo.get('stdr'),  stockinfo.get('closeMean'), stockinfo.get('marketHigh'), stockinfo.get('marketLow'), stockinfo.get('gap')]
                for item in datatemp:
                    if not item:
                        print(datatemp)
                        dataadd = 0
                if(dataadd):
                    data.append(datatemp)

            dfrst = pd.DataFrame(data)
            dfrst.columns = ['stockSymbol', 'Date', 'marketPrice', 'stdm', 'stdw', 'stdr', 'meanPrice', 'marketHigh', 'marketLow', 'gap']
            dfrst['buy'] = dfrst.apply(lambda x: pointIndicator(x['marketLow'],  x['meanPrice'], x['stdm']), axis=1)
            dfrst['sell'] = dfrst.apply(lambda x: pointIndicator(x['marketHigh'],  x['meanPrice'], x['stdm']), axis=1)
            #good copy
            #dfrst['buy'] = dfrst.apply(lambda x: -1 if (((x['mean']-buyadj*x['std'])>=math.floor(x['marketLow']))) else 0, axis=1)
            #dfrst['sell'] = dfrst.apply(lambda x: 1 if (((x['mean']+selladj*x['std'])<=math.ceil(x['marketHigh'])) ) else 0, axis=1
            #dfrst['buy'] = dfrst.apply(lambda x: 1 if (((x['mean']-buyadj*x['std'])<=math.ceil(x['marketHigh'])) & ((x['mean']-buyadj*x['std'])>=math.ceil(['marketLow']))) else 0, axis=1)
            #dfrst['sell'] = dfrst.apply(lambda x: 1 if (((x['mean']+selladj*x['std'])<=math.ceil(x['marketHigh'])) & ((x['mean']+selladj*x['std'])>=math.floor(['marketLow']))) else 0, axis=1)
            buy0Count = dfrst[(dfrst['buy']<=0) & (dfrst['buy']>-1)].buy.count()
            sell0Count = dfrst[(dfrst['sell']>0) & (dfrst['sell']<=1)].sell.count()
            buy1Count = dfrst[(dfrst['buy']<=-1) & (dfrst['buy']>-2)].buy.count()
            sell1Count = dfrst[(dfrst['sell']>1) & (dfrst['sell']<=2)].sell.count()
            buy2Count = dfrst[(dfrst['buy']<=-2) & (dfrst['buy']>-3)].buy.count()
            sell2Count = dfrst[(dfrst['sell']>2) & (dfrst['sell']<=3)].sell.count()
            buy3Count = dfrst[dfrst['buy']<=-3].buy.count()
            sell3Count = dfrst[dfrst['sell']>3].sell.count()
            marketPrice = round(dfrst.head(1).marketPrice.values[0], 2)
            gap = round(dfrst.head(1).gap.values[0], 2)
            stdm = round(dfrst.head(1).stdm.values[0], 2)
            zbuy = dfrst.head(1).buy.values[0]
            zsell = dfrst.head(1).sell.values[0]
            monthMean = dfrst.head(1).meanPrice.values[0]
            
            rptlst.append([stockSymbol, buy3Count, buy2Count, buy1Count, buy0Count, sell0Count, sell1Count, sell2Count, sell3Count, len(dfrst), marketPrice, gap, stdm, zbuy, zsell, monthMean])            
                
        

        if(savetofile):
            #dfrst['buy'] = dfrst.apply(lambda x: -0.5 if (((x['mean']- x['marketLow']- 0.5*x['std'])>0.5)) else 0, axis=1)
            #dfrst['sell'] = dfrst.apply(lambda x: 0.5 if (((x['marketHigh'] - x['mean'] - 0.5*x['std']) >0.5)) else 0, axis=1)
           
            dfrst['meanstdrh'] = dfrst.apply(lambda x:  round((x['meanPrice']+x['stdr']), 2), axis=1)
            dfrst['stdpre'] = dfrst['stdm'].shift(1)
            dfrst['stdnext'] = dfrst['stdm'].shift(-1)
            dfrst['stdind'] = dfrst.apply(lambda x: 1 if (x['stdm'] == max(x['stdpre'], x['stdm'], x['stdnext'])) else 0, axis=1)
                                 
            dfrst.drop(columns=['stdpre', 'stdnext'], axis=1)        
            rstpath = '/home/lan/Documents/py3ds/output/stockRpt/save/'+ stockSymbol+'_obs.csv'
            dfrst.to_csv(rstpath)

        todaybuy = dfrst.head(1).buy.values[0]
        todaysell = dfrst.head(1).sell.values[0]
        if((todaybuy<=-1) or ((todaybuy<=0) and savetofile)):                
            rstpath = '/home/lan/Documents/py3ds/output/stockRpt/buy/' + stockSymbol +str(todaybuy)+'buy.csv'
            dfrst.to_csv(rstpath)
        if(todaysell>=2):
            rstpath = '/home/lan/Documents/py3ds/output/stockRpt/sell/' + stockSymbol+'_' + str(todaysell)+'sell.csv'
            dfrst.to_csv(rstpath)
                
                #rstpath = '/home/lan/Documents/py3ds/output/stockRpt/'+ stockSymbol+'_stockRpt.csv'
                #dfrst.to_csv(rstpath)
    except:
        print(stockSymbol, '_error in stockStdMethod')
    return rptlst

def changeForecast(priceList):
    rate = 1
    price0 = priceList[0]
    for i in range(1, len(priceList)):
        rate = rate*(priceList[i]/price0)
        price0 = priceList[i] 

    if rate>1:
        adj = 1
    else:
        adj = -1 
    data = {'rate' : round(rate, 2), 'adj': adj}
    return data

def stocksChangesRate(stockList):
    rst = []
    for stockSymbol in stockList:
        stockCsvPath = r'file:///home/lan/Documents/py3ds/output/stockPrice/'+stockSymbol+'.csv'
        df = pd.read_csv(stockCsvPath, delimiter = ",")
        marketPrice = round(df['Close'].iloc[-1], 2)
        volume = df['Volume'].iloc[-1]
        marketCap = marketPrice*volume

        df0 = df.tail(200)
        halflen = round(len(df0)/2)
        dfh = df0.head(halflen)
        dft = df0.tail(halflen)
        
        firstHalfMean =  round(dfh.Close.mean(), 2)
        secondHalfMean = round(dft.Close.mean(), 2)
        changeRate = round((secondHalfMean-firstHalfMean)/firstHalfMean, 2)
        """
        if (((changeRate>0.5) & (marketCap>50000000))|((changeRate>=0.01) & (marketCap>1000000000))):
            data = [stockSymbol, firstHalfMean, secondHalfMean, changeRate, marketPrice, marketCap]
            rst.append(data)
        """
        if ((changeRate>=1) & (volume>10000000)):
            data = [stockSymbol, firstHalfMean, secondHalfMean, changeRate, marketPrice, marketCap, volume]
            rst.append(data)

       
    dfrst = pd.DataFrame(rst)
    dfrst.columns = ['stockSymbol', 'mean1', 'mean2', 'changeRate', 'marketPrice', 'marketCap', 'volume']
    rstpath = '/home/lan/Documents/py3ds/output/stockRpt/bullStocksRpt_increaed100.csv'
    dfrst.to_csv(rstpath)

       
    
    #return rptlst

def selectBullStocks(stockList):
    rst = []
    for stockSymbol in stockList:
        stockCsvPath = r'file:///home/lan/Documents/py3ds/output/stockRpt/sell/'+stockSymbol+'_sell_2021-02-06.csv'
        df = pd.read_csv(stockCsvPath, delimiter = ",")
        close = round(df['marketPrice'].iloc[0], 2)
        high = round(df['marketHigh'].iloc[0], 2)
        low = round(df['marketLow'].iloc[0], 2)
        std = round(df['std'].iloc[0], 2)
        date = df['date'].iloc[0]
        mean = round(df['mean'].iloc[0], 2)

        df0 = df.head(200)
        buycount = abs(df0.buy.sum())
        sellcount = abs(df0.sell.sum())
        if(buycount>0):
            rate = round((sellcount/buycount), 2)
        if rate>0.9:
            data = [date, stockSymbol, mean, std, high, low, close, buycount, sellcount, rate]
            rst.append(data)
       
    dfrst = pd.DataFrame(rst)
    dfrst.columns = ['Date', 'stockSymbol', 'mean', 'std', 'high', 'low', 'close', 'buy', 'sell', 'rate']
    rstpath = '/home/lan/Documents/py3ds/output/stockRpt/bullStocksRpt_bull.csv'
    dfrst.to_csv(rstpath)

       
    
    #return rptlst
def dailyStockTest(stockList):
    
    rptlst = []
    researchFullList = 0
    n=0
    for stockSymbol in stockList:
        #stockCsvPath = r'file:///home/lan/Documents/py3ds/output/downloadedStockcsv/'+stockSymbol+'.csv'
        stockCsvPath = r'file:///home/lan/Documents/py3ds/output/stockPrice/'+stockSymbol+'.csv'
        savetofile = 1
        if stockSymbol in saveStockList:
            savetofile = 1        
        rptdata = stockStdMethod(stockSymbol, stockCsvPath, savetofile, researchFullList)
        if (len(rptdata)>0):
            dfdata = pd.DataFrame(rptdata)
            if n==0:
                dfrpt = dfdata
                rptlst = rptdata
            else:
                rptlst.extend(rptdata)
            n +=1
        print(stockSymbol, '_stockAna')
   
    dfrpt = pd.DataFrame(rptlst)
    dfrpt.columns = ['stockSymbol', 'buy3std', 'bu2std', 'buy1std', 'buy0std', 'sell0std', 'sell1std', 'sell2std', 'sell3std', 'sampleSize', 'marketPrice', 'gap', 'stdm', 'zbuy', 'zsell', 'mean']
    dfrpt.to_csv('/home/lan/Documents/py3ds/output/stockRpt/_stockRpt_'+ todaystr + '.csv')

def rptFromObsCsv(stockList):
    filePath0 =  r'/home/lan/Documents/py3ds/output/stockRpt/save/'
    for stockSymbol in stockList:
        csv_file = filePath0 + stockSymbol + 'obs.csv'
        dfrst = pd.read_csv(csv_file)
        buy0Count = dfrst[(dfrst['buy']<=0) & (dfrst['buy']>-1)].buy.count()
        sell0Count = dfrst[(dfrst['sell']>0) & (dfrst['sell']<=1)].sell.count()
        buy1Count = dfrst[(dfrst['buy']<=-1) & (dfrst['buy']>-2)].buy.count()
        sell1Count = dfrst[(dfrst['sell']>1) & (dfrst['sell']<=2)].sell.count()
        buy2Count = dfrst[(dfrst['buy']<=-2) & (dfrst['buy']>-3)].buy.count()
        sell2Count = dfrst[(dfrst['sell']>2) & (dfrst['sell']<=3)].sell.count()
        buy3Count = dfrst[dfrst['buy']<=-3].buy.count()
        sell3Count = dfrst[dfrst['sell']>3].sell.count()
        marketPrice = round(dfrst.head(1).marketPrice.values[0], 2)
        gap = round(dfrst.head(1).gap.values[0], 2)
        stdm = round(dfrst.head(1).stdm.values[0], 2)
        zbuy = dfrst.head(1).buy.values[0]
        zsell = dfrst.head(1).sell.values[0]
        monthMean = dfrst.head(1).meanPrice.values[0]

if __name__ == "__main__":
    #saveStockList = ['MMC', 'MTSL', 'NVDA', 'DISCB', 'BNTX', 'NVDA', 'MMC', 'HD', 'FB', 'RH', 'ORCL', 'MVIS', 'MMC', 'XHB', 'V', 'TXN', 'STAA', 'RH', 'MSFT', 'MSCI', 'MA', 'KR', 'IYR', 'BMY', 'AMZN', 'W', 'TRMB', 'TQQQ', 'STOR', 'STAA', 'SQ', 'SPY', 'SONO', 'SIVB', 'SI', 'ROK', 'RIOT', 'REKR', 'QQQ', 'PFE', 'ORCL', 'MAMA', 'LMT']
    saveStockList = ['MSFT']
    #stockList = saveStockList

    dfsymbol = pd.read_csv(r'/home/lan/Documents/py3ds/output/stockList/mylist.csv') 
    #dfsymbol = pd.read_csv(r'/home/lan/Documents/py3ds/output/stockList/Snp500Plus.csv')
    dfsymbol_removeB = dfsymbol[dfsymbol['Symbol'].str.contains('.B')==False]
    stockList = dfsymbol_removeB.Symbol.values
    #stockList = ['WU']

    """
    csv_file = r'file:///home/lan/Documents/py3ds/optionlist.csv'
    df = pd.read_csv(csv_file, delimiter=',')
    stockList = df.columns
    stocksChangesRate(stockList)
    
    csv_file = r'file:///home/lan/Documents/py3ds/output/stockRpt/bullStocksRpt_increaed100.csv'
    df = pd.read_csv(csv_file, delimiter=',')
    stockList = df.stockSymbol
    print(stockList[:3])
    #stocksChangesRate(stockList)
    dfrpt = pd.DataFrame()"""
    #dailyStockTest(stockList)
    rptFromObsCsv(stockList)
    
    
   
    
   