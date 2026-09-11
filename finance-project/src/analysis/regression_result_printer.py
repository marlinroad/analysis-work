#%%
import pandas as pd
from report.report import display_header, display_report

def get_significance_stars(p_value):
    if p_value < 0.01:
        return "***"
    if p_value < 0.05:
        return "**"
    if p_value < 0.10:
        return "*"
    return ""

def build_regression_summary_table(model):
    rows = []
    for name in model.params.index:
        label = "alpha" if name == "const" else name
        rows.append(
            {
                "Factor": label,
                "Coefficient": model.params[name],
                "t-stat": model.tvalues[name],
                "p-value": model.pvalues[name],
                "Sig.": get_significance_stars(model.pvalues[name]),
            }
        )
    return pd.DataFrame(rows)

def build_regression_fit_table(model):
    values = pd.Series(
        [model.rsquared, model.rsquared_adj, int(model.nobs)],
        dtype=object,
    )
    return pd.DataFrame({0: ["R-squared", "Adj. R-squared", "N"], 1: values})

def print_regression_summary(model):
    summary_table = build_regression_summary_table(model)
    fit_table = build_regression_fit_table(model)

    styled_summary = (
        summary_table.style
        .format("{:.3f}", subset=["Coefficient"])
        .format("{:.2f}", subset=["t-stat", "p-value"])
        .hide(axis="index")
    )
    styled_fit = (
        fit_table.style
        .format(lambda value: str(value) if isinstance(value, int) else f"{value:.2f}", subset=[1])
        .hide(axis="index")
        .hide(axis="columns")
    )

    display_header("Regression results")
    display_header("Portfolio excess returns regressed on FF3 factors (Market, SMB, HML) and momentum factor", level=4)
    display_report(styled_summary)
    display_report(styled_fit)
