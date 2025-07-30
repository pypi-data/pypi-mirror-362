from enum import Enum


class CreateApiKeyResponseScopeItem(str, Enum):
    ADMINISTER = "ADMINISTER"
    PREDICT = "PREDICT"

    def __str__(self) -> str:
        return str(self.value)
