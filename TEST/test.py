from datetime import datetime
import pandas as pd
import numpy as np
import yfinance as yf

def dict2list(dictitm):
    dictlist = []
    for key, value in dictitm.items():
        keylst = []
        for i in range(len(key)):
            keylst.append(key[i])
        keylst.append(value)
        dictlist.append(keylst)
    return dictlist


#df0 = pd.read_csv(r'/home/lan/Documents/py3ds/output/stockRpt/zdays/AMZN_zdays_close_10pct.csv')
df0 = pd.read_csv(r'/home/lan/Documents/py3ds/output/stockRpt/re_ana/AMZN_nzday_ana.csv')
#df0['weekDay'] = df0.apply(lambda x: datetime.date(datetime.strptime(x['Date'], "%Y-%m-%d")).weekday, axis=1)

#df =  df0.loc[(df0['accz']>0)]
#print(df0[['accz', 'buyP']].describe())


df = df0
dictgrp =  df[:1979].groupby(['zcode', 'pCode'])['zcode'].count()
dictitm = dict(dictgrp)
grplst = dict2list(dictitm)
dfgrp = pd.DataFrame(grplst)
dfgrp.columns = ['zcode', 'pctCode', 'count']

print(dfgrp)
#dfgrp.describe().to_csv('/home/lan/Documents/py3ds/output/stockRpt/AAPL/AAPL_ana_1999_60_real.csv', index=False)

#dfgrp =  df[['zdiff', 'zdays']]
#dfgrp.to_csv('/home/lan/Documents/py3ds/output/stockRpt/re_ana/AMZN_count_weekday.csv')

