"""
FEAT-25: Single/Dual-Axis Tracker Mechanical Actuator Diagnostics
Monitors motor current draw and angle encoder feedback on single/dual axis solar trackers.
"""
from typing import Dict, Any

class TrackerActuatorDiagnostics:
    def __init__(self, max_motor_current_a: float = 12.0):
        self.max_motor_current_a = max_motor_current_a

    def diagnose_tracker(self, tracker_id: str, target_angle_deg: float, actual_angle_deg: float, motor_current_a: float) -> Dict[str, Any]:
        """Diagnoses tracker motor binding or mechanical alignment failure."""
        angle_error = abs(target_angle_deg - actual_angle_deg)
        binding_fault = motor_current_a > self.max_motor_current_a
        alignment_fault = angle_error > 3.0

        status = "HEALTHY"
        if binding_fault:
            status = "MECHANICAL_BINDING_CURRENT_OVERLOAD"
        elif alignment_fault:
            status = "POSITION_ENCODER_MISALIGNMENT"

        return {
            "tracker_id": tracker_id,
            "target_angle_deg": target_angle_deg,
            "actual_angle_deg": actual_angle_deg,
            "angle_error_deg": round(angle_error, 2),
            "motor_current_a": motor_current_a,
            "status": status,
            "maintenance_required": binding_fault or alignment_fault
        }
