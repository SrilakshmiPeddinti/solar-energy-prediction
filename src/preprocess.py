"""
preprocess.py — Data generation, cleaning, and feature engineering
for the Solar Energy Output Predictor.

Run:
    python src/preprocess.py
"""

import os
import sys
import numpy as np
import pandas as pd

# Allow imports from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils import get_logger, save_data, describe_data

logger = get_logger("preprocess")


# ─────────────────────────────────────────────
# SYNTHETIC DATA GENERATOR
# (Replace with real NASA POWER / Kaggle data)
# ─────────────────────────────────────────────

def generate_synthetic_data(n_days: int = 730, seed: int = 42) -> pd.DataFrame:
    """
    Generates realistic synthetic solar energy data for 2 years
    at hourly resolution (daylight hours only).

    In production: replace this with NASA POWER API or Kaggle dataset.
    """
    np.random.seed(seed)
    logger.info(f"Generating synthetic data for {n_days} days …")

    records = []
    start_date = pd.Timestamp("2022-01-01")

    for day_offset in range(n_days):
        date = start_date + pd.Timedelta(days=day_offset)
        month = date.month
        day_of_week = date.dayofweek
        is_weekend = int(day_of_week >= 5)

        # Monthly solar potential (higher in summer)
        solar_potential = 0.4 + 0.6 * np.sin(np.pi * (month - 1) / 11)

        # Daily weather baseline
        base_temp       = 15 + 20 * solar_potential + np.random.normal(0, 3)
        base_humidity   = 80 - 30 * solar_potential + np.random.normal(0, 8)
        base_cloud      = max(0, 60 - 50 * solar_potential + np.random.normal(0, 15))
        daily_rainfall  = max(0, np.random.exponential(2) if base_cloud > 50 else 0)

        # Hourly data (6am–7pm = 14 hours of daylight)
        for hour in range(6, 20):
            # Solar irradiance bell curve peaking at noon
            hour_factor = max(0, np.sin(np.pi * (hour - 6) / 13))

            irradiance = (
                1000 * solar_potential * hour_factor
                * (1 - base_cloud / 150)
                + np.random.normal(0, 20)
            )
            irradiance = max(0, irradiance)

            temperature = base_temp + 5 * hour_factor + np.random.normal(0, 1.5)
            humidity    = max(0, base_humidity - 10 * hour_factor + np.random.normal(0, 3))
            cloud_cover = max(0, min(100, base_cloud + np.random.normal(0, 5)))
            wind_speed  = max(0, np.random.gamma(2, 2))
            rainfall    = daily_rainfall / 14 if hour in range(6, 20) else 0

            # Energy output formula (physics-inspired)
            panel_efficiency = 0.18
            panel_area_m2    = 20
            efficiency_loss  = 1 - 0.004 * max(0, temperature - 25)  # temp coefficient
            cloud_factor     = 1 - 0.8 * (cloud_cover / 100)

            energy_kwh = (
                irradiance
                * panel_efficiency
                * panel_area_m2
                * efficiency_loss
                * cloud_factor
                / 1000
            )
            energy_kwh = max(0, energy_kwh + np.random.normal(0, 0.05))

            records.append({
                "timestamp":            date + pd.Timedelta(hours=hour),
                "temperature_c":        round(temperature, 2),
                "humidity_pct":         round(max(0, min(100, humidity)), 2),
                "cloud_cover_pct":      round(cloud_cover, 2),
                "solar_irradiance_wm2": round(irradiance, 2),
                "wind_speed_ms":        round(wind_speed, 2),
                "rainfall_mm":          round(rainfall, 2),
                "energy_output_kwh":    round(energy_kwh, 4),
            })

    df = pd.DataFrame(records)
    logger.info(f"Generated {len(df):,} records.")
    return df


# ─────────────────────────────────────────────
# PREPROCESSING PIPELINE
# ─────────────────────────────────────────────

