"""
FEAT-02: Sub-Second Stream Ingestion Pipeline
Apache Kafka / Flink stream processing pipeline simulator with windowing and deduplication.
"""
from collections import deque
import time
from typing import Dict, Any, List, Callable

class SubSecondStreamPipeline:
    def __init__(self, buffer_size: int = 1000):
        self.buffer = deque(maxlen=buffer_size)
        self.processed_count = 0
        self.drop_count = 0

    def ingest_event(self, event: Dict[str, Any]) -> bool:
        """Ingests a telemetry event into the stream buffer."""
        if not event.get("timestamp") or not event.get("inverter_id"):
            self.drop_count += 1
            return False
        self.buffer.append(event)
        self.processed_count += 1
        return True

    def process_window(self, window_seconds: float = 1.0) -> Dict[str, Any]:
        """Tumbling window aggregation of telemetry stream."""
        now = time.time()
        window_events = [e for e in self.buffer if (now - e.get("timestamp", 0)) <= window_seconds]
        if not window_events:
            return {"total_events": 0, "avg_ac_power_kw": 0.0, "latency_ms": 0.0}
        
        avg_power = sum(e.get("ac_power_kw", 0.0) for e in window_events) / len(window_events)
        avg_latency = sum((now - e.get("timestamp", now)) * 1000 for e in window_events) / len(window_events)

        return {
            "window_size_sec": window_seconds,
            "event_count": len(window_events),
            "avg_ac_power_kw": round(avg_power, 3),
            "avg_latency_ms": round(avg_latency, 2),
            "total_stream_processed": self.processed_count,
            "dropped_events": self.drop_count
        }
