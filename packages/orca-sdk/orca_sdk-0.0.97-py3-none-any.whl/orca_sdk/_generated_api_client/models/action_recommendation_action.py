from enum import Enum


class ActionRecommendationAction(str, Enum):
    ADD_MEMORIES = "add_memories"
    DETECT_MISLABELS = "detect_mislabels"
    FINETUNING = "finetuning"
    REMOVE_DUPLICATES = "remove_duplicates"

    def __str__(self) -> str:
        return str(self.value)
