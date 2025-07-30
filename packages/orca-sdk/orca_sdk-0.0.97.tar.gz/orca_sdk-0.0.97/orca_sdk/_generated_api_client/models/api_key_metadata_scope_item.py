from enum import Enum


class ApiKeyMetadataScopeItem(str, Enum):
    ADMINISTER = "ADMINISTER"
    PREDICT = "PREDICT"

    def __str__(self) -> str:
        return str(self.value)
