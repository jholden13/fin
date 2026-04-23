import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

prices = pd.read_csv("prices.csv", index_col="Date", parse_dates=True)
returns = prices.pct_change().iloc[1:]

names_df = pd.read_csv("names.csv")
TICKER_NAMES = dict(zip(names_df["Ticker"], names_df["Name"]))

st.title("Stock Correlation Analysis")
st.caption("Top 30 Stocks - Daily return correlations for last 60 days and 120 days")

tickers = sorted(returns.columns.tolist())
target = st.selectbox("Pick target stock", tickers)

corr_3mo = returns.tail(60).corr()[target].sort_values(ascending=False)
corr_6mo = returns.tail(120).corr()[target].sort_values(ascending=False)

dates_3mo = returns.tail(60).index
dates_6mo = returns.tail(120).index

range_3mo = f"{dates_3mo.min().date()} to {dates_3mo.max().date()}"
range_6mo = f"{dates_6mo.min().date()} to {dates_6mo.max().date()}"

TOPN = 31

corr_3mo = corr_3mo.head(TOPN)
corr_6mo = corr_6mo.head(TOPN)

vol_3mo = returns.tail(60).std() * (252 ** 0.5)
vol_6mo = returns.tail(120).std() * (252 ** 0.5)

table_3mo = pd.DataFrame({
    "Name": corr_3mo.index.map(TICKER_NAMES),
    "Correlation": corr_3mo.values,
    "Volatility": vol_3mo.reindex(corr_3mo.index).values,
}, index=corr_3mo.index)

table_6mo = pd.DataFrame({
    "Name": corr_6mo.index.map(TICKER_NAMES),
    "Correlation": corr_6mo.values,
    "Volatility": vol_6mo.reindex(corr_6mo.index).values,
}, index=corr_6mo.index)

chart_3mo = corr_3mo.rename("correlation").to_frame()
chart_6mo = corr_6mo.rename("correlation").to_frame()

col1, col2 = st.columns(2)

with col1:
    st.subheader("60 Day Correlation")
    st.caption(range_3mo)
    st.dataframe(table_3mo)
 #   st.bar_chart(chart_3mo, horizontal=True, height=400)

with col2:
    st.subheader("120 Day Correlation")
    st.caption(range_6mo)
    st.dataframe(table_6mo)
#    st.bar_chart(chart_6mo, horizontal=True, height=400)
