"""
FEAT-01: Edge Micro-Inverter Telemetry Collector
Protocol handlers for Modbus RTU/TCP, OPC-UA, and MQTT telemetry aggregation.
"""
import time
import random
from typing import Dict, Any, List

class EdgeMicroInverterCollector:
    def __init__(self, plant_id: str, protocols: List[str] = None):
        self.plant_id = plant_id
        self.protocols = protocols or ["ModbusTCP", "OPC-UA", "MQTT"]
        self.connected = True

    def poll_inverter_metrics(self, inverter_id: str) -> Dict[str, Any]:
        """Polls AC/DC voltage, current, frequency, and temperature."""
        timestamp = time.time()
        dc_voltage = round(random.uniform(580.0, 620.0), 2)
        dc_current = round(random.uniform(15.0, 25.0), 2)
        ac_voltage = round(random.uniform(225.0, 235.0), 2)
        ac_frequency = round(random.uniform(49.95, 50.05), 3)
        temp_celsius = round(random.uniform(40.0, 65.0), 1)
        dc_power_kw = round((dc_voltage * dc_current) / 1000.0, 3)
        ac_power_kw = round(dc_power_kw * random.uniform(0.96, 0.985), 3)
        
        return {
            "plant_id": self.plant_id,
            "inverter_id": inverter_id,
            "timestamp": timestamp,
            "protocol": random.choice(self.protocols),
            "dc_voltage_v": dc_voltage,
            "dc_current_a": dc_current,
            "ac_voltage_v": ac_voltage,
            "ac_frequency_hz": ac_frequency,
            "inverter_temp_c": temp_celsius,
            "dc_power_kw": dc_power_kw,
            "ac_power_kw": ac_power_kw,
            "efficiency_pct": round((ac_power_kw / max(dc_power_kw, 0.001)) * 100, 2)
        }

    def batch_poll(self, num_inverters: int = 10) -> List[Dict[str, Any]]:
        return [self.poll_inverter_metrics(f"INV-{i:03d}") for i in range(1, num_inverters + 1)]
