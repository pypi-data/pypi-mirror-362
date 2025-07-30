from enum import Enum


class TelemetryFieldType0ItemType0(str, Enum):
    FEEDBACK_METRICS = "feedback_metrics"

    def __str__(self) -> str:
        return str(self.value)
