import pandas as pd

def build_features(df):
    features = pd.DataFrame()

    features["rsi_signal"] = (df["rsi"] > 50).astype(int)
    features["ema_crossover"] = (df["ema_short"] > df["ema_long"]).astype(int)
    features["macd_signal"] = (df["macd_hist"] > 0).astype(int)
    features["price_above_bb_mid"] = (df["close"] > df["bb_middle"]).astype(int)

    features["volume_spike"] = (
        df["volume"] > df["volume"].rolling(5).mean()
    ).astype(int)

    features["close"] = df["close"]

    return features.fillna(0)

def create_target(df):
    return (df["close"].shift(-1) > df["close"]).astype(int)
