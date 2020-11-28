import pickle
import bokeh
from bokeh.plotting import figure
from bokeh.io import output_file,show
from bokeh.models.tools import HoverTool
from bokeh.models import ColumnDataSource
from datetime import timedelta
import matplotlib.dates as mdates
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


import pandas as pd
df = pd.read_csv('sent_stock_data2.csv')
df.info()

df['time']=pd.to_datetime(df['time'])
part = df
source = ColumnDataSource(part)
print(source)
values_x = [ 1,2,3,4,5,6,7,8]
values_y = [ a for a in part.stock_price]


plot = figure(title= "Stock price", x_axis_label='Date', y_axis_label='stock price',x_axis_type='datetime')
plot.line(x=part.time,y=values_y, line_color='blue', line_width = 5)

for a in range(len(values_y)):
    if part.Sentiment[a] > 10:
        plot.circle(df.iloc[a]["time"],values_y[a], fill_color='blue', size=50)
    else:
        plot.circle(df.iloc[a]["time"],values_y[a], fill_color='green', size=50)

hover = HoverTool()
hover.tooltips=[
    ('Average sentiment', '@time')
]

plot.add_tools(hover)


output_file('index.html')
show(plot)