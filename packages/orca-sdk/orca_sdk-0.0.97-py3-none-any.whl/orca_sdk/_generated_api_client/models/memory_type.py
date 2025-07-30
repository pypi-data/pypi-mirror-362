from enum import Enum


class MemoryType(str, Enum):
    LABELED = "LABELED"
    SCORED = "SCORED"

    def __str__(self) -> str:
        return str(self.value)
