# Phase 2 Deep-Dive: Physics-Informed ML Architectures & Enterprise MLOps Governance

## 📌 Executive Summary

Phase 2 introduces the core artificial intelligence forecasting engine and production MLOps pipeline for the **AI-Powered Solar Energy Prediction & Analytics Platform**.

This phase spans **10 Enterprise Features** across 2 core packages:
1. **Next-Gen ML Architectures & Physics Modeling** (`src/ml_engine/`): FEAT 11 - 15
2. **MLOps, Model Governance & Observability** (`src/mlops/`): FEAT 26 - 30

---

## 🧠 1. Next-Gen ML Architectures & Physics Modeling (`src/ml_engine/`)

### FEAT-11: Physics-Informed Neural Networks (PINN) (`pinn_solar.py`)
- **Problem Addressed**: Pure data-driven deep learning models often predict physically impossible solar power outputs (e.g., negative generation at night, or exceeding thermodynamic efficiency limits).
- **Engineering Solution**: Implements a PyTorch Physics-Informed Neural Network (PINN). The network loss function combines standard Mean Squared Error ($\mathcal{L}_{\text{data}}$) with physical thermodynamic constraint penalties ($\mathcal{L}_{\text{physics}}$):
  $$\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{data}} + \lambda_1 \mathcal{L}_{\text{thermal}} + \lambda_2 \mathcal{L}_{\text{bound}}$$

- **Thermodynamic Equations Injected**:
  1. Photovoltaic Cell Temperature:
     $$T_{\text{cell}} = T_{\text{ambient}} + \left( \frac{\text{GHI}}{800} \right) \cdot (\text{NOCT} - 20^\circ\text{C})$$
  2. Thermal Temperature Power Derate:
     $$\eta_{\text{temp}} = 1 + \alpha_{\text{temp}} \cdot (T_{\text{cell}} - 25^\circ\text{C})$$
  3. Bounded Solar Generation:
     $$0 \le P_{\text{PINN}} \le P_{\text{STC}} \cdot \left(\frac{\text{GHI}}{1000}\right) \cdot \eta_{\text{temp}}$$

---

### FEAT-12: Temporal Fusion Transformer (TFT) (`tft_forecaster.py`)
- **Problem Addressed**: Multi-horizon solar forecasting requires modeling complex temporal dependencies across static site features, known future inputs (sun zenith angle), and historical telemetry time-series.
- **Engineering Solution**: Builds a multi-horizon Temporal Fusion Transformer (TFT). Employs Variable Selection Networks (VSN) to filter noisy inputs, Gated Residual Networks (GRN) to suppress irrelevant layers, and Multi-Head Attention to capture daily and seasonal periodicities across 15-min, 1-hr, 24-hr, and 7-day forecast lookahead horizons.

---

### FEAT-13: Quantile Loss Ensembling (P10/P50/P90) (`quantile_ensemble.py`)
- **Problem Addressed**: Grid operators and financial lenders require probabilistic confidence bands rather than single point estimates to assess financial downside risk.
- **Engineering Solution**: Implements quantile regression neural networks optimizing Pinball (Quantile) Loss:
  $$\mathcal{L}_{q}(y, \hat{y}) = \max\left( q(y - \hat{y}), (q - 1)(y - \hat{y}) \right)$$
- **Output Curves**:
  - **P10**: High confidence downside floor (10th percentile - 90% probability of exceedance).
  - **P50**: Median expected generation (50th percentile baseline).
  - **P90**: Optimistic generation ceiling (90th percentile).

---

### FEAT-14: Graph Neural Networks (GNN) for Array Topology (`gnn_array_topology.py`)
- **Problem Addressed**: Solar arrays are physically interconnected electrical graphs; shading on one string impacts string voltage across the entire inverter bus.
- **Engineering Solution**: Models solar array layout as a spatial graph $\mathcal{G} = (\mathcal{V}, \mathcal{E})$. Nodes $\mathcal{V}$ represent individual PV strings; edges $\mathcal{E}$ represent physical wiring and spatial proximity. Uses Graph Convolutional Networks (GCN) to pass spatial features between adjacent panels.

---

### FEAT-15: Online Learning & Concept Drift Detection (`online_learning.py`)
- **Problem Addressed**: Weather seasonal shifts, panel aging, and severe weather events degrade offline-trained batch ML models over time.
- **Engineering Solution**: Implements the ADWIN (Adaptive Windowing) concept drift algorithm. Continuously monitors streaming prediction residual errors; upon detecting distribution shifts ($p < 0.01$), it automatically triggers incremental online model weight retraining.

---

## 📊 2. Enterprise MLOps Governance & Observability (`src/mlops/`)

### FEAT-26: Enterprise Feature Store Infrastructure (`feature_store.py`)
- **Problem Addressed**: Training-serving skew occurs when offline model training features differ from low-latency online inference features.
- **Engineering Solution**: Integrated Feast & MLflow Feature Store architecture. Provides an offline feature store (Parquet / S3 / GCS) for batch model training and an online feature store (Redis Cluster) serving inference features in under 5ms.

---

### FEAT-27: Real-Time SHAP Explainability Engine (`model_explainability.py`)
- **Problem Addressed**: Black-box AI predictions are rejected by risk officers and grid regulators who require transparent explainability.
- **Engineering Solution**: Real-time TreeSHAP and Integrated Gradients calculation engine. Computes exact Shapley values for every inference prediction, breaking down power generation output into feature contributions (e.g., $+45\text{ kW}$ Irradiance, $-12\text{ kW}$ Temperature, $-5\text{ kW}$ Soiling).

---

### FEAT-28: Shadow Deployment & A/B Testing (`shadow_deployment.py`)
- **Problem Addressed**: Deploying newly trained models directly to production risks unhandled edge cases causing incorrect SCADA control actions.
- **Engineering Solution**: Implements a Shadow Deployment proxy pattern. Mirrors live production telemetry to challenger candidate models running asynchronously in shadow mode, computing relative Mean Absolute Error (MAE) and tracking performance for 14 days before automated promotion.

---

### FEAT-29: Data & Model Lineage Provenance (`lineage_provenance.py`)
- **Problem Addressed**: Auditing requires tracking exact raw data payloads, code commits, and hyperparameter configurations that produced a specific model binary.
- **Engineering Solution**: OpenLineage and DVC integration constructing directed acyclic graphs (DAGs) of model provenance. Every model binary is cryptographically bound to its raw dataset SHA-256 hash and Git commit ID.

---

### FEAT-30: Data Quality Sinks & Anomaly Isolation (`data_quality.py`)
- **Problem Addressed**: Corrupt sensor payloads (e.g., negative irradiance or $999^\circ\text{C}$ temperature spikes) poison ML training pipelines.
- **Engineering Solution**: Great Expectations validation pipeline checking incoming data schemas against predefined expectation suites. Out-of-range payloads are automatically quarantined to Dead Letter Queues (DLQ) with alert notifications sent to PagerDuty.
