def stockDayChanges(stockList):
    for stockSymbol in stockList:
        stockCsvPath = r'file:///home/lan/Documents/py3ds/output/downloadedStockcsv/'+stockSymbol+'.csv'
        datalst = []
        df0 = pd.read_csv(stockCsvPath, delimiter = ",")
        lendf0 = len(df0)
        buyTrigger = 0
        sellTrigger = 0
        ## days when transaction should be places
        transdays = 2
        ## days that used for transaction price reference
        refdays = 3
        for i in range(0, 100):            
            df = df0.head(lendf0-i)
            ##last 5 days
            dfs = df.tail(transdays)
            
            df30h = df0.head(lendf0-i-transdays)
            dfref = df30h.tail(refdays)
            #df30 = df30h.tail(30)

            
            priceRefHighRate = changeForecast(dfref.High.values)
            priceRefLowRate = changeForecast(dfref.Low.values)
            priceRefLow = round(dfref['Low'].iloc[-1], 2)
            priceRefHigh = round(dfref['High'].iloc[-1], 2)
            priceHigh = round(dfs.High.max(), 2)
            priceLow = round(dfs.Low.min(), 2)
            weekStartDate = dfs['Date'].iloc[0]
            weekEndDate = dfs['Date'].iloc[-1]
            meanDate = dfref['Date'].iloc[-1]
            ##recently 5 days mean
            marketPrice = round(dfref['Close'].iloc[-1], 2)
            priceMean = round(dfref.Close.mean(), 2)  
            priceStd = round(dfref.Close.std(), 2)
            priceDiff = round((priceHigh - priceLow), 2)
            diffMean = round(((priceHigh-priceLow)/priceMean), 2)
            diffStd = round(((priceHigh-priceLow)/priceStd), 2)
            stdMean = round((priceStd/priceMean), 2)
            ##buy with std and mean in last n days
            priceBuy = smartRound((priceMean-priceStd/2), 0.5)
            priceSell = smartRound((priceMean+priceStd/2), 0.5) 
            # # buy with last n days trend, result less better than use ref data mean and std
            #priceBuy = smartRound((priceRefLow*priceRefLowRate.get('rate') + priceRefLowRate.get('adj')*priceStd/2), 0.5)         
            #priceSell = smartRound((priceRefHigh*priceRefHighRate.get('rate') - priceRefHighRate.get('adj')*priceStd/2), 0.5)
            if((priceBuy>priceLow) & (priceSell>priceBuy)) :
                buyTrigger = 1
            else:
                buyTrigger = 0
            if((priceHigh>priceSell) & (priceSell>priceBuy)):
                sellTrigger = 1
            else:
                sellTrigger = 0
            data = [meanDate, weekStartDate, weekEndDate, marketPrice, priceLow, priceBuy, priceHigh, priceSell, priceDiff, priceMean, priceStd, stdMean, diffMean, diffStd, buyTrigger, sellTrigger]
            #print(data)
            datalst.append(data)
        dfrst = pd.DataFrame(datalst)
        dfrst.columns = ["Date", "startDate", "endDate", "marketPrice", "daysLow", "priceBuy", "daysHigh", "priceSell", "priceDiff", "priceMean", "priceStd", 
        "stdMean", "diffMean", "diffStd", "buyTrigger", "sellTrigger"]
        #dfrst['gain'] = dfrst.apply(lambda x: x['priceSell']-x['priceBuy'] if (x['buyTrigger']+x['sellTrigger']==2) else 0, axis=1)
        dfrst['gain'] = dfrst.apply(lambda x: 1 if (x['buyTrigger']+x['sellTrigger']==2) else 0, axis=1)
        print(dfrst.gain.sum())
        rstpath = '/home/lan/Documents/py3ds/output/stockRpt/diff/'+ stockSymbol+'_'+ str(transdays)+'days.csv'
        dfrst.to_csv(rstpath)
       
    
    #return rptlst
