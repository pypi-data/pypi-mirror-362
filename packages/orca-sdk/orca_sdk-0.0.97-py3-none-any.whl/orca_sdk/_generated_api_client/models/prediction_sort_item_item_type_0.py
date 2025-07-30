from enum import Enum


class PredictionSortItemItemType0(str, Enum):
    ANOMALY_SCORE = "anomaly_score"
    CONFIDENCE = "confidence"
    TIMESTAMP = "timestamp"

    def __str__(self) -> str:
        return str(self.value)
