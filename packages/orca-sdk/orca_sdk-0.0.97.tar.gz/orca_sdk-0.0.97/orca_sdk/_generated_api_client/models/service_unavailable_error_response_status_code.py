from enum import IntEnum


class ServiceUnavailableErrorResponseStatusCode(IntEnum):
    VALUE_503 = 503

    def __str__(self) -> str:
        return str(self.value)
