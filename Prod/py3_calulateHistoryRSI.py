import pandas as pd
import py3_RSI as rsi

dfsymbol = pd.read_csv(r'/home/lan/Documents/py3ds/output/S&P500-Symbols.csv')
#dfsymbol['Symbol'] = dfsymbol.symbol
dfsymbol_removeB = dfsymbol[dfsymbol['Symbol'].str.contains('.B')==False]
stocklist = dfsymbol_removeB.Symbol.values

#todaystr = datetime.now().strftime('%Y-%m-%d')

i=0
for stockname in stocklist:
    i=i+1
    rsi.getCSVRSI(stockname, 60)
    print(i)
