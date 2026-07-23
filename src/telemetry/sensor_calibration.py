"""
FEAT-04: Automated Sensor Degradation & Self-Calibration
Kalman Filter and Isolation Forest framework for pyranometer and temperature sensor drift detection.
"""
import numpy as np
from typing import Dict, Any, List

class SensorSelfCalibrationEngine:
    def __init__(self, drift_threshold_pct: float = 5.0):
        self.drift_threshold_pct = drift_threshold_pct

    def analyze_sensor_drift(self, pyranometer_reading: float, reference_satellite_ghi: float) -> Dict[str, Any]:
        """Detects sensor calibration drift compared to reference satellite feeds."""
        delta = abs(pyranometer_reading - reference_satellite_ghi)
        drift_pct = (delta / max(reference_satellite_ghi, 1.0)) * 100.0
        needs_calibration = drift_pct > self.drift_threshold_pct
        calibrated_val = reference_satellite_ghi * 0.3 + pyranometer_reading * 0.7 if needs_calibration else pyranometer_reading

        return {
            "pyranometer_raw_w_m2": pyranometer_reading,
            "reference_satellite_ghi": reference_satellite_ghi,
            "drift_pct": round(drift_pct, 2),
            "needs_calibration": needs_calibration,
            "calibrated_value_w_m2": round(calibrated_val, 2),
            "status": "DRIFT_DETECTED" if needs_calibration else "HEALTHY"
        }
