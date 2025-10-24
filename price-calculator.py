import os
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# Path to your Excel file (can also set via .env if you prefer)
_DATA_PATH = os.getenv(
    "DATA_PATH",
    "data/car-values.xlsx"  # relative path inside backend container
)

_MODEL = None


def _train_model():
    # Load your real Excel dataset
    df = pd.read_excel(_DATA_PATH, engine="openpyxl")

    # Make sure expected columns exist
    if not {"year", "mileage", "value_usd"} <= set(df.columns):
        raise ValueError(
            f"Dataset must have columns year, mileage, value_usd — found {df.columns}"
        )

    X = df[["year", "mileage"]].to_numpy(dtype=float)
    y = df["value_usd"].to_numpy(dtype=float)
    model = LinearRegression().fit(X, y)
    return model


def get_model():
    global _MODEL
    if _MODEL is None:
        _MODEL = _train_model()
    return _MODEL


def trade(year: int, mileage: int) -> float:
    model = get_model()
    X_new = np.array([[float(year), float(mileage)]], dtype=float)
    return float(model.predict(X_new)[0])