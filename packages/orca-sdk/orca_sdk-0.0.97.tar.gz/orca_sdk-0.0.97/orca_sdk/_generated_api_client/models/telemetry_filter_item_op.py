from enum import Enum


class TelemetryFilterItemOp(str, Enum):
    IN = "in"
    NOT_IN = "not in"
    VALUE_0 = "=="
    VALUE_1 = "!="
    VALUE_2 = ">"
    VALUE_3 = ">="
    VALUE_4 = "<"
    VALUE_5 = "<="

    def __str__(self) -> str:
        return str(self.value)
