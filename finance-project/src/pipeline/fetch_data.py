#%%
from common.constants import get_path
import pandas as pd

from client.alpaca_client import get_daily_stock_prices

def fetch_stock_prices():
    symbols = ["AAPL", "WMT", "JPM", "XOM", "JNJ", "CAT"]
    df_stocks = get_daily_stock_prices(symbols)
    df_stocks.to_csv(get_path("stocks_daily_rets.csv"), index=False)
    df_spy = get_daily_stock_prices(["SPY"])
    df_spy.to_csv(get_path("SPY_daily_rets.csv"), index=False)

def add_daily_return_for_stocks(df_stocks):
    df_stocks = df_stocks.sort_values(["symbol", "timestamp"])
    df_stocks["daily_return"] = df_stocks.groupby("symbol")["close"].pct_change()
    return df_stocks

def first_set():
    df_stocks = pd.read_csv(get_path("stocks_daily_rets.csv"))
    df_stocks = add_daily_return_for_stocks(df_stocks)
    df_stocks.rename(columns={"timestamp": "date"}, inplace=True)
    df_stocks.to_csv(get_path("stocks_daily_rets_v2.csv"), index=False)

    df_spy = pd.read_csv(get_path("SPY_daily_rets.csv"))
    df_spy = add_daily_return_for_stocks(df_spy)
    df_spy.rename(columns={"timestamp": "date"}, inplace=True)
    df_spy.to_csv(get_path("SPY_daily_rets_v2.csv"), index=False)
    
def fetch_and_save(symbol):
    df = get_daily_stock_prices([symbol])
    df = add_daily_return_for_stocks(df)
    df.rename(columns={"timestamp": "date"}, inplace=True)
    df.to_csv(get_path(f"{symbol}_daily_rets_v2.csv"), index=False)
    return df

def fetch_all():
    fetch_stock_prices()
    first_set()
    fetch_and_save("QQQ")

def test_fetch(symbol):
    return get_daily_stock_prices([symbol])

if __name__ == "__main__":
    fetch_all()    
    # df = test_fetch("QQQ")
    

# %%
