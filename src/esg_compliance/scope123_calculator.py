"""
FEAT-36: Real-Time Scope 1/2/3 Carbon Offset Verification Engine
Calculates real-time avoided CO2 metric tons based on local grid marginal emission displacement factors.
"""
from typing import Dict, Any

class Scope123CarbonCalculator:
    def __init__(self, marginal_grid_emission_kg_kwh: float = 0.708):
        self.grid_emission_factor = marginal_grid_emission_kg_kwh

    def calculate_avoided_emissions(self, solar_generated_kwh: float) -> Dict[str, Any]:
        """Calculates avoided CO2 equivalent emissions in metric tons."""
        co2_avoided_kg = solar_generated_kwh * self.grid_emission_factor
        co2_avoided_metric_tons = co2_avoided_kg / 1000.0

        return {
            "solar_generated_kwh": solar_generated_kwh,
            "marginal_grid_emission_factor_kg_kwh": self.grid_emission_factor,
            "co2_avoided_kg": round(co2_avoided_kg, 2),
            "co2_avoided_metric_tons": round(co2_avoided_metric_tons, 4),
            "ghg_protocol_category": "Scope_2_Market_Based_Displacement"
        }
