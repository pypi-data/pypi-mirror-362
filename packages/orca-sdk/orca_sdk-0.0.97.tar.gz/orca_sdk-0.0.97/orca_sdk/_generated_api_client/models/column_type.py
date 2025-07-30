from enum import Enum


class ColumnType(str, Enum):
    BOOL = "BOOL"
    ENUM = "ENUM"
    FLOAT = "FLOAT"
    IMAGE = "IMAGE"
    INT = "INT"
    OTHER = "OTHER"
    STRING = "STRING"

    def __str__(self) -> str:
        return str(self.value)
