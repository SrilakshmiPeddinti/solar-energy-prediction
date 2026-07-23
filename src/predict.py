"""
predict.py — Prediction module for the Solar Energy Output Predictor.

Usage:
    from src.predict import SolarPredictor
    predictor = SolarPredictor()
    result = predictor.predict({
        "temperature_c": 28.5,
        "humidity_pct": 45.0,
        "cloud_cover_pct": 10.0,
        "solar_irradiance_wm2": 850.0,
        "wind_speed_ms": 3.5,
        "rainfall_mm": 0.0,
        "hour": 13,
        "month": 6,
    })
    print(result)
"""

import os
import sys

# Allow imports from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
import pandas as pd
import joblib

from src.utils import get_logger, validate_input

logger = get_logger("predict")

MODEL_PATH = "models/solar_model.pkl"


class SolarPredictor:
    """
    Wraps the trained solar energy prediction model.
    Handles feature engineering and validation automatically.
    """

    def __init__(self, model_path: str = MODEL_PATH):
        self.model_path   = model_path
        self.model        = None
        self.feature_cols = None
        self.model_name   = None
        self._load_model()

    def _load_model(self) -> None:
        """Load the saved model from disk."""
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"No model found at '{self.model_path}'. "
                "Run 'python src/train.py' first."
            )
        data = joblib.load(self.model_path)
        self.model        = data["model"]
        self.feature_cols = data["feature_cols"]
        self.model_name   = data.get("model_name", "Unknown")
        self.trained_at   = data.get("trained_at", "Unknown")
        logger.info(f"Loaded model: {self.model_name} (trained {self.trained_at})")

    def _build_feature_vector(self, raw_input: dict) -> np.ndarray:
        """
        Given a raw input dict, compute all required features
        (including engineered ones) and return an array matching
        the model's expected feature_cols.
        """
        # Derived features
        hour  = raw_input.get("hour", 12)
        month = raw_input.get("month", 6)
        temp  = raw_input.get("temperature_c", 25)
        irr   = raw_input.get("solar_irradiance_wm2", 500)
        cloud = raw_input.get("cloud_cover_pct", 20)
        hum   = raw_input.get("humidity_pct", 50)
        dow   = raw_input.get("day_of_week", 1)

        extended = {
            **raw_input,
            "day_of_week":        dow,
            "is_weekend":         int(dow >= 5),
            "hour_sin":           np.sin(2 * np.pi * hour  / 24),
            "hour_cos":           np.cos(2 * np.pi * hour  / 24),
            "month_sin":          np.sin(2 * np.pi * month / 12),
            "month_cos":          np.cos(2 * np.pi * month / 12),
            "temp_irradiance":    temp * irr,
            "cloud_humidity":     cloud * hum,
            "clear_sky_index":    1 - (cloud / 100),
        }

        # Build vector in the order the model was trained on
        vector = np.array([extended.get(col, 0.0) for col in self.feature_cols]).reshape(1, -1)
        return vector

    def predict(self, input_data: dict) -> dict:
        """
        Make a single prediction.

        Parameters
        ----------
        input_data : dict
            Keys: temperature_c, humidity_pct, cloud_cover_pct,
                  solar_irradiance_wm2, wind_speed_ms, rainfall_mm,
                  hour, month

        Returns
        -------
        dict with keys:
            - predicted_kwh : float
            - model_name    : str
            - confidence    : str (qualitative)
        """
        validated = validate_input(input_data)
        X = self._build_feature_vector(validated)
        predicted = float(self.model.predict(X)[0])
        predicted = max(0.0, predicted)

        # Simple qualitative confidence based on irradiance
        irr = validated.get("solar_irradiance_wm2", 0)
        cloud = validated.get("cloud_cover_pct", 100)
        if irr > 600 and cloud < 30:
            confidence = "High"
        elif irr > 300 and cloud < 60:
            confidence = "Medium"
        else:
            confidence = "Low"

        result = {
            "predicted_kwh": round(predicted, 4),
            "model_name":    self.model_name,
            "confidence":    confidence,
        }
        logger.info(f"Prediction: {result}")
        return result

    def predict_batch(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Make predictions for a DataFrame of weather conditions.

        Parameters
        ----------
        df : pd.DataFrame — must contain all required feature columns.

        Returns
        -------
        df with a new column 'predicted_kwh'.
        """
        df = df.copy()

        # Parse timestamp if it exists to extract date/time features
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            if "hour" not in df.columns:
                df["hour"] = df["timestamp"].dt.hour
            if "month" not in df.columns:
                df["month"] = df["timestamp"].dt.month
            if "day_of_week" not in df.columns:
                df["day_of_week"] = df["timestamp"].dt.dayofweek
            if "is_weekend" not in df.columns:
                df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)

        # Add engineered features if missing
        if "hour_sin" not in df.columns:
            hour  = df.get("hour",  12)
            month = df.get("month", 6)
            temp  = df.get("temperature_c", 25)
            irr   = df.get("solar_irradiance_wm2", 500)
            cloud = df.get("cloud_cover_pct", 20)
            hum   = df.get("humidity_pct", 50)

            df["hour_sin"]       = np.sin(2 * np.pi * hour  / 24)
            df["hour_cos"]       = np.cos(2 * np.pi * hour  / 24)
            df["month_sin"]      = np.sin(2 * np.pi * month / 12)
            df["month_cos"]      = np.cos(2 * np.pi * month / 12)
            df["temp_irradiance"]= temp * irr
            df["cloud_humidity"] = cloud * hum
            df["clear_sky_index"]= 1 - (cloud / 100)
            if "is_weekend" not in df.columns:
                df["is_weekend"] = (df.get("day_of_week", pd.Series([0]*len(df))) >= 5).astype(int)

        # Verify all feature columns are present or add them as 0.0
        for col in self.feature_cols:
            if col not in df.columns:
                logger.warning(f"Missing required feature column '{col}' — filling with 0.0")
                df[col] = 0.0

        X = df[self.feature_cols].values
        df["predicted_kwh"] = np.maximum(0, self.model.predict(X))
        logger.info(f"Batch prediction complete: {len(df):,} rows.")
        return df

    def info(self) -> dict:
        """Return model metadata."""
        return {
            "model_name":   self.model_name,
            "trained_at":   self.trained_at,
            "feature_cols": self.feature_cols,
            "model_path":   self.model_path,
        }


# ─────────────────────────────────────────────
# QUICK TEST
# ─────────────────────────────────────────────

if __name__ == "__main__":
    predictor = SolarPredictor()

    # Example: sunny summer noon
    result = predictor.predict({
        "temperature_c":        32.0,
        "humidity_pct":         35.0,
        "cloud_cover_pct":      5.0,
        "solar_irradiance_wm2": 950.0,
        "wind_speed_ms":        2.5,
        "rainfall_mm":          0.0,
        "hour":                 12,
        "month":                7,
    })
    print(f"\nSunny summer noon prediction:")
    print(f"  Predicted energy : {result['predicted_kwh']} kWh")
    print(f"  Confidence       : {result['confidence']}")
    print(f"  Model            : {result['model_name']}\n")

    # Example: cloudy winter morning
    result2 = predictor.predict({
        "temperature_c":        8.0,
        "humidity_pct":         80.0,
        "cloud_cover_pct":      85.0,
        "solar_irradiance_wm2": 120.0,
        "wind_speed_ms":        7.0,
        "rainfall_mm":          2.5,
        "hour":                 9,
        "month":                12,
    })
    print(f"Cloudy winter morning prediction:")
    print(f"  Predicted energy : {result2['predicted_kwh']} kWh")
    print(f"  Confidence       : {result2['confidence']}")
    print(f"  Model            : {result2['model_name']}\n")
