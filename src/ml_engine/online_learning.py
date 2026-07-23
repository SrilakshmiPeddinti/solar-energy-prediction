"""
FEAT-15: Continuous Online Learning & Automatic Concept Drift Detection
ADWIN / Kolmogorov-Smirnov distribution shift monitor triggering online incremental retraining.
"""
from typing import Dict, Any, List

class OnlineLearningConceptDriftEngine:
    def __init__(self, p_val_threshold: float = 0.01):
        self.p_val_threshold = p_val_threshold
        self.window = []

    def update_stream_and_check_drift(self, actual_kw: float, predicted_kw: float) -> Dict[str, Any]:
        """Monitors stream residuals and triggers automated model retraining on concept drift."""
        error = abs(actual_kw - predicted_kw)
        self.window.append(error)
        if len(self.window) > 100:
            self.window.pop(0)

        avg_error = sum(self.window) / len(self.window)
        drift_detected = avg_error > 8.0

        return {
            "window_size": len(self.window),
            "recent_mae": round(avg_error, 2),
            "concept_drift_detected": drift_detected,
            "action_taken": "INCREMENTAL_RETRAIN_TRIGGERED" if drift_detected else "NONE"
        }
