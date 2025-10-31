import os
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

# expects data/Car_Value_Dataset.csv
_DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "Car_Value_Dataset.csv")
if not os.path.exists(_DATA_PATH):
    raise FileNotFoundError(f"Training data not found at {_DATA_PATH}")

df = pd.read_csv(_DATA_PATH)
df.columns = [c.strip().lower() for c in df.columns]

year_col = next((c for c in df.columns if c in ("year", "yr")), None)
mileage_col = next((c for c in df.columns if c in ("mileage", "miles", "odometer")), None)
price_col = next((c for c in df.columns if c in ("price", "value", "target")), None)
if not (year_col and mileage_col and price_col):
    raise ValueError("Expected columns like year/yr, mileage/miles, and price/value in car-values.xlsx")

df = df[[year_col, mileage_col, price_col]].dropna()

X = df[[year_col, mileage_col]].astype(float).values
y = df[price_col].astype(float).values

_model = Pipeline([
    ("scale", StandardScaler()),
    ("linreg", LinearRegression())
])
_model.fit(X, y)

def trade(year: int, mileage: float) -> float:
    """Return estimated trade-in value."""
    x = np.array([[float(year), float(mileage)]])
    pred = float(_model.predict(x)[0])
    return max(0.0, round(pred, 2))