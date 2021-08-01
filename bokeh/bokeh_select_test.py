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
    sp = dforg[['ior', 'pe', 'GICS Sector', 'GICS Sub Industry', 'symbol', 'fpe']]
    sp.columns = ['x', 'y', 'gic', 'gicsub', 'symbol', 'fpe']
    sp1 = sp.loc[sp['y'].notnull()]
    
    spA = sp1.reset_index().dropna().set_index('index')
    sp = spA[(spA['x']<30)&(spA['y']<100)]

    MARKERS = ['circle', 'circle_x', 'hex', 'triangle']
    sp['markers'] = MARKERS[0]
    sp.loc[((sp['fpe']/sp['y']>1)&((sp['fpe']/sp['y'])<=1.5)), 'markers']=MARKERS[1]
    sp.loc[((sp['fpe']/sp['y']>1.5)&((sp['fpe']/sp['y'])<=2.5)), 'markers']=MARKERS[2]
    sp.loc[((sp['fpe']/sp['y'])>2.5), 'markers']=MARKERS[3]

    sp.loc[len(sp), :] = [0, 0, 'ALL', 'ALL', '', 0,  MARKERS[0]]
    gics = list(sp['gic'].unique())
    gicsub = list(sp['gicsub'].unique())

    source = sp
    sourcex = source[source['gic']!='ALL']
    Overall=ColumnDataSource(source)
    sc=ColumnDataSource(sourcex)


    #TOOLTIPS = [('index', '$index'), ('(ior, pe)', '(@ior{0.0}, @eps)'), ('symbol', '@symbol')] 
    #hover = HoverTool(tooltips=TOOLTIPS)
    #p = figure(plot_width = 900, plot_height=500, tooltips=TOOLTIPS)

    p = figure(plot_width = 900, plot_height=500)
    #p.circle(x='x', y='y', size=5, source=sc)
    #p.circle(x='x', y='y', size=5, source=sc, color=factor_cmap('gic', 'Category10_3', gics))
    
    p.scatter('x', 'y', source=sc, legend='markers', 
          fill_alpha=0.4, size=12,
          marker=factor_mark('markers', MARKERS, MARKERS),
          color=factor_cmap('gicsub', 'Category10_3', gicsub))
    

    labels = LabelSet(x='x', y='y', source=sc, text='symbol')
    p.add_layout(labels)

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
        sc.data['gicsub'] = [];
        sc.data['symbol'] = [];
        sc.data['fpe'] = [];
        sc.data['markers'] = [];
        for (var i = 0; i <= source.get_length(); i++){
            if (gic == 'ALL') {
                if (source.data['x'][i] >= ior ){
                sc.data['x'].push(source.data['x'][i]);
                sc.data['y'].push(source.data['y'][i]);
                sc.data['gic'].push(source.data['gic'][i]);   
                sc.data['gicsub'].push(source.data['gicsub'][i]);  
                sc.data['symbol'].push(source.data['symbol'][i]); 
                sc.data['fpe'].push(source.data['fpe'][i]); 
                sc.data['markers'].push(source.data['markers'][i]);                 
                }  
            }
            else {
                if (source.data['x'][i] >= ior && source.data['gic'][i] == gic ){
                sc.data['x'].push(source.data['x'][i]);
                sc.data['y'].push(source.data['y'][i]);
                sc.data['gic'].push(source.data['gic'][i]);   
                sc.data['gicsub'].push(source.data['gicsub'][i]);  
                sc.data['symbol'].push(source.data['symbol'][i]);
                sc.data['fpe'].push(source.data['fpe'][i]); 
                sc.data['markers'].push(source.data['markers'][i]);   
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