import pandas as pd
import joblib
from backend.utils.market_api import fetch_candles
from backend.indicators.technicals import add_all_indicators
from backend.model.features import build_features, create_target

def backtest_model():
    print("📊 Running backtest...")

    # Load trained model
    model = joblib.load("backend/model/model.pkl")

    # Fetch historical data
    df = fetch_candles(symbol="BTCUSDT", interval="1m", limit=500)

    # Indicators + features
    df = add_all_indicators(df)
    X = build_features(df)
    y = create_target(df)

    # Remove last row (no future)
    X = X.iloc[:-1]
    y = y.iloc[:-1]

    # Predictions
    preds = model.predict(X)
    probs = model.predict_proba(X)

    results = pd.DataFrame({
        "actual": y.values,
        "predicted": preds,
        "confidence": probs.max(axis=1)
    })

    # Accuracy
    accuracy = (results["actual"] == results["predicted"]).mean()

    print(f"✅ Accuracy: {accuracy * 100:.2f}%")

    # Confidence-based analysis
    high_conf = results[results["confidence"] > 0.7]

    high_conf_acc = (
        high_conf["actual"] == high_conf["predicted"]
    ).mean()

    print(f"🔥 High-confidence accuracy (>60%): {high_conf_acc * 100:.2f}%")
    print(f"Trades taken: {len(high_conf)} / {len(results)}")
    print(results["confidence"].describe())


if __name__ == "__main__":
    backtest_model()
