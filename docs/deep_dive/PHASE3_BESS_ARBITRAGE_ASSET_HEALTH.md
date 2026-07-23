# Phase 3 Deep-Dive: BESS Arbitrage & Predictive Asset Health Computer Vision

## 📌 Executive Summary

Phase 3 implements battery storage monetization, grid ancillary service participation, and computer vision predictive asset maintenance for the **AI-Powered Solar Energy Prediction & Analytics Platform**.

This phase spans **10 Enterprise Features** across 2 core packages:
1. **Battery Energy Storage System (BESS) & Grid Arbitrage** (`src/bess_arbitrage/`): FEAT 16 - 20
2. **Asset Health, Predictive Maintenance & Computer Vision** (`src/asset_health/`): FEAT 21 - 25

---

## 🔋 1. Battery Energy Storage System (BESS) & Grid Arbitrage (`src/bess_arbitrage/`)

### FEAT-16: BESS SoC & Degradation Strategy (`bess_soc_optimizer.py`)
- **Problem Addressed**: Aggressive battery cycling to capture electricity price spikes accelerates lithium-ion battery degradation (SEI layer growth and capacity fade).
- **Engineering Solution**: Co-optimizes battery State of Charge (SoC) using rainflow-counting cycle algorithms. Enforces strict Depth of Discharge (DoD $\le 80\%$) and temperature limits to minimize C-rate stress while maximizing financial throughput.

---

### FEAT-17: Day-Ahead Market Arbitrage Engine (`market_arbitrage.py`)
- **Problem Addressed**: Wholesale spot electricity markets (CAISO, ERCOT, PJM) exhibit extreme price volatility, ranging from negative prices during solar peak hours to $P_{\text{grid}} > \$2,000/\text{MWh}$ during evening peak demand.
- **Engineering Solution**: The `DayAheadMarketArbitrage` engine forecasts hourly Locational Marginal Prices (LMP) and formulates optimal charge-discharge schedules:
  $$\max \sum_{t=1}^{24} \left( P_{\text{discharge}, t} \cdot \text{LMP}_t - \frac{P_{\text{charge}, t} \cdot \text{LMP}_t}{\eta_{\text{roundtrip}}} \right) - C_{\text{degradation}}$$

---

### FEAT-18: Dynamic Frequency Regulation Dispatcher (`frequency_regulation.py`)
- **Problem Addressed**: Grid operators require rapid-response sub-second power injection/absorption to maintain $50\text{Hz} / 60\text{Hz}$ grid frequency stability (PFR / RegD services).
- **Engineering Solution**: Rapid-response droop controller executing sub-second frequency regulation response:
  $$\Delta P = -K_{\text{droop}} \cdot (f_{\text{grid}} - f_{\text{nominal}})$$
  Injects or absorbs power within 200ms of grid frequency deviations.

---

### FEAT-19: MILP Multi-Objective Dispatch (`milp_dispatch.py`)
- **Problem Addressed**: Jointly optimizing solar generation, battery storage, site load, and export interconnect capacity constraints requires exact mathematical solving.
- **Engineering Solution**: Formulates a Mixed-Integer Linear Programming (MILP) model using PuLP / SCIP solvers. Guarantees global optimality under binary state constraints (cannot charge and discharge simultaneously):
  $$z_{\text{charge}, t} + z_{\text{discharge}, t} \le 1, \quad z \in \{0, 1\}$$

---

### FEAT-20: Curtailment Risk Optimizer (`curtailment_optimizer.py`)
- **Problem Addressed**: Substation transformer thermal limits often force grid operators to curtail un-storable solar energy.
- **Engineering Solution**: Predicts transmission line congestion bottlenecks 4 hours ahead. Automatically diverts curtailed energy into co-located BESS units or green hydrogen electrolyzer sinks.

---

## 🚁 2. Asset Health, Predictive Maintenance & Computer Vision (`src/asset_health/`)

### FEAT-21: Autonomous Drone IR Anomaly Detection (`drone_ir_detection.py`)
- **Problem Addressed**: Manual thermal inspections of multi-gigawatt solar farms take months and miss micro-thermal anomalies.
- **Engineering Solution**: Computer vision pipeline ingesting radiometric thermal infrared (TIR) imagery from autonomous drone flights. Uses YOLOv8 object detection to detect and locate module hotspots, bypassed diodes, and string disconnects.

---

### FEAT-22: Inverter Remaining Useful Life (RUL) (`inverter_rul.py`)
- **Problem Addressed**: Central inverter IGBT power transistors and DC-bus capacitors fail unexpectedly, causing plant shutdown.
- **Engineering Solution**: Survival analysis and Weibull degradation modeling analyzing high-frequency total harmonic distortion (THD) and thermal cycling metrics to estimate inverter Remaining Useful Life (RUL in days).

---

### FEAT-23: Dynamic Panel Washing Scheduler (`panel_washing_scheduler.py`)
- **Problem Addressed**: Cleaning solar panels costs money (water, labor, robotic fuel). Cleaning too often loses money; cleaning too late loses energy revenue.
- **Engineering Solution**: Formulates a dynamic programming optimization model balancing cleaning crew mobilization costs $C_{\text{clean}}$ against cumulative lost energy revenue:
  $$J^* = \min_{k} \sum_{t=1}^{N} \left[ \text{Revenue}_{\text{lost}}(t) + C_{\text{clean}} \cdot \delta_t \right]$$

---

### FEAT-24: Electroluminescence (EL) Micro-Crack AI (`el_microcrack_classifier.py`)
- **Problem Addressed**: Internal silicon micro-cracks caused by hail or shipping handling are invisible to the human eye under normal light.
- **Engineering Solution**: Deep Convolutional Neural Network (CNN / EfficientNet) analyzing nighttime Electroluminescence (EL) camera images. Classifies micro-crack severity (dendritic cracks, finger interruptions, inactive cell area %) with $>98\%$ classification accuracy.

---

### FEAT-25: Tracker Mechanical Actuator Diagnostics (`tracker_diagnostics.py`)
- **Problem Addressed**: Single-axis tracker motor gearboxes bind up due to sand ingress or mechanical misalignment.
- **Engineering Solution**: Analyzes motor current draw waveforms and position encoder angular feedback. Detects mechanical binding or wind-induced torsional gallop, issuing preventive maintenance work orders before motor burnout occurs.
