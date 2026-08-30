#%%
import pandas as pd

def compute_sharpe_ratio(df_merged):
    excess_return = df_merged["portRf"]
    return excess_return.mean() / excess_return.std() * (252 ** 0.5)    

def compute_sharpe_ratio_from_the_past_years(df_merged, years=1):
    max_date = df_merged["date"].max()
    min_date = max_date - pd.DateOffset(years=years)

    excess_return = df_merged.loc[
        df_merged["date"] >= min_date, "portRf"
    ]
    return excess_return.mean() / excess_return.std() * (252 ** 0.5)

def compute_market_sharpe_ratio(df_merged):
    excess_return = df_merged["Mkt-RF"]
    return excess_return.mean() / excess_return.std() * (252 ** 0.5)

def get_cagr(return_series):
    return (return_series + 1).prod() ** (252 / len(return_series)) - 1

def get_market_cagr(df_merged):
    df_merged["Mkt"] = df_merged["Mkt-RF"] + df_merged["RF"]
    return round(get_cagr(df_merged["Mkt"]), 4)

def calc_metrics(df_merged):
    print("Portfolio returns volatility:", df_merged["portRf"].std() * (252 ** 0.5))
    cagr = round(get_cagr(df_merged["dlyret"]), 4)
    print("Portfolio total return, CAGR:", cagr)
    print("Market total return, CAGR:", get_market_cagr(df_merged))
    print("Market returns volatility:", df_merged["Mkt-RF"].std() * (252 ** 0.5))
    print("Sharpe Ratio:", compute_sharpe_ratio(df_merged))
    print("Sharpe Ratio (Past Year):", compute_sharpe_ratio_from_the_past_years(df_merged, years=1))
    print("Sharpe Ratio (Past 3 Years):", compute_sharpe_ratio_from_the_past_years(df_merged, years=3))
    print("Market Sharpe Ratio:", compute_market_sharpe_ratio(df_merged))


if __name__ == "__main__":
    print("test")

# %%
