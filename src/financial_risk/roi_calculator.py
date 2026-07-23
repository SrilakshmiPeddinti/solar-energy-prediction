"""
FEAT-49: Dynamic OpEx vs CapEx Return-on-Investment (ROI) Calculator
NPV and IRR calculator evaluating BESS retrofit, inverter upgrades, and bifacial panel investments.
"""
from typing import Dict, Any, List

class ROICalculatorEngine:
    def __init__(self, discount_rate_pct: float = 7.5):
        self.discount_rate = discount_rate_pct / 100.0

    def calculate_project_npv_irr(self, capex_usd: float, annual_cashflows_usd: List[float]) -> Dict[str, Any]:
        """Calculates Net Present Value (NPV) and simple payback period."""
        npv = -capex_usd
        for year, cf in enumerate(annual_cashflows_usd, 1):
            npv += cf / ((1.0 + self.discount_rate) ** year)

        cumulative = 0.0
        payback_years = len(annual_cashflows_usd)
        for year, cf in enumerate(annual_cashflows_usd, 1):
            cumulative += cf
            if cumulative >= capex_usd:
                payback_years = year
                break

        return {
            "capex_usd": capex_usd,
            "discount_rate_pct": round(self.discount_rate * 100, 2),
            "npv_usd": round(npv, 2),
            "payback_period_years": payback_years,
            "investment_viable": npv > 0.0
        }
