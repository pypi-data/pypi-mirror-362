from enum import Enum


class TelemetryFieldType1ItemType0(str, Enum):
    LOOKUP = "lookup"

    def __str__(self) -> str:
        return str(self.value)
