'''from test2 import sent_getter as s
from textblob import TextBlob
print(s.sentiment("I m watching 1928 Disney cartoons and I love them,they are the best "))
#print(TextBlob.sentiment.po("I m watching 1928 Disney cartoons and I love them,they are the best and most amazing"))'''
import pickle
import bokeh
from bokeh.plotting import figure
from bokeh.io import output_file,show
from datetime import timedelta
import matplotlib.dates as mdates
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


import pandas as pd
'''df = pd.read_csv('msft5.csv')
df['Sentiment'] = pd.to_numeric(df['Sentiment'])
most_pos_index = df['Sentiment'].argmax()
most_neg_index = df['Sentiment'].argmin()
neg_tweet = df.iloc[most_neg_index]["tweet_text"]
pos_tweet = df.iloc[most_pos_index]["tweet_text"]
print(most_neg_index,neg_tweet)
print(most_pos_index,pos_tweet)'''




df = pd.read_csv('sent_stock_data2.csv')
df.info()
part = df

fig,ax = plt.subplots()
ax.plot(part.time, part.stock_price, color="red", marker="o")
ax.set_xlabel("date",fontsize=14)
# Tell matplotlib to interpret the x-axis values as dates
#ax.xaxis_date()
# Make space for and rotate the x-axis tick labels
#fig.autofmt_xdate()
# set y-axis label
ax.set_ylabel("Price",color="red",fontsize=14)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
fig.autofmt_xdate()
ax2=ax.twinx()
ax2.plot(part.time, part.Sentiment, marker="o")
ax2.set_ylabel("Sentiment",color="blue",fontsize=14)
plt.show()



