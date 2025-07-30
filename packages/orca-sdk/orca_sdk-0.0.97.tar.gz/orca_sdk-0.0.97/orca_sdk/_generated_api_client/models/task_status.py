from enum import Enum


class TaskStatus(str, Enum):
    ABORTED = "ABORTED"
    ABORTING = "ABORTING"
    COMPLETED = "COMPLETED"
    DISPATCHED = "DISPATCHED"
    FAILED = "FAILED"
    INITIALIZED = "INITIALIZED"
    PROCESSING = "PROCESSING"

    def __str__(self) -> str:
        return str(self.value)
