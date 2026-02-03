import pandas as pd
import ta

def add_rsi(df, period=14):
    df["rsi"] = ta.momentum.RSIIndicator(
        close=df["close"],
        window=period
    ).rsi()
    return df

def add_ema(df, short=9, long=21):
    df["ema_short"] = ta.trend.EMAIndicator(
        close=df["close"],
        window=short
    ).ema_indicator()

    df["ema_long"] = ta.trend.EMAIndicator(
        close=df["close"],
        window=long
    ).ema_indicator()

    return df

def add_macd(df):
    macd = ta.trend.MACD(close=df["close"])

    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()
    df["macd_hist"] = macd.macd_diff()

    return df

def add_bollinger_bands(df):
    bb = ta.volatility.BollingerBands(close=df["close"])

    df["bb_upper"] = bb.bollinger_hband()
    df["bb_middle"] = bb.bollinger_mavg()
    df["bb_lower"] = bb.bollinger_lband()

    return df

def add_all_indicators(df):
    df = add_rsi(df)
    df = add_ema(df)
    df = add_macd(df)
    df = add_bollinger_bands(df)

    return df
