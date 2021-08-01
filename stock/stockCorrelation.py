
import os
import pandas as pd
import pickle
import csv
import numpy as np

def testStd(stdPreList, stdYesterday, stdToday):
    rst = 0
    if (stdYesterday == max(stdPreList, stdYesterday, stdToday)):
        rst = 1

    return rst

def getStockCorrelation(stock, stockList, compareDays):
    rptlst = []
    n = compareDays
    stock1 = stock
    df1 = pd.read_csv(r'/home/lan/Documents/py3ds/output/stockPrice/'+stock1+'.csv')
    print(stock1, 'len ', len(df1))
    price1 = df1.head(n).Close.to_numpy()
    for j in range(len(stockList)):
        stock2 = stockList[j]
        try: 
            df2 = pd.read_csv(r'/home/lan/Documents/py3ds/output/stockPrice/'+stock2+'.csv')
            if((len(df2))>=n):
                price2 = df2.head(n).Close.to_numpy()
                r = round(np.corrcoef(price1, price2)[1,0], 3)     
                rptlst.append([stock1, stock2, r])
        except:
            print('error in corr', stock1, stock2)

    dfrpt = pd.DataFrame(rptlst)
    dfrpt.columns = ['stockSymbol1', 'stockSymbol2', 'corr']
    dfrpt.to_csv('/home/lan/Documents/py3ds/output/stockRpt/correlation/'+stock1 + '_' + str(n) +'_stockCorr.csv')

def daysMeanRoiStd(df, days):
    rptList = []
    roiList = []
    roiStdList = []
    mean = df['meanPrice'].to_numpy()

    previousMean = mean[days:]
    for i in range(len(previousMean)):
        roi = round(((mean[i]-previousMean[i])/previousMean[i]), 4)
        roiList.append(roi)
    
    #get roistd, 
    for i in range(len(roiList)-days):
        roistd = round(np.std(roiList[i:i+days]), 4)
        roiStdList.append(roistd)
        rptList.append([mean[i], previousMean[i], roiList[i], roistd])
    
    
    dfrpt = pd.DataFrame(rptList)
    dfrpt.columns = ['mean', 'preMean', 'meanRoi', 'meanRoiStd']
    dfrpt['meanRoiStd'] =  dfrpt['meanRoiStd'].astype(float)
    return dfrpt

def getROICorrelation(stock, stockList, compareDays):
    rptlst = []
    n = compareDays
    stock1 = stock
    df1 = pd.read_csv(r'/home/lan/Documents/py3ds/output/stockRpt/save/'+stock1+'_obs.csv')
    roi1 = daysMeanRoiStd(df1.head(n), 28)
    #roistd1 = 2*roi1['meanRoiStd'].to_numpy()
    
    roistd1 = roi1['meanRoiStd'].to_numpy()

    #calculate correlation of std to mean price
    #df1['std2mean'] = df1.apply(lambda x: round((x['gap']/x['marketPrice']), 2), axis=1)
    #gap2marketPrice1 = df1['std2mean'].to_numpy()
    #calculate correlation of buy based on std variation
    buystdm1 = df1['buy'].to_numpy()
    
    for j in range(len(stockList)):
        stock2 = stockList[j]
        try:
            df2 = pd.read_csv(r'/home/lan/Documents/py3ds/output/stockRpt/save/'+stock2+'_obs.csv')
            #df2['std2mean'] = df2.apply(lambda x: round((x['gap']/x['marketPrice']), 2), axis=1)
            #gap2marketPrice2 = df2['std2mean'].to_numpy()
            buystdm2 = df2['buy'].to_numpy()
            if((len(df2))>=n):
                roi2 = daysMeanRoiStd(df2.head(n), 28)
                roistd2 = roi2['meanRoiStd'].to_numpy()
                r = round(np.corrcoef(roistd1, roistd2)[1,0], 3) 
                #c = round(np.cov(roistd1, roistd2)[1,0]*1000000, 3)
                #c = round(np.corrcoef(gap2marketPrice1, gap2marketPrice2)[1,0], 3)
                c = round(np.corrcoef(buystdm1, buystdm2)[1,0], 3)
                rptlst.append([stock1, stock2, r, c])
        except:
            print(stock2, "not exist")

    print(rptlst)
    dfrpt = pd.DataFrame(rptlst)
    dfrpt.columns = ['stockSymbol1', 'stockSymbol2', 'corr', 'cov']
    dfrpt.to_csv('/home/lan/Documents/py3ds/output/stockRpt/correlation/'+stock1 + '_' + str(n) +'_meanROICorr.csv')

