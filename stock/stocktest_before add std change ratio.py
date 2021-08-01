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
        stockPrice1mon = df.tail(7*4)       
        stockPrice3mon = df.tail(7*12)
        stockPrice12mon = df.tail(7*53)
        pastCloseAvg = round(stockPrice1mon.Close.mean(), 2)
        pastMin = round(stockPrice1mon.Low.min(), 2)
        pastMax = round(stockPrice1mon.High.max(), 2)
        pastCloseStd = round(stockPrice1mon.Close.std(), 2)
        pastCloseStd3mon = round(stockPrice3mon.Close.std(), 2)
        pastCloseStd12mon = round(stockPrice12mon.Close.std(), 2)
        
        latestDate = df.tail(1).Date.values[0]
        marketPrice = round(df.tail(1).Close.values[0], 2)
        marketHigh = round(df.tail(1).High.values[0], 2)
        marketLow = round(df.tail(1).Low.values[0], 2)

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
            'std': pastCloseStd
            }
        
        #print(data)                  
              
    except:
        print('outStockCSV', stockSymbol)
    return data  

def pointIndicator(marketRef, meanPrice, std):
    rst = smartRound(((marketRef-meanPrice)/std), 0.5)
    return rst


def stockStdMethod(stockSymbol, stockCsvPath, savetofile):
    df0 = pd.read_csv(stockCsvPath, delimiter = ",")
    df = df0.tail(300)
    marketPrice0 = round(df['Close'].iloc[-1], 2)
    marketHigh0 = round(df['High'].iloc[-1], 2)
    marketLow0 = round(df['Low'].iloc[-1], 2)
    ##in case std too low, use minstd
    ##minstd0 = math.ceil(marketPrice0*0.02)
    ## remove minstd0, see how market behaviour 2020/02/15
    minstd0 = 0

    data = []
    dataadd = 1
    rptlst = []
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
        max(minstd0, stockinfo.get('std')), stockinfo.get('closeMean'), stockinfo.get('marketHigh'), stockinfo.get('marketLow')]
        for item in datatemp:
            if not item:
                print(datatemp)
                dataadd = 0
        if(dataadd):
            data.append(datatemp)

    
    buyadj = 0.1
    selladj = 1.0
    for buya in drange(0.1, 1.5, 0.1):
        buyadj = round(buya, 1)
        for sella in drange(1.0, 3.0, 0.2):
            selladj = round(sella, 1)
            dfrst = pd.DataFrame(data)
            dfrst.columns = ['stockSymbol', 'date', 'marketPrice', 'std', 'mean', 'marketHigh', 'marketLow']
            dfrst['buy'] = dfrst.apply(lambda x: -1 if ((abs(x['mean']- buyadj*x['std'] - x['marketLow'])<=0.5) | ((x['mean']-buyadj*x['std'] - x['marketLow'])>0.5)) else 0, axis=1)
            dfrst['sell'] = dfrst.apply(lambda x: 1 if ((abs(x['mean']+selladj*x['std'] - x['marketHigh'])<=0.5) | ((x['marketHigh'] - x['mean'] - selladj*x['std']) >0.5)) else 0, axis=1)
            #good copy
            #dfrst['buy'] = dfrst.apply(lambda x: -1 if (((x['mean']-buyadj*x['std'])>=math.floor(x['marketLow']))) else 0, axis=1)
            #dfrst['sell'] = dfrst.apply(lambda x: 1 if (((x['mean']+selladj*x['std'])<=math.ceil(x['marketHigh'])) ) else 0, axis=1
            #dfrst['buy'] = dfrst.apply(lambda x: 1 if (((x['mean']-buyadj*x['std'])<=math.ceil(x['marketHigh'])) & ((x['mean']-buyadj*x['std'])>=math.ceil(x['marketLow']))) else 0, axis=1)
            #dfrst['sell'] = dfrst.apply(lambda x: 1 if (((x['mean']+selladj*x['std'])<=math.ceil(x['marketHigh'])) & ((x['mean']+selladj*x['std'])>=math.floor(x['marketLow']))) else 0, axis=1)
            buyCount = abs(dfrst.buy.sum()) 
            sellCount = max(abs(dfrst.sell.sum()), 1) 
            
            buySellCountRatio = round(buyCount/sellCount, 2)
           
            if(abs(buySellCountRatio-1)<0.5):
                rptlst.append([stockSymbol, buyadj, selladj, dfrst.buy.sum(), dfrst.sell.sum(), len(dfrst), marketPrice0])            
        
    
    
    if(savetofile):
        #dfrst['buy'] = dfrst.apply(lambda x: -0.5 if (((x['mean']- x['marketLow']- 0.5*x['std'])>0.5)) else 0, axis=1)
        #dfrst['sell'] = dfrst.apply(lambda x: 0.5 if (((x['marketHigh'] - x['mean'] - 0.5*x['std']) >0.5)) else 0, axis=1)
        dfrst['buy'] = dfrst.apply(lambda x: pointIndicator(x['marketLow'],  x['mean'], x['std']), axis=1)
        dfrst['sell'] = dfrst.apply(lambda x: pointIndicator(x['marketHigh'],  x['mean'], x['std']), axis=1)
        dfrst['stdpre'] = dfrst['std'].shift(1)
        dfrst['stdnext'] = dfrst['std'].shift(-1)
        dfrst['stdind'] = dfrst.apply(lambda x: 1 if (x['std'] == max(x['stdpre'], x['std'], x['stdnext'])) else 0, axis=1)
        dfrst.drop(columns=['stdpre', 'stdnext'], axis=1)        
        rstpath = '/home/lan/Documents/py3ds/output/stockRpt/save/'+ stockSymbol+'_save_.csv'
        dfrst.to_csv(rstpath)
    else: 
        if((meanPrice0-marketLow0 - 0.5*std0)>0.5):
            dfrst['buy'] = dfrst.apply(lambda x: -1 if (((x['mean']- x['marketLow'])>0.5)) else 0, axis=1)
            dfrst['sell'] = dfrst.apply(lambda x: 1 if (((x['marketHigh'] - x['mean'] - x['std']) >0.5)) else 0, axis=1)
            rstpath = '/home/lan/Documents/py3ds/output/stockRpt/buy/'+ stockSymbol+'_buy_'+todaystr+'.csv'
            dfrst.to_csv(rstpath)
        if((marketHigh0-meanPrice0-1.5*std0)>0.5):
            dfrst['buy'] = dfrst.apply(lambda x: -1 if (((x['mean']- x['marketLow'])>0.5)) else 0, axis=1)
            dfrst['sell'] = dfrst.apply(lambda x: 1 if (((x['marketHigh'] - x['mean'] - x['std']) >0.5)) else 0, axis=1)
            rstpath = '/home/lan/Documents/py3ds/output/stockRpt/sell/'+ stockSymbol+'_sell_'+todaystr+'.csv'
            dfrst.to_csv(rstpath)
            
            #rstpath = '/home/lan/Documents/py3ds/output/stockRpt/'+ stockSymbol+'_stockRpt.csv'
            #dfrst.to_csv(rstpath)
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


