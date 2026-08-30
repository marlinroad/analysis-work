import pandas as pd
import pytest

from custom_portfolio.create_portfolio_values import calculate_portfolio_daily_values


@pytest.fixture
def df_stocks():
    # AAA is missing a close price on day 4 to exercise the forward-fill path
    return pd.DataFrame([
        ("AAA", "2023-01-01 05:00:00+00:00", 10),
        ("AAA", "2023-01-02 05:00:00+00:00", 11),
        ("AAA", "2023-01-03 05:00:00+00:00", 12),
        ("AAA", "2023-01-05 05:00:00+00:00", 14),
        ("AAA", "2023-01-06 05:00:00+00:00", 15),
        ("BBB", "2023-01-01 05:00:00+00:00", 100),
        ("BBB", "2023-01-02 05:00:00+00:00", 101),
        ("BBB", "2023-01-03 05:00:00+00:00", 102),
        ("BBB", "2023-01-04 05:00:00+00:00", 103),
        ("BBB", "2023-01-05 05:00:00+00:00", 104),
        ("BBB", "2023-01-06 05:00:00+00:00", 105),
    ], columns=["symbol", "timestamp", "close"])


@pytest.fixture
def df_config():
    return pd.DataFrame([
        ("AAA", "2023-1-1", 10, 10),
        ("AAA", "2023-1-4", 20, 30),
        ("BBB", "2023-1-2", 5, 5),
    ], columns=["symbol", "timestamp", "shares", "total_shares"])


def test_output_starts_at_first_transaction_date(df_stocks, df_config):
    df_portfolio_values = calculate_portfolio_daily_values(df_stocks, df_config)
    assert df_portfolio_values["timestamp"].min() == pd.Timestamp("2023-01-01")


def test_value_before_topup(df_stocks, df_config):
    df_portfolio_values = calculate_portfolio_daily_values(df_stocks, df_config)
    row = df_portfolio_values.loc[df_portfolio_values["timestamp"] == pd.Timestamp("2023-01-03")]
    # AAA: 10 shares * 12 close = 120, BBB: 5 shares * 102 close = 510
    assert row["close"].iloc[0] == pytest.approx(630)


def test_value_after_topup_with_forward_filled_price(df_stocks, df_config):
    df_portfolio_values = calculate_portfolio_daily_values(df_stocks, df_config)
    row = df_portfolio_values.loc[df_portfolio_values["timestamp"] == pd.Timestamp("2023-01-04")]
    # AAA: 30 shares * forward-filled close (12, carried from day 3) = 360, BBB: 5 shares * 103 close = 515
    assert row["close"].iloc[0] == pytest.approx(875)


def test_value_on_last_day(df_stocks, df_config):
    df_portfolio_values = calculate_portfolio_daily_values(df_stocks, df_config)
    row = df_portfolio_values.loc[df_portfolio_values["timestamp"] == pd.Timestamp("2023-01-06")]
    # AAA: 30 shares * 15 close = 450, BBB: 5 shares * 105 close = 525
    assert row["close"].iloc[0] == pytest.approx(975)
