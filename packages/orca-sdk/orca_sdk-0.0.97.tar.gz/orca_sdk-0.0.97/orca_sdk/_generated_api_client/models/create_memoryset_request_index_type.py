from enum import Enum


class CreateMemorysetRequestIndexType(str, Enum):
    DISKANN = "DISKANN"
    FLAT = "FLAT"
    HNSW = "HNSW"
    IVF_FLAT = "IVF_FLAT"
    IVF_PQ = "IVF_PQ"
    IVF_SQ8 = "IVF_SQ8"

    def __str__(self) -> str:
        return str(self.value)