def getSTDCorrelation(stock, stockList, compareDays):
    rptlst = []
    n = compareDays
    stock1 = stock
    df1 = pd.read_csv(r'/home/lan/Documents/py3ds/output/stockRpt/save/'+stock1+'_obs.csv')
    
    buystdm1 = df1['buy'].to_list()[:n]
    for j in range(len(stockList)):
    #test for j in range(1):
        stock2 = stockList[j]
        try:
            df2 = pd.read_csv(r'/home/lan/Documents/py3ds/output/stockRpt/save/'+stock2+'_obs.csv')
            #df2['std2mean'] = df2.apply(lambda x: round((x['gap']/x['marketPrice']), 2), axis=1)
            #gap2marketPrice2 = df2['std2mean'].to_numpy()
            buystdm2 = df2['buy'].to_list()[:n]
            r = round(np.corrcoef(buystdm1, buystdm2)[0][1], 2)          
            c = round(np.cov(buystdm1, buystdm2)[0][1], 2)
            rptlst.append([stock1, stock2, r, c])

        except:
            print(stock2, "not exist")

    dfrpt = pd.DataFrame(rptlst)
    dfrpt.columns = ['stockSymbol1', 'stockSymbol2', 'corr', 'cov']
    dfrpt.to_csv('/home/lan/Documents/py3ds/output/stockRpt/correlation/'+stock1 + '_' + str(n) +'_StdCorr.csv')
  


