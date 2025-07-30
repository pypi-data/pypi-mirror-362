from enum import Enum


class EmbeddingFinetuningMethod(str, Enum):
    BATCH_TRIPLET_LOSS = "batch_triplet_loss"
    CLASSIFICATION = "classification"

    def __str__(self) -> str:
        return str(self.value)