if __name__ == "__main__":
    stockList = ['AMZN','AAPL', 'ALXN', 'JPM', 'QQQ', 'MSFT',  'SPY', 'ERIC', 'TSLA', 'BIP', 'AEM',  'GLD', 'RIO', 'WMT', 'HD', 'HOME',
    'CNQ', 'FANG', 'PFE',  'AMD', 'LLY',  'V', 'MA', 'PINS', 'GOOG', 'KL', 'CNI', 'CP', 'TD', 'APHA', 'TLRY','SLV', 'NVAX', 'FANG', 'AEZS',
    'TRIL', 'VCYT', 'CLNE', 'BNTX', 'MRNA', 'HIMX']  
    stockList = ['AAPL', 'AEM', 'AEZS','ALGN', 'ALXN', 'AMBA', 'AMD', 'AMZN', 'APHA', 'APPN', 'APPS', 'ARWR', 'ARKG', 'ARKW', 'ARKF', 'ARKQ', 'ATOM',
     'ATVI', 'AUVI', 'BEAM', 'BIDU', 
    'BILI', 'BIP', 'BLMN', 'BNTX','CLNE', 'CNI', 'CNQ', 'CP', 'CRM', 'CRNC', 'CZR', 'DKNG', 'ERIC', 'ETSY', 'EXPI', 'FANG', 'FCEL', 'FLGT', 
     'FUV', 'GLD', 'GOOG', 'GOOGL', 'GRWG', 'HD', 'HIMX', 'HOME', 'IBB', 'IDEX', 'ILMN', 'IWM', 'IYR', 'JG', 'JPM', 'KL', 'KOPN', 
     'LLY', 'MA', 'MGNI', 'MOOV', 'MRK', 'MRNA', 'MSFT', 'MSTR', 'MVIS', 'NVAX', 'NVDA', 'PDD', 'PENN', 'PERI', 'PFE', 'PINS', 'PLAY', 'PYPL', 'QCOM',
      'QQQ', 'QTRX', 'RDFN', 'REKR', 'RIDE', 'RIO', 'RIOT', 'SHOP', 'SIVB', 'SLV',  'SONO', 'SPY', 'STAA', 'STNE', 'TD', 'TDOC', 'TGTX',
       'TIGR', 'TLRY', 'TLT', 'TNA', 'TQQQ', 'TTOO','TRIL', 'TSLA', 'TTD', 'V', 'VCYT', 'VERU', 'WKHS', 'WMT', 'WWR', 'XBI', 'XHB', 'XLE', 'Z',
        'ZG', 'ZS'] 
    saveStockList = ['AMD','APHA', 'ERIC', 'RIOT']
    stockList = saveStockList
    

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
    rptlst = []
    n=0
    for stockSymbol in stockList:
        #stockCsvPath = r'file:///home/lan/Documents/py3ds/output/downloadedStockcsv/'+stockSymbol+'.csv'
        stockCsvPath = r'file:///home/lan/Documents/py3ds/output/stockPrice/'+stockSymbol+'.csv'
        savetofile = 0
        if stockSymbol in saveStockList:
            savetofile = 1
        rptdata = stockStdMethod(stockSymbol, stockCsvPath, savetofile)
        dfdata = pd.DataFrame(rptdata)
        if n==0:
            dfrpt = dfdata
            rptlst = rptdata
        else:
            rptlst.extend(rptdata)
        n +=1
        print(stockSymbol, '_stockAna')

    dfrpt = pd.DataFrame(rptlst)
    dfrpt.columns = ['stockSymbol', 'buystd', 'sellstd', 'buytime', 'selltime', 'sampleSize', 'marketPrice']
    dfrpt.to_csv('/home/lan/Documents/py3ds/output/stockRpt/_stockRpt.csv')
    
   