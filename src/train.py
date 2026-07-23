"""
train.py — Model training, evaluation, and selection pipeline
for the Solar Energy Output Predictor.

Run:
    python src/train.py
"""

import os
import sys

# Allow imports from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

try:
    from xgboost import XGBRegressor
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False

from src.utils import (
    get_logger, load_data, set_plot_style, save_plot,
    print_metrics, FEATURE_COLS, TARGET_COL, timestamp_now
)

logger = get_logger("train")


# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────

DATA_PATH   = "data/processed/solar_data_processed.csv"
MODEL_PATH  = "models/solar_model.pkl"
METRICS_PATH= "models/metrics.json"
TEST_SIZE   = 0.2
RANDOM_STATE= 42


# ─────────────────────────────────────────────
# MODEL DEFINITIONS
# ─────────────────────────────────────────────

def get_models() -> dict:
    """Returns a dict of model name → sklearn estimator."""
    models = {
        "Linear Regression": LinearRegression(),
        "Ridge Regression": Ridge(alpha=1.0),
        "Random Forest": RandomForestRegressor(
            n_estimators=200,
            max_depth=12,
            min_samples_split=5,
            random_state=RANDOM_STATE,
            n_jobs=-1,
        ),
        "Gradient Boosting": GradientBoostingRegressor(
            n_estimators=200,
            learning_rate=0.05,
            max_depth=5,
            random_state=RANDOM_STATE,
        ),
    }

    if XGBOOST_AVAILABLE:
        models["XGBoost"] = XGBRegressor(
            n_estimators=300,
            learning_rate=0.05,
            max_depth=6,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=RANDOM_STATE,
            verbosity=0,
        )

    return models


# ─────────────────────────────────────────────
# EVALUATION
# ─────────────────────────────────────────────

def evaluate_model(model, X_test, y_test) -> dict:
    """Compute MAE, RMSE, and R² for a fitted model."""
    y_pred = model.predict(X_test)
    mae  = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2   = r2_score(y_test, y_pred)
    return {"mae": mae, "rmse": rmse, "r2": r2, "predictions": y_pred}


# ─────────────────────────────────────────────
# PLOTS
# ─────────────────────────────────────────────

def plot_model_comparison(results: dict, output_dir: str = "data/processed/plots") -> None:
    """Bar chart comparing all models on MAE, RMSE, R²."""
    set_plot_style()
    models = list(results.keys())
    mae_vals  = [results[m]["mae"]  for m in models]
    rmse_vals = [results[m]["rmse"] for m in models]
    r2_vals   = [results[m]["r2"]   for m in models]

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle("Model Comparison", fontsize=16, fontweight="bold", color="#FFD700")
    fig.patch.set_facecolor("#0f1117")

    color = "#FFD700"
    for ax, vals, title, fmt in zip(
        axes,
        [mae_vals, rmse_vals, r2_vals],
        ["MAE (lower is better)", "RMSE (lower is better)", "R² Score (higher is better)"],
        [".3f", ".3f", ".4f"],
    ):
        bars = ax.bar(models, vals, color=color, edgecolor="#2a2d3a", linewidth=0.5)
        ax.set_title(title, color="#e0e0e0", fontsize=11)
        ax.set_facecolor("#1a1d27")
        ax.tick_params(axis="x", rotation=20)
        for bar, val in zip(bars, vals):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() * 0.97,
                f"{val:{fmt}}",
                ha="center", va="top", fontsize=9, color="#0f1117", fontweight="bold",
            )

    plt.tight_layout()
    save_plot(fig, "model_comparison.png", output_dir)
    logger.info("Model comparison plot saved.")


def plot_predictions_vs_actual(
    y_test, y_pred, model_name: str, output_dir: str = "data/processed/plots"
) -> None:
    """Scatter plot of predicted vs actual energy output."""
    set_plot_style()
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(f"{model_name}: Prediction Analysis", fontsize=14, color="#FFD700")
    fig.patch.set_facecolor("#0f1117")

    # Scatter
    ax = axes[0]
    ax.scatter(y_test, y_pred, alpha=0.4, s=10, color="#FFD700")
    lims = [min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max())]
    ax.plot(lims, lims, "r--", lw=1.5, label="Perfect Prediction")
    ax.set_xlabel("Actual kWh")
    ax.set_ylabel("Predicted kWh")
    ax.set_title("Predicted vs Actual")
    ax.legend()
    ax.set_facecolor("#1a1d27")

    # Residuals
    ax = axes[1]
    residuals = y_pred - y_test
    ax.hist(residuals, bins=60, color="#06D6A0", edgecolor="#0f1117", linewidth=0.3)
    ax.axvline(0, color="#FF6B35", linestyle="--", linewidth=1.5)
    ax.set_xlabel("Residual (Predicted − Actual)")
    ax.set_ylabel("Count")
    ax.set_title("Residual Distribution")
    ax.set_facecolor("#1a1d27")

    plt.tight_layout()
    save_plot(fig, f"predictions_{model_name.replace(' ', '_').lower()}.png", output_dir)


def plot_feature_importance(model, feature_names: list, output_dir: str = "data/processed/plots") -> None:
    """Horizontal bar chart of feature importances."""
    if not hasattr(model, "feature_importances_"):
        logger.info("Model does not support feature importances — skipping.")
        return

    set_plot_style()
    importances = model.feature_importances_
    sorted_idx  = np.argsort(importances)

    fig, ax = plt.subplots(figsize=(10, 7))
    fig.patch.set_facecolor("#0f1117")
    ax.set_facecolor("#1a1d27")

    colors = plt.cm.YlOrRd(np.linspace(0.3, 0.9, len(sorted_idx)))
    ax.barh(
        [feature_names[i] for i in sorted_idx],
        importances[sorted_idx],
        color=colors,
    )
    ax.set_xlabel("Importance Score", color="#e0e0e0")
    ax.set_title("Feature Importances", fontsize=14, color="#FFD700", fontweight="bold")
    plt.tight_layout()
    save_plot(fig, "feature_importance.png", output_dir)
    logger.info("Feature importance plot saved.")


# ─────────────────────────────────────────────
# MAIN TRAINING PIPELINE
# ─────────────────────────────────────────────

def train_pipeline() -> None:
    """
    Full training pipeline:
    1. Load processed data
    2. Split features / target
    3. Train/test split
    4. Train and evaluate all models
    5. Select best model
    6. Save best model + metrics
    7. Generate plots
    """
    logger.info("=" * 50)
    logger.info("  SOLAR ENERGY OUTPUT PREDICTOR — TRAINING")
    logger.info("=" * 50)

    # 1. Load data
    df = load_data(DATA_PATH)

    # 2. Select features available in the dataset
    available_features = [col for col in FEATURE_COLS if col in df.columns]
    # Add engineered features if present
    extra_features = [
        "hour_sin", "hour_cos", "month_sin", "month_cos",
        "temp_irradiance", "cloud_humidity", "clear_sky_index",
    ]
    all_features = available_features + [f for f in extra_features if f in df.columns]

    X = df[all_features].values
    y = df[TARGET_COL].values
    logger.info(f"Features used ({len(all_features)}): {all_features}")

    # 3. Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )
    logger.info(f"Train: {X_train.shape[0]:,}  |  Test: {X_test.shape[0]:,}")

    # 4. Train and evaluate all models
    models  = get_models()
    results = {}

    for name, model in models.items():
        logger.info(f"Training: {name} …")
        model.fit(X_train, y_train)
        eval_result = evaluate_model(model, X_test, y_test)
        results[name] = eval_result
        print_metrics(name, eval_result["mae"], eval_result["rmse"], eval_result["r2"])

    # 5. Select best model (highest R²)
    best_name  = max(results, key=lambda m: results[m]["r2"])
    best_model = models[best_name]
    best_metrics = results[best_name]
    logger.info(f"Best model: {best_name} (R² = {best_metrics['r2']:.4f})")

    # 6. Save best model
    os.makedirs("models", exist_ok=True)
    model_data = {
        "model":        best_model,
        "feature_cols": all_features,
        "model_name":   best_name,
        "trained_at":   timestamp_now(),
    }
    joblib.dump(model_data, MODEL_PATH)
    logger.info(f"Model saved: {MODEL_PATH}")

    # Save metrics JSON
    metrics_out = {}
    for name, res in results.items():
        metrics_out[name] = {
            "mae":  round(res["mae"],  4),
            "rmse": round(res["rmse"], 4),
            "r2":   round(res["r2"],   4),
        }
    metrics_out["best_model"] = best_name

    with open(METRICS_PATH, "w") as f:
        json.dump(metrics_out, f, indent=2)
    logger.info(f"Metrics saved: {METRICS_PATH}")

    # 7. Generate plots
    os.makedirs("data/processed/plots", exist_ok=True)
    plot_model_comparison(results)
    plot_predictions_vs_actual(y_test, best_metrics["predictions"], best_name)
    plot_feature_importance(best_model, all_features)

    logger.info("Training pipeline complete.")
    return best_model, all_features


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    train_pipeline()
