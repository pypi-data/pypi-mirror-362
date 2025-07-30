from enum import Enum


class FilterItemFieldType2ItemType1(str, Enum):
    CLUSTER = "cluster"
    CURRENT_LABEL_NEIGHBOR_CONFIDENCE = "current_label_neighbor_confidence"
    DUPLICATE_MEMORY_IDS = "duplicate_memory_ids"
    EMBEDDING_2D = "embedding_2d"
    HAS_POTENTIAL_DUPLICATES = "has_potential_duplicates"
    IS_DUPLICATE = "is_duplicate"
    NEIGHBOR_LABEL_LOGITS = "neighbor_label_logits"
    NEIGHBOR_PREDICTED_LABEL = "neighbor_predicted_label"
    NEIGHBOR_PREDICTED_LABEL_AMBIGUITY = "neighbor_predicted_label_ambiguity"
    NEIGHBOR_PREDICTED_LABEL_CONFIDENCE = "neighbor_predicted_label_confidence"
    NEIGHBOR_PREDICTED_LABEL_MATCHES_CURRENT_LABEL = "neighbor_predicted_label_matches_current_label"
    NORMALIZED_NEIGHBOR_LABEL_ENTROPY = "normalized_neighbor_label_entropy"
    POTENTIAL_DUPLICATE_MEMORY_IDS = "potential_duplicate_memory_ids"
    SPREAD = "spread"
    UNIFORMITY = "uniformity"

    def __str__(self) -> str:
        return str(self.value)
