"""
FEAT-33: Granular Role-Based (RBAC) & Attribute-Based Access Control (ABAC)
Policy decision point (PDP) evaluating user role, resource region, and action authorization.
"""
from typing import Dict, Any, List

class AccessControlPolicyEngine:
    def __init__(self):
        self.rules = {
            "Admin": ["READ", "WRITE", "EXECUTE_DISPATCH", "ADMIN"],
            "Operator": ["READ", "EXECUTE_DISPATCH"],
            "Analyst": ["READ"]
        }

    def evaluate_access(self, user_role: str, action: str, resource_region: str, user_region: str) -> Dict[str, Any]:
        """Evaluates RBAC permissions and ABAC regional attribute constraints."""
        role_allowed = action in self.rules.get(user_role, [])
        region_allowed = (user_region == "GLOBAL") or (user_region == resource_region)
        authorized = role_allowed and region_allowed

        return {
            "authorized": authorized,
            "user_role": user_role,
            "action": action,
            "resource_region": resource_region,
            "policy_decision": "PERMIT" if authorized else "DENY",
            "reason": "Sufficient role and regional attribute match" if authorized else "Unauthorized action or regional mismatch"
        }
