# ☀️ AI-Powered Solar Energy Prediction & Analytics Platform

> **Industrial Utility-Scale Clean Energy Intelligence, Physics AI & Grid Management Platform**

[![Python CI/CD Pipeline](https://github.com/SrilakshmiPeddinti/solar-energy-prediction/actions/workflows/ci.yml/badge.svg)](https://github.com/SrilakshmiPeddinti/solar-energy-prediction/actions/workflows/ci.yml)
[![Security & CodeQL](https://github.com/SrilakshmiPeddinti/solar-energy-prediction/actions/workflows/security.yml/badge.svg)](https://github.com/SrilakshmiPeddinti/solar-energy-prediction/actions/workflows/security.yml)
[![Docker Build](https://github.com/SrilakshmiPeddinti/solar-energy-prediction/actions/workflows/docker.yml/badge.svg)](https://github.com/SrilakshmiPeddinti/solar-energy-prediction/actions/workflows/docker.yml)
[![Python Version](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Architecture: V2.0 Enterprise](https://img.shields.io/badge/Architecture-V2.0%20Enterprise-orange.svg)](50_UPGRADE_FEATURES.md)

---

## 📑 Table of Contents

- [📌 Executive Overview](#-executive-overview)
- [🎨 Enterprise Technical Block Diagrams](#-enterprise-technical-block-diagrams)
- [🔬 Core Physics & Mathematical Formulations](#-core-physics--mathematical-formulations)
- [🏢 Complete 50 Enterprise Features Directory](#-complete-50-enterprise-features-directory)
  - [⚡ Category 1: Real-Time Telemetry, Edge Computing & SCADA Integration (FEAT 01-05)](#-category-1-real-time-telemetry-edge-computing--scada-integration)
  - [🛰️ Category 2: Advanced Weather, GIS & Satellite Earth Observation (FEAT 06-10)](#️-category-2-advanced-weather-gis--satellite-earth-observation)
  - [🧠 Category 3: Next-Gen ML Architectures & Physics-Informed Modeling (FEAT 11-15)](#-category-3-next-gen-ml-architectures--physics-informed-modeling)
  - [🔋 Category 4: Battery Energy Storage System (BESS) & Grid Arbitrage (FEAT 16-20)](#-category-4-battery-energy-storage-system-bess--grid-arbitrage)
  - [🚁 Category 5: Asset Health, Predictive Maintenance & Computer Vision (FEAT 21-25)](#-category-5-asset-health-predictive-maintenance--computer-vision)
  - [📊 Category 6: MLOps, Model Governance & Observability (FEAT 26-30)](#-category-6-mlops-model-governance--observability)
  - [🔒 Category 7: Multi-Tenant Architecture, Security & Enterprise RBAC (FEAT 31-35)](#-category-7-multi-tenant-architecture-security--enterprise-rbac)
  - [🌱 Category 8: Carbon Offsetting, ESG Analytics & Compliance Reporting (FEAT 36-40)](#-category-8-carbon-offsetting-esg-analytics--compliance-reporting)
  - [☁️ Category 9: Enterprise API, High Availability & Distributed Infrastructure (FEAT 41-45)](#️-category-9-enterprise-api-high-availability--distributed-infrastructure)
  - [💼 Category 10: Financial Risk Management, Portfolio & ROI Analytics (FEAT 46-50)](#-category-10-financial-risk-management-portfolio--roi-analytics)
- [💻 Comprehensive Python API Reference](#-comprehensive-python-api-reference)
- [📁 Repository Structure](#-repository-structure)
- [⚡ Installation & Quick Start](#-installation--quick-start)
- [⚙️ CI/CD & Security Automation](#️-cicd--security-automation)
- [📄 License & Maintainer](#-license--maintainer)

---

## 📌 Executive Overview

The **AI-Powered Solar Energy Prediction & Analytics System** is an industrial utility-scale clean energy intelligence platform. Designed for commercial solar plant operators, Virtual Power Plant (VPP) aggregators, and energy trading desks, the platform integrates sub-second telemetry streaming, physics-informed AI neural networks, battery storage optimization, computer vision drone diagnostics, zero-trust security, and automated carbon offset auditing.

The system is fully modular and production-ready, featuring **50 implemented enterprise features** across 10 strategic domain packages in Python.

---

## 🎨 Enterprise Technical Block Diagrams

### 1. Overall System Architecture
![Overall System Architecture](docs/images/system_architecture_diagram.png)
*Figure 1: End-to-end multi-tier pipeline connecting edge telemetry, satellite AI nowcasting, physics ML, battery arbitrage, and security.*

### 2. Real-Time Edge Telemetry & SCADA Control Loop
![Edge SCADA BESS Flow](docs/images/edge_scada_bess_flow.png)
*Figure 2: Edge microinverter telemetry ingestion via Modbus/OPC-UA/MQTT into Apache Kafka with closed-loop SCADA active power control.*

### 3. Physics-Informed AI & MLOps Pipeline
![Physics MLOps Pipeline](docs/images/physics_mlops_pipeline.png)
*Figure 3: Physics-Informed Neural Network (PINN) loss layers, Temporal Fusion Transformers, Feast Feature Store, and SHAP explainability.*

### 4. Drone IR Vision & Computer Vision Asset Health Workflow
![Asset Health CV Workflow](docs/images/asset_health_cv_workflow.png)
*Figure 4: Computer vision asset diagnostics processing aerial radiometric infrared drone imagery and electroluminescence (EL) cell scans.*

### 5. Virtual Power Plant & Financial Risk Engine
![VPP Financial Risk Architecture](docs/images/vpp_financial_risk_architecture.png)
*Figure 5: Multi-site VPP aggregation, 50,000-iteration Monte Carlo yield VaR modeling, and PPA automated billing.*

---

## 🔬 Core Physics & Mathematical Formulations

### 1. Photovoltaic Thermodynamic Cell Temperature & Derate
Panel cell operating temperature \( T_{\text{cell}} \) and output power derate factor \( \eta_{\text{temp}} \) are computed using physical thermal balance equations:

\[
T_{\text{cell}} = T_{\text{ambient}} + \left( \frac{\text{GHI}}{800} \right) \cdot \frac{\text{NOCT} - 20^\circ\text{C}}{1 + 0.05 \cdot v_{\text{wind}}}
\]

\[
P_{\text{PINN}} = P_{\text{STC}} \cdot \left( \frac{\text{GHI}}{1000} \right) \cdot \left[ 1 + \alpha_{\text{temp}} \cdot (T_{\text{cell}} - 25^\circ\text{C}) \right]
\]

### 2. Stochastic Monte Carlo Value at Risk (VaR)
50,000 Monte Carlo weather and price iterations compute financial yield probability distributions:

\[
\text{VaR}_{95\%} = P_{50}(\text{Revenue}) - P_{10}(\text{Revenue})
\]

---

## 🏢 Complete 50 Enterprise Features Directory

### ⚡ Category 1: Real-Time Telemetry, Edge Computing & SCADA Integration

- **FEAT-01: Edge Micro-Inverter Telemetry Collector** (`src/telemetry/edge_collector.py`)
  - Aggregates AC/DC voltage, current, frequency, and thermal metrics via Modbus RTU/TCP, OPC-UA, and MQTT protocols down to string and panel levels.
- **FEAT-02: Sub-Second Stream Ingestion Pipeline** (`src/telemetry/stream_ingestion.py`)
  - Apache Kafka / Flink streaming engine performing sub-second event ingestion, deduplication, and sliding window aggregation under 10ms latency.
- **FEAT-03: Ultra-Low Latency Edge AI Inference Engine** (`src/telemetry/edge_inference.py`)
  - ONNX Runtime and TensorRT wrapper executing localized ML inference directly on edge hardware gateways (e.g., NVIDIA Jetson).
- **FEAT-04: Automated Sensor Degradation & Self-Calibration** (`src/telemetry/sensor_calibration.py`)
  - Kalman Filter and Isolation Forest framework detecting calibration drift in pyranometers and ambient temperature sensors against satellite references.
- **FEAT-05: Two-Way Microgrid SCADA & DERMS Control Loop** (`src/telemetry/scada_derms.py`)
  - Closed-loop interface executing active power curtailment and ramp rate adjustments via DNP3 and IEC 61850 protocol handlers.

---

### 🛰️ Category 2: Advanced Weather, GIS & Satellite Earth Observation

- **FEAT-06: Geostationary Satellite Irradiance Nowcasting** (`src/gis_weather/satellite_nowcasting.py`)
  - Ingests GOES-16 and Sentinel-2 optical flow satellite imagery to nowcast Global Horizontal Irradiance (GHI) up to 6 hours ahead.
- **FEAT-07: Microclimate Aerosol Optical Depth & Dust Soiling Simulator** (`src/gis_weather/aerosol_soiling.py`)
  - Integrates CAMS atmosphere data to model aerosol optical depth (AOD) attenuation and panel dust deposition rates.
- **FEAT-08: High-Precision LiDAR Topographical 3D Shading Engine** (`src/gis_weather/lidar_shading.py`)
  - Ray-tracing engine processing 3D LiDAR point clouds to compute topographical terrain shading masks across different sun azimuths.
- **FEAT-09: Multi-Model Weather Ensemble Blending Engine** (`src/gis_weather/weather_ensemble.py`)
  - Dynamic meta-learning stacking ensemble weighting ECMWF, GFS, HRRR, and Open-Meteo weather predictions.
- **FEAT-10: Severe Weather Risk Vectors & Cloud Velocity Field Predictor** (`src/gis_weather/severe_weather.py`)
  - Optical flow radar cell tracking predicting hail risk and extreme wind vectors to trigger automated panel stowing angles.

---

### 🧠 Category 3: Next-Gen ML Architectures & Physics-Informed Modeling

- **FEAT-11: Physics-Informed Neural Networks (PINN) for Photovoltaic Thermodynamics** (`src/ml_engine/pinn_solar.py`)
  - PyTorch neural network integrating panel heat dissipation equations and thermodynamic loss constraints directly into model loss functions.
- **FEAT-12: Multi-Horizon Temporal Fusion Transformer (TFT) Forecasting** (`src/ml_engine/tft_forecaster.py`)
  - Temporal Fusion Transformers for multi-horizon time-series forecasting across 15-minute, 1-hour, 24-hour, and 7-day lookahead windows.
- **FEAT-13: Probabilistic Quantile Loss Prediction Ensembling (P10/P50/P90)** (`src/ml_engine/quantile_ensemble.py`)
  - Quantile regression models producing complete probability distribution curves for P10 downside risk, P50 baseline, and P90 optimistic yield.
- **FEAT-14: Graph Neural Networks (GNN) for Solar Array Spatial Topology** (`src/ml_engine/gnn_array_topology.py`)
  - Graph Convolutional Networks (GCN) representing solar strings, micro-inverters, and transformers as connected spatial graph nodes.
- **FEAT-15: Continuous Online Learning & Automatic Concept Drift Detection** (`src/ml_engine/online_learning.py`)
  - ADWIN / KS-test distribution shift detector triggering automated incremental online model retraining upon concept drift.

---

### 🔋 Category 4: Battery Energy Storage System (BESS) & Grid Arbitrage

- **FEAT-16: BESS State-of-Charge & Degradation-Aware Charging Strategy** (`src/bess_arbitrage/bess_soc_optimizer.py`)
  - Co-optimizes solar storage into lithium-ion batteries while enforcing strict depth-of-discharge (DoD) and degradation cost boundaries.
- **FEAT-17: Day-Ahead & Real-Time Electricity Market Arbitrage Engine** (`src/bess_arbitrage/market_arbitrage.py`)
  - Schedules solar-battery sales into wholesale electricity spot markets (CAISO, ERCOT, PJM) during peak price intervals.
- **FEAT-18: Dynamic Frequency Regulation & Grid Ancillary Services Dispatcher** (`src/bess_arbitrage/frequency_regulation.py`)
  - Rapid-response droop control dispatcher for Primary Frequency Response (PFR) grid ancillary service market bidding.
- **FEAT-19: Mixed-Integer Linear Programming (MILP) Multi-Objective Dispatch** (`src/bess_arbitrage/milp_dispatch.py`)
  - Exact MILP optimization solver formulating joint solar, BESS, grid load, and export tariff constraints.
- **FEAT-20: Interconnection Capacity Limit & Curtailment Risk Optimizer** (`src/bess_arbitrage/curtailment_optimizer.py`)
  - Predicts sub-station congestion bottlenecks and automatically diverts excess power into battery or thermal sinks before curtailment commands occur.

---

### 🚁 Category 5: Asset Health, Predictive Maintenance & Computer Vision

- **FEAT-21: Autonomous Drone Radiometric IR Hotspot & Anomaly Detection** (`src/asset_health/drone_ir_detection.py`)
  - Computer vision pipeline processing drone radiometric thermal infrared images to detect cracked cells, bypassed diodes, and hotspots.
- **FEAT-22: Inverter Component Remaining Useful Life (RUL) Prognostics** (`src/asset_health/inverter_rul.py`)
  - Survival analysis and harmonic distortion analytics predicting inverter capacitor and IGBT switch failure timelines.
- **FEAT-23: Automated Panel Soiling Dynamics & Dynamic Washing Scheduler** (`src/asset_health/panel_washing_scheduler.py`)
  - Cost-benefit dynamic programming optimizer balancing cleaning crew costs against projected energy recovery revenue.
- **FEAT-24: Electroluminescence (EL) Cell Micro-Crack Automated Diagnostics** (`src/asset_health/el_microcrack_classifier.py`)
  - High-resolution deep learning image classifier detecting internal silicon micro-cracks in factory and field EL scans.
- **FEAT-25: Single/Dual-Axis Tracker Mechanical Actuator Diagnostics** (`src/asset_health/tracker_diagnostics.py`)
  - Monitors motor current draw and position encoder feedback on single/dual-axis trackers to detect mechanical binding or gear faults.

---

### 📊 Category 6: MLOps, Model Governance & Observability

- **FEAT-26: Enterprise Feature Store Infrastructure** (`src/mlops/feature_store.py`)
  - Centralized Feast / MLflow feature store caching low-latency online features and historical training feature stores.
- **FEAT-27: Real-Time Model Explainability & Feature Attribution (SHAP)** (`src/mlops/model_explainability.py`)
  - Computes TreeSHAP and Integrated Gradients values for every inference prediction to display feature impact metrics.
- **FEAT-28: Automated Shadow Deployment & Champion-Challenger Testing** (`src/mlops/shadow_deployment.py`)
  - Mirrors production traffic to challenger models in shadow mode, automatically evaluating relative MAE/RMSE before promotion.
- **FEAT-29: Data & Model Lineage Provenance Tracking** (`src/mlops/lineage_provenance.py`)
  - Integrates OpenLineage and DVC to capture audit graphs tracking raw telemetry payloads, preprocessing commits, and model binaries.
- **FEAT-30: Automated Data Quality Sinks & Anomaly Isolation** (`src/mlops/data_quality.py`)
  - Great Expectations payload validation pipeline detecting out-of-range metrics and isolating corrupt data to dead-letter queues.

---

### 🔒 Category 7: Multi-Tenant Architecture, Security & Enterprise RBAC

- **FEAT-31: Multi-Tenant Workspace Isolation with Cell-Level KMS Encryption** (`src/security/multi_tenant.py`)
  - PostgreSQL Row-Level Security (RLS) and AWS KMS envelope key encryption isolating tenant data on shared infrastructure.
- **FEAT-32: Single Sign-On (SSO) & IdP Federation** (`src/security/sso_idp.py`)
  - SAML 2.0 and OIDC authentication provider connector supporting Okta, Azure Active Directory (Azure AD), and Auth0.
- **FEAT-33: Granular Role-Based (RBAC) & Attribute-Based Access Control (ABAC)** (`src/security/rbac_abac.py`)
  - Policy Decision Point (PDP) evaluating user role, resource region, and action authorization policies (Casbin / OPA logic).
- **FEAT-34: Enterprise Audit Trail, SOC 2 / ISO 27001 Compliance & SIEM Ingestion** (`src/security/audit_siem.py`)
  - Immutable append-only audit logger streaming cryptographically signed event records directly to Splunk and Datadog.
- **FEAT-35: Zero-Trust API Gateway with mTLS & Dynamic Rate Limiting** (`src/security/api_gateway.py`)
  - Gateway enforcing Mutual TLS (mTLS), JWT token validation, and Redis token-bucket client rate limiting.

---

### 🌱 Category 8: Carbon Offsetting, ESG Analytics & Compliance Reporting

- **FEAT-36: Real-Time Scope 1/2/3 Carbon Offset Verification Engine** (`src/esg_compliance/scope123_calculator.py`)
  - Calculates real-time avoided CO2 metric tons based on localized marginal grid displacement emission factors.
- **FEAT-37: Automated Renewable Energy Certificate (REC) & GO Ledger** (`src/esg_compliance/rec_ledger.py`)
  - Packages clean solar generation into tokenized RECs and Guarantees of Origin (GOs) with cryptographic serial numbers.
- **FEAT-38: Automated Environmental Regulatory Reporting Engine** (`src/esg_compliance/regulatory_reporting.py`)
  - Auto-generates compliance reporting documentation for US EPA, EU Environment Agency, and India CEA regulations.
- **FEAT-39: EU Taxonomy & SEC Climate Disclosure Automated Documentation** (`src/esg_compliance/eu_sec_disclosures.py`)
  - Reporting templates evaluating EU Taxonomy Substantial Contribution criteria (<100g CO2e/kWh) and SEC Climate rules.
- **FEAT-40: Photovoltaic Lifecycle Footprint & Panel Circularity Tracker** (`src/esg_compliance/pv_lifecycle.py`)
  - Tracks embodied carbon, silicon origin, and end-of-life panel module circularity index scores.

---

### ☁️ Category 9: Enterprise API, High Availability & Distributed Infrastructure

- **FEAT-41: Multi-Region Active-Active High Availability Deployment** (`src/enterprise_api/k8s_multi_region.py`)
  - Multi-region Kubernetes (EKS/GKE) cluster health probe and automated geo-DNS failover controller guaranteeing 99.99% SLA.
- **FEAT-42: Event-Driven Asynchronous GraphQL & gRPC Streaming APIs** (`src/enterprise_api/grpc_graphql_stream.py`)
  - High-throughput Protobuf gRPC streaming channels and GraphQL subscriptions for real-time telemetry streaming.
- **FEAT-43: Distributed In-Memory Predictive Caching Layer** (`src/enterprise_api/distributed_caching.py`)
  - Redis Cluster and Ray Core multi-tiered predictive caching layer serving forecast lookups under 10 milliseconds.
- **FEAT-44: Disaster Recovery, Point-in-Time Restore & Immutable Vault** (`src/enterprise_api/disaster_recovery.py`)
  - Automated point-in-time recovery (PITR) snapshot backups with WORM ransomware protection locks.
- **FEAT-45: Distributed High-Throughput Batch Inference Pipeline** (`src/enterprise_api/ray_batch_inference.py`)
  - Ray Workflows distributed task engine executing concurrent inference across 10,000+ solar sites in parallel.

---

### 💼 Category 10: Financial Risk Management, Portfolio & ROI Analytics

- **FEAT-46: Monte Carlo Financial Risk & Revenue Yield Variance Simulator** (`src/financial_risk/monte_carlo_yield.py`)
  - 50,000-iteration Monte Carlo engine simulating weather volatility, P50/P90 revenue distributions, and Value at Risk (VaR).
- **FEAT-47: Virtual Power Plant (VPP) Aggregation & Portfolio Management** (`src/financial_risk/vpp_aggregator.py`)
  - Aggregates hundreds of distributed C&I solar arrays into a single unified Virtual Power Plant entity for wholesale market bidding.
- **FEAT-48: Power Purchase Agreement (PPA) Automated Settlement & Billing** (`src/financial_risk/ppa_billing.py`)
  - Automates monthly PPA energy billing calculations based on strike prices, delivered energy, and deemed generation credits.
- **FEAT-49: Dynamic OpEx vs CapEx Return-on-Investment (ROI) Calculator** (`src/financial_risk/roi_calculator.py`)
  - Financial analytics engine computing Net Present Value (NPV), IRR, and payback periods for BESS retrofits and inverter upgrades.
- **FEAT-50: Synthetic Weather Derivative Hedging & Insurance Claim Modeling** (`src/financial_risk/weather_hedging.py`)
  - Actuarial pricing engine calculating Solar Volume Hedge (SVH) payouts during unseasonably low-irradiance years.

---

## 💻 Comprehensive Python API Reference

```python
# Import Enterprise Modules
from src.telemetry import EdgeMicroInverterCollector, SubSecondStreamPipeline
from src.gis_weather import SatelliteNowcastingEngine
from src.ml_engine import PhysicsInformedSolarNN, TemporalFusionTransformerForecaster
from src.bess_arbitrage import BESSSoCOptimizer, MarketArbitrageEngine
from src.asset_health import DroneIRAnomalyDetector, InverterRULPrognostics
from src.mlops import EnterpriseFeatureStore, ModelExplainabilityEngine
from src.security import MultiTenantWorkspaceManager, ZeroTrustAPIGateway
from src.esg_compliance import Scope123CarbonCalculator, RenewableEnergyCertificateLedger
from src.financial_risk import MonteCarloYieldRiskSimulator, VPPAggregator

# 1. Telemetry Ingestion
collector = EdgeMicroInverterCollector(plant_id="PLANT-PUNE-01")
metrics = collector.poll_inverter_metrics("INV-001")
print(f"Edge Inverter AC Power: {metrics['ac_power_kw']} kW")

# 2. Physics-Informed AI Prediction
pinn = PhysicsInformedSolarNN()
pinn_output = pinn.predict_pinn_power(ambient_temp_c=32.0, irradiance_w_m2=920.0, wind_speed_mps=3.5)
print(f"PINN Constrained Power: {pinn_output['pinn_bounded_power_kw']} kW")

# 3. Battery Arbitrage Optimization
bess = BESSSoCOptimizer(capacity_kwh=1000.0)
bess_dispatch = bess.optimize_charge_discharge(current_soc_pct=40.0, excess_solar_kw=200.0, grid_price_usd_mwh=175.0)
print(f"BESS Recommended Action: {bess_dispatch['recommended_action']}")

# 4. Financial Risk Monte Carlo Simulation
mc = MonteCarloYieldRiskSimulator(iterations=1000)
risk_profile = mc.run_simulation(baseline_annual_mwh=12000.0)
print(f"Monte Carlo P50 Revenue: ${risk_profile['p50_expected_revenue_usd']:,.2f}")
```

---

## 📁 Repository Structure

```
solar-energy-prediction/
├── .github/
│   └── workflows/
│       ├── ci.yml                # Multi-Python matrix test & lint pipeline
│       ├── security.yml          # Bandit & CodeQL security scanning
│       ├── docker.yml            # Docker build automation
│       └── release.yml           # Automated release tagger
│
├── 50_UPGRADE_FEATURES.md        # Full 50 Enterprise Feature Specification
├── Dockerfile                    # Production Container Blueprint
├── LICENSE                       # MIT License
├── CONTRIBUTING.md               # Guidelines for Contributors
├── CODE_OF_CONDUCT.md            # Community Code of Conduct
├── SECURITY.md                   # Security Disclosure Policy
├── requirements.txt              # Production Dependencies
│
├── docs/
│   └── images/                   # Technical Block Diagrams
│       ├── system_architecture_diagram.png
│       ├── edge_scada_bess_flow.png
│       ├── physics_mlops_pipeline.png
│       ├── asset_health_cv_workflow.png
│       └── vpp_financial_risk_architecture.png
│
├── src/                          # Enterprise Platform Source Code
│   ├── telemetry/                # FEAT 01-05: Modbus, Streaming, Edge AI, SCADA
│   ├── gis_weather/              # FEAT 06-10: Satellite Nowcasting, LiDAR Shading
│   ├── ml_engine/                # FEAT 11-15: PINNs, Transformers, GNN Topology
│   ├── bess_arbitrage/           # FEAT 16-20: BESS SoC, Market Arbitrage, MILP
│   ├── asset_health/             # FEAT 21-25: Drone IR, Inverter RUL, EL Microcrack
│   ├── mlops/                    # FEAT 26-30: Feature Store, SHAP, Shadow Deploy
│   ├── security/                 # FEAT 31-35: Multi-Tenant KMS, OPA RBAC, mTLS
│   ├── esg_compliance/           # FEAT 36-40: Scope 1-3 Carbon, RECs, EU Taxonomy
│   ├── enterprise_api/           # FEAT 41-45: Multi-Region K8s, Ray Batch Compute
│   └── financial_risk/           # FEAT 46-50: Monte Carlo Risk, VPP Aggregator
│
├── app/
│   └── streamlit_app.py          # Interactive Analytics Dashboard
│
└── tests/
    └── test_50_features.py       # Integration Test Suite covering all 50 Features
```

---

## ⚡ Installation & Quick Start

### 1. Clone & Virtual Environment Setup
```bash
git clone https://github.com/SrilakshmiPeddinti/solar-energy-prediction.git
cd solar-energy-prediction

python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Run Comprehensive Integration Test Suite
```bash
powershell -Command "$env:PYTHONPATH='.'; python -m pytest tests/test_50_features.py -v"
```

### 3. Run via Docker
```bash
docker build -t solar-energy-prediction:latest .
docker run -p 8501:8501 solar-energy-prediction:latest
```

---

## ⚙️ CI/CD & Security Automation

The platform features automated GitHub Actions workflows:
- **CI Build & Test Matrix** (`.github/workflows/ci.yml`): Runs unit tests and coverage across Python 3.9, 3.10, 3.11, and 3.12.
- **Security Audit** (`.github/workflows/security.yml`): Bandit static security analysis and GitHub CodeQL vulnerability scans.
- **Container Build** (`.github/workflows/docker.yml`): Automated Docker container build and linting.
- **Automated Release** (`.github/workflows/release.yml`): Generates GitHub release notes on git tag push (`v*.*.*`).

---

## 📄 License & Maintainer

Distributed under the **MIT License**. See [LICENSE](LICENSE) for details.

Developed & Maintained by **Srilakshmi Peddinti** ([pslakshmi1526@gmail.com](mailto:pslakshmi1526@gmail.com)).
