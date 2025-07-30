from enum import IntEnum


class UnauthenticatedErrorResponseStatusCode(IntEnum):
    VALUE_401 = 401

    def __str__(self) -> str:
        return str(self.value)
