import joblib
import os
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from backend.utils.data_loader import load_market_data
from backend.indicators.technicals import add_all_indicators
from backend.model.features import build_features, create_target



def train_model():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "sample_market.csv")

    df = load_market_data(DATA_PATH)

    df = add_all_indicators(df)

    X = build_features(df)
    y = create_target(df)

    # Remove last row (no future target)
    X = X.iloc[:-1]
    y = y.iloc[:-1]

    from sklearn.calibration import CalibratedClassifierCV

    base_model = LogisticRegression(max_iter=1000)
    model = CalibratedClassifierCV(base_model, method="sigmoid")
    model.fit(X, y)


    MODEL_PATH = os.path.join(BASE_DIR, "model", "model.pkl")
    joblib.dump(model, MODEL_PATH)


    print("✅ Model trained and saved")

if __name__ == "__main__":
    train_model()
