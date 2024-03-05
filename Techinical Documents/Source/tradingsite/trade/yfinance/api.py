import yfinance as yf
from django.conf import settings

multi_data = yf.download(["AAPL", "MSFT"], period="10y")

for stock_name in multi_data["Open"]:
    yf.download([stock_name], period="10y").to_csv(stock_name+'_hist.csv')
    print(stock_name)


print(multi_data)
