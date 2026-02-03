import pandas as pd

def load_market_data(csv_path):
    """
    Loads market candle data from CSV.
    """
    df = pd.read_csv(csv_path)

    # Basic validation
    required_columns = {"open", "high", "low", "close", "volume"}
    if not required_columns.issubset(df.columns):
        raise ValueError("CSV missing required candle columns")

    return df
