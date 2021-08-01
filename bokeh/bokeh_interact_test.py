import pandas as pd
import numpy as np
from yahoofinancials import YahooFinancials
import datetime as dt
from bokeh.plotting import figure, output_file, save, show
from bokeh.models.sources import ColumnDataSource
from bokeh.models import Range1d
from bokeh.models.tools import HoverTool, PointDrawTool
from bokeh.layouts import row, column, layout, widgetbox
#from bokeh.models.widgets import Slider, Select
from bokeh.models import CustomJS, ColumnDataSource, Slider, Select
from bokeh.models import ColumnDataSource, CDSView, IndexFilter, BooleanFilter, HoverTool


#import py3_RSI as rsi

'''
today = dt.date.today().strftime('%Y-%m-%d')
startdate = dt.datetime(2015, 1, 1)
AAPLrsi = rsi.getRSIList(startdate, 'NTDOY', 14)
AAPL = AAPLrsi[['Date', 'Close', 'RSI']]
AAPL.to_csv('/home/lan/Documents/py3ds/output/stockcsv/ntdoy.csv')
'''
dforg=pd.read_csv(r'/home/lan/Documents/py3ds/output/stockcsv/inner_sp.csv')
sp = dforg[['ior', 'eps',	'GICS Sector']]
sp.columns = ['ior', 'eps', 'GIC']
   # print(len(sp))
spA = sp.reset_index().dropna().set_index('index')
sp = spA[(spA['ior']<30)&(spA['eps']<30)]
gics = list(sp['GIC'].unique())
gics.append('ALL')



def jscallback(source):   
    callback = CustomJS(args=dict(source=source), code="""
    var data = source.data;
    var f = cb_obj.value
    var x = data['ior']
    var y = data['eps']
    source.change.emit();
""")

def drawROI_EPS(dforg):
    tooltips = []
    '''
    filename = '/home/lan/Documents/py3ds/output/stockchart/' + dforg + '.html'
    output_file(filename)
    #output_file('/home/lan/Documents/py3ds/output/td.html')
    save(p)
    
    #p.line(x='Date', y='Close', color='blue', line_width=1, source=data_source)
    #prsi.line(x=xlist, y=yrsi)
    #show(prsi)
    pclose.line(x=xlist, y=yclose)
    prsi.line(x=xlist, y=yrsi)
    show(column(prsi, pclose))
    '''
def select_gic(gic_selector, ior_slider):
    selected = sp
    gic = gic_selector.value
    min_ior = ior_slider.value

    if (gic != 'ALL'):
        selected = selected[selected['GIC'] == gic]
    
    selected = selected[selected['ior']>=min_ior]

    print('gic = ', gic)
    print('Min ior = ', min_ior )
    return selected

def update():
    df = select_gic()
    #print(list(df['GIC']))
    #source.data = dict(x=df['ior'], y=df['eps'], GIC=df['GIC'])
    source = ColumnDataSource(df)


def main():

    output_file("callback.html")

    
    dforg=pd.read_csv(r'/home/lan/Documents/py3ds/output/stockcsv/inner_sp.csv')
    sp = dforg[['ior', 'eps', 'GICS Sector']]
    sp.columns = ['x', 'y', 'gic']
   # print(len(sp))
    spA = sp.reset_index().dropna().set_index('index')
    sp = spA[(spA['x']<30)&(spA['y']<30)]
    gics = list(sp['gic'].unique())
    gics.append('ALL')

    x = sp['x']
    y = sp['y']
    gic = sp['gic']
   # source = ColumnDataSource(dict(x=x, y=y))

    source = sp
    #sourcex = source[(source['x'] > 0.1& source['gic']=='Health Care')]
    sourcex = source[source['gic']=='Health Care']
    Overall=ColumnDataSource(source)
    sc=ColumnDataSource(sourcex)

    dfe = source[source['gic']=='Energy']
    sce = ColumnDataSource(dfe)
    dfhc = source[source['gic']=='Health Care']
    schc = ColumnDataSource(dfhc)
    #boolinit = source['x']>0.5
    #view = CDSView(source=Overall, filters=[BooleanFilter(boolinit)])
    #hover3 = HoverTool(tooltips = [('day', '@day'),('Sales','@{Sales}{0,0}')],
     #              formatters = {'day': 'datetime','Sales': 'numeral'})

    TOOLTIPS = [('ior', '$ior'), ('eps', '$eps'), ('GIC', '@GIC')] 
    p = figure(plot_width = 600, plot_height=300, tooltips=TOOLTIPS)
    p.circle('x', 'y', size=5, source=sc)


    #gic_callback = CustomJS(args=dict(source=Overall,ts=sc), code = '''
    gic_callback = CustomJS(args=dict(source=Overall, sc=sc), code = '''
        var f = cb_obj.value;
        console.log(' changed selected option', f);
        sc = sc
        sc.data['x'] = [];
        sc.data['y'] = [];
        sc.data['gic'] = [];
        for (var i = 0; i <= source.get_length(); i++){
            if (source.data['gic'][i] == f){
            sc.data['x'].push(source.data['x'][i]);
            sc.data['y'].push(source.data['y'][i]);
            sc.data['gic'].push(source.data['gic'][i]);   
          }            
        }
        sc.change.emit();

        ''')  
    #slider_1 = Slider(start=0.1, end=1, value=.1, step=.01, title="ior",callback=ior_callback)
    #ior_callback.args['slider'] = slider_1  
    #select = Select(title='GIC', options=sorted(gics), value='ALL', callback=gic_callback)  
    select = Select(title="Option:", value="ALL", options=sorted(gics))
    select.callback = gic_callback
    #gic_callback.args['select'] = select
   

    layout = column( select, p)
