import numpy as np
import pandas as pd

from bokeh.models import ColorBar, ColumnDataSource, Mapper
from bokeh.palettes import Spectral6,  brewer
from bokeh.plotting import figure, output_file, show
from bokeh.transform import linear_cmap
from bokeh.transform import factor_cmap, factor_mark

from bokeh.plotting import figure
from bokeh.io import output_notebook, show
from bokeh.models import Range1d

from bokeh.models import LinearAxis
from bokeh.models import DatetimeTickFormatter

from bokeh.palettes import Category10

import bokeh.models as bmo
from bokeh.palettes import d3
"""
#import bokeh.plotting as bpl
import bokeh.models as bmo
from bokeh.palettes import d3
#bpl.output_notebook()
"""
def corrtest():
    x1 = [2, 2.5, 2, 1.5, 3]
    x2 = [2, 1.5, 2, 2.5, 1]
    n = 900

    stocks0 = ['AAPL', 'CNQ', 'APHA']
    stocks = [stocks0[1], stocks0[2], stocks0[0]]

    df1 = pd.read_csv(r'/home/lan/Documents/py3ds/output/stockRpt/save/test/'+ stocks[0]+'_obs.csv')
    X1 = df1.head(n).meanPrice.to_numpy()
    df2 = pd.read_csv(r'/home/lan/Documents/py3ds/output/stockRpt/save/test/'+stocks[1] +'_obs.csv')
    X2 = df2.head(n).meanPrice.to_numpy()
    df3 = pd.read_csv(r'/home/lan/Documents/py3ds/output/stockRpt/save/test/'+stocks[2] +'_obs.csv')
    X3 = df3.head(n).meanPrice.to_numpy()

    x1 = [float(num) for num in X1]
    x2 = [float(num) for num in X2]
    x3 = [float(num) for num in X3]



    cov12 = np.corrcoef(x1, x2)
    cov13 = np.corrcoef(x1, x3)
    cov23 = np.corrcoef(x2, x3)

    #print(cov12, cov13, cov23)

    #correlate = np.corrcoef([x1, x2])
    #print(correlate)


    rptlst = []
    roi1 = 1 + round(((x1[n-1]-x1[0])/x1[0]), 4)
    roi2 = 1 + round(((x2[n-1]-x2[0])/x2[0]), 4)
    roi3 = 1 + round(((x3[n-1]-x3[0])/x3[0]), 4)
    print(roi1, roi2, roi3)

    step100 = [round(step*0.01, 2) for step in range(1, 100)]
    step10 = [round(step*0.1, 2) for step in range(1, 10)]
    for a in step100:
        #b = 1.0 - a
        for c in step10:
            aa = a
            bb = round((1-a)*c, 2)
            cc = round((1-a)*(1-c), 2)
            
            xa = [aa*num for num in x1]
            xb = [bb*num for num in x2]
            xc = [cc*num for num in x3]

            xcorr = round((np.cov([xa, xb])[1, 0]), 4) + round((np.cov([xa, xc])[1, 0]), 4) + round((np.cov([xb, xc])[1, 0]), 4)
            r = round((aa*roi1 + bb*roi2 + cc*roi3), 4)
            rptlst.append([aa, bb, cc, xcorr, r, round(abs(r*xcorr), 4)])

    dfrpt = pd.DataFrame(rptlst)
    dfrpt.columns = ['aa', 'bb', 'cc', 'xcorr', 'r', 'ratio']

    print(stocks, dfrpt[(dfrpt['ratio']==dfrpt.ratio.max())] )
    p = figure(title='std', 
                plot_width=1200, 
                plot_height=800,
                x_axis_label='std', y_axis_label='Return')

        
    X = dfrpt.xcorr
    Y = dfrpt.r
    p.scatter(x=X, y=Y)

    show(p)

def addColorinPointNotice():
    buyind = -1
    sellind = 2
    stocks = ['AAPL', 'CNQ', 'APHA']
    df1 = pd.read_csv(r'/home/lan/Documents/py3ds/output/stockRpt/save/'+ stocks[1]+'_obs.csv')
    df1['indicator1'] = df1.apply(lambda x: 'BUY' if (x['buy']<= -1) else 'SELL' if (x['sell']>=1) else 'NONE' , axis=1)
    df1['indicator2'] = df1.apply(lambda x: 'BUY' if (x['buy']<= -2) else 'SELL' if (x['sell']>=2.5) else 'NONE' , axis=1)
    df1['indicator3'] = df1.apply(lambda x: 'BUY' if (x['buy']<= -2.5) else 'SELL' if (x['sell']>=3.5) else 'NONE' , axis=1)
    #df1['indicator'] = df1.apply(lambda x: 'SELL' if (x['sell']>3.0) else 'NONE', axis=1)
    #dfrst.apply(lambda x: pointIndicator(x['marketHigh'],  x['meanPrice'], x['stdm']), axis=1)
    df = df1[['Date', 'marketPrice', 'meanPrice', 'indicator1', 'indicator2', 'indicator3']]
    startIndex = df.index[0]
    data = df.sort_index(ascending=True, axis=0)
    newColumnNames = data.columns    
    new_data = pd.DataFrame(index=range(0, len(data)), columns=newColumnNames)

    for i in range(0,len(data)):
        for cname in newColumnNames:
            new_data[cname][i] =  data[cname][i+startIndex]
    new_data['Date']=pd.to_datetime(new_data['Date'])

    dfsource = ColumnDataSource(new_data)
   
    INDICATOR = ['NONE', 'BUY', 'SELL']
    MARKERS1 = ['circle', 'diamond_cross', 'circle_x']
    MARKERS2 = ['circle', 'inverted_triangle', 'triangle']
    colormap = {'NONE': 'beige', 'BUY': 'red', 'SELL': 'green'}
    colors = [colormap[x] for x in INDICATOR]

    p = figure(title='PricePoint '+ str(buyind) + '_' + str(sellind), 
            plot_width=1200, 
            plot_height=800,
            x_axis_label='Month-Year', y_axis_label='Price',
            x_axis_type='datetime'
            )

    p.scatter("Date", "marketPrice", source=dfsource, legend="indicator2", 
          fill_alpha=0.4, size=8,
          marker=factor_mark('indicator2', MARKERS1, INDICATOR),
          #color=factor_cmap('indicator2', 'Category10_3', INDICATOR))
          color=factor_cmap('indicator2', colors, INDICATOR))
    
    p.scatter("Date", "marketPrice", source=dfsource, legend="indicator3", 
          fill_alpha=0.4, size=2,
          color=factor_cmap('indicator3', colors, INDICATOR))
    
    p.scatter("Date", "meanPrice", source=dfsource)

    show(p)
   

    

    

    #p.scatter(x = new_data.Date, y = new_data.meanPrice, color=mapper, size = 2)
    #p.scatter(x = new_data.Date, y = new_data.marketPrice, color='blue', size = 2)

if __name__ == "__main__":
    addColorinPointNotice()