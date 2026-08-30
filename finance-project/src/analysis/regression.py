#%%
import numpy as np
import plotly.graph_objects as go
import statsmodels.api as sm

from common.constants import get_ff3 
from common.constants import get_portfolio_daily_values_and_returns

def fit_ff3_regression(port_rf, df_merged):
    factors = sm.add_constant(df_merged[["Mkt-RF", "SMB", "HML"]])
    return sm.OLS(port_rf, factors).fit()

def print_regression_summary(model):
    print("\nAlpha and factor betas")
    for name in model.params.index:
        label = "alpha" if name == "const" else name
        print(f"{label:>8}: coef={model.params[name]: .6f}  t={model.tvalues[name]: .2f}  p={model.pvalues[name]:.4f}")
    print(f"\nR-squared: {model.rsquared:.4f}  Adj. R-squared: {model.rsquared_adj:.4f}  N: {int(model.nobs)}")

def plot_portrf_vs_mktrf(df_merged):
    mkt_rf = df_merged["Mkt-RF"]
    slope, intercept = np.polyfit(mkt_rf, df_merged["portRf"], 1)
    line_x = np.array([mkt_rf.min(), mkt_rf.max()])

    figure = go.Figure()
    figure.add_trace(go.Scatter(x=mkt_rf, y=df_merged["portRf"], mode="markers", name="portRf"))
    figure.add_trace(go.Scatter(x=line_x, y=slope * line_x + intercept, mode="lines", name="linear fit", line=dict(color="orange")))
    figure.update_layout(xaxis_title="Mkt-RF", yaxis_title="portRf", title="Portfolio excess return vs. Mkt-RF")
    figure.show(renderer="svg")

def regress_returns(df_merged):
    plot_portrf_vs_mktrf(df_merged)
    model = fit_ff3_regression(df_merged["portRf"], df_merged)
    print(model.summary())
    print_regression_summary(model)
    return df_merged

if __name__ == "__main__":
    print("ok")
    
    
# %%
