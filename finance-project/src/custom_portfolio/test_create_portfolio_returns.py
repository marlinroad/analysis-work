import pandas as pd
import pytest

from custom_portfolio.create_portfolio_returns import calculate_portfolio_daily_returns


def make_portfolio_values(closes):
    return pd.DataFrame({
        "timestamp": pd.date_range("2024-10-01", periods=len(closes), freq="D"),
        "close": closes,
    })


def make_config(rows):
    return pd.DataFrame(rows, columns=["symbol", "timestamp", "shares", "total_shares", "cashflow"])


def test_return_without_cashflow_is_percentage_change():
    values = make_portfolio_values([100, 110])
    config = make_config([])

    result = calculate_portfolio_daily_returns(values, config)

    assert pd.isna(result.loc[0, "dlyret"])
    assert result.loc[1, "cashflow"] == 0
    assert result.loc[1, "dlyret"] == pytest.approx(0.10)


def test_purchase_cashflow_is_removed_from_value_change():
    values = make_portfolio_values([10000, 11800])
    config = make_config([("GOOG", "2024-10-02", 20, 120, -1800)])

    result = calculate_portfolio_daily_returns(values, config)

    assert result.loc[1, "cashflow"] == -1800
    assert result.loc[1, "dlyret"] == pytest.approx(0.0)


def test_multiple_cashflows_on_same_date_are_summed():
    values = make_portfolio_values([100, 130])
    config = make_config([
        ("GOOG", "2024-10-02", 10, 110, -20),
        ("MSFT", "2024-10-02", 5, 5, 10),
    ])

    result = calculate_portfolio_daily_returns(values, config)

    assert result.loc[1, "cashflow"] == -10
    assert result.loc[1, "dlyret"] == pytest.approx(0.20)


def test_missing_cashflow_column_defaults_to_zero():
    values = make_portfolio_values([100, 110])
    config = pd.DataFrame({"symbol": ["GOOG"], "timestamp": ["2024-10-02"]})

    result = calculate_portfolio_daily_returns(values, config)

    assert result.loc[1, "cashflow"] == 0
    assert result.loc[1, "dlyret"] == pytest.approx(0.10)


def test_zero_previous_close_has_no_defined_return():
    values = make_portfolio_values([0, 100])
    config = make_config([])

    result = calculate_portfolio_daily_returns(values, config)

    assert pd.isna(result.loc[1, "dlyret"])


def test_original_columns_are_preserved_before_new_columns():
    values = make_portfolio_values([100, 110])
    values["source"] = "portfolio"
    config = make_config([])

    result = calculate_portfolio_daily_returns(values, config)

    assert list(result.columns) == ["timestamp", "close", "source", "cashflow", "dlyret"]
