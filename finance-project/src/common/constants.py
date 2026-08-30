#%%
import pandas as pd
from pathlib import Path


def resolve_data_root():
    return Path(__file__).resolve().parents[2] / "data"
    
def get_path(subpath=""):
    return resolve_data_root() / subpath

def get_stocks_data():
    df_stocks = pd.read_csv(get_path("stocks_daily_rets_v2.csv"))
    return df_stocks    

def get_spy_data():
    df_spy = pd.read_csv(get_path("SPY_daily_rets_v2.csv"))
    return df_spy

def get_portfolio_daily_values_and_returns():
    df_port = pd.read_csv(get_path("portfolio_daily_values_and_returns.csv"), parse_dates=["date"])
    df_port = df_port.iloc[1:].reset_index(drop=True)
    return df_port

def get_ff3():    
    df = pd.read_csv(get_path("F-F_Research_Data_Factors_daily.csv"), skiprows=4, skipfooter=2, engine="python", parse_dates=[0])
    df.rename(columns={df.columns[0]: "date"}, inplace=True)
    df.loc[:, df.columns != "date"] /= 100
    return df
    
def get_portfolio_config():
    df_config = pd.read_csv(get_path("portfolio_transactions.csv"))
    return df_config