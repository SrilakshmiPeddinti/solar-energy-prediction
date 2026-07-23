"""
FEAT-47: Virtual Power Plant (VPP) Aggregation & Multi-Site Portfolio Management
Aggregates distributed rooftop solar and C&I assets into a single unified VPP market dispatch entity.
"""
from typing import Dict, Any, List

class VPPAggregator:
    def __init__(self, vpp_id: str = "VPP-WEST-COAST-01"):
        self.vpp_id = vpp_id

    def aggregate_portfolio(self, site_capacities_kw: List[float]) -> Dict[str, Any]:
        """Aggregates site capacities and calculates virtual power plant total dispatch power."""
        total_nameplate_kw = sum(site_capacities_kw)
        available_dispatch_kw = total_nameplate_kw * 0.85  # 85% availability factor

        return {
            "vpp_id": self.vpp_id,
            "connected_sites_count": len(site_capacities_kw),
            "total_nameplate_capacity_kw": round(total_nameplate_kw, 2),
            "available_dispatch_power_kw": round(available_dispatch_kw, 2),
            "vpp_market_status": "READY_FOR_GRID_BID"
        }
