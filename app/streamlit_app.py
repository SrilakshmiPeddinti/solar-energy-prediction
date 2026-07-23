"""
streamlit_app.py — Interactive Solar Energy Output Predictor Web App

Run:
    streamlit run app/streamlit_app.py
"""

import os
import sys
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import streamlit as st

# Allow imports from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="☀️ Solar Energy Predictor",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────

st.markdown("""
<style>
    /* Main background */
    .stApp { background: #0d1117; color: #e6edf3; }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #161b22;
        border-right: 1px solid #30363d;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        color: #FFD700 !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #8b949e !important;
    }
    
    /* Headers */
    h1 { color: #FFD700 !important; }
    h2 { color: #FFA500 !important; }
    h3 { color: #e6edf3 !important; }
    
    /* Slider labels */
    .stSlider label { color: #c9d1d9 !important; }
    
    /* Button */
    .stButton button {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: #0d1117;
        font-weight: 700;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-size: 1.1rem;
        transition: transform 0.1s;
    }
    .stButton button:hover { transform: scale(1.03); }
    
    /* Info boxes */
    .info-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-left: 4px solid #FFD700;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
    }
    
    /* Divider */
    hr { border-color: #30363d !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

PLOT_BG = "#0d1117"
PLOT_AX  = "#161b22"

def set_dark_style():
    plt.rcParams.update({
        "figure.facecolor": PLOT_BG,
        "axes.facecolor":   PLOT_AX,
        "axes.edgecolor":   "#30363d",
        "axes.labelcolor":  "#c9d1d9",
        "xtick.color":      "#8b949e",
        "ytick.color":      "#8b949e",
        "text.color":       "#c9d1d9",
        "grid.color":       "#21262d",
        "grid.alpha":       0.6,
    })

@st.cache_data
def load_processed_data():
    path = "data/processed/solar_data_processed.csv"
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

@st.cache_resource
def load_predictor():
    try:
        from src.predict import SolarPredictor
        return SolarPredictor(), None
    except FileNotFoundError as e:
        return None, str(e)

@st.cache_data
def load_metrics():
    path = "models/metrics.json"
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None


def energy_gauge(value: float, max_val: float = 4.0) -> plt.Figure:
    """Render a half-donut gauge for the predicted kWh."""
    set_dark_style()
    fig, ax = plt.subplots(figsize=(4, 2.5), subplot_kw={"aspect": "equal"})
    fig.patch.set_facecolor(PLOT_BG)
    ax.set_facecolor(PLOT_BG)

    pct   = min(value / max_val, 1.0)
    angle = pct * 180

    # Background arc
    theta = np.linspace(np.pi, 0, 100)
    ax.plot(np.cos(theta), np.sin(theta), color="#30363d", lw=18, solid_capstyle="round")

    # Fill arc
    theta_fill = np.linspace(np.pi, np.pi - np.radians(angle), max(2, int(angle)))
    color = "#06D6A0" if pct > 0.6 else "#FFD700" if pct > 0.3 else "#FF6B35"
    ax.plot(np.cos(theta_fill), np.sin(theta_fill), color=color, lw=18, solid_capstyle="round")

    # Center text
    ax.text(0, -0.15, f"{value:.3f}", ha="center", va="center",
            fontsize=22, fontweight="bold", color="#FFD700")
    ax.text(0, -0.45, "kWh", ha="center", va="center", fontsize=12, color="#8b949e")

    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-0.7, 1.2)
    ax.axis("off")
    plt.tight_layout(pad=0)
    return fig


# ─────────────────────────────────────────────
# SIDEBAR — INPUTS
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown("## ☀️ Solar Predictor")
    st.markdown("---")
    st.markdown("### 🌤 Weather Conditions")

    temperature      = st.slider("🌡 Temperature (°C)",        -10.0, 55.0,  28.0, 0.5)
    humidity         = st.slider("💧 Humidity (%)",              0.0, 100.0,  45.0, 1.0)
    cloud_cover      = st.slider("☁️ Cloud Cover (%)",           0.0, 100.0,  10.0, 1.0)
    solar_irradiance = st.slider("☀️ Solar Irradiance (W/m²)",   0.0, 1200.0, 850.0, 10.0)
    wind_speed       = st.slider("💨 Wind Speed (m/s)",          0.0,  40.0,   3.5, 0.5)
    rainfall         = st.slider("🌧 Rainfall (mm)",             0.0, 100.0,   0.0, 0.5)

    st.markdown("---")
    st.markdown("### 🕐 Time")
    hour  = st.slider("Hour of Day",  6, 19, 12)
    month = st.selectbox(
        "Month",
        options=list(range(1, 13)),
        format_func=lambda m: [
            "January","February","March","April","May","June",
            "July","August","September","October","November","December"
        ][m-1],
        index=5,
    )

    st.markdown("---")
    predict_btn = st.button("⚡ Predict Energy Output", use_container_width=True)


# ─────────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────────

st.markdown("# ☀️ Solar Energy Output Predictor")
st.markdown("**AI-Powered Solar Power Forecasting Dashboard**  |  Machine Learning × Renewable Energy Analytics")
st.markdown("---")

predictor, pred_error = load_predictor()
df = load_processed_data()
metrics = load_metrics()

# ── TOP KPI ROW ──────────────────────────────

if df is not None:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 Total Records",   f"{len(df):,}")
    with col2:
        avg_kwh = df["energy_output_kwh"].mean()
        st.metric("⚡ Avg Output",       f"{avg_kwh:.3f} kWh")
    with col3:
        max_kwh = df["energy_output_kwh"].max()
        st.metric("🔝 Peak Output",      f"{max_kwh:.3f} kWh")
    with col4:
        if metrics:
            bm = metrics.get("best_model", "—")
            r2 = metrics.get(bm, {}).get("r2", 0) * 100
            st.metric("🤖 Best Model R²",  f"{r2:.1f}%")
        else:
            st.metric("🤖 Best Model R²", "Train first")

st.markdown("---")

# ── PREDICTION PANEL ─────────────────────────

tab1, tab2, tab3, tab4 = st.tabs(["⚡ Prediction", "📈 Analytics", "🤖 Models", "ℹ️ About"])

with tab1:
    st.markdown("## ⚡ Live Energy Prediction")
    
    if pred_error:
        st.warning(f"⚠️ Model not loaded: {pred_error}")
        st.info("Run `python src/preprocess.py` then `python src/train.py` to train the model.")
    else:
        col_left, col_right = st.columns([1.2, 1])

        with col_left:
            if predict_btn or True:
                result = predictor.predict({
                    "temperature_c":        temperature,
                    "humidity_pct":         humidity,
                    "cloud_cover_pct":      cloud_cover,
                    "solar_irradiance_wm2": solar_irradiance,
                    "wind_speed_ms":        wind_speed,
                    "rainfall_mm":          rainfall,
                    "hour":                 hour,
                    "month":                month,
                })

                predicted_kwh = result["predicted_kwh"]
                confidence    = result["confidence"]
                model_name    = result["model_name"]

                conf_color = {"High": "#06D6A0", "Medium": "#FFD700", "Low": "#FF6B35"}[confidence]

                st.markdown(f"""
                <div class="info-card">
                    <h3 style="margin:0; color:#FFD700">Predicted Output</h3>
                    <p style="font-size:3rem; font-weight:900; margin:0.2rem 0; color:#FFD700">
                        {predicted_kwh:.4f} kWh
                    </p>
                    <p style="margin:0; color:#8b949e">
                        Confidence: <span style="color:{conf_color}; font-weight:bold">{confidence}</span>
                        &nbsp;|&nbsp; Model: <span style="color:#58a6ff">{model_name}</span>
                    </p>
                </div>
                """, unsafe_allow_html=True)

                # Daily estimate
                daily_est = predicted_kwh * 10  # rough: peak-sun hours
                monthly_est = daily_est * 30
                co2_saved = monthly_est * 0.42  # kg CO2 per kWh (avg grid)

                st.markdown("")
                c1, c2, c3 = st.columns(3)
                c1.metric("☀️ Daily Est.", f"{daily_est:.2f} kWh")
                c2.metric("📅 Monthly Est.", f"{monthly_est:.1f} kWh")
                c3.metric("🌱 CO₂ Saved/mo", f"{co2_saved:.1f} kg")

        with col_right:
            st.markdown("**Output Gauge**")
            gauge = energy_gauge(predicted_kwh, max_val=max(4.0, predicted_kwh * 1.2))
            st.pyplot(gauge, use_container_width=True)
            plt.close()

        # Input summary table
        st.markdown("---")
        st.markdown("**Input Summary**")
        input_df = pd.DataFrame([{
            "Temperature (°C)":     temperature,
            "Humidity (%)":         humidity,
            "Cloud Cover (%)":      cloud_cover,
            "Irradiance (W/m²)":    solar_irradiance,
            "Wind Speed (m/s)":     wind_speed,
            "Rainfall (mm)":        rainfall,
            "Hour":                 hour,
            "Month":                month,
        }]).T.reset_index()
        input_df.columns = ["Parameter", "Value"]
        st.dataframe(input_df, use_container_width=True, hide_index=True)


with tab2:
    st.markdown("## 📈 Data Analytics")

    if df is None:
        st.warning("No processed data found. Run `python src/preprocess.py` first.")
    else:
        set_dark_style()

        # Monthly average output
        st.markdown("### Monthly Energy Output Trends")
        month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        monthly = df.groupby("month")["energy_output_kwh"].mean().reset_index()

        fig, ax = plt.subplots(figsize=(12, 4))
        fig.patch.set_facecolor(PLOT_BG)
        ax.set_facecolor(PLOT_AX)
        colors = ["#FFD700" if v == monthly["energy_output_kwh"].max() else "#FFA500"
                  for v in monthly["energy_output_kwh"]]
        bars = ax.bar([month_names[m-1] for m in monthly["month"]], monthly["energy_output_kwh"], color=colors, edgecolor="#0d1117", linewidth=0.5)
        ax.set_xlabel("Month")
        ax.set_ylabel("Avg Energy Output (kWh)")
        ax.set_title("Average Solar Energy Output by Month", color="#FFD700", fontweight="bold")
        ax.grid(axis="y", alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()

        col1, col2 = st.columns(2)

        # Hourly pattern
        with col1:
            st.markdown("### Hourly Generation Pattern")
            hourly = df.groupby("hour")["energy_output_kwh"].mean().reset_index()
            fig, ax = plt.subplots(figsize=(6, 4))
            fig.patch.set_facecolor(PLOT_BG)
            ax.set_facecolor(PLOT_AX)
            ax.fill_between(hourly["hour"], hourly["energy_output_kwh"], alpha=0.4, color="#FFD700")
            ax.plot(hourly["hour"], hourly["energy_output_kwh"], color="#FFD700", lw=2)
            ax.set_xlabel("Hour of Day")
            ax.set_ylabel("Avg kWh")
            ax.set_title("Generation by Hour", color="#FFD700", fontweight="bold")
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close()

        # Irradiance vs output scatter
        with col2:
            st.markdown("### Irradiance vs Energy Output")
            sample = df.sample(min(2000, len(df)), random_state=42)
            fig, ax = plt.subplots(figsize=(6, 4))
            fig.patch.set_facecolor(PLOT_BG)
            ax.set_facecolor(PLOT_AX)
            sc = ax.scatter(
                sample["solar_irradiance_wm2"],
                sample["energy_output_kwh"],
                c=sample["cloud_cover_pct"],
                cmap="YlOrRd_r",
                alpha=0.5, s=8,
            )
            plt.colorbar(sc, ax=ax, label="Cloud Cover %")
            ax.set_xlabel("Solar Irradiance (W/m²)")
            ax.set_ylabel("Energy Output (kWh)")
            ax.set_title("Irradiance vs Output", color="#FFD700", fontweight="bold")
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close()

        # Correlation heatmap
        st.markdown("### Feature Correlation Heatmap")
        corr_cols = ["temperature_c","humidity_pct","cloud_cover_pct",
                     "solar_irradiance_wm2","wind_speed_ms","rainfall_mm","energy_output_kwh"]
        corr_cols = [c for c in corr_cols if c in df.columns]
        corr = df[corr_cols].corr()

        fig, ax = plt.subplots(figsize=(9, 6))
        fig.patch.set_facecolor(PLOT_BG)
        sns.heatmap(
            corr, annot=True, fmt=".2f", cmap="YlOrRd",
            ax=ax, linewidths=0.5, linecolor="#0d1117",
            annot_kws={"size": 9},
        )
        ax.set_title("Feature Correlation Matrix", color="#FFD700", fontweight="bold")
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()


with tab3:
    st.markdown("## 🤖 Model Performance")

    if metrics is None:
        st.warning("No metrics found. Run `python src/train.py` to train models.")
    else:
        best_model = metrics.pop("best_model", None)
        metrics_df = pd.DataFrame(metrics).T.reset_index()
        metrics_df.columns = ["Model", "MAE", "RMSE", "R²"]
        metrics_df = metrics_df.sort_values("R²", ascending=False).reset_index(drop=True)

        # Highlight best
        def highlight_best(row):
            if best_model and row["Model"] == best_model:
                return ["background-color: #1f2d1f; color: #06D6A0; font-weight: bold"] * len(row)
            return [""] * len(row)

        st.dataframe(
            metrics_df.style.apply(highlight_best, axis=1).format(
                {"MAE": "{:.4f}", "RMSE": "{:.4f}", "R²": "{:.4f}"}
            ),
            use_container_width=True,
            hide_index=True,
        )

        if best_model:
            st.success(f"✅ Best Model: **{best_model}** (R² = {metrics[best_model]['r2']:.4f})")

        # Bar chart
        set_dark_style()
        fig, axes = plt.subplots(1, 3, figsize=(14, 4))
        fig.suptitle("Model Comparison", color="#FFD700", fontweight="bold")
        fig.patch.set_facecolor(PLOT_BG)

        for ax, metric, title in zip(axes, ["R²", "MAE", "RMSE"],
                                      ["R² Score (↑ better)", "MAE (↓ better)", "RMSE (↓ better)"]):
            colors_bar = ["#06D6A0" if m == best_model else "#FFD700" for m in metrics_df["Model"]]
            ax.bar(metrics_df["Model"], metrics_df[metric], color=colors_bar, edgecolor="#0d1117")
            ax.set_title(title, color="#c9d1d9")
            ax.set_facecolor(PLOT_AX)
            ax.tick_params(axis="x", rotation=20)

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()


with tab4:
    st.markdown("## ℹ️ About This Project")
    st.markdown("""
    <div class="info-card">
        <h3>☀️ AI-Powered Solar Energy Output Prediction & Analytics System</h3>
        <p>An end-to-end Machine Learning project for predicting solar energy generation (kWh) 
        based on real-time weather conditions.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🏗️ Tech Stack")
        st.markdown("""
        | Layer | Technology |
        |---|---|
        | Language | Python 3.9+ |
        | Data Processing | Pandas, NumPy |
        | Machine Learning | Scikit-learn, XGBoost |
        | Visualization | Matplotlib, Seaborn |
        | Web App | Streamlit |
        | Model Persistence | Joblib |
        """)

    with col2:
        st.markdown("### 🌱 Input Features")
        st.markdown("""
        | Feature | Unit |
        |---|---|
        | Temperature | °C |
        | Humidity | % |
        | Cloud Cover | % |
        | Solar Irradiance | W/m² |
        | Wind Speed | m/s |
        | Rainfall | mm |
        | Hour of Day | 0–23 |
        | Month | 1–12 |
        """)

    st.markdown("### 🚀 How to Run the Full Pipeline")
    st.code("""
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate data & preprocess
python src/preprocess.py

# 3. Train ML models
python src/train.py

# 4. Launch this app
streamlit run app/streamlit_app.py
    """, language="bash")

    st.markdown("### 📌 Resume Project Title")
    st.info("**AI-Powered Solar Energy Output Prediction & Analytics System**")
