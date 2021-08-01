import pandas as pd
import py3_RSI as RSI
import numpy as np
import datetime as dt

import py3_yahoo_financedata as yahoo


today = dt.date.today().strftime('%Y-%m-%d')

table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
df = table[0]
df.to_csv('/home/lan/Documents/py3ds/output/S&P500-Info.csv')
df.to_csv("/home/lan/Documents/py3ds/output/S&P500-Symbols.csv", columns=['Symbol'])

dfsymbol = pd.read_csv(r'/home/lan/Documents/py3ds/output/nyse_left.csv')
dfsymbol['Symbol'] = dfsymbol.symbol
dfsymbol_removeB = dfsymbol[dfsymbol['Symbol'].str.contains('.B')==False]
stocklist = dfsymbol_removeB.Symbol.values
##stocklistadd = np.append(stocklist, ['AAPL'])
##print(stocklistadd)

timespan = 14
dfrsi = pd.DataFrame(index=range(0,len(stocklist)),columns=['symbol', 'rsi'])
dfrsi_index = 0

#dfsymbol = pd.read_csv(r'/home/lan/Documents/py3ds/output/S&P500-Symbols.csv')
#dfsymbol_removeB = dfsymbol[dfsymbol['Symbol'].str.contains('.B')==False]
#stocklist = dfsymbol_removeB.Symbol.values

columnsList = ['symbol', 'pe', 'fpe', 'pefpe', 'ops_income', 'ior', 'volumne_ratio',
        'payout', 'divident', 'eps', 'yearly_high', 'yearly_low', 'prev_close_price', 'open_price']
yahoodata = pd.DataFrame(columns=columnsList)

for stocksymbol in stocklist:
    if('.B' in stocksymbol):
            continue
    else:
        try:
            rsivalue = RSI.getTodayRSI(stocksymbol, timespan)
            dfrsi['symbol'][dfrsi_index] = stocksymbol
            dfrsi['rsi'][dfrsi_index] = rsivalue
            dfrsi_index = dfrsi_index+1
        except:
            break
    
cnt = 0
for stocksymbol in stocklist:   
    if('.B' in stocksymbol):
            continue
    else:
        try: 
            yahoolist = yahoo.get_yahooFinancials(stocksymbol)
            yahoodata.loc[len(yahoodata)] = yahoolist
            print(cnt)
            cnt = cnt +1
        except:
            print(stocksymbol)
            break

yahoocsv = '/home/lan/Documents/py3ds/output/yahoodata_' + today +'.csv'  
yahoodata.to_csv(yahoocsv)

#rsicsv_name = rsi+today+'.csv'
#dfrsi.to_csv('/home/lan/Documents/py3ds/output/'+)
#yahoodata.to_csv('/home/lan/Documents/py3ds/output/yahoodata.csv')

#rsicsv = '/home/lan/Documents/py3ds/output/rsi_' + today +'.csv'  
#rsi.to_csv(rsicsv)
'''
    if rsivalue<40:
        buystocklist.append(stocksymbol)
    if rsivalue>80:
        sellstocklist.append(stocksymbol)

if len(buystocklist)>0:
    print('buy: ', buystocklist)
if len(sellstocklist)>0:
    print('sell: ', sellstocklist)
'''

