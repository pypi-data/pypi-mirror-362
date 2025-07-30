from enum import Enum


class FeedbackType(str, Enum):
    BINARY = "BINARY"
    CONTINUOUS = "CONTINUOUS"

    def __str__(self) -> str:
        return str(self.value)
