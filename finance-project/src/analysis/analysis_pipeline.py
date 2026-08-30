#%%

from analysis.regression import regress_returns
from analysis.metrics import calc_metrics
from common.constants import get_ff3, get_portfolio_daily_values_and_returns

def filter_data_by_date(df_ff3, df_returns):
    start_date = min(df_returns["date"])
    end_date = min(df_returns["date"].max(), df_ff3["date"].max())
    df_ff3 = df_ff3[(df_ff3["date"] >= start_date) & (df_ff3["date"] <= end_date)]    

    df_returns = df_returns[(df_returns["date"] >= start_date) & (df_returns["date"] <= end_date)]
    return df_ff3, df_returns

def create_excess_return_and_filter_dates():
    df_port = get_portfolio_daily_values_and_returns()
    df_ff3 = get_ff3()
    df_ff3, df_returns = filter_data_by_date(df_ff3, df_port)
    df_merged = df_returns.merge(df_ff3, on="date", how="inner")
    df_merged["portRf"] = compute_excess_return(df_merged)
    return df_merged

def compute_excess_return(df_merged):
    return (df_merged["dlyret"] - df_merged["RF"]).rename("portRf")

def run_analysis_pipeline():
    df_merged = create_excess_return_and_filter_dates()
    df = regress_returns(df_merged)
    calc_metrics(df_merged)

if __name__ == "__main__":
    run_analysis_pipeline()



# %%
