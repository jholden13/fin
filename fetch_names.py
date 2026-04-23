import yfinance as yf
import pandas as pd

tickers_df = pd.read_csv("tickers.csv")
tickers = tickers_df["Ticker"].tolist()
print(f"Fetching names for {len(tickers)} tickers...\n")

names = {}
for ticker in tickers:
    print(f" {ticker}...", end=" ")
    try:
        info = yf.Ticker(ticker).info
        name = info.get("longName") or info.get("shortName") or ticker
        names[ticker] = name
        print(name)
    except Exception as e:
        print(f"FAILED ({e})")
        names[ticker] = ticker

# Save the names to a CSV file
names_df = pd.DataFrame(list(names.items()), columns=["Ticker", "Name"])
names_df.to_csv("names.csv", index=False)

print(f"\nSaved {len(names_df)} ticker/name pairs to names.csv")
print(names_df)