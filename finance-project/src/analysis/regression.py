#%%
import numpy as np
import plotly.graph_objects as go
import statsmodels.api as sm
from analysis.regression_result_printer import print_regression_summary

from common.constants import get_ff3 
from common.constants import get_portfolio_daily_values_and_returns

def fit_factor_regression(port_rf, df_merged):
    factors = sm.add_constant(df_merged[["Mkt-RF", "SMB", "HML", "Mom"]])
    return sm.OLS(port_rf, factors).fit()

def plot_portrf_vs_mktrf(df_merged):
    mkt_rf = df_merged["Mkt-RF"]
    slope, intercept = np.polyfit(mkt_rf, df_merged["portRf"], 1)
    line_x = np.array([mkt_rf.min(), mkt_rf.max()])
    fit_label = f"linear fit:<br>{intercept:.4f} + {slope:.2f} * Mkt-Rf"

    figure = go.Figure()
    figure.add_trace(go.Scatter(x=mkt_rf, y=df_merged["portRf"], mode="markers", name="portRf"))
    figure.add_trace(go.Scatter(x=line_x, y=slope * line_x + intercept, mode="lines", name=fit_label, line=dict(color="orange")))
    figure.update_layout(xaxis_title="Market Excess Return (Mkt-Rf)", yaxis_title="Portfolio Excess Return", title="Portfolio excess return vs. Market excess return")
    figure.show(renderer="svg")

def regress_returns(df_merged):
    plot_portrf_vs_mktrf(df_merged)
    model = fit_factor_regression(df_merged["portRf"], df_merged)
    # print(model.summary())
    print_regression_summary(model)
    return df_merged

if __name__ == "__main__":
    print("ok")
    
    
# %%
