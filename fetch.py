import yfinance as yf
import pandas as pd

tickers_df = pd.read_csv("tickers.csv")
tickers = tickers_df["Ticker"].tolist()

data = yf.download(tickers, period="1y", interval="1d")
close_prices = data["Close"]
close_prices.to_csv("prices.csv")
print(f"Saved {len(close_prices.columns)} tickers with {len(close_prices)} days of data")
