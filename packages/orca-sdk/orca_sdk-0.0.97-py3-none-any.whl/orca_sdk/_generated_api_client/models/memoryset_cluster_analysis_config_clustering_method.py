from enum import Enum


class MemorysetClusterAnalysisConfigClusteringMethod(str, Enum):
    DENSITY = "density"
    GRAPH = "graph"

    def __str__(self) -> str:
        return str(self.value)
