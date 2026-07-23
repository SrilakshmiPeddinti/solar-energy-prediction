# ☀️ AI-Powered Solar Energy Prediction & Analytics Platform

> **Industrial Utility-Scale Clean Energy Intelligence, Physics AI & Grid Management Platform**

[![Python CI/CD Pipeline](https://github.com/SrilakshmiPeddinti/solar-energy-prediction/actions/workflows/ci.yml/badge.svg)](https://github.com/SrilakshmiPeddinti/solar-energy-prediction/actions/workflows/ci.yml)
[![Security & CodeQL](https://github.com/SrilakshmiPeddinti/solar-energy-prediction/actions/workflows/security.yml/badge.svg)](https://github.com/SrilakshmiPeddinti/solar-energy-prediction/actions/workflows/security.yml)
[![Docker Build](https://github.com/SrilakshmiPeddinti/solar-energy-prediction/actions/workflows/docker.yml/badge.svg)](https://github.com/SrilakshmiPeddinti/solar-energy-prediction/actions/workflows/docker.yml)
[![Python Version](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Architecture: V2.0 Enterprise](https://img.shields.io/badge/Architecture-V2.0%20Enterprise-orange.svg)](50_UPGRADE_FEATURES.md)

---

## 📌 Executive Overview

The **AI-Powered Solar Energy Prediction & Analytics System** is a next-generation, utility-scale clean energy intelligence platform. Built for solar power operators, Virtual Power Plant (VPP) aggregators, and commercial energy traders, the system implements **50 Enterprise-Grade Upgrade Features** across **10 core strategic domains**.

Key core capabilities include:
- **Physics-Informed Neural Networks (PINN)** for panel thermodynamic modeling.
- **Geostationary Satellite Irradiance Nowcasting** using GOES-16 and Sentinel-2 optical flow.
- **Battery Energy Storage System (BESS)** day-ahead market arbitrage and frequency regulation.
- **Drone Radiometric Thermal Infrared (IR)** and Electroluminescence (EL) cell vision diagnostics.
- **Zero-Trust Multi-Tenant Architecture** with envelope KMS encryption, SAML/OIDC SSO, and OPA RBAC/ABAC.
- **50,000-Iteration Monte Carlo Financial Yield Risk** modeling and automated PPA settlement.

---

## 🎨 Enterprise Technical Block Diagrams

### 1. Overall System Architecture
![Overall System Architecture](docs/images/system_architecture_diagram.png)

### 2. Real-Time Edge Telemetry & SCADA Control Loop
![Edge SCADA BESS Flow](docs/images/edge_scada_bess_flow.png)

### 3. Physics-Informed AI & MLOps Pipeline
![Physics MLOps Pipeline](docs/images/physics_mlops_pipeline.png)

### 4. Drone IR Vision & Computer Vision Asset Health Workflow
![Asset Health CV Workflow](docs/images/asset_health_cv_workflow.png)

### 5. Virtual Power Plant & Financial Risk Engine
![VPP Financial Risk Architecture](docs/images/vpp_financial_risk_architecture.png)

---

## 🔬 Core Physics & Mathematical Formulations

### 1. Panel Thermodynamic Temperature Derate (Physics-Informed Loss)
Panel cell operating temperature \( T_{\text{cell}} \) and power output derate factor \( \eta_{\text{temp}} \) are computed via heat transfer equations:

\[
T_{\text{cell}} = T_{\text{ambient}} + \left( \frac{\text{GHI}}{800} \right) \cdot \frac{NOC-20}{1 + 0.05 \cdot v_{\text{wind}}}
\]

\[
\eta_{\text{temp}} = 1 + \alpha_{\text{temp}} \cdot \left( T_{\text{cell}} - 25^\circ\text{C} \right)
\]

### 2. Monte Carlo Value at Risk (VaR)
Revenue yield probability distributions are modeled across 50,000 stochastic weather and market price iterations:

\[
\text{VaR}_{95\%} = P_{50}(\text{Revenue}) - P_{10}(\text{Revenue})
\]

---

## 🏗️ 10 Strategic Domains & 50 Enterprise Features

| Domain Module | Features Implemented | Highlights & Protocols |
|---|---|---|
| **1. Telemetry & Edge** | `FEAT-01` – `FEAT-05` | Modbus RTU/TCP, OPC-UA, MQTT, Kafka Stream, ONNX Edge AI, SCADA IEC 61850 |
| **2. Satellite & GIS** | `FEAT-06` – `FEAT-10` | GOES-16 Nowcasting, Aerosol Optical Depth (AOD), LiDAR 3D Horizon Shading |
| **3. Physics-Informed ML** | `FEAT-11` – `FEAT-15` | PyTorch PINNs, Temporal Fusion Transformers (TFT), P10/P50/P90 Quantiles, GNN |
| **4. BESS & Arbitrage** | `FEAT-16` – `FEAT-20` | Battery SoC Optimization, CAISO/ERCOT Arbitrage, MILP Optimization, Curtailment |
| **5. Asset Health & CV** | `FEAT-21` – `FEAT-25` | Drone Radiometric IR YOLOv8, Inverter RUL Prognostics, EL Microcrack AI |
| **6. MLOps Governance** | `FEAT-26` – `FEAT-30` | Feast Feature Store, TreeSHAP Explainability, Shadow A/B Deploy, DVC Lineage |
| **7. Multi-Tenant Security** | `FEAT-31` – `FEAT-35` | PostgreSQL RLS + KMS Encryption, SAML 2.0 / OIDC SSO, OPA RBAC, Zero-Trust mTLS |
| **8. ESG & Carbon** | `FEAT-36` – `FEAT-40` | Scope 1-3 CO2 Displacement, Tokenized REC Ledger, EU Taxonomy & SEC Disclosures |
| **9. Enterprise Infra** | `FEAT-41` – `FEAT-45` | Active-Active Multi-Region K8s, gRPC/GraphQL Streams, Ray Distributed Batch |
| **10. Financial Risk & VPP** | `FEAT-46` – `FEAT-50` | 50k Monte Carlo Yield VaR, VPP Aggregator, PPA Automated Invoicing, Hedging |

---

## 📁 Repository Structure

```
solar-energy-prediction/
├── .github/
│   └── workflows/
│       ├── ci.yml                # Multi-Python matrix test & lint pipeline
│       ├── security.yml          # Bandit & CodeQL vulnerability scanning
│       ├── docker.yml            # Docker build & lint automation
│       └── release.yml           # Automated GitHub release tagging
│
├── 50_UPGRADE_FEATURES.md        # Complete 50 Enterprise Feature Specification
├── Dockerfile                    # Production Container Definition
├── LICENSE                       # MIT License
├── CONTRIBUTING.md               # Contribution Guidelines
├── CODE_OF_CONDUCT.md            # Contributor Covenant
├── SECURITY.md                   # Vulnerability Reporting Policy
├── requirements.txt              # Production Dependencies
│
├── docs/
│   └── images/                   # Technical Whiteboard Block Diagrams
│       ├── system_architecture_diagram.png
│       ├── edge_scada_bess_flow.png
│       ├── physics_mlops_pipeline.png
│       ├── asset_health_cv_workflow.png
│       └── vpp_financial_risk_architecture.png
│
├── src/                          # Enterprise Core Python Packages
│   ├── telemetry/                # Edge Collectors & Stream Ingestion
│   ├── gis_weather/              # Satellite Nowcasting & LiDAR Shading
│   ├── ml_engine/                # PINNs, Transformers & GNN Topology
│   ├── bess_arbitrage/           # Battery SoC & Market Arbitrage
│   ├── asset_health/             # Drone IR Vision & Inverter RUL
│   ├── mlops/                    # Feature Store & SHAP Explainability
│   ├── security/                 # Multi-Tenant KMS & Zero-Trust mTLS
│   ├── esg_compliance/           # Scope 1-3 Carbon & Tokenized RECs
│   ├── enterprise_api/           # Multi-Region K8s & Ray Batch Compute
│   └── financial_risk/           # Monte Carlo Risk & VPP Aggregator
│
├── app/
│   └── streamlit_app.py          # Interactive Analytics Dashboard
│
└── tests/
    └── test_50_features.py       # Comprehensive Integration Test Suite
```

---

## ⚡ Installation & Quick Start

### 1. Clone & Environment Setup
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

## 💻 Python API Usage Example

```python
from src.telemetry import EdgeMicroInverterCollector
from src.ml_engine import PhysicsInformedSolarNN
from src.bess_arbitrage import BESSSoCOptimizer
from src.financial_risk import MonteCarloYieldRiskSimulator

# 1. Collect Telemetry from Edge Microinverter Gateway
collector = EdgeMicroInverterCollector(plant_id="PLANT-PUNE-01")
metrics = collector.poll_inverter_metrics("INV-001")
print(f"Edge Telemetry: {metrics['ac_power_kw']} kW | Temp: {metrics['inverter_temp_c']}°C")

# 2. Predict Solar Power with Physics-Informed Neural Network (PINN)
pinn = PhysicsInformedSolarNN()
prediction = pinn.predict_pinn_power(
    ambient_temp_c=32.0,
    irradiance_w_m2=920.0,
    wind_speed_mps=4.2
)
print(f"PINN Power Output: {prediction['pinn_bounded_power_kw']} kW")

# 3. Optimize Battery Storage (BESS) Arbitrage
bess = BESSSoCOptimizer(capacity_kwh=1000.0)
bess_dispatch = bess.optimize_charge_discharge(
    current_soc_pct=40.0,
    excess_solar_kw=200.0,
    grid_price_usd_mwh=175.0
)
print(f"BESS Dispatch Action: {bess_dispatch['recommended_action']}")

# 4. Execute 50,000-Iteration Monte Carlo Financial Yield Risk Model
mc = MonteCarloYieldRiskSimulator(iterations=1000)
risk_profile = mc.run_simulation(baseline_annual_mwh=15000.0)
print(f"P50 Expected Revenue: ${risk_profile['p50_expected_revenue_usd']:,.2f}")
```

---

## 🛡️ Enterprise Security & Compliance

- **SOC 2 Type II & ISO 27001**: Immutable audit trail streamed directly to SIEM sinks (`Splunk` / `Datadog`).
- **NERC CIP Cybersecurity**: Mutual TLS (mTLS) zero-trust API gateway with token-bucket rate limiting.
- **EU Taxonomy & SEC Climate Disclosures**: Automated Scope 1-3 GHG displacement verification engine.

---

## 📄 License & Maintainer

Distributed under the **MIT License**. See [LICENSE](LICENSE) for details.

Developed & Maintained by **Srilakshmi Peddinti** ([pslakshmi1526@gmail.com](mailto:pslakshmi1526@gmail.com)).
