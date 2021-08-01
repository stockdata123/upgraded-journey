
import pandas as pd
import numpy as np
import json
import datetime as dt

df_income_0 = pd.read_csv(r'/home/lan/Documents/DownloadData/income.csv')
df_income_0['ReportDate'] = pd.to_datetime(df_income_0['Report Date'])

earliest_date = pd.to_datetime('2009-01-01')
latest_date = pd.to_datetime('2018-06-01')
df_latest_0 = pd.DataFrame(df_income_0.groupby(['Ticker'])['ReportDate'].max())
df_earliest_0 = pd.DataFrame(df_income_0.groupby(['Ticker'])['ReportDate'].min())
df_earliest_1 = df_earliest_0[df_earliest_0['ReportDate']<=earliest_date]
df_latest_1 = df_latest_0[df_latest_0['ReportDate']>=latest_date]


tickerList = pd.merge(df_latest_1, df_earliest_1, how='inner', on='Ticker')
df_income_1 =  pd.merge(tickerList, df_income_0, how='left', on='Ticker')
df_income_1.fillna(0)

df3 = df_income_1[df_income_1['Ticker']=='ABC']
print(df3['Research & Development'])
'''
df_income_1['incomeWithoutAmortization'] = df_income_1.apply(lambda x: (x['Gross Profit']
+ x['Selling, General & Administrative']+x['Research & Development']), axis=1)
df_income_1['GrossProfitMargin'] = df_income_1.apply(lambda x: (x['Gross Profit']/x['Revenue']), axis=1)
df_income_1['ior'] = df_income_1.apply(lambda x: (x['incomeWithoutAmortization']/x['Revenue']), axis=1)
#df_income_1['perv_incomeWithoutAmortization'] = df_income_1.groupby('Ticker')['incomeWithoutAmortization'].shift()
df_income_2 = df_income_1[['Ticker', 'Report Date', 'SimFinId', 'Currency', 'Fiscal Year',
       'Fiscal Period', 'Publish Date', 'Shares (Basic)', 'Shares (Diluted)',
       'Revenue', 'incomeWithoutAmortization', 'ior']].copy()
#df_income_2['perv_incomeWithoutAmortization'] = df_income_2[['incomeWithoutAmortization']]
df_income_2['perv_incomeWithoutAmortization'] = df_income_2.groupby('Ticker')['incomeWithoutAmortization'].shift()

L1 = [np.nan]
m1 = df_income_2['perv_incomeWithoutAmortization'].isin(L1)
df_income_2['perv_incomeWithoutAmortization'] = df_income_2['perv_incomeWithoutAmortization'].mask(m1, df_income_2['incomeWithoutAmortization'])
#df_income_2['perv_incomeWithoutAmortization'] = df_income_2['perv_incomeWithoutAmortization'].mask(m1, 0.00)

df_income_2['incomeIncreasedRate'] = df_income_2.apply(lambda x: ((x['incomeWithoutAmortization']-x['perv_incomeWithoutAmortization'])/x['incomeWithoutAmortization']), axis=1)
df_income_2.to_csv(r'/home/lan/Documents/py3ds/output/dataWatch/incomeIncrease.csv')
'''
