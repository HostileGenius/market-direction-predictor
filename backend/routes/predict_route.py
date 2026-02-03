from flask import Blueprint, jsonify
from utils.data_loader import load_market_data
from indicators.technicals import add_all_indicators
from model.features import build_features
from model.predict import load_model, predict_probability, interpret_prediction
from utils.market_api import fetch_candles

import os

predict_bp = Blueprint("predict", __name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "sample_market.csv")

model = load_model()

def generate_user_message(bias, confidence):
    if bias == "NO TRADE":
        return "Market is unclear right now. Best to wait and avoid trading."

    if confidence == "LOW":
        return (
            "Market shows a weak signal. "
            "Trading now can be risky. Consider waiting."
        )

    if bias == "UP":
        return (
            "Market shows upward movement. "
            "Prices may rise. Trade only if you understand the risk."
        )

    if bias == "DOWN":
        return (
            "Market shows downward movement. "
            "Prices may fall. Trade only if you understand the risk."
        )

    return "No clear guidance available."







@predict_bp.route("/predict")
def predict():
    df = fetch_candles(symbol="BTCUSDT", interval="1m", limit=100)

    df = add_all_indicators(df)
    X = build_features(df)

    latest_features = X.iloc[-1].tolist()
    prob = predict_probability(model, latest_features)
    interpretation = interpret_prediction(prob)

    latest_candle_time = str(df.iloc[-1]["time"])

    user_message = generate_user_message(
    interpretation["bias"],
    interpretation["confidence"]
)

    return jsonify({
    "probability": prob,
    **interpretation,
    "user_message": user_message,
    "meta": {
        "last_candle_time": latest_candle_time
    }
})
