from bokeh.plotting import figure
from bokeh.io import output_notebook, show
import pandas as pd
from bokeh.models import Range1d

from bokeh.models import LinearAxis
from bokeh.models import DatetimeTickFormatter
from bokeh.models.sources import ColumnDataSource
from bokeh.palettes import brewer


dictx = {'x': [1, 2, 3]}
dicty1 = {'y1': [4, 3, 4]}
dicty2 = {'y2': [3, 3, 3]}

p = figure(title='Price', 
            plot_width=1200, 
            plot_height=800)
X = dictx.get('x')
Y1 = dicty1.get('y1')
Y2 = dicty2.get('y2')
source = ColumnDataSource(data=dict(x=X, y1=Y1, y2=Y2))
p.line('x','y1',  source=source, line_color="red")
p.line('x','y2',  source=source, line_color="blue")
show(p)
