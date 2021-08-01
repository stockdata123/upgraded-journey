import pandas as pd
import numpy as np
from yahoofinancials import YahooFinancials
import datetime as dt
from bokeh.plotting import figure, output_file, save, show
from bokeh.models.sources import ColumnDataSource
from bokeh.models import Range1d
from bokeh.models.tools import HoverTool, PointDrawTool
from bokeh.layouts import row, column, layout, widgetbox
from bokeh.palettes import Spectral
#from bokeh.models.widgets import Slider, Select
from bokeh.models import CustomJS, ColumnDataSource, Slider, Select
from bokeh.models import ColumnDataSource, CDSView, IndexFilter, BooleanFilter, HoverTool
from bokeh.transform import factor_cmap, factor_mark



#import py3_RSI as rsi

dforg=pd.read_csv(r'/home/lan/Documents/py3ds/output/stockcsv/inner_sp.csv')
sp = dforg[['ior', 'eps',	'GICS Sector']]
sp.columns = ['ior', 'eps', 'GIC']
   # print(len(sp))
spA = sp.reset_index().dropna().set_index('index')
sp = spA[(spA['ior']<30)&(spA['eps']<30)]

gics = list(sp['GIC'].unique())
gics.append('ALL')
n = len(gics)
colors = []
for item in Spectral[10]:
    colors.append(item)
if (n<=19):
    for item in Spectral[9]:
        colors.append(item)

gic_color = pd.DataFrame(zip(gics, colors))

color = colors[:n]
def get_color(x):
    for i in range(n):
        if(gic_color[0][i]==x['gic']):
            return gic_color[1][i]

def main():

    output_file("callback.html")    
    dforg=pd.read_csv(r'/home/lan/Documents/py3ds/output/stockcsv/inner_sp.csv')
    sp = dforg[['ior', 'eps', 'GICS Sector']]
    sp.columns = ['x', 'y', 'gic'] 
   # print(len(sp))
    spA = sp.reset_index().dropna().set_index('index')
    sp = spA[(spA['x']<30)&(spA['y']<30)]
    #sp['color'] = sp.apply(lambda x: get_color(x), axis=1)
    #print(sp.head())
    sp.loc[len(sp), :] = [0, 0, 'ALL']
    print(sp.tail())
    gics = list(sp['gic'].unique())
    #gics.append('ALL')

    source = sp
    sourcex = source[source['gic']!='ALL']
    Overall=ColumnDataSource(source)
    sc=ColumnDataSource(sourcex)


    TOOLTIPS = [('index', '$index'), ('(ior, eps)', '(@ior, @eps)'), ('gic', '@gic')] 
    hover = HoverTool(tooltips=TOOLTIPS)
    p = figure(plot_width = 600, plot_height=300, tooltips=TOOLTIPS)
    p.circle('x', 'y', size=5, source=sc, color=factor_cmap('gic', 'Category10_3', gics))
    '''p.scatter("x", "y", source=sc, legend="gics", 
          fill_alpha=0.4, size=12,
          color=factor_cmap('gic', 'Category10_3', gics))'''
        

    slider = Slider(start=0.1, end=1, value=.1, step=.01, title="ior") 
    select = Select(title="Option:", value="ALL", options=sorted(gics))

    ior_callback = CustomJS(args=dict(source=Overall, sc=sc, select = select, slider=slider), code = '''
        var ior = slider.value;
        var gic = select.value;
        console.log('gic=', select.value, ' ior=', slider.value);
        source = source;
        sc = sc;
        sc.data['x'] = [];
        sc.data['y'] = [];
        sc.data['gic'] = [];
        for (var i = 0; i <= source.get_length(); i++){
            if (gic == 'ALL') {
                if (source.data['x'][i] > ior ){
                sc.data['x'].push(source.data['x'][i]);
                sc.data['y'].push(source.data['y'][i]);
                sc.data['gic'].push(source.data['gic'][i]);   
                }  
            }
            else {
                if (source.data['x'][i] > ior && source.data['gic'][i] == gic ){
                sc.data['x'].push(source.data['x'][i]);
                sc.data['y'].push(source.data['y'][i]);
                sc.data['gic'].push(source.data['gic'][i]);   
                 }  
            }          
        }
        sc.change.emit();
        ''')
        

   
    #select = Select(title='GIC', options=sorted(gics), value='ALL', callback=gic_callback)
    select.callback = ior_callback
    slider.callback = ior_callback
   

    layout = column(slider, select, p)
# execute a callback whenever the plot canvas is tapped
    show(layout)



if __name__ == '__main__':
    main()
    
'''

                sc.data['color'].push(source.data['color'][i]);  
    gic_callback = CustomJS(args=dict(source=Overall, sc=sc, select = select, slider=slider), code = 
        var gic = select.value;
        var ior = slider.value;
        console.log('gic=', select.value, ' ior=', slider.value);
        source = source;
        sc = sc;
        sc.data['x'] = [];
        sc.data['y'] = [];
        sc.data['gic'] = [];
        for (var i = 0; i <= source.get_length(); i++){
            if (source.data['x'][i] <= ior && source.data['gic'][i] == gic ){
            sc.data['x'].push(source.data['x'][i]);
            sc.data['y'].push(source.data['y'][i]);
            sc.data['gic'].push(source.data['gic'][i]);   
          }            
        }
        sc.change.emit();

        ) '''