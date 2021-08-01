import pandas as pd
import numpy as np
#from yahoofinancials import YahooFinancials
import datetime as dt
from bokeh.plotting import figure, output_file, save, show
from bokeh.models.sources import ColumnDataSource
from bokeh.models import Circle, Range1d, LabelSet, Label, Plot
from bokeh.models.tools import HoverTool, PointDrawTool
from bokeh.layouts import row, column, layout, widgetbox
from bokeh.palettes import Spectral
#from bokeh.models.widgets import Slider, Select
from bokeh.models import CustomJS, ColumnDataSource, Slider, Select
from bokeh.models import ColumnDataSource, CDSView, IndexFilter, BooleanFilter, HoverTool
from bokeh.transform import factor_cmap, factor_mark
#from cluster get beta and roi list
clusterlst = [[1.5, 2], [1, 1.3], [0.9, 1.1], [1.1, 1.2]]
#, [0.5, 1.1]

def main():
    x_value = []
    y_value = []
    w_value = []
    rst = []
    rstsize = []
    if len(clusterlst)==1:
        print(100, clusterlst[0][0], clusterlst[0][1])
        return [100, clusterlst[0][0], clusterlst[0][1]]

    if len(clusterlst)==2:
        x_value, y_value, w_value, rst, rstsize = porfolio2(clusterlst)
        df = pd.DataFrame(rst, columns=['w1', 'w2', 'beta', 'roi', 'rst'])

    if len(clusterlst)==3:
        x_value, y_value, w_value, rst, rstsize = porfolio3(clusterlst)
        df = pd.DataFrame(rst, columns=['w1', 'w2', 'w3', 'beta', 'roi', 'rst'])

    if len(clusterlst)==4:
        x_value, y_value, w_value, rst, rstsize = porfolio4(clusterlst)
        df = pd.DataFrame(rst, columns=['w1', 'w2', 'w3', 'w4','beta', 'roi', 'rst'])
    
    print(df[df['rst']==df['rst'].max()])
    p = figure(plot_width=900, plot_height=500)    
    p.circle(x=x_value, y=y_value, size=rstsize, fill_color="white")
    show(p)    

def porfolio2(clusterlst):
    betalst = []
    roilst = []

    x_value = []
    y_value = []
    w_value = []
    rst = []
    rstsize = []

    for lst in clusterlst:
        betalst.append(lst[0])
        roilst.append(lst[1])


    rtnweight = []
    output_file("porfolio2.html")  

    for i in range(0, 100, 1):
        w1 = i/100.0
        w2 = 1 - w1
        
        x = betalst[0]*w1+ betalst[1]*w2
        x_value.append(x)
        y = roilst[0]*w1+ roilst[1]*w2
        y_value.append(y)
        #w_value.append([w1, w21, w22])
        rstsize.append(int((y/x)*10))
        rst.append([w1, w2, x, y, y/x])
    
    return x_value, y_value, w_value, rst, rstsize


    #arr = np.array((x_value, y_value, rst))
    

def porfolio3(clusterlst):
    betalst = []
    roilst = []

    x_value = []
    y_value = []
    w_value = []
    rst = []
    rstsize = []

    for lst in clusterlst:
        betalst.append(lst[0])
        roilst.append(lst[1])    

    for i in range(0, 100, 1):
        w1 = i/100.0
        w2 = 1 - w1
        for j in range(0, 100, 10):
            w21 = w2*(j/100.0)
            w22 = w2*(1-j/100.0)
            x = betalst[0]*w1+ betalst[1]*w21 + betalst[2]*w22
            #x = w1*w1*a*a + w2*w2*b*b + 2*w1*w2*a*b
            x_value.append(x)
            y = roilst[0]*w1+ roilst[1]*w21 + roilst[2]*w22
            y_value.append(y)
            #w_value.append([w1, w21, w22])
            rstsize.append(int((y/x)*10))
            rst.append([w1, w21, w22, x, y, y/x])

    return x_value, y_value, w_value, rst, rstsize
    '''
    p = figure(plot_width=900, plot_height=500)    
    p.circle(x=x_value, y=y_value, size=rstsize, fill_color="white")
    show(p)

    #arr = np.array((x_value, y_value, rst))
    df = pd.DataFrame(rst, columns=['w1', 'w2', 'w3', 'beta', 'roi', 'rst'])
    print(df[df['rst']==df['rst'].max()])
    '''

def porfolio4(clusterlst):
    betalst = []
    roilst = []

    x_value = []
    y_value = []
    w_value = []
    rst = []
    rstsize = []

    for lst in clusterlst:
        betalst.append(lst[0])
        roilst.append(lst[1])    

    for i in range(0, 100, 1):
        w1 = i/100.0
        w2 = 1 - w1
        for j in range(0, 100, 2):
            w21 = w2*(j/100.0)
            w22 = w2*(1-j/100.0)
            for p in range(0, 100, 10):
                w31 = w22*(p/100)
                w32 = w22*(1-p/100)
                x = betalst[0]*w1+ betalst[1]*w21 + betalst[2]*w31 + betalst[3]*w32
                #x = w1*w1*a*a + w2*w2*b*b + 2*w1*w2*a*b
                x_value.append(x)
                y = roilst[0]*w1+ roilst[1]*w21 + roilst[2]*w31 + roilst[3]*w32
                y_value.append(y)
                #w_value.append([w1, w21, w22])
                rstsize.append(int((y/x)*10))
                rst.append([w1, w21, w31, w32, x, y, y/x])

    return x_value, y_value, w_value, rst, rstsize


if __name__ == '__main__':
    main()
