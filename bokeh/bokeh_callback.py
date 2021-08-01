#from bokeh.io import output_file, show
#from bokeh.models.widgets import CheckboxGroup, ColorPicker, Slider, Select
from bokeh.layouts import column
from bokeh.models import CustomJS, ColumnDataSource, Slider
from bokeh.plotting import Figure, output_file, show

'''
###checkboc
output_file("checkbox_group.html")
checkbox_group = CheckboxGroup(
        labels=["Option 1", "Option 2", "Option 3"], active=[0, 1])
show(checkbox_group)
'''

output_file("callback.html")

x = [x*0.005 for x in range(0, 200)]
y = x

source = ColumnDataSource(data=dict(x=x, y=y))

plot = Figure(plot_width=400, plot_height=400)
plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

callback(source=source, window=None)
data = source.data
f = cb_obj.value
x, y = data['x'], data['y']
for i in range(len(x)):
    y[i] = window.Math.pow(x[i], f)
source.change.emit()

slider = Slider(start=0.1, end=4, value=1, step=.1, title="power",
                callback=CustomJS(callback))

layout = column(slider, plot)

show(layout)
