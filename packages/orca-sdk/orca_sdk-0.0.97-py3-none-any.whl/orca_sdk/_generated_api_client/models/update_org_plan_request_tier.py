from enum import Enum


class UpdateOrgPlanRequestTier(str, Enum):
    CANCELLED = "CANCELLED"
    ENTERPRISE = "ENTERPRISE"
    FREE = "FREE"
    PRO = "PRO"

    def __str__(self) -> str:
        return str(self.value)
