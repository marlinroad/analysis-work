#%%
import pandas as pd
from analytics.drawdown import compute_drawdown_metrics
from report.report import display_header, display_report

def get_sharpe(excess_return):
    return excess_return.mean() / excess_return.std() * (252 ** 0.5)

def compute_sharpe_ratio(df_merged):
    return get_sharpe(df_merged["portRf"])

def compute_sharpe_ratio_from_the_past_years(df_merged, years=1):
    max_date = df_merged["date"].max()
    min_date = max_date - pd.DateOffset(years=years)
    recent = df_merged.loc[df_merged["date"] >= min_date]

    portfolio_sharpe = get_sharpe(recent["portRf"])
    market_sharpe = get_sharpe(recent["Mkt-RF"])
    return portfolio_sharpe, market_sharpe

def compute_market_sharpe_ratio(df_merged):
    return get_sharpe(df_merged["Mkt-RF"])

def get_sharpe_ratios(df_merged):
    sharpe_past_year_portfolio, sharpe_past_year_market = compute_sharpe_ratio_from_the_past_years(
        df_merged, years=1
    )
    sharpe_past_3_years_portfolio, sharpe_past_3_years_market = compute_sharpe_ratio_from_the_past_years(
        df_merged, years=3
    )

    return {
        "portfolio": compute_sharpe_ratio(df_merged),
        "market": compute_market_sharpe_ratio(df_merged),
        "portfolio_past_year": sharpe_past_year_portfolio,
        "market_past_year": sharpe_past_year_market,
        "portfolio_past_3_years": sharpe_past_3_years_portfolio,
        "market_past_3_years": sharpe_past_3_years_market,
    }

def get_cagr(return_series):
    return (return_series + 1).prod() ** (252 / len(return_series)) - 1

def get_market_cagr(df_merged):
    df_merged["Mkt"] = df_merged["Mkt-RF"] + df_merged["RF"]
    return round(get_cagr(df_merged["Mkt"]), 4)

def style_metrics(metrics):
    percentage_rows = metrics.index[
        metrics["Metric"].isin(["CAGR", "Total return", "Annualized volatility"])
    ]
    ratio_rows = metrics.index.difference(percentage_rows)

    return (
        metrics.style
        .format(
            "{:.2%}",
            subset=pd.IndexSlice[
                percentage_rows,
                ["Portfolio", "Market"],
            ],
            na_rep="—",
        )
        .format(
            "{:.2f}",
            subset=pd.IndexSlice[
                ratio_rows,
                ["Portfolio", "Market"],
            ],
            na_rep="—",
        )
        .hide(axis="index")
    )

def calc_perf_metrics(df_merged):
    sharpe_ratios = get_sharpe_ratios(df_merged)

    metrics = pd.DataFrame(
        [
            {
                "Metric": "CAGR",
                "Portfolio": get_cagr(df_merged["dlyret"]),
                "Market": get_market_cagr(df_merged),
            },                     
            {
                "Metric": "Total return",
                "Portfolio": ((df_merged["dlyret"] + 1).prod() - 1),
                "Market": ((df_merged["Mkt-RF"] + df_merged["RF"] + 1).prod() - 1),
            },
            {
                "Metric": "Annualized volatility",
                "Portfolio": df_merged["portRf"].std() * (252**0.5),
                "Market": df_merged["Mkt-RF"].std() * (252**0.5),
            },
            {
                "Metric": "Sharpe ratio",
                "Portfolio": sharpe_ratios["portfolio"],
                "Market": sharpe_ratios["market"],
            },
            {
                "Metric": "Sharpe ratio, past year",
                "Portfolio": sharpe_ratios["portfolio_past_year"],
                "Market": sharpe_ratios["market_past_year"],
            },
            {
                "Metric": "Sharpe ratio, past 3 years",
                "Portfolio": sharpe_ratios["portfolio_past_3_years"],
                "Market": sharpe_ratios["market_past_3_years"],
            },
        ]
    )

    styled_metrics = style_metrics(metrics)
    display_header("Performance metrics")
    display_report(styled_metrics)

def style_drawdown_table(drawdown_table):
    return (
        drawdown_table.drop(columns=["returns_type", "rank"])
        .rename(
            columns={
                "drawdown": "Drawdown",
                "start_date": "Start date",
                "end_date": "End date",
                "num_days": "Amount days",
            }
        )
        .style
        .format(
            {
                "Drawdown": "{:.2%}",
                "Start date": "{:%Y-%m-%d}",
                "End date": "{:%Y-%m-%d}",
            }
        )
        .hide(axis="index")
    )

def calc_drawdown_metrics(df_merged):
    drawdown_metrics = compute_drawdown_metrics(df_merged)

    display_header("Max 5 Drawdowns")
    for returns_type in ["Portfolio", "Market"]:
        drawdown_table = drawdown_metrics.loc[drawdown_metrics["returns_type"] == returns_type]
        display_header(returns_type, level=3)
        display_report(style_drawdown_table(drawdown_table))

    return drawdown_metrics

def calc_metrics(df_merged):
    calc_perf_metrics(df_merged)
    calc_drawdown_metrics(df_merged)
    

if __name__ == "__main__":
    print("test")

# %%
