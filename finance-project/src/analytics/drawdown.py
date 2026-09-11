#%%
import pandas as pd

def find_drawdown_episodes(dates, cumulative_returns, drawdown):
    """Walks the series once, grouping consecutive negative-drawdown days into episodes."""
    episodes = []
    current_episode = None
    peak_date = dates.iloc[0]

    for date, dd in zip(dates, drawdown):
        if dd < 0:
            if current_episode is None:
                current_episode = {
                    "peak_date": peak_date,
                    "trough_date": date,
                    "trough_drawdown": dd,
                }
            elif dd < current_episode["trough_drawdown"]:
                current_episode["trough_date"] = date
                current_episode["trough_drawdown"] = dd
        else:
            if current_episode is not None:
                episodes.append(current_episode)
                current_episode = None
            peak_date = date

    if current_episode is not None:
        episodes.append(current_episode)

    return episodes

def compute_drawdowns(dates, returns, top_n=5):
    cumulative_returns = (1 + returns).cumprod()
    running_max = cumulative_returns.cummax()
    drawdown = cumulative_returns / running_max - 1

    episodes = find_drawdown_episodes(dates, cumulative_returns, drawdown)
    worst_episodes = sorted(episodes, key=lambda episode: episode["trough_drawdown"])[:top_n]

    return pd.DataFrame(
        [
            {
                "rank": rank,
                "drawdown": episode["trough_drawdown"],
                "start_date": episode["peak_date"],
                "end_date": episode["trough_date"],
                "num_days": (episode["trough_date"] - episode["peak_date"]).days,
            }
            for rank, episode in enumerate(worst_episodes, start=1)
        ]
    )

def compute_drawdown_metrics(df_merged):
    market_returns = df_merged["Mkt-RF"] + df_merged["RF"]

    portfolio_drawdowns = compute_drawdowns(df_merged["date"], df_merged["dlyret"])
    portfolio_drawdowns.insert(0, "returns_type", "Portfolio")

    market_drawdowns = compute_drawdowns(df_merged["date"], market_returns)
    market_drawdowns.insert(0, "returns_type", "Market")

    return pd.concat([portfolio_drawdowns, market_drawdowns], ignore_index=True)

