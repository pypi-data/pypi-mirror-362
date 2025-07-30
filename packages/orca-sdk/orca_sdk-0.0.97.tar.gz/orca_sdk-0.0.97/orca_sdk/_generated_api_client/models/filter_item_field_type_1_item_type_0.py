from enum import Enum


class FilterItemFieldType1ItemType0(str, Enum):
    METADATA = "metadata"

    def __str__(self) -> str:
        return str(self.value)
