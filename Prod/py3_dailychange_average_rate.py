import pandas as pd
import os

dfsymbol = pd.read_csv(r'/home/lan/Documents/py3ds/output/S&P500-Symbols.csv')
#dfsymbol['Symbol'] = dfsymbol.symbol
dfsymbol_removeB = dfsymbol[dfsymbol['Symbol'].str.contains('.B')==False]
stocklist = dfsymbol_removeB.Symbol.values

#todaystr = datetime.now().strftime('%Y-%m-%d')

def getAverage(stockSymbol, daynum):
    filename = '/home/lan/Documents/py3ds/output/downloadedStockcsv/'+stockSymbol+'_Stock.csv'
    if os.path.isfile(filename):
        df1 = pd.read_csv(filename)
        df0 = df1[:233]

        data = df0.sort_index(ascending=True, axis=0)
        data['Date'] = data.index
        new_data = pd.DataFrame(index=range(0,len(data)),columns=['Date', 'Close', 'Loss', 'Gain'])

        for i in range(0,len(data)):
            #print(data['Date'][i])
            new_data['Date'][i] = data['Date'][i]
            new_data['Close'][i] = data['Close'][i]   
            if i > 1:
                if (data['Close'][i-1]>data['Close'][i]):
                    new_data['Loss'][i] = (data['Close'][i-1]-data['Close'][i])/data['Close'][i]
                    new_data['Gain'][i] = 0
                if (data['Close'][i]>data['Close'][i-1]):
                    new_data['Gain'][i] = (data['Close'][i]-data['Close'][i-1])/data['Close'][i]
                    new_data['Loss'][i] = 0
            else:
                new_data['Gain'][0] = 0
                new_data['Loss'][0] = 0

       
        new_data['avgGain'] = new_data['Gain'].rolling(min_periods=1, window=daynum).mean()
        new_data['avgLoss'] = new_data['Loss'].rolling(min_periods=1, window=daynum).mean()
        
        avgGainCount = len(new_data[new_data['Gain']>0])
        avgLossCount = len(new_data[new_data['Loss']>0])
        earlyPrice = data.Close[0]
        todayPrice =data.Close[len(data)-1]
        ds = new_data.describe()
        #print(ds)
        rst = []
        rst.append(stockSymbol)
        rst.append(avgGainCount)
        rst.append(avgLossCount)
        rst.append(earlyPrice)
        rst.append(todayPrice)
        for v in ds.avgGain.values:
            rst.append(v)
        for v in ds.avgLoss.values:
            rst.append(v)
        
        return rst

        '''
        ds = new_data.describe()
        avgGain_list = []
        avgGain_list.append(stockSymbol)
        avgGain_list.append('avgGain')
        avgLoss_list = []
        avgLoss_list.append(stockSymbol)
        avgLoss_list.append('avgLoss')        
        for v in ds.avgGain.values:
            avgGain_list.append(v)
        for v in ds.avgLoss.values:
            avgLoss_list.append(v)
        
        columns = ['Symbol', 'gainCount', 'lossCount', 
        'gcount', 'gmean', 'gstd', 'gmin', 'g25', 'g50', 'g75', 'gmax',
        'lcount', 'lmean', 'lstd', 'lmin', 'l25', 'l50', 'l75', 'lmax']
        df = pd.DataFrame([avgGain_list, avgLoss_list], columns=columns)
        return df
        #new_data.to_csv(r'/home/lan/Documents/py3ds/output/stockchange/'+stockSymbol+'_changes.csv')
        '''

def main():
    #columns = ['Symbol', 'count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']
    columns = ['Symbol', 'gainCount', 'lossCount', 'startprice', 'todayprice', 
        'gcount', 'gmean', 'gstd', 'gmin', 'g25', 'g50', 'g75', 'gmax',
        'lcount', 'lmean', 'lstd', 'lmin', 'l25', 'l50', 'l75', 'lmax']
    df = pd.DataFrame(columns=columns)
    rstlist = []
    j=0
    for stockname in stocklist:
        j=j+1
        rst = getAverage(stockname, 5)
        if rst:
            rstlist.append(rst)
        else:
            pass
        print(j)
        

        #frames = [dfi, df]
        #df = pd.concat(frames)
    df = pd.DataFrame(rstlist, columns=columns)
    df.to_csv(r'/home/lan/Documents/py3ds/output/stockchange/avg_changes_5.csv')
    


if __name__=='__main__':
    main()