import os

import pandas as pd
import numpy as np
from datetime import datetime

from bokeh.plotting import figure
from bokeh.io import output_notebook, show
import pandas as pd
from bokeh.models import Range1d

from bokeh.models import LinearAxis
from bokeh.models import DatetimeTickFormatter
from bokeh.models.sources import ColumnDataSource

from py3_datadownload import yahooDownloadData, yahooDownloadSingleStock

todaystr = datetime.now().strftime('%Y-%m-%d')
def filterStockByChangeRate():
    filePath = r"file:///home/lan/Documents/py3ds/output/stockList/stockRateWeekly.csv"
    stockcsv = pd.read_csv(filePath, delimiter = ",")
    filter0 = stockcsv[(stockcsv['increaseCounts']>stockcsv['decreaseCounts']) &
    (stockcsv['increaseRateAvg']>stockcsv['decreaseRateAvg'])].copy()
    stockIncreaseCountMean = filter0.increaseCounts.mean()
    stockIncreaseMean = filter0.increaseRateAvg.mean()

    filter1 = filter0[(filter0['increaseCounts'] > stockIncreaseCountMean) &
    (filter0['increaseRateAvg']>stockIncreaseMean)].copy()

    #print(filter1.Symbol)
    startDate = '2020-10-18'
    endDate = todaystr
    yahooDownloadData(filter0.Symbol, startDate, todaystr)
    path = '/home/lan/Documents/py3ds/DownloadData/stockcsv_'+startDate.replace('-', '')+'_'+endDate.replace('-', '')
    
    stocklist = []
    for stocksymbol in filter0.Symbol:
        filename = stocksymbol +'.csv' 
        filePath = os.path.join(path, filename)
        yahooDownloadSingleStock(stocksymbol, startDate, endDate)
        stockcsv = pd.read_csv(filePath, delimiter = ",")
        lastClose =  np.array(stockcsv.Close)[-1]
        
        buymin =  np.array(filter0[(filter0['Symbol']==stocksymbol)]['increaseSubBuyMin'])[-1]
        buymean =  np.array(filter0[(filter0['Symbol']==stocksymbol)]['increaseSubBuyMean'])[-1]
        
        if ((lastClose<buymin)|(lastClose<buymean)):
            stocklist.append(stocksymbol)
        
        stockrst =  filter0[filter0['Symbol'].isin(stocklist)]
        stockrst.to_csv("./output/weeklySelected.csv", sep=",", index=False)

   # weeklyList = [filter1.Symbol,  filter1.increaseCounts.mean(), filter1.increaseRateAvg.mean()]
    #filter1.to_csv("./output/monthlySelected.csv", sep=",", index=False)
   
      




def main():
    filterStockByChangeRate()

if __name__ == '__main__':
    main()