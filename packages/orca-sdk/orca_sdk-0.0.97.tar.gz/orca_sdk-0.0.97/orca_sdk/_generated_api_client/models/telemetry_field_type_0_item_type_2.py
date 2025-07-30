from enum import Enum


class TelemetryFieldType0ItemType2(str, Enum):
    AVG = "avg"
    COUNT = "count"

    def __str__(self) -> str:
        return str(self.value)
