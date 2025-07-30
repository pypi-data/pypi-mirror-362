from enum import Enum


class PredictionSortItemItemType1(str, Enum):
    ASC = "asc"
    DESC = "desc"

    def __str__(self) -> str:
        return str(self.value)
