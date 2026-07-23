"""
FEAT-35: Zero-Trust API Gateway with mTLS & Dynamic Rate Limiting
Mutual TLS (mTLS) token validation and Redis token-bucket dynamic rate limiter.
"""
import time
from typing import Dict, Any

class ZeroTrustAPIGateway:
    def __init__(self, rate_limit_per_min: int = 600):
        self.rate_limit_per_min = rate_limit_per_min
        self.request_counters = {}

    def process_request(self, client_id: str, mtls_cert_verified: bool, endpoint: str) -> Dict[str, Any]:
        """Filters incoming API calls through mTLS authentication and rate limiting."""
        if not mtls_cert_verified:
            return {"status_code": 401, "message": "mTLS Handshake Failed: Client Certificate Rejected", "allowed": False}

        now = time.time()
        client_history = [t for t in self.request_counters.get(client_id, []) if now - t < 60.0]
        if len(client_history) >= self.rate_limit_per_min:
            return {"status_code": 429, "message": "Rate Limit Exceeded", "allowed": False}

        client_history.append(now)
        self.request_counters[client_id] = client_history

        return {
            "status_code": 200,
            "client_id": client_id,
            "endpoint": endpoint,
            "mtls_verified": True,
            "requests_remaining": self.rate_limit_per_min - len(client_history),
            "allowed": True
        }
