"""
utils.py — Utility functions for the Solar Energy Output Predictor
"""

import os
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# ─────────────────────────────────────────────
# LOGGING SETUP
# ─────────────────────────────────────────────

def get_logger(name: str = "solar_predictor") -> logging.Logger:
    """Returns a configured logger."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return logging.getLogger(name)


logger = get_logger()


# ─────────────────────────────────────────────
# DATA UTILITIES
# ─────────────────────────────────────────────

def load_data(filepath: str) -> pd.DataFrame:
    """Load a CSV file into a DataFrame."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    df = pd.read_csv(filepath)
    logger.info(f"Loaded data: {filepath} — shape {df.shape}")
    return df


def save_data(df: pd.DataFrame, filepath: str) -> None:
    """Save a DataFrame to CSV."""
    dir_name = os.path.dirname(filepath)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    df.to_csv(filepath, index=False)
    logger.info(f"Saved data: {filepath} — shape {df.shape}")


def describe_data(df: pd.DataFrame) -> None:
    """Print a detailed data description."""
    print("\n" + "="*60)
    print("DATASET OVERVIEW")
    print("="*60)
    print(f"Shape:         {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"Memory usage:  {df.memory_usage(deep=True).sum() / 1024:.1f} KB")
    print(f"\nColumn Types:\n{df.dtypes}")
    print(f"\nMissing Values:\n{df.isnull().sum()}")
    print(f"\nStatistical Summary:\n{df.describe().round(2)}")
    print("="*60 + "\n")


# ─────────────────────────────────────────────
# FEATURE UTILITIES
# ─────────────────────────────────────────────

FEATURE_COLS = [
    "temperature_c",
    "humidity_pct",
    "cloud_cover_pct",
    "solar_irradiance_wm2",
    "wind_speed_ms",
    "rainfall_mm",
    "hour",
    "month",
    "day_of_week",
    "is_weekend",
]

TARGET_COL = "energy_output_kwh"


def get_feature_columns() -> list:
    return FEATURE_COLS


def get_target_column() -> str:
    return TARGET_COL


# ─────────────────────────────────────────────
# EVALUATION UTILITIES
# ─────────────────────────────────────────────

def print_metrics(model_name: str, mae: float, rmse: float, r2: float) -> None:
    """Print model evaluation metrics in a formatted table."""
    print(f"\n{'─'*40}")
    print(f"  Model: {model_name}")
    print(f"{'─'*40}")
    print(f"  MAE  : {mae:.4f}")
    print(f"  RMSE : {rmse:.4f}")
    print(f"  R²   : {r2:.4f}")
    print(f"{'─'*40}\n")


# ─────────────────────────────────────────────
# PLOT UTILITIES
# ─────────────────────────────────────────────

PLOT_STYLE = {
    "figure.facecolor": "#0f1117",
    "axes.facecolor": "#1a1d27",
    "axes.edgecolor": "#3a3d4a",
    "axes.labelcolor": "#e0e0e0",
    "xtick.color": "#b0b0b0",
    "ytick.color": "#b0b0b0",
    "text.color": "#e0e0e0",
    "grid.color": "#2a2d3a",
    "grid.linestyle": "--",
    "grid.alpha": 0.5,
}

SOLAR_PALETTE = ["#FFD700", "#FFA500", "#FF6B35", "#E63946", "#06D6A0", "#118AB2"]


def set_plot_style() -> None:
    """Apply the solar dark theme to all matplotlib plots."""
    plt.rcParams.update(PLOT_STYLE)
    sns.set_palette(SOLAR_PALETTE)


def save_plot(fig: plt.Figure, filename: str, output_dir: str = "data/processed/plots") -> None:
    """Save a matplotlib figure to disk."""
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, filename)
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    logger.info(f"Plot saved: {path}")
    plt.close(fig)


# ─────────────────────────────────────────────
# TIME UTILITIES
# ─────────────────────────────────────────────

def timestamp_now() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def season_from_month(month: int) -> str:
    """Return season name from month number (Northern Hemisphere)."""
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Autumn"


# ─────────────────────────────────────────────
# VALIDATION UTILITIES
# ─────────────────────────────────────────────

def validate_input(data: dict) -> dict:
    """
    Validate and clamp user input values to realistic ranges.
    Returns a dict with valid values.
    """
    ranges = {
        "temperature_c":       (-10, 55),
        "humidity_pct":        (0,   100),
        "cloud_cover_pct":     (0,   100),
        "solar_irradiance_wm2":(0,   1200),
        "wind_speed_ms":       (0,   40),
        "rainfall_mm":         (0,   300),
        "hour":                (0,   23),
        "month":               (1,   12),
    }

    validated = {}
    for key, value in data.items():
        if key in ranges:
            lo, hi = ranges[key]
            clamped = max(lo, min(hi, value))
            if clamped != value:
                logger.warning(f"Input '{key}' clamped from {value} to {clamped}")
            validated[key] = clamped
        else:
            validated[key] = value

    return validated
