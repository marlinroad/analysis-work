#%%
import pandas as pd
import plotly.graph_objects as go

from common.constants import get_path


def normalize_dates(values):
	return pd.to_datetime(values, utc=True).dt.tz_localize(None).dt.normalize()

def build_growth_index(daily_returns):
	growth_index = pd.Series(index=daily_returns.index, dtype="float64")
	if growth_index.empty:
		return growth_index

	growth_index.iloc[0] = 100.0
	for index in range(1, len(daily_returns)):
		daily_return = daily_returns.iloc[index]
		previous_value = growth_index.iloc[index - 1]
		if pd.isna(daily_return) or pd.isna(previous_value):
			growth_index.iloc[index] = previous_value
		else:
			growth_index.iloc[index] = previous_value * (1 + daily_return)
	return growth_index

def prepare_return_series(df_portfolio, df_spy, df_qqq):
	portfolio = df_portfolio.copy()
	spy = df_spy.copy()
	qqq = df_qqq.copy()

	portfolio["date"] = normalize_dates(portfolio["date"])
	spy["date"] = normalize_dates(spy["date"])
	portfolio = portfolio.sort_values("date")
	spy = spy.sort_values("date")
	qqq["date"] = normalize_dates(qqq["date"])
	qqq = qqq.sort_values("date")

	start_date = portfolio["date"].min()
	end_date = portfolio["date"].max()
	portfolio = portfolio.loc[
		portfolio["date"].between(start_date, end_date)
	].copy()
	spy = spy.loc[spy["date"].between(start_date, end_date)].copy()
	qqq = qqq.loc[qqq["date"].between(start_date, end_date)].copy()

	portfolio["index"] = build_growth_index(
		pd.to_numeric(portfolio["dlyret"], errors="coerce")
	)
	spy["index"] = build_growth_index(
		pd.to_numeric(spy["daily_return"], errors="coerce")
	)
	qqq["index"] = build_growth_index(
		pd.to_numeric(qqq["daily_return"], errors="coerce")
	)

	return portfolio[["date", "index"]], spy[["date", "index"]], qqq[["date", "index"]]

def create_returns_figure(df_portfolio, df_spy, df_qqq):
	portfolio, spy, qqq = prepare_return_series(df_portfolio, df_spy, df_qqq)
	figure = go.Figure()
	figure.add_trace(
		go.Scatter(
			x=portfolio["date"],
			y=portfolio["index"],
			mode="lines",
			name="Portfolio",
		)
	)
	figure.add_trace(
		go.Scatter(
			x=spy["date"],
			y=spy["index"],
			mode="lines",
			name="SPY",
		)
	)
	figure.add_trace(
		go.Scatter(
			x=qqq["date"],
			y=qqq["index"],
			mode="lines",
			name="QQQ",
		)
	)
	figure.update_layout(
		title="Portfolio vs SPY vs QQQ Growth",
		xaxis_title="Date",
		yaxis_title="Growth Index (Base 100)",
		hovermode="x unified",
	)
	return figure

def plot_returns_vs_spy():
    portfolio_values = pd.read_csv(
        get_path("portfolio_daily_values_and_returns.csv")
    )
    spy_values = pd.read_csv(get_path("SPY_daily_rets_v2.csv"))
    qqq_values = pd.read_csv(get_path("QQQ_daily_rets_v2.csv"))
    returns_figure = create_returns_figure(portfolio_values, spy_values, qqq_values) 
    returns_figure.show(renderer="svg")

if __name__ == "__main__":
	plot_returns_vs_spy()


# %%
