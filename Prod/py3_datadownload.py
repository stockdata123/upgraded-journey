import numpy
import pandas as pd
import yfinance as yf
from datetime import datetime
import matplotlib.pyplot as plt
import json
'''
table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
df = table[0]
df.to_csv('/home/lan/Documents/py3ds/output/S&P500-Info.csv')
df.to_csv("/home/lan/Documents/py3ds/output/S&P500-Symbols.csv", columns=['Symbol'])
'''

'''dfsymbol = pd.read_csv(r'/home/lan/Documents/py3ds/output/nyse_left.csv')
dfsymbol['Symbol'] = dfsymbol.Symbol
dfsymbol_removeB = dfsymbol[dfsymbol['Symbol'].str.contains('.B')==False]
stocklist = dfsymbol_removeB.Symbol.values'''

stocklist = ['NVAX']

todaystr = datetime.now().strftime('%Y-%m-%d')
i=0
for stockname in stocklist:
    i=1+1
    data = yf.download(stockname,'2016-01-01', todaystr)
    data.to_csv(r'/home/lan/Documents/py3ds/output/downloadedStockcsv/'+stockname+'_Stock.csv')
    print(i)


'''
data['cash'] = data['Close']*data['Volume']
print(data.describe())

df = data[['Adj Close']]
df.reset_index(level=0, inplace=True)
df.columns=['ds','y']

exp1 = df.y.ewm(span=12, adjust=False).mean()
exp2 = df.y.ewm(span=26, adjust=False).mean()
macd = exp1-exp2

dfcom = df
dfcom['exp1'] = exp1
dfcom['exp2'] = exp2
dfcom['macd'] = macd


#xaxis_df = df[['ds']].copy()
#xaxis_df['ds'] =  xaxis_df.apply(lambda x: str(x['ds']), axis=1)                                 
#pd.to_datetime(xaxis_df["Date"]).dt.strftime('%Y-%m-%d')
#x_dict = xaxis_df.to_dict('dict')
#json.dumps(x_dict)


#df_2016 = macd[macd['ds']<'2017-01-01']
#df_2017 = macd[macd['ds']>='2017-01-01' & macd['ds']<'2018-01-01']
#df_2018 = macd[macd['ds']>='2018-01-01' & macd['ds']<'2019-01-01']

print(dfcom.head())
dfcom.to_csv(r'/home/lan/Documents/py3ds/df.csv')
'''
