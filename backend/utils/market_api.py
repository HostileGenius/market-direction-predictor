import requests
import pandas as pd

BINANCE_URL = "https://api.binance.com/api/v3/klines"

def fetch_candles(
    
    symbol="BTCUSDT",
    interval="1m",
    limit=100
):
    print("📡 Fetching fresh market data from Binance")

    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    

    response = requests.get(BINANCE_URL, params=params)
    data = response.json()

    df = pd.DataFrame(data, columns=[
        "time",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_"
    ])

    df = df[["time", "open", "high", "low", "close", "volume"]]
    


    df["open"] = df["open"].astype(float)
    df["high"] = df["high"].astype(float)
    df["low"] = df["low"].astype(float)
    df["close"] = df["close"].astype(float)
    df["volume"] = df["volume"].astype(float)

    return df
