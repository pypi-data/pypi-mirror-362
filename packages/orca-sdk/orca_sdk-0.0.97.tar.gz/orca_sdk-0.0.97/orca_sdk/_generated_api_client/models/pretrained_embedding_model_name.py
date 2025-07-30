from enum import Enum


class PretrainedEmbeddingModelName(str, Enum):
    BGE_BASE = "BGE_BASE"
    CDE_SMALL = "CDE_SMALL"
    CLIP_BASE = "CLIP_BASE"
    DISTILBERT = "DISTILBERT"
    E5_LARGE = "E5_LARGE"
    GIST_LARGE = "GIST_LARGE"
    GTE_BASE = "GTE_BASE"
    GTE_SMALL = "GTE_SMALL"
    MXBAI_LARGE = "MXBAI_LARGE"
    QWEN2_1_5B = "QWEN2_1_5B"

    def __str__(self) -> str:
        return str(self.value)
