from enum import Enum


class CreateApiKeyRequestScopeItem(str, Enum):
    ADMINISTER = "ADMINISTER"
    PREDICT = "PREDICT"

    def __str__(self) -> str:
        return str(self.value)
