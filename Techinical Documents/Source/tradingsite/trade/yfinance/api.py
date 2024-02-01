import yfinance as yf

multi_data = yf.download(["AAPL", "MSFT"], period="10y")

for stock_name in multi_data["Close"]:
    yf.download([stock_name], period="10y").to_csv(f"stock_data/{stock_name}_hist.csv")
    print(stock_name)


print(multi_data)
