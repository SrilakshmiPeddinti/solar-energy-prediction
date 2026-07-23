"""
FEAT-20: Interconnection Capacity Limit & Curtailment Risk Optimizer
Predicts sub-station congestion bottlenecks and diverts excess generation into local storage sinks.
"""
from typing import Dict, Any

class CurtailmentRiskOptimizer:
    def __init__(self, substation_cap_kw: float = 5000.0):
        self.substation_cap_kw = substation_cap_kw

    def evaluate_curtailment_risk(self, total_site_gen_kw: float) -> Dict[str, Any]:
        """Predicts curtailment risk and calculates optimal diversion."""
        overage_kw = max(0.0, total_site_gen_kw - self.substation_cap_kw)
        curtailment_risk_pct = min(100.0, (overage_kw / self.substation_cap_kw) * 100.0)

        return {
            "substation_capacity_kw": self.substation_cap_kw,
            "site_generation_kw": total_site_gen_kw,
            "overage_kw": round(overage_kw, 2),
            "curtailment_risk_pct": round(curtailment_risk_pct, 2),
            "action_required": "DIVERT_TO_THERMAL_OR_BATTERY_SINK" if overage_kw > 0 else "NO_CURTAILMENT_NEEDED"
        }
