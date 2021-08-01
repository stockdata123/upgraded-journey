import shutil, os
import glob
import pandas as pd
import numpy as np
from datetime import datetime
from getPriceRateAvg import findRate

def getStockNameCSV(timeSpan):
    #to get the current working directory name
    cwd = os.getcwd()
    #print(cwd)
    #directory = r"/home/lan/Documents/py3ds/DownloadData/stockcsv_less10_9"
    #deldirectory = r"/home/lan/Documents/py3ds/DownloadData/stockcsv_10yearsOver10_8"
    directory = r"/home/lan/Documents/py3ds/DownloadData/stockcsv_20100101_20201018"
    stocklist = []
    cnt = 0
    stockDictList = []
    timeSpan = timeSpan
    for filename in os.listdir(directory):
        if filename.endswith(".csv") :
            filePath = os.path.join(directory, filename)
            stockSymbol =  str(filename)[0:-4]
            rfilePath = filePath
            stockcsv = pd.read_csv(rfilePath, delimiter = ",")
            df = stockcsv[(stockcsv.Date>'2020-09-01')]
            stockDict = {}
            ratelist = findRate(df, timeSpan)  
            if ratelist:          
                stockDict = ratelist 
                stockDict['Symbol'] =  stockSymbol
                stockDict['timeSpan'] =  timeSpan
                stockDictList.append(stockDict)           
                """            if cnt>3 :
                    dfnew = pd.DataFrame.from_dict(stockDictList)
                    print(dfnew)
                    break
                """
            else:
                print(stockSymbol)

            #findRate(df, 'Month')
            """  lastVolumeNum = np.array(stockcsv['Volume'].tail(1))[0]
                lastClosePrice = np.array(stockcsv['Close'].tail(1))[0]
                marketCap =  lastClosePrice*lastVolumeNum
                if (marketCap>100000000):
                    stocklist.append(stockSymbol)
                else:
                    shutil.move(filePath, deldirectory)
                else:
                    shutil.move(filePath, deldirectory)
                    print(stockSymbol)
                """
        else:
            print(stockSymbol)
            continue
    dfnew = pd.DataFrame.from_dict(stockDictList)
    
    #df = pd.DataFrame(data={"Symbol": stocklist})
    dfnew.to_csv("./DownloadData/stockRate"+timeSpan+"ly.csv", sep=",", index=False)


def chooseStockByPrice(minprice, maxprice):
    #to get the current working directory name
    cwd = os.getcwd()
    #print(cwd)
    #directory = r"/home/lan/Documents/py3ds/DownloadData/stockcsv_less10_9"
    #deldirectory = r"/home/lan/Documents/py3ds/DownloadData/stockcsv_10yearsOver10_8"
    directory = r"/home/lan/Documents/py3ds/DownloadData/stockcsv_20201018_20201122"
    stocklist = []

    for filename in os.listdir(directory):
        if filename.endswith(".csv") :
            filePath = os.path.join(directory, filename)
            stockSymbol =  str(filename)[0:-4]
            rfilePath = filePath
            stockcsv = pd.read_csv(rfilePath, delimiter = ",")
            try:
                closePrice = stockcsv.Close.mean()
                avgCap = closePrice*stockcsv.Volume.mean() 
                if (closePrice>minprice and closePrice<maxprice and avgCap>50000000):
                    stocklist.append([stockSymbol, round(closePrice, 2),  int(avgCap)])
            except:
                print(stockSymbol)
                continue
                
    stockdf = pd.DataFrame(stocklist)
    stockdf.to_csv("./DownloadData/chooseStock/stockPrice7_15.csv", sep=",", index=False)
   
    
    #df = pd.DataFrame(data={"Symbol": stocklist})
    #dfnew.to_csv("./DownloadData/stockRate"+timeSpan+"ly.csv", sep=",", index=False)



if __name__ == '__main__':
    #main()
    #getStockNameCSV('Week')
    chooseStockByPrice(7.0, 15.0)
