from enum import Enum


class CreateOrgPlanRequestTier(str, Enum):
    CANCELLED = "CANCELLED"
    ENTERPRISE = "ENTERPRISE"
    FREE = "FREE"
    PRO = "PRO"

    def __str__(self) -> str:
        return str(self.value)