if __name__ == "__main__":
    stockList = ['AAPL', 'ADSK', 'ADYEN', 'AEM', 'AEZS', 'AGIO', 'ALGN', 'ALTR', 'ALXN', 'AMBA', 'AMAT', 'AMD', 'AMGN', 'AMZN', 'APHA', 'APLS', 'APPN', 'APPS', 'ARKF', 'ARKG', 'ARKQ', 'ARKW', 'ARNA', 'ARWR', 'ATOM', 'ATVI', 'AUVI ', 'AVAV', 'BA', 'BABA', 'BAM', 'BBIO', 'BEAM', 'BGTC', 'BIDU', 'BIIB', 'BILI', 'BIP', 'BLMN', 'BLOK', 'BNTX', 'BNSF', 'CDNA', 'CLNE', 'CNI', 'CNQ', 'CP', 'CSIQ', 'CRM', 'CRNC', 'CZR', 'DDD', 'DE', 'DKNG', 'EDIT', 'ERIC', 'ETSY', 'EXAS', 'EXPI', 'FANG', 'FATE', 'FB', 'FCEL', 'FLGT ', 'FLIR', 'FUV', 'GBTC', 'GE', 'GLD', 'GLEN', 'GLXY', 'GOOG', 'GOOGL', 'GRWG', 'HD', 'HIMX', 'KO', 'HIVE', 'HOME', 'HPQ', 'IBB', 'ICE', 'IDEX', 'ILMN', 'ILMN', 'IONS', 'IOVA', 'IRDM', 'IWM', 'IYR', 'JD', 'JG', 'JPM', 'KL', 'KOD', 'KOPN ', 'KTOS', 'LLY', 'MA', 'MARA', 'MGNI', 'MOOV', 'MRK', 'MRNA', 'MSFT', 'MSTR', 'MTLS', 'MTSL', 'MVIS', 'NNDM', 'NVAX', 'NVDA', 'NVTA', 'PACB', 'PDD', 'PENN', 'PERI', 'PFE', 'PINS', 'PLAY', 'PLL', 'PSTG', 'PTC', 'PYPL', 'QCOM', 'QQQ', 'QTRX', 'RDFN', 'REKR', 'RIDE', 'RIO', 'RIOT', 'ROKU', 'SAGE', 'SAP', 'SGEN', 'SHOP', 'SI', 'SIVB', 'SLV', 'SNAP', 'SONO', 'SPOT', 'SPY', 'SQ', 'SSYS', 'STAA', 'STMN', 'STNE', 'TCEHY', 'TD', 'TDOC', 'TGTX', 'TIGR', 'TLRY', 'TLT', 'TNA', 'TQQQ', 'TRIL', 'TRMB', 'TSLA', 'TTD', 'TTOO', 'TWST', 'TXN', 'V', 'VCYT', 'VERU', 'VLDR', 'W', 'WKHS', 'WMT', 'WWR', 'XBI', 'XHB', 'XLE', 'Z', 'ZG', 'ZS', 'STZ', 'NRG', 'KRNT', 'KSPILI', 'IONS', 'TER', 'BLI', 'AONE', 'ESLT', 'TSM', 'DE', 'CAT', 'KMTUY', 'NTDOY', 'HIMS', 'TER', 'SPLK', 'TWLO', 'U', 'CDNS', 'MSCI', 'LMT', 'ANSS', 'TTDKY', 'NIKE']
    stockList = ['AAPL', 'ABBV', 'ABT', 'ACN', 'ADBE', 'ADI', 'ADP', 'ADSK', 'AEP', 'AIG', 'ALGN', 'ALXN', 'AMAT', 'AMD', 'AMGN', 'AMT', 'AMZN', 'ANSS', 'ASML', 'ATVI', 'AVGO', 'AXP', 'BA', 'BAC', 'BIDU', 'BIIB', 'BK', 'BKNG', 'BLK', 'BMY', 'BRK.B', 'C', 'CAT', 'CDNS', 'CDW', 'CERN', 'CHKP', 'CHTR', 'CL', 'CMCSA', 'COF', 'COP', 'COST', 'CPRT', 'CRM', 'CSCO', 'CSX', 'CTAS', 'CTSH', 'CVS', 'CVX', 'DD', 'DHR', 'DIS', 'DLTR', 'DOCU', 'DOW', 'DUK', 'DXCM', 'EA', 'EBAY', 'EMR', 'EXC', 'F', 'FAST', 'FB', 'FDX', 'FISV', 'FOX', 'FOXA', 'GD', 'GE', 'GILD', 'GM', 'GOOG', 'GOOGL', 'GS', 'HD', 'HON', 'IBM', 'IDXX', 'ILMN', 'INCY', 'INTC', 'INTU', 'ISRG', 'JD', 'JNJ', 'JPM', 'KDP', 'KHC', 'KLAC', 'KO', 'LIN', 'LLY', 'LMT', 'LOW', 'LRCX', 'LULU', 'MA', 'MAR', 'MCD', 'MCHP', 'MDLZ', 'MDT', 'MELI', 'MET', 'MMM', 'MNST', 'MO', 'MRK', 'MRNA', 'MRVL', 'MS', 'MSFT', 'MTCH', 'MU', 'MXIM', 'NEE', 'NFLX', 'NKE', 'NTES', 'NVDA', 'NXPI', 'OKTA', 'ORCL', 'ORLY', 'PAYX', 'PCAR', 'PDD', 'PEP', 'PFE', 'PG', 'PM', 'PTON', 'PYPL', 'QCOM', 'REGN', 'ROST', 'RTX', 'SBUX', 'SGEN', 'SIRI', 'SNPS', 'SO', 'SPG', 'SPLK', 'SWKS', 'T', 'TCOM', 'TEAM', 'TGT', 'TMO', 'TMUS', 'TSLA', 'TXN', 'UNH', 'UNP', 'UPS', 'USB', 'V', 'VRSK', 'VRSN', 'VRTX', 'VZ', 'WBA', 'WDAY', 'WFC', 'WMT', 'XEL', 'XLNX', 'XOM', 'ZM']
    
    dfsymbol = pd.read_csv(r'/home/lan/Documents/py3ds/output/stockList/Snp500Plus.csv') 
    #dfsymbol = pd.read_csv(r'/home/lan/Documents/py3ds/output/stockList/nasdaqlisted.csv', delimiter='|')
    dfsymbol_removeB = dfsymbol[dfsymbol['Symbol'].str.contains('.B')==False]
    stockList = dfsymbol_removeB.Symbol.values

    rptlst = stockList
    n = 777
    stock1 = 'AAPL'
    #stockList = ['NKE']
    #getROICorrelation(stock1, stockList, n)
    #getStockCorrelation(stock1, stockList, n)
    getSTDCorrelation(stock1, stockList, n)
    