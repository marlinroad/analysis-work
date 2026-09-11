import pandas as pd
import pytest

from analytics.drawdown import compute_drawdowns


def make_returns(values):
    dates = pd.date_range("2024-01-01", periods=len(values), freq="D")
    return dates.to_series(index=range(len(values))), pd.Series(values)


def test_single_drawdown_episode_is_detected():
    dates, returns = make_returns([0.01, -0.02, -0.03, 0.05])

    result = compute_drawdowns(dates, returns)

    assert len(result) == 1
    assert result.loc[0, "rank"] == 1
    assert result.loc[0, "drawdown"] == pytest.approx(-0.0494, abs=1e-4)
    assert result.loc[0, "start_date"] == dates.iloc[0]
    assert result.loc[0, "end_date"] == dates.iloc[2]
    assert result.loc[0, "num_days"] == 2


def test_separate_episodes_are_ranked_worst_first():
    dates, returns = make_returns([0.01, -0.10, 0.20, -0.02, 0.05])

    result = compute_drawdowns(dates, returns)

    assert len(result) == 2
    assert result.loc[0, "rank"] == 1
    assert result.loc[0, "drawdown"] < result.loc[1, "drawdown"]


def test_top_n_limits_number_of_episodes_returned():
    dates, returns = make_returns([-0.01, 0.02, -0.02, 0.03, -0.03, 0.04, -0.04, 0.05])

    result = compute_drawdowns(dates, returns, top_n=2)

    assert len(result) == 2


def test_no_drawdown_returns_empty_result():
    dates, returns = make_returns([0.01, 0.02, 0.03])

    result = compute_drawdowns(dates, returns)

    assert result.empty
