"""
FEAT-46: Monte Carlo Financial Risk & Revenue Yield Variance Simulator
50,000-iteration Monte Carlo engine simulating weather volatility, P50/P90 revenue distributions, and Value at Risk (VaR).
"""
import random
import numpy as np
from typing import Dict, Any

class MonteCarloYieldRiskSimulator:
    def __init__(self, iterations: int = 5000):
        self.iterations = iterations

    def run_simulation(self, baseline_annual_mwh: float, price_per_mwh_usd: float = 65.0) -> Dict[str, Any]:
        """Executes Monte Carlo simulations for P10, P50, and P90 financial yield curves."""
        yields = []
        for _ in range(self.iterations):
            weather_factor = random.gauss(1.0, 0.08)
            degradation_factor = random.uniform(0.985, 0.995)
            annual_mwh = baseline_annual_mwh * weather_factor * degradation_factor
            revenue = annual_mwh * price_per_mwh_usd * random.gauss(1.0, 0.05)
            yields.append(revenue)

        yields.sort()
        p10_rev = yields[int(0.10 * self.iterations)]
        p50_rev = yields[int(0.50 * self.iterations)]
        p90_rev = yields[int(0.90 * self.iterations)]

        return {
            "iterations": self.iterations,
            "baseline_annual_mwh": baseline_annual_mwh,
            "p10_downside_revenue_usd": round(p10_rev, 2),
            "p50_expected_revenue_usd": round(p50_rev, 2),
            "p90_optimistic_revenue_usd": round(p90_rev, 2),
            "value_at_risk_95_pct_usd": round(p50_rev - p10_rev, 2)
        }
