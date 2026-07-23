"""
FEAT-07: Microclimate Aerosol Optical Depth & Dust Soiling Simulator
Integrates CAMS / MODIS atmospheric aerosol optical depth and dust soiling deposition rates.
"""
from typing import Dict, Any

class AerosolSoilingSimulator:
    def __init__(self, baseline_aod: float = 0.15):
        self.baseline_aod = baseline_aod

    def calculate_soiling_derate(self, days_since_wash: int, aod_index: float = 0.25) -> Dict[str, Any]:
        """Estimates efficiency loss due to atmospheric aerosols and panel dust accumulation."""
        daily_soiling_rate_pct = 0.18 + (aod_index * 0.12)
        total_soiling_loss_pct = min(25.0, daily_soiling_rate_pct * days_since_wash)
        efficiency_factor = round(1.0 - (total_soiling_loss_pct / 100.0), 4)

        return {
            "days_since_wash": days_since_wash,
            "aod_index": aod_index,
            "daily_soiling_rate_pct": round(daily_soiling_rate_pct, 3),
            "accumulated_soiling_loss_pct": round(total_soiling_loss_pct, 2),
            "derate_efficiency_factor": efficiency_factor
        }
