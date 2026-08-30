#%%
import pandas as pd

from common.constants import get_path, get_stocks_data, get_portfolio_config

def get_forward_filled_close_prices(df_stocks, symbol, master_dates_df):
    symbol_prices = (
        df_stocks.loc[df_stocks["symbol"] == symbol, ["date", "close"]]
        .sort_values("date")
    )
    symbol_prices = master_dates_df.merge(symbol_prices, on="date", how="left").sort_values("date")
    return symbol_prices["close"].ffill().fillna(0).to_numpy()

def get_shares_held_over_time(df_config, symbol, master_dates_df):
    symbol_transactions = df_config.loc[df_config["symbol"] == symbol, ["date", "total_shares"]].sort_values("date")
    shares_held = pd.merge_asof(master_dates_df.sort_values("date"), symbol_transactions, on="date", direction="backward")
    return shares_held["total_shares"].fillna(0).to_numpy()

def build_master_dates_df(df_stocks, df_config):
    start_date = df_config["date"].min()
    master_dates = pd.Series(sorted(df_stocks.loc[df_stocks["date"] >= start_date, "date"].unique()))
    return pd.DataFrame({"date": master_dates})

def calculate_portfolio_daily_values(df_stocks, df_config):
    df_stocks = df_stocks.copy()
    df_config = df_config.copy()

    # stock dates carry a UTC offset; drop tz and time so dates line up with config dates
    df_stocks["date"] = pd.to_datetime(df_stocks["date"]).dt.tz_localize(None).dt.normalize()
    df_config["date"] = pd.to_datetime(df_config["date"]).dt.normalize()

    master_dates_df = build_master_dates_df(df_stocks, df_config)

    total_value = pd.Series(0.0, index=master_dates_df.index)
    for symbol in df_config["symbol"].unique():
        close_prices = get_forward_filled_close_prices(df_stocks, symbol, master_dates_df)
        shares_held = get_shares_held_over_time(df_config, symbol, master_dates_df)
        total_value += shares_held * close_prices

    df_portfolio_values = pd.DataFrame({"date": master_dates_df["date"], "close": total_value.round(2)})
    return df_portfolio_values

def generate_portfolio_values():
    df_stocks = get_stocks_data()
    df_config = get_portfolio_config()
    df_portfolio_values = calculate_portfolio_daily_values(df_stocks, df_config)
    df_portfolio_values.to_csv(get_path("portfolio_daily_values.csv"), index=False) 

if __name__ == "__main__":
    generate_portfolio_values()    
    

# %%
