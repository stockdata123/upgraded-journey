import pandas as pd
import numpy as np
from yahoofinancials import YahooFinancials
import datetime as dt
from bokeh.plotting import figure, output_file, save, show
from bokeh.models.sources import ColumnDataSource
from bokeh.models import Range1d, LabelSet, Label
from bokeh.models.tools import HoverTool, PointDrawTool
from bokeh.layouts import row, column, layout, widgetbox
from bokeh.palettes import Spectral
#from bokeh.models.widgets import Slider, Select
from bokeh.models import CustomJS, ColumnDataSource, Slider, Select
from bokeh.models import ColumnDataSource, CDSView, IndexFilter, BooleanFilter, HoverTool
from bokeh.transform import factor_cmap, factor_mark


def main():

    output_file("callback.html")    
    dforg=pd.read_csv(r'/home/lan/Documents/py3ds/output/stockcsv/inner_sp.csv', header='infer')
    sp = dforg[['ior', 'pe', 'GICS Sector', 'symbol', 'fpe']]
    sp.columns = ['x', 'y', 'gic', 'symbol', 'fpe']
    sp1 = sp.dropna()

    
    sp1.round(2)
    print(len(sp))
    spA = sp1.reset_index().dropna().set_index('index')
    sp = spA[(spA['x']<30)&(spA['y']<100)]
  
    MARKERS = ['circle', 'triangle']
    sp['markers'] = MARKERS[0]
    #sp['markers'].apply((lambda x: MARKERS[1] if x['fpe']<x['y']), axis=1 )
    sp.loc[sp['fpe']<sp['y'], 'markers']=MARKERS[1]
    print(sp.head())

    #sp['color'] = sp.apply(lambda x: get_color(x), axis=1)
    #print(sp.head())
    sp.loc[len(sp), :] = [0, 0, 'ALL', '', 0, MARKERS[0]]
    gics = list(sp['gic'].unique())

    source = sp
    sourcex = source[source['gic']!='ALL']
    Overall=ColumnDataSource(source)
    sc=ColumnDataSource(sourcex) 

    p = figure(plot_width = 900, plot_height=500)
    #p.circle(x='x', y='y', size=5, source=sc)
    #p.circle(x='x', y='y', size=5, source=sc, color=factor_cmap('gic', 'Category10_3', gics))
  
    p.scatter('x', 'y', source=sc, legend='gics', 
          fill_alpha=0.4, size=12,
          marker=factor_mark('markers', MARKERS, MARKERS),
          color=factor_cmap('gic', 'Category10_3', gics))
    

    labels = LabelSet(x='x', y='y', source=sc, text='symbol')
    p.add_layout(labels)
    show(p)


if __name__ == '__main__':
    main()
