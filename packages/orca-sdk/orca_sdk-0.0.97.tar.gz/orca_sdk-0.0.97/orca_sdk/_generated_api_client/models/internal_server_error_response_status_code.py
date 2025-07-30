from enum import IntEnum


class InternalServerErrorResponseStatusCode(IntEnum):
    VALUE_500 = 500

    def __str__(self) -> str:
        return str(self.value)
