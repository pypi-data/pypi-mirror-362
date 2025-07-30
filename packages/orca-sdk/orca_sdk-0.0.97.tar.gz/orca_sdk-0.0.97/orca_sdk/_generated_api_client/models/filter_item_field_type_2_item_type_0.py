from enum import Enum


class FilterItemFieldType2ItemType0(str, Enum):
    METRICS = "metrics"

    def __str__(self) -> str:
        return str(self.value)
