"""
FEAT-23: Automated Panel Soiling Dynamics & Dynamic Washing Scheduler
Cost-benefit dynamic programming optimizer balancing panel cleaning crew costs vs recovered power.
"""
from typing import Dict, Any

class PanelWashingScheduler:
    def __init__(self, cleaning_cost_per_mw_usd: float = 350.0):
        self.cleaning_cost = cleaning_cost_per_mw_usd

    def optimize_cleaning_schedule(self, plant_capacity_mw: float, current_soiling_loss_pct: float, electricity_tariff_usd_kwh: float) -> Dict[str, Any]:
        """Determines if panel cleaning dispatch is economically viable."""
        daily_lost_kwh = plant_capacity_mw * 1000.0 * 5.5 * (current_soiling_loss_pct / 100.0)
        daily_lost_revenue_usd = daily_lost_kwh * electricity_tariff_usd_kwh

        cleaning_cost_total = plant_capacity_mw * self.cleaning_cost
        payback_days = cleaning_cost_total / max(daily_lost_revenue_usd, 0.01)
        dispatch_recommended = payback_days <= 14.0

        return {
            "plant_capacity_mw": plant_capacity_mw,
            "soiling_loss_pct": current_soiling_loss_pct,
            "daily_lost_revenue_usd": round(daily_lost_revenue_usd, 2),
            "total_cleaning_cost_usd": round(cleaning_cost_total, 2),
            "payback_period_days": round(payback_days, 1),
            "dispatch_washing_crew": dispatch_recommended
        }
