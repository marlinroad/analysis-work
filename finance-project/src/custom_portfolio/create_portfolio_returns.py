#%%
import pandas as pd

from common.constants import get_path, get_portfolio_config

def normalize_dates(values):
    return pd.to_datetime(values, utc=True).dt.tz_localize(None).dt.normalize()

def get_daily_cashflows(df_config):
    config = df_config.copy()
    config["date"] = normalize_dates(config["date"])
    # sum tx cfs per date, maybe many txs per date
    return config.groupby("date")["cashflow"].sum()

def calculate_portfolio_daily_returns(df_portfolio_values, df_config):
    portfolio_values = df_portfolio_values.copy()
    portfolio_values["date"] = normalize_dates(portfolio_values["date"])
    # portfolio_values["close"] = pd.to_numeric(portfolio_values["close"])
    portfolio_values = portfolio_values.sort_values("date").reset_index(drop=True)

    daily_cashflows = get_daily_cashflows(df_config)
    portfolio_values["cashflow"] = (
        portfolio_values["date"].map(daily_cashflows).fillna(0.0)
    )

    previous_close = portfolio_values["close"].shift(1)
    portfolio_values["dlyret"] = (
        (portfolio_values["close"] + portfolio_values["cashflow"] - previous_close)
        .div(previous_close)
        .where(previous_close.ne(0))
    )
    return portfolio_values

def generate_portfolio_returns():
    portfolio_values = pd.read_csv(get_path("portfolio_daily_values.csv"))
    portfolio_config = get_portfolio_config()
    portfolio_values_and_returns = calculate_portfolio_daily_returns(
        portfolio_values,
        portfolio_config,
    )
    portfolio_values_and_returns.to_csv(
        get_path("portfolio_daily_values_and_returns.csv"),
        index=False,
    )

if __name__ == "__main__":
    generate_portfolio_returns()

# %%
