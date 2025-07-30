from enum import Enum


class RACHeadType(str, Enum):
    BMMOE = "BMMOE"
    FF = "FF"
    KNN = "KNN"
    MMOE = "MMOE"

    def __str__(self) -> str:
        return str(self.value)
