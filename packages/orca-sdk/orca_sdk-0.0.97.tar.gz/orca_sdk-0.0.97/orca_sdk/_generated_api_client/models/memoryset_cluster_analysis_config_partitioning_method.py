from enum import Enum


class MemorysetClusterAnalysisConfigPartitioningMethod(str, Enum):
    CPM = "cpm"
    NG = "ng"
    RB = "rb"

    def __str__(self) -> str:
        return str(self.value)