# execute a callback whenever the plot canvas is tapped
    show(layout)


    '''
        ior_callback = CustomJS(args=dict(source=Overall, sc=sc), code = 
        var f = cb_obj.value;
        sc.data['x'] = [];
        sc.data['y'] = [];
        sc.data['gic'] = [];
        for (var i = 0; i <= source.get_length(); i++){
           if (source.data['x'][i] >= f){
            sc.data['x'].push(source.data['x'][i])
            sc.data['y'].push(source.data['y'][i])
            sc.data['gic'].push(source.data['gic'][i])    
          }            
        }
        sc.change.emit();
        ) 
        sc.data['x'] = [];
        sc.data['y'] = [];
        sc.data['gic'] = [];

        for(var i=0;i<gic.length; i++){
            if(section[i]==f){
            sc.data['x'].push(source.data['x'][i])
            sc.data['y'].push(source.data['y'][i])
            sc.data['gic'].push(source.data['gic'][i])    
            }
        }
        var f = slider.value;
    dforg=pd.read_csv(r'/home/lan/Documents/py3ds/output/stockcsv/inner_sp.csv')
    sp = dforg[['ior', 'eps',	'GICS Sector']]
    sp.columns = ['ior', 'eps', 'GIC']
   # print(len(sp))
    spA = sp.reset_index().dropna().set_index('index')
    sp = spA[(spA['ior']<30)&(spA['eps']<30)]
    
    #sp['GIC'] = sp['GIC'].str.strip()
    gics = list(sp['GIC'].unique())
    gics.append('ALL')
    #print(regions)
    '''
    '''
    #source = ColumnDataSource(data=dict(x=[], y=[], GIC=[]))``
    source = ColumnDataSource(sp)
    TOOLTIPS = [('ior', '$ior'), ('eps', '$eps'), ('GIC', '@GIC')] 
    p = figure(plot_width = 600, plot_height=300, tooltips=TOOLTIPS)
    p.circle(x='ior', y='eps', size=5, source=source)

    ior_slider = Slider(start=0, end=1, value=0.3, step=.01, title='minimum IOR')
    gic_selector = Select(title='GIC', options=sorted(gics), value='ALL')
    
    ior_slider.js_on_change('value', jscallback(select_gic(gic_selector, ior_slider)))
    gic_selector.js_on_change('value', jscallback(select_gic(gic_selector, ior_slider)))

    layout = column(ior_slider, gic_selector, p)
    show(layout)
    
    
    #widget not working
    #gic_selector = Select(title='GIC', options=sorted(gics), value='ALL')
    gic_selector.on_change('value', lambda attr, old, new:update())
    #ior_slider = Slider(start=0, end=1, value=0.3, step=.01, title='minimum IOR')
    ior_slider.on_change('value', lambda attr, old, new: update())
    #update(sp, gic_selector, ior_slider, source)
    update()
    TOOLTIPS = [('ior', '$ior'), ('eps', '$eps'), ('GIC', '@GIC')]    
    p = figure(plot_width = 600, plot_height=300, tooltips=TOOLTIPS)
    p.circle(x='ior', y='eps', size=5, source=source)
    inputs = widgetbox(gic_selector, ior_slider)
    plot_layout = layout([inputs], [p])
    show(plot_layout)
    #update(sp, gic_selector, ior_slider, source)
    '''
   


'''
    #sp = sp.dropna(how='any') 
    X = list(sp['ior'])
    Y = list(sp['eps'])
    Z = list(sp['GIC'])
    
    #convert string to numeric
    #sp['ior'] = pd.to_numeric(sp['ior'], errors = 'coerce')
    #sp['eps'] = pd.to_numeric(sp['eps'], errors = 'coerce')
    #data_source = ColumnDataSource(data=dict(x=X, y=Y, GIC=Z,))
    data_source = ColumnDataSource(sp)
    
    TOOLTIPS = [('ior', '$ior'), ('eps', '$eps'), ('GIC', '@GIC')]
    toolbox = ['pan', 'box_zoom', 'box_select', 'save', 'reset', 'hover']
    p = figure(plot_width = 600, plot_height=300, tooltips=TOOLTIPS, toolbar_location='below',\
        toolbar_sticky = False, tools = toolbox)
    
    circles = p.circle(x='ior', y='eps', size=5, color='red', source=data_source)
    point_tool = PointDrawTool(renderers=[circles])

    p.circle(x='ior', y='eps', size=10, source=data_source)
    p.add_tools(point_tool)

    show(p)
'''
if __name__ == '__main__':
    main()
    