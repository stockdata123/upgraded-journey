import pandas as pd
import quandl
import matplotlib.pyplot as plt
import math


def fetch_data(string1, string2, string3, filename):
    w = quandl.get(string1, authtoken = string2, start_date = string3)
    w.to_csv(filename)
    w = pd.read_csv(filename)
    return w

def test_data(string1, string2, string3):
    w = quandl.get(string1, authtoken = string2, start_date = string3)
    return w

#Data = test_data("CHRIS/CME_SP1", "", "2021-01-01")
Data = test_data("CHRIS/CME_SP1", "", "2021-01-01")
#Data1 = test_data("CHRIS/SPX_PC", "", "2020-07-31")
#Data['future'] = Data1['Last']
#Data['VIX'] = Data['VIX Close']
#print(Data)

mydata = quandl.get("WIKI/AAPL", rows=5)
print(mydata)