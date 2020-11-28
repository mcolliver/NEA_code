import pandas as pd
from yahoo_fin import stock_info
import datetime
import matplotlib.pyplot as plt
#df = pd.read_csv(stock_url, parse_dates=True, index_col=0)
alphav_api_key= "E7LPT7HF7GMJ6QLH"
stock_url='https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol=MSFT&interval=60min&slice=year1month1&apikey={}'.format(alphav_api_key)
df = pd.read_csv(stock_url)
#df['time'] = pd.to_datetime(df['time'], format="%d-%m-%Y %H:%M:%S")
df.info()
part = df.head(20)
#print(part)
msft_price = stock_info.get_live_price('msft')
test_date = "2020-11-20 09:00:00"
current_time = datetime.datetime.now().time()
start_time = datetime.time(9,30)
end_time = datetime.time(16,15)
print(start_time)
print(end_time)
print(start_time>current_time)
print(current_time>end_time)

#print(part)
'''fig,ax=plt.subplots()
ax.plot(part.time, part.close, marker="o")
ax.set_xlabel("year")
ax.set_ylabel("price")
#ax.plot(gapminder_us.year, gapminder_us["gdpPercap"], marker="o")
plt.show()'''