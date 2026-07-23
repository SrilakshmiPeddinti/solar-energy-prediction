"""
FEAT-16: BESS State-of-Charge (SoC) & Degradation-Aware Charging Strategy
Co-optimizes solar generation storage into lithium-ion battery banks while enforcing depth-of-discharge (DoD) limits.
"""
from typing import Dict, Any

class BESSSoCOptimizer:
    def __init__(self, capacity_kwh: float = 1000.0, max_dod_pct: float = 80.0):
        self.capacity_kwh = capacity_kwh
        self.min_soc_pct = 100.0 - max_dod_pct
        self.max_soc_pct = 95.0

    def optimize_charge_discharge(self, current_soc_pct: float, excess_solar_kw: float, grid_price_usd_mwh: float) -> Dict[str, Any]:
        """Calculates optimal charge/discharge action balancing battery degradation costs."""
        action = "HOLD"
        kw_action = 0.0

        if grid_price_usd_mwh > 150.0 and current_soc_pct > self.min_soc_pct:
            action = "DISCHARGE_TO_GRID"
            kw_action = min(500.0, (current_soc_pct - self.min_soc_pct) * (self.capacity_kwh / 100.0))
        elif excess_solar_kw > 50.0 and current_soc_pct < self.max_soc_pct:
            action = "CHARGE_FROM_SOLAR"
            kw_action = min(excess_solar_kw, (self.max_soc_pct - current_soc_pct) * (self.capacity_kwh / 100.0))

        return {
            "capacity_kwh": self.capacity_kwh,
            "current_soc_pct": current_soc_pct,
            "grid_price_usd_mwh": grid_price_usd_mwh,
            "recommended_action": action,
            "power_kw": round(kw_action, 2),
            "degradation_cost_usd": round(kw_action * 0.015, 2)
        }
