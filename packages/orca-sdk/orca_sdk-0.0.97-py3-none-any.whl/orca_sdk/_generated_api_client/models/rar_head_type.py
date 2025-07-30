from enum import Enum


class RARHeadType(str, Enum):
    MMOE = "MMOE"

    def __str__(self) -> str:
        return str(self.value)