def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Fill or drop missing values."""
    initial_nulls = df.isnull().sum().sum()
    if initial_nulls > 0:
        logger.warning(f"Found {initial_nulls} missing values — applying forward fill …")
        df = df.ffill().bfill()
    else:
        logger.info("No missing values found.")
    return df


def remove_outliers(df: pd.DataFrame, cols: list, z_thresh: float = 3.5) -> pd.DataFrame:
    """Remove rows where any numeric feature is beyond z_thresh standard deviations."""
    from scipy import stats
    before = len(df)
    z_scores = np.abs(stats.zscore(df[cols].select_dtypes(include=[np.number])))
    mask = (z_scores < z_thresh).all(axis=1)
    df = df[mask].reset_index(drop=True)
    removed = before - len(df)
    if removed:
        logger.info(f"Removed {removed:,} outlier rows.")
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Extract and create additional features from the timestamp."""
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["hour"]        = df["timestamp"].dt.hour
    df["month"]       = df["timestamp"].dt.month
    df["day_of_week"] = df["timestamp"].dt.dayofweek
    df["is_weekend"]  = (df["day_of_week"] >= 5).astype(int)
    df["day_of_year"] = df["timestamp"].dt.dayofyear
    df["week_of_year"]= df["timestamp"].dt.isocalendar().week.astype(int)

    # Cyclical encoding for hour and month (better for ML)
    df["hour_sin"]  = np.sin(2 * np.pi * df["hour"]  / 24)
    df["hour_cos"]  = np.cos(2 * np.pi * df["hour"]  / 24)
    df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
    df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)

    # Interaction features
    df["temp_irradiance"]   = df["temperature_c"] * df["solar_irradiance_wm2"]
    df["cloud_humidity"]    = df["cloud_cover_pct"] * df["humidity_pct"]
    df["clear_sky_index"]   = 1 - (df["cloud_cover_pct"] / 100)

    logger.info(f"Feature engineering complete. Columns: {list(df.columns)}")
    return df


def scale_features(df: pd.DataFrame, numeric_cols: list) -> pd.DataFrame:
    """Add min-max scaled versions of numeric columns (for EDA/viz)."""
    for col in numeric_cols:
        col_min = df[col].min()
        col_max = df[col].max()
        if col_max > col_min:
            df[f"{col}_scaled"] = (df[col] - col_min) / (col_max - col_min)
    return df


def run_preprocessing_pipeline(
    raw_path: str = None,
    output_path: str = "data/processed/solar_data_processed.csv",
) -> pd.DataFrame:
    """
    Full preprocessing pipeline:
    1. Load (or generate) raw data
    2. Handle missing values
    3. Remove outliers
    4. Engineer features
    5. Save processed data
    """
    logger.info("Starting preprocessing pipeline …")

    # Step 1: Load or generate data
    if raw_path and os.path.exists(raw_path):
        df = pd.read_csv(raw_path)
        logger.info(f"Loaded raw data from: {raw_path}")
    else:
        logger.info("No raw data found — generating synthetic dataset …")
        df = generate_synthetic_data(n_days=730)
        raw_out = "data/raw/solar_data_raw.csv"
        os.makedirs("data/raw", exist_ok=True)
        df.to_csv(raw_out, index=False)
        logger.info(f"Raw data saved to: {raw_out}")

    # Step 2: Missing values
    df = handle_missing_values(df)

    # Step 3: Outlier removal
    numeric_cols = [
        "temperature_c", "humidity_pct", "cloud_cover_pct",
        "solar_irradiance_wm2", "wind_speed_ms", "rainfall_mm",
        "energy_output_kwh",
    ]
    df = remove_outliers(df, numeric_cols)

    # Step 4: Feature engineering
    df = engineer_features(df)

    # Step 5: Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    save_data(df, output_path)

    logger.info("Preprocessing pipeline complete.")
    describe_data(df)
    return df


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Preprocess solar data.")
    parser.add_argument("--raw", type=str, default=None, help="Path to raw weather data CSV")
    parser.add_argument("--output", type=str, default="data/processed/solar_data_processed.csv", help="Path to save processed CSV")
    args = parser.parse_args()
    
    # Auto-detect Pune weather data if no raw path is specified
    raw_path = args.raw
    if not raw_path:
        default_pune = "data/raw/pune_weather_data.csv"
        default_raw = "data/raw/solar_data_raw.csv"
        if os.path.exists(default_pune):
            raw_path = default_pune
        elif os.path.exists(default_raw):
            raw_path = default_raw
            
    run_preprocessing_pipeline(raw_path=raw_path, output_path=args.output)
