from enum import Enum


class TelemetryFieldType1ItemType1(str, Enum):
    COUNT = "count"

    def __str__(self) -> str:
        return str(self.value)
