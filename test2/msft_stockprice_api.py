import pandas as pd
import matplotlib.pyplot as matplt
import json
import urllib.request
alphav_api_key= "E7LPT7HF7GMJ6QLH"
stock_url='https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&outputsize=full&apikey={}'.format(alphav_api_key)
with urllib.request.urlopen(stock_url) as msft_url:
    msft_data = json.loads(msft_url.read().decode())["Time Series (Daily)"]
    #print(msft_data)
    stockdf = pd.DataFrame(columns=["Date","Open","High","low","close","volume"])
    stock_info_list = []
    for dates,info in msft_data.items():
        #new_date = datetime.datetime.strptime(dates,"%Y:%m:%d")
        stock_info_list.append([dates,float(info['1. open']),float(info['2. high']),float(info['3. low']),float(info['4. close']),float(info['5. volume'])])

    for row in stock_info_list[::-1]:
        stockdf.loc[len(msft_data)+1] = row
        stockdf.index -= 1

    print(stock_info_list[3])



#stockdf.iloc[::-1].reset_index(drop=True)
#stockdf["dateindex"] = pd.to_datetime(stockdf['date'],format='%Y/%m/%d')
#stockdf = stockdf.set_index(stockdf["dateindex"])
#stockdf.to_csv('stock_msft.csv')
#df = pd.read_csv('stock_msft.csv', parse_dates=True, index_col=0)
#part = df[4000:]
#part[['Open','close']].plot()
#matplt.show()
stockdf.to_csv('stock_msft.csv')
df = pd.read_csv('stock_msft.csv', parse_dates=True, index_col=0)
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)
df.info()
part = df[4000:]
part[['Open']].plot()
matplt.show()
#print(stockdf[4500:])


print("msft stock data written to csv")

