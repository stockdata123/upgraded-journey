import shutil, os
import glob
import pandas as pd
import numpy as np
from datetime import datetime



def choseByIncome(incomedf):
    df0 = incomedf[['Ticker', 'Operating Income (Loss)']].copy()
    df0.rename(columns = {'Operating Income (Loss)':'OprIncome'}, inplace = True)    
    #dfgrp = df0.groupby('Ticker', as_index=False).agg(Average=('OprIncome', 'mean'))
    stocklist =  df0.Ticker.unique()
    stockSelected = []
    for stockname in stocklist:
        dfs = df0[df0['Ticker']==stockname]
        incomeChg = dfs['OprIncome'].pct_change()
        incomeIncreaseCnt = (incomeChg[incomeChg>0]).count()
        incomeDecreaseCnt = (incomeChg[incomeChg<0]).count()
        incomeChgavg = incomeChg.mean()
        if(incomeChgavg>0.1):
            stockSelected.append(stockname)
    print(len(stockSelected))   
    

def main():
    filePath = r"file:///home/lan/Documents/py3ds/DownloadData/income.csv"
    incomedf = pd.read_csv(filePath, delimiter = ",")
    choseByIncome(incomedf)

if __name__ == '__main__':
    main()
    
