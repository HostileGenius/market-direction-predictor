import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "model.pkl")

def load_model():
    return joblib.load(MODEL_PATH)

def predict_probability(model, features_row):
    prob = model.predict_proba([features_row])[0]
    return {
        "down": round(float(prob[0]), 3),
        "up": round(float(prob[1]), 3)
    }

def interpret_prediction(prob):
    up = prob["up"]

    if up >= 0.65:
        return {
            "bias": "UP",
            "confidence": "HIGH",
            "recommendation": "TRADE"
        }
    elif up >= 0.55:
        return {
            "bias": "UP",
            "confidence": "MEDIUM",
            "recommendation": "TRADE WITH CAUTION"
        }
    elif up <= 0.35:
        return {
            "bias": "DOWN",
            "confidence": "HIGH",
            "recommendation": "TRADE"
        }
    elif up <= 0.45:
        return {
            "bias": "DOWN",
            "confidence": "MEDIUM",
            "recommendation": "TRADE WITH CAUTION"
        }
    else:
        return {
            "bias": "NO TRADE",
            "confidence": "LOW",
            "recommendation": "AVOID"
        }
