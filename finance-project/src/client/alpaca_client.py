#%%
import json
from datetime import datetime
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.enums import Adjustment

from common.constants import get_path

def get_alpaca_config():
    with open(get_path("alpaca_config.json")) as f:
        return json.load(f)

def get_daily_stock_prices(tickers, adjustment="ALL"):
    adj = None
    if adjustment=="ALL":
        adj=Adjustment.ALL
    else:
        adj=Adjustment.SPLIT
    
    config = get_alpaca_config()
    client = StockHistoricalDataClient(
        config["api_key"],
        config["api_secret"]
    )

    request = StockBarsRequest(
        symbol_or_symbols=tickers,
        timeframe=TimeFrame.Day,
        start=datetime(2020, 1, 1),
        end=datetime(2026, 8, 25),
        adjustment=Adjustment.ALL
    )

    bars = client.get_stock_bars(request)

    df = bars.df
    return df.reset_index()