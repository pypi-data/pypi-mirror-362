from enum import Enum


class FilterItemFieldType0Item(str, Enum):
    CREATED_AT = "created_at"
    EDITED_AT = "edited_at"
    LABEL = "label"
    MEMORY_ID = "memory_id"
    METADATA = "metadata"
    METRICS = "metrics"
    SCORE = "score"
    SOURCE_ID = "source_id"
    UPDATED_AT = "updated_at"
    VALUE = "value"

    def __str__(self) -> str:
        return str(self.value)
