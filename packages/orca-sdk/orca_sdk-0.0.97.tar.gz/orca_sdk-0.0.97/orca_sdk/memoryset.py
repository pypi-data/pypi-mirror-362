from __future__ import annotations

import logging
from abc import ABC
from datetime import datetime, timedelta
from os import PathLike
from typing import Any, Generic, Iterable, Literal, Self, TypeVar, cast, overload

import pandas as pd
import pyarrow as pa
from attrs import fields
from datasets import Dataset
from torch.utils.data import DataLoader as TorchDataLoader
from torch.utils.data import Dataset as TorchDataset

from ._generated_api_client.api import (
    analyze_memoryset,
    clone_memoryset,
    create_embedding_evaluation,
    create_memoryset,
    delete_memories,
    delete_memoryset,
    get_analysis,
    get_embedding_evaluation,
    get_memories,
    get_memory,
    get_memoryset,
    insert_memories_gpu,
    list_memories_with_feedback,
    list_memorysets,
    memoryset_lookup_gpu,
    potential_duplicate_groups,
    query_memoryset,
    suggest_cascading_edits,
    update_memories_gpu,
    update_memory_gpu,
    update_memoryset,
)
from ._generated_api_client.models import (
    CascadeEditSuggestionsRequest,
    CascadingEditSuggestion,
    CloneMemorysetRequest,
    ColumnType,
    CreateMemorysetRequest,
    CreateMemorysetRequestIndexParams,
    CreateMemorysetRequestIndexType,
    DeleteMemoriesRequest,
    EmbeddingEvaluationRequest,
    FilterItem,
    FilterItemOp,
    GetMemoriesRequest,
)
from ._generated_api_client.models import LabeledMemory as LabeledMemoryResponse
from ._generated_api_client.models import (
    LabeledMemoryInsert,
    LabeledMemoryInsertMetadata,
)
from ._generated_api_client.models import (
    LabeledMemoryLookup as LabeledMemoryLookupResponse,
)
from ._generated_api_client.models import (
    LabeledMemoryUpdate,
    LabeledMemoryUpdateMetadataType0,
    LabeledMemoryWithFeedbackMetrics,
    LabelPredictionMemoryLookup,
    ListMemoriesRequest,
    LookupRequest,
    MemorysetAnalysisConfigs,
    MemorysetAnalysisRequest,
    MemorysetMetadata,
    MemorysetUpdate,
    MemoryType,
    PretrainedEmbeddingModelName,
)
from ._generated_api_client.models import ScoredMemory as ScoredMemoryResponse
from ._generated_api_client.models import (
    ScoredMemoryInsert,
    ScoredMemoryInsertMetadata,
)
from ._generated_api_client.models import (
    ScoredMemoryLookup as ScoredMemoryLookupResponse,
)
from ._generated_api_client.models import (
    ScoredMemoryUpdate,
    ScoredMemoryUpdateMetadataType0,
    ScoredMemoryWithFeedbackMetrics,
    ScorePredictionMemoryLookup,
    TelemetryFilterItem,
    TelemetryFilterItemOp,
    TelemetryMemoriesRequest,
    TelemetrySortOptions,
    TelemetrySortOptionsDirection,
)
from ._generated_api_client.types import UNSET as CLIENT_UNSET
from ._utils.common import UNSET, CreateMode, DropMode
from .datasource import Datasource
from .embedding_model import (
    FinetunedEmbeddingModel,
    PretrainedEmbeddingModel,
    _EmbeddingModel,
)
from .job import Job, Status

TelemetrySortItem = tuple[str, Literal["asc", "desc"]]
"""
Sort expression for telemetry data consisting of a field and a direction.

* **`field`**: The field to sort on.
* **`direction`**: The direction to sort in.

Examples:
    >>> ("feedback_metrics.accuracy.avg", "asc")
    >>> ("lookup.count", "desc")
"""

FilterOperation = Literal["==", "!=", ">", ">=", "<", "<=", "in", "not in", "like"]
"""
Operations that can be used in a filter expression.
"""

FilterValue = str | int | float | bool | datetime | None | list[str] | list[int] | list[float] | list[bool]
"""
Values that can be used in a filter expression.
"""

FilterItemTuple = tuple[str, FilterOperation, FilterValue]
"""
Filter expression consisting of a field, an operator, and a value:

* **`field`**: The field to filter on.
* **`operation`**: The operation to apply to the field and value.
* **`value`**: The value to compare the field against.

Examples:
    >>> ("label", "==", 0)
    >>> ("metadata.author", "like", "John")
    >>> ("source_id", "in", ["123", "456"])
    >>> ("feedback_metrics.accuracy.avg", ">", 0.95)
"""

IndexType = Literal["FLAT", "IVF_FLAT", "IVF_SQ8", "IVF_PQ", "HNSW", "DISKANN"]

DEFAULT_COLUMN_NAMES = {"value", "source_id"}
TYPE_SPECIFIC_COLUMN_NAMES = {"label", "score"}
FORBIDDEN_METADATA_COLUMN_NAMES = {
    "memory_id",
    "memory_version",
    "embedding",
    "created_at",
    "updated_at",
    "metrics",
    "feedback_metrics",
    "lookup",
}


def _parse_filter_item_from_tuple(input: FilterItemTuple) -> FilterItem | TelemetryFilterItem:
    field = input[0].split(".")
    if (
        len(field) == 1
        and field[0] not in DEFAULT_COLUMN_NAMES | TYPE_SPECIFIC_COLUMN_NAMES | FORBIDDEN_METADATA_COLUMN_NAMES
    ):
        field = ["metadata", field[0]]
    op = FilterItemOp(input[1])
    value = input[2]
    if field[0] in ["feedback_metrics", "lookup"]:
        if not (
            (isinstance(value, list) and all(isinstance(v, float) or isinstance(v, int) for v in value))
            or isinstance(value, float)
            or isinstance(value, int)
        ):
            raise ValueError(f"Invalid value for {field[0]} filter: {value}")
        if field[0] == "feedback_metrics" and (len(field) != 3 or field[2] not in ["avg", "count"]):
            raise ValueError(
                "Feedback metrics filters must follow the format `feedback_metrics.<feedback_category_name>.<avg | count>`"
            )
        elif field[0] == "lookup" and (len(field) != 2 or field[1] != "count"):
            raise ValueError("Lookup filters must follow the format `lookup.count`")
        op = TelemetryFilterItemOp(op)

        return TelemetryFilterItem(field=field, op=op, value=cast(list[float] | list[int] | float | int, value))

    return FilterItem(field=field, op=op, value=value)


def _parse_sort_item_from_tuple(
    input: TelemetrySortItem,
) -> TelemetrySortOptions:
    field = input[0].split(".")

    if len(field) == 1:
        raise ValueError("Sort field must be a telemetry field with an aggregate function name value")
    if field[0] not in ["feedback_metrics", "lookup"]:
        raise ValueError("Sort field must be one of telemetry fields: feedback_metrics or lookup")
    if field[0] == "feedback_metrics":
        if len(field) != 3:
            raise ValueError(
                "Feedback metrics must follow the format `feedback_metrics.<feedback_category_name>.<avg | count>`"
            )
        if field[2] not in ["avg", "count"]:
            raise ValueError("Feedback metrics can only be sorted on avg or count")
    if field[0] == "lookup":
        if len(field) != 2:
            raise ValueError("Lookup must follow the format `lookup.count`")
        if field[1] != "count":
            raise ValueError("Lookup can only be sorted on count")
    return TelemetrySortOptions(field=field, direction=TelemetrySortOptionsDirection(input[1]))


def _parse_memory_insert(memory: dict[str, Any], type: MemoryType) -> LabeledMemoryInsert | ScoredMemoryInsert:
    value = memory.get("value")
    if not isinstance(value, str):
        raise ValueError("Memory value must be a string")
    source_id = memory.get("source_id")
    if source_id and not isinstance(source_id, str):
        raise ValueError("Memory source_id must be a string")
    match type:
        case MemoryType.LABELED:
            label = memory.get("label")
            if not isinstance(label, int):
                raise ValueError("Memory label must be an integer")
            metadata = LabeledMemoryInsertMetadata.from_dict(
                {k: v for k, v in memory.items() if k not in DEFAULT_COLUMN_NAMES | {"label"}}
            )
            if any(k in metadata for k in FORBIDDEN_METADATA_COLUMN_NAMES):
                raise ValueError(
                    f"The following column names are reserved: {', '.join(FORBIDDEN_METADATA_COLUMN_NAMES)}"
                )
            return LabeledMemoryInsert(value=value, label=label, source_id=source_id, metadata=metadata)
        case MemoryType.SCORED:
            score = memory.get("score")
            if not isinstance(score, (int, float)):
                raise ValueError("Memory score must be a number")
            metadata = ScoredMemoryInsertMetadata.from_dict(
                {k: v for k, v in memory.items() if k not in DEFAULT_COLUMN_NAMES | {"score"}}
            )
            if any(k in metadata for k in FORBIDDEN_METADATA_COLUMN_NAMES):
                raise ValueError(
                    f"The following column names are reserved: {', '.join(FORBIDDEN_METADATA_COLUMN_NAMES)}"
                )
            return ScoredMemoryInsert(value=value, score=score, source_id=source_id, metadata=metadata)


@overload
def _parse_memory_update(update: dict[str, Any], type: Literal[MemoryType.LABELED]) -> LabeledMemoryUpdate:
    pass


@overload
def _parse_memory_update(update: dict[str, Any], type: Literal[MemoryType.SCORED]) -> ScoredMemoryUpdate:
    pass


@overload
def _parse_memory_update(update: dict[str, Any], type: MemoryType) -> ScoredMemoryUpdate | LabeledMemoryUpdate:
    pass


def _parse_memory_update(update: dict[str, Any], type: MemoryType) -> LabeledMemoryUpdate | ScoredMemoryUpdate:
    if "memory_id" not in update:
        raise ValueError("memory_id must be specified in the update dictionary")
    memory_id = update["memory_id"]
    if not isinstance(memory_id, str):
        raise ValueError("memory_id must be a string")
    value = update.get("value", CLIENT_UNSET)
    if value is not CLIENT_UNSET and not isinstance(value, str):
        raise ValueError("value must be a string or unset")
    source_id = update.get("source_id", CLIENT_UNSET)
    if source_id is not CLIENT_UNSET and not isinstance(source_id, str):
        raise ValueError("source_id must be a string or unset")
    match type:
        case MemoryType.LABELED:
            label = update.get("label", CLIENT_UNSET)
            if label is not CLIENT_UNSET and not isinstance(label, int):
                raise ValueError("label must be an integer or unset")
            metadata = LabeledMemoryUpdateMetadataType0.from_dict(
                {k: v for k, v in update.items() if k not in DEFAULT_COLUMN_NAMES | {"memory_id", "label"}}
            )
            if any(k in metadata for k in FORBIDDEN_METADATA_COLUMN_NAMES):
                raise ValueError(
                    f"Cannot update the following metadata keys: {', '.join(FORBIDDEN_METADATA_COLUMN_NAMES)}"
                )
            return LabeledMemoryUpdate(
                memory_id=memory_id, value=value, label=label, source_id=source_id, metadata=metadata
            )
        case MemoryType.SCORED:
            score = update.get("score", CLIENT_UNSET)
            if score is not CLIENT_UNSET and not isinstance(score, (int, float)):
                raise ValueError("score must be a number or unset")
            metadata = ScoredMemoryUpdateMetadataType0.from_dict(
                {k: v for k, v in update.items() if k not in DEFAULT_COLUMN_NAMES | {"memory_id", "score"}}
            )
            if any(k in metadata for k in FORBIDDEN_METADATA_COLUMN_NAMES):
                raise ValueError(
                    f"Cannot update the following metadata keys: {', '.join(FORBIDDEN_METADATA_COLUMN_NAMES)}"
                )
            return ScoredMemoryUpdate(
                memory_id=memory_id, value=value, score=score, source_id=source_id, metadata=metadata
            )


class _Memory(ABC):
    value: str
    embedding: list[float]
    source_id: str | None
    created_at: datetime
    updated_at: datetime
    metadata: dict[str, str | float | int | bool | None]
    metrics: dict[str, Any]
    memory_id: str
    memory_version: int
    feedback_metrics: dict[str, Any]
    lookup_count: int
    memory_type: MemoryType  # defined by subclasses

    def __init__(
        self,
        memoryset_id: str,
        memory: (
            LabeledMemoryResponse
            | LabeledMemoryLookupResponse
            | LabeledMemoryWithFeedbackMetrics
            | LabelPredictionMemoryLookup
            | ScoredMemoryResponse
            | ScoredMemoryLookupResponse
            | ScoredMemoryWithFeedbackMetrics
            | ScorePredictionMemoryLookup
        ),
    ):
        # for internal use only, do not document
        self.memoryset_id = memoryset_id
        self.memory_id = memory.memory_id
        self.memory_version = memory.memory_version
        self.value = memory.value
        self.embedding = memory.embedding
        self.source_id = memory.source_id
        self.created_at = memory.created_at
        self.updated_at = memory.updated_at
        self.metadata = memory.metadata.to_dict()
        self.metrics = memory.metrics.to_dict() if memory.metrics else {}
        self.feedback_metrics = (
            getattr(memory, "feedback_metrics").to_dict() if hasattr(memory, "feedback_metrics") else {}
        )
        self.lookup_count = getattr(memory, "lookup_count", 0)

    def __getattr__(self, key: str) -> Any:
        if key.startswith("__") or key not in self.metadata:
            raise AttributeError(f"{key} is not a valid attribute")
        return self.metadata[key]

    def update(
        self,
        *,
        value: str = UNSET,
        source_id: str | None = UNSET,
        **metadata: None | bool | float | int | str,
    ) -> Self:
        """
        Update the memory with new values

        Note:
            If a field is not provided, it will default to [UNSET][orca_sdk.UNSET] and not be updated.

        Params:
            value: New value of the memory
            label: New label of the memory
            score: New score of the memory
            source_id: New source ID of the memory
            **metadata: New values for metadata properties

        Returns:
            The updated memory
        """
        response = update_memory_gpu(
            self.memoryset_id,
            body=_parse_memory_update(
                {"memory_id": self.memory_id}
                | ({"value": value} if value is not UNSET else {})
                | ({"source_id": source_id} if source_id is not UNSET else {})
                | {k: v for k, v in metadata.items() if v is not UNSET},
                type=self.memory_type,
            ),
        )
        self.__dict__.update(self.__class__(self.memoryset_id, response).__dict__)
        return self


class LabeledMemory(_Memory):
    """
    A row of the [`LabeledMemoryset`][orca_sdk.LabeledMemoryset]

    Attributes:
        value: Value represented by the row
        embedding: Embedding of the value of the memory for semantic search, automatically generated
            with the [`LabeledMemoryset.embedding_model`][orca_sdk.LabeledMemoryset]
        label: Class label of the memory
        label_name: Human-readable name of the label, automatically populated from the
            [`LabeledMemoryset.label_names`][orca_sdk.LabeledMemoryset]
        source_id: Optional unique identifier of the memory in a system of reference
        metrics: Metrics about the memory, generated when running an analysis on the
            [`LabeledMemoryset`][orca_sdk.LabeledMemoryset]
        metadata: Metadata associated with the memory that is not used in the model. Metadata
            properties are also accessible as individual attributes on the instance.
        memory_id: Unique identifier for the memory, automatically generated on insert
        memory_version: Version of the memory, automatically updated when the label or value changes
        created_at: When the memory was created, automatically generated on insert
        updated_at: When the memory was last updated, automatically updated on update

    ## Other Attributes:
    * **`...`** (<code>[str][str] | [float][float] | [int][int] | [bool][bool] | None</code>): All metadata properties can be accessed as attributes
    """

    label: int
    label_name: str | None
    memory_type = MemoryType.LABELED

    def __init__(
        self,
        memoryset_id: str,
        memory: (
            LabeledMemoryResponse
            | LabeledMemoryLookupResponse
            | LabelPredictionMemoryLookup
            | LabeledMemoryWithFeedbackMetrics
        ),
    ):
        # for internal use only, do not document
        super().__init__(memoryset_id, memory)
        self.label = memory.label
        self.label_name = memory.label_name

    def __repr__(self) -> str:
        return (
            "LabeledMemory({ "
            + f"label: {('<' + self.label_name + ': ' + str(self.label) + '>') if self.label_name else str(self.label)}"
            + f", value: '{self.value[:100] + '...' if isinstance(self.value, str) and len(self.value) > 100 else self.value}'"
            + (f", source_id: '{self.source_id}'" if self.source_id is not None else "")
            + " })"
        )

    def __eq__(self, other: object) -> bool:
        return isinstance(other, LabeledMemory) and self.memory_id == other.memory_id

    def update(
        self,
        *,
        value: str = UNSET,
        label: int = UNSET,
        source_id: str | None = UNSET,
        **metadata: None | bool | float | int | str,
    ) -> LabeledMemory:
        """
        Update the memory with new values

        Note:
            If a field is not provided, it will default to [UNSET][orca_sdk.UNSET] and not be updated.

        Params:
            value: New value of the memory
            label: New label of the memory
            source_id: New source ID of the memory
            **metadata: New values for metadata properties

        Returns:
            The updated memory
        """
        super().update(value=value, label=label, source_id=source_id, **metadata)
        return self


class LabeledMemoryLookup(LabeledMemory):
    """
    Lookup result for a memory in a memoryset

    Attributes:
        lookup_score: Similarity between the memory embedding and search query embedding
        attention_weight: Weight the model assigned to the memory during prediction if this lookup
            happened as part of a prediction
        value: Value represented by the row
        embedding: Embedding of the value of the memory for semantic search, automatically generated
            with the [`LabeledMemoryset.embedding_model`][orca_sdk.LabeledMemoryset]
        label: Class label of the memory
        label_name: Human-readable name of the label, automatically populated from the
            [`LabeledMemoryset.label_names`][orca_sdk.LabeledMemoryset]
        source_id: Optional unique identifier of the memory in a system of reference
        metrics: Metrics about the memory, generated when running an analysis on the
            [`LabeledMemoryset`][orca_sdk.LabeledMemoryset]
        metadata: Metadata associated with the memory that is not used in the model. Metadata
            properties are also accessible as individual attributes on the instance.
        memory_id: The unique identifier for the memory, automatically generated on insert
        memory_version: The version of the memory, automatically updated when the label or value changes
        created_at: When the memory was created, automatically generated on insert
        updated_at: When the memory was last updated, automatically updated on update

    ## Other Attributes:
    * **`...`** (<code>[str][str] | [float][float] | [int][int] | [bool][bool] | None</code>): All metadata properties can be accessed as attributes
    """

    lookup_score: float
    attention_weight: float | None

    def __init__(self, memoryset_id: str, memory_lookup: LabeledMemoryLookupResponse | LabelPredictionMemoryLookup):
        # for internal use only, do not document
        super().__init__(memoryset_id, memory_lookup)
        self.lookup_score = memory_lookup.lookup_score
        self.attention_weight = (
            memory_lookup.attention_weight if isinstance(memory_lookup, LabelPredictionMemoryLookup) else None
        )

    def __repr__(self) -> str:
        return (
            "LabeledMemoryLookup({ "
            + f"label: {('<' + self.label_name + ': ' + str(self.label) + '>') if self.label_name else str(self.label)}"
            + f", lookup_score: {self.lookup_score:.2f}"
            + (f", attention_weight: {self.attention_weight:.2f}" if self.attention_weight is not None else "")
            + f", value: '{self.value[:100] + '...' if isinstance(self.value, str) and len(self.value) > 100 else self.value}'"
            + (f", source_id: '{self.source_id}'" if self.source_id is not None else "")
            + " })"
        )


class ScoredMemory(_Memory):
    """
    A row of the [`ScoredMemoryset`][orca_sdk.ScoredMemoryset]

    Attributes:
        value: Value represented by the row
        embedding: Embedding of the value of the memory for semantic search, automatically generated
            with the [`ScoredMemoryset.embedding_model`][orca_sdk.ScoredMemoryset]
        score: Score of the memory
        source_id: Optional unique identifier of the memory in a system of reference
        metrics: Metrics about the memory, generated when running an analysis on the
            [`ScoredMemoryset`][orca_sdk.ScoredMemoryset]
        metadata: Metadata associated with the memory that is not used in the model. Metadata
            properties are also accessible as individual attributes on the instance.
        memory_id: Unique identifier for the memory, automatically generated on insert
        memory_version: Version of the memory, automatically updated when the score or value changes
        created_at: When the memory was created, automatically generated on insert
        updated_at: When the memory was last updated, automatically updated on update

    ## Other Attributes:
    * **`...`** (<code>[str][str] | [float][float] | [int][int] | [bool][bool] | None</code>): All metadata properties can be accessed as attributes
    """

    score: float
    memory_type = MemoryType.SCORED

    def __init__(
        self,
        memoryset_id: str,
        memory: (
            ScoredMemoryResponse
            | ScoredMemoryLookupResponse
            | ScorePredictionMemoryLookup
            | ScoredMemoryWithFeedbackMetrics
        ),
    ):
        # for internal use only, do not document
        super().__init__(memoryset_id, memory)
        self.score = memory.score

    def __repr__(self) -> str:
        return (
            "ScoredMemory({ "
            + f"score: {self.score:.2f}"
            + f", value: '{self.value[:100] + '...' if isinstance(self.value, str) and len(self.value) > 100 else self.value}'"
            + (f", source_id: '{self.source_id}'" if self.source_id is not None else "")
            + " })"
        )

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ScoredMemory) and self.memory_id == other.memory_id

    def update(
        self,
        *,
        value: str = UNSET,
        score: float = UNSET,
        source_id: str | None = UNSET,
        **metadata: None | bool | float | int | str,
    ) -> ScoredMemory:
        """
        Update the memory with new values

        Note:
            If a field is not provided, it will default to [UNSET][orca_sdk.UNSET] and not be updated.

        Params:
            value: New value of the memory
            score: New score of the memory
            source_id: New source ID of the memory
            **metadata: New values for metadata properties

        Returns:
            The updated memory
        """
        super().update(value=value, score=score, source_id=source_id, **metadata)
        return self


class ScoredMemoryLookup(ScoredMemory):
    """
    Lookup result for a memory in a memoryset

    Attributes:
        lookup_score: Similarity between the memory embedding and search query embedding
        attention_weight: Weight the model assigned to the memory during prediction if this lookup
            happened as part of a prediction
        value: Value represented by the row
        embedding: Embedding of the value of the memory for semantic search, automatically generated
            with the [`ScoredMemoryset.embedding_model`][orca_sdk.ScoredMemoryset]
        score: Score of the memory
        source_id: Optional unique identifier of the memory in a system of reference
        metrics: Metrics about the memory, generated when running an analysis on the
            [`ScoredMemoryset`][orca_sdk.ScoredMemoryset]
        memory_id: The unique identifier for the memory, automatically generated on insert
        memory_version: The version of the memory, automatically updated when the score or value changes
        created_at: When the memory was created, automatically generated on insert
        updated_at: When the memory was last updated, automatically updated on update

    ## Other Attributes:
    * **`...`** (<code>[str][str] | [float][float] | [int][int] | [bool][bool] | None</code>): All metadata properties can be accessed as attributes
    """

    lookup_score: float
    attention_weight: float | None

    def __init__(self, memoryset_id: str, memory_lookup: ScoredMemoryLookupResponse | ScorePredictionMemoryLookup):
        # for internal use only, do not document
        super().__init__(memoryset_id, memory_lookup)
        self.lookup_score = memory_lookup.lookup_score
        self.attention_weight = (
            memory_lookup.attention_weight if isinstance(memory_lookup, ScorePredictionMemoryLookup) else None
        )

    def __repr__(self) -> str:
        return (
            "ScoredMemoryLookup({ "
            + f"score: {self.score:.2f}"
            + f", lookup_score: {self.lookup_score:.2f}"
            + f", value: '{self.value[:100] + '...' if isinstance(self.value, str) and len(self.value) > 100 else self.value}'"
            + (f", source_id: '{self.source_id}'" if self.source_id is not None else "")
            + " })"
        )


MemoryT = TypeVar("MemoryT", bound=_Memory)
MemoryLookupT = TypeVar("MemoryLookupT", bound=_Memory)


class _Memoryset(Generic[MemoryT, MemoryLookupT], ABC):
    """
    A Handle to a collection of memories with labels in the OrcaCloud

    Attributes:
        id: Unique identifier for the memoryset
        name: Unique name of the memoryset
        description: Description of the memoryset
        length: Number of memories in the memoryset
        embedding_model: Embedding model used to embed the memory values for semantic search
        created_at: When the memoryset was created, automatically generated on create
        updated_at: When the memoryset was last updated, automatically updated on updates
    """

    id: str
    name: str
    description: str | None
    memory_type: MemoryType  # defined by subclasses

    length: int
    created_at: datetime
    updated_at: datetime
    insertion_status: Status
    embedding_model: _EmbeddingModel
    index_type: IndexType
    index_params: dict[str, Any]

    def __init__(self, metadata: MemorysetMetadata):
        # for internal use only, do not document
        if metadata.pretrained_embedding_model_name:
            self.embedding_model = PretrainedEmbeddingModel._get(metadata.pretrained_embedding_model_name)
        elif metadata.finetuned_embedding_model_id:
            self.embedding_model = FinetunedEmbeddingModel.open(metadata.finetuned_embedding_model_id)
        else:
            raise ValueError("Either pretrained_embedding_model_name or finetuned_embedding_model_id must be provided")
        self.id = metadata.id
        self.name = metadata.name
        self.description = metadata.description
        self.length = metadata.length
        self.created_at = metadata.created_at
        self.updated_at = metadata.updated_at
        self.insertion_status = Status(metadata.insertion_status.value)
        self._last_refresh = datetime.now()
        self.index_type = metadata.index_type.value
        self.index_params = metadata.index_params.to_dict()
        self.memory_type = MemoryType(metadata.memory_type.value)

    def __eq__(self, other) -> bool:
        return isinstance(other, _Memoryset) and self.id == other.id

    def __repr__(self) -> str:
        return (
            "Memoryset({\n"
            f"    name: '{self.name}',\n"
            f"    length: {self.length},\n"
            f"    embedding_model: {self.embedding_model},\n"
            "})"
        )

    @overload
    @classmethod
    def create(
        cls,
        name: str,
        datasource: Datasource,
        *,
        embedding_model: FinetunedEmbeddingModel | PretrainedEmbeddingModel | None = None,
        value_column: str = "value",
        label_column: str | None = None,
        score_column: str | None = None,
        source_id_column: str | None = None,
        description: str | None = None,
        label_names: list[str] | None = None,
        max_seq_length_override: int | None = None,
        prompt: str | None = None,
        remove_duplicates: bool = True,
        index_type: IndexType = "FLAT",
        index_params: dict[str, Any] = {},
        if_exists: CreateMode = "error",
        background: Literal[True],
    ) -> Job[Self]:
        pass

    @overload
    @classmethod
    def create(
        cls,
        name: str,
        datasource: Datasource,
        *,
        embedding_model: FinetunedEmbeddingModel | PretrainedEmbeddingModel | None = None,
        value_column: str = "value",
        label_column: str | None = None,
        score_column: str | None = None,
        source_id_column: str | None = None,
        description: str | None = None,
        label_names: list[str] | None = None,
        max_seq_length_override: int | None = None,
        prompt: str | None = None,
        remove_duplicates: bool = True,
        index_type: IndexType = "FLAT",
        index_params: dict[str, Any] = {},
        if_exists: CreateMode = "error",
        background: Literal[False] = False,
    ) -> Self:
        pass

    @classmethod
    def create(
        cls,
        name: str,
        datasource: Datasource,
        *,
        embedding_model: FinetunedEmbeddingModel | PretrainedEmbeddingModel | None = None,
        value_column: str = "value",
        label_column: str | None = None,
        score_column: str | None = None,
        source_id_column: str | None = None,
        description: str | None = None,
        label_names: list[str] | None = None,
        max_seq_length_override: int | None = None,
        prompt: str | None = None,
        remove_duplicates: bool = True,
        index_type: IndexType = "FLAT",
        index_params: dict[str, Any] = {},
        if_exists: CreateMode = "error",
        background: bool = False,
    ) -> Self | Job[Self]:
        """
        Create a new memoryset in the OrcaCloud

        All columns from the datasource that are not specified in the `value_column`,
        `label_column`, or `source_id_column` will be stored as metadata in the memoryset.

        Params:
            name: Name for the new memoryset (must be unique)
            datasource: Source data to populate the memories in the memoryset
            embedding_model: Embedding model to use for embedding memory values for semantic search.
                If not provided, a default embedding model for the memoryset will be used.
            value_column: Name of the column in the datasource that contains the memory values
            label_column: Name of the column in the datasource that contains the memory labels,
                these must be contiguous integers starting from 0
            score_column: Name of the column in the datasource that contains the memory scores
            source_id_column: Optional name of the column in the datasource that contains the ids in
                the system of reference
            description: Optional description for the memoryset, this will be used in agentic flows,
                so make sure it is concise and describes the contents of your memoryset not the
                datasource or the embedding model.
            label_names: List of human-readable names for the labels in the memoryset, must match
                the number of labels in the `label_column`. Will be automatically inferred if a
                [Dataset][datasets.Dataset] with a [`ClassLabel`][datasets.ClassLabel] feature for
                labels is used as the datasource
            max_seq_length_override: Maximum sequence length of values in the memoryset, if the
                value is longer than this it will be truncated, will default to the model's max
                sequence length if not provided
            prompt: Optional prompt to use when embedding documents/memories for storage
            remove_duplicates: Whether to remove duplicates from the datasource before inserting
                into the memoryset
            index_type: Type of vector index to use for the memoryset, defaults to `"FLAT"`. Valid
                values are `"FLAT"`, `"IVF_FLAT"`, `"IVF_SQ8"`, `"IVF_PQ"`, `"HNSW"`, and `"DISKANN"`.
            index_params: Parameters for the vector index, defaults to `{}`
            if_exists: What to do if a memoryset with the same name already exists, defaults to
                `"error"`. Other option is `"open"` to open the existing memoryset.
            background: Whether to run the operation none blocking and return a job handle

        Returns:
            Handle to the new memoryset in the OrcaCloud

        Raises:
            ValueError: If the memoryset already exists and if_exists is `"error"` or if it is
                `"open"` and the params do not match those of the existing memoryset.
        """
        if embedding_model is None:
            embedding_model = PretrainedEmbeddingModel.CDE_SMALL

        if label_column is None and score_column is None:
            raise ValueError("label_column or score_column must be provided")

        if cls.exists(name):
            if if_exists == "error":
                raise ValueError(f"Memoryset with name {name} already exists")
            elif if_exists == "open":
                existing = cls.open(name)
                for attribute in {"label_names", "embedding_model"}:
                    if locals()[attribute] is not None and locals()[attribute] != getattr(existing, attribute):
                        raise ValueError(f"Memoryset with name {name} already exists with a different {attribute}.")
                return existing

        response = create_memoryset(
            body=CreateMemorysetRequest(
                name=name,
                description=description,
                datasource_id=datasource.id,
                datasource_label_column=label_column,
                datasource_score_column=score_column,
                datasource_value_column=value_column,
                datasource_source_id_column=source_id_column,
                pretrained_embedding_model_name=(
                    embedding_model._model_name if isinstance(embedding_model, PretrainedEmbeddingModel) else None
                ),
                finetuned_embedding_model_id=(
                    embedding_model.id if isinstance(embedding_model, FinetunedEmbeddingModel) else None
                ),
                label_names=label_names,
                max_seq_length_override=max_seq_length_override,
                remove_duplicates=remove_duplicates,
                index_type=CreateMemorysetRequestIndexType[index_type],
                index_params=CreateMemorysetRequestIndexParams.from_dict(index_params),
                prompt=prompt,
            ),
        )
        job = Job(response.insertion_task_id, lambda: cls.open(response.id))
        return job if background else job.result()

    @overload
    @classmethod
    def from_hf_dataset(cls, name: str, hf_dataset: Dataset, background: Literal[True], **kwargs: Any) -> Self:
        pass

    @overload
    @classmethod
    def from_hf_dataset(cls, name: str, hf_dataset: Dataset, background: Literal[False] = False, **kwargs: Any) -> Self:
        pass

    @classmethod
    def from_hf_dataset(
        cls, name: str, hf_dataset: Dataset, background: bool = False, **kwargs: Any
    ) -> Self | Job[Self]:
        """
        Create a new memoryset from a Hugging Face [`Dataset`][datasets.Dataset] in the OrcaCloud

        This will automatically create a [`Datasource`][orca_sdk.Datasource] with the same name
        appended with `_datasource` and use that as the datasource for the memoryset.

        All features that are not specified to be used as `value_column`, `label_column`, or
        `source_id_column` will be stored as metadata in the memoryset.

        Params:
            name: Name for the new memoryset (must be unique)
            hf_dataset: Hugging Face dataset to create the memoryset from
            kwargs: Additional parameters for creating the memoryset. See
                [`create`][orca_sdk.LabeledMemoryset.create] attributes for details.

        Returns:
            Handle to the new memoryset in the OrcaCloud
        """
        datasource = Datasource.from_hf_dataset(
            f"{name}_datasource", hf_dataset, if_exists=kwargs.get("if_exists", "error")
        )
        kwargs["background"] = background
        return cls.create(name, datasource, **kwargs)

    @overload
    @classmethod
    def from_pytorch(
        cls,
        name: str,
        torch_data: TorchDataLoader | TorchDataset,
        *,
        column_names: list[str] | None = None,
        background: Literal[True],
        **kwargs: Any,
    ) -> Job[Self]:
        pass

    @overload
    @classmethod
    def from_pytorch(
        cls,
        name: str,
        torch_data: TorchDataLoader | TorchDataset,
        *,
        column_names: list[str] | None = None,
        background: Literal[False] = False,
        **kwargs: Any,
    ) -> Self:
        pass

    @classmethod
    def from_pytorch(
        cls,
        name: str,
        torch_data: TorchDataLoader | TorchDataset,
        *,
        column_names: list[str] | None = None,
        background: bool = False,
        **kwargs: Any,
    ) -> Self | Job[Self]:
        """
        Create a new memoryset from a PyTorch [`DataLoader`][torch.utils.data.DataLoader] or
        [`Dataset`][torch.utils.data.Dataset] in the OrcaCloud

        This will automatically create a [`Datasource`][orca_sdk.Datasource] with the same name
        appended with `_datasource` and use that as the datasource for the memoryset.

        All properties that are not specified to be used as `value_column`, `label_column`, or
        `source_id_column` will be stored as metadata in the memoryset.

        Params:
            name: Name for the new memoryset (must be unique)
            torch_data: PyTorch data loader or dataset to create the memoryset from
            column_names: If the provided dataset or data loader returns unnamed tuples, this
                argument must be provided to specify the names of the columns.
            background: Whether to run the operation in the background
            kwargs: Additional parameters for creating the memoryset. See
                [`create`][orca_sdk.LabeledMemoryset.create] attributes for details.

        Returns:
            Handle to the new memoryset in the OrcaCloud
        """
        datasource = Datasource.from_pytorch(
            f"{name}_datasource", torch_data, column_names=column_names, if_exists=kwargs.get("if_exists", "error")
        )
        kwargs["background"] = background
        return cls.create(name, datasource, **kwargs)

    @overload
    @classmethod
    def from_list(
        cls,
        name: str,
        data: list[dict],
        *,
        background: Literal[True],
        **kwargs: Any,
    ) -> Job[Self]:
        pass

    @overload
    @classmethod
    def from_list(
        cls,
        name: str,
        data: list[dict],
        *,
        background: Literal[False] = False,
        **kwargs: Any,
    ) -> Self:
        pass

    @classmethod
    def from_list(
        cls,
        name: str,
        data: list[dict],
        *,
        background: bool = False,
        **kwargs: Any,
    ) -> Self | Job[Self]:
        """
        Create a new memoryset from a list of dictionaries in the OrcaCloud

        This will automatically create a [`Datasource`][orca_sdk.Datasource] with the same name
        appended with `_datasource` and use that as the datasource for the memoryset.

        All properties that are not specified to be used as `value_column`, `label_column`, or
        `source_id_column` will be stored as metadata in the memoryset.

        Params:
            name: Name for the new memoryset (must be unique)
            data: List of dictionaries to create the memoryset from
            background: Whether to run the operation in the background
            kwargs: Additional parameters for creating the memoryset. See
                [`create`][orca_sdk.LabeledMemoryset.create] attributes for details.

        Returns:
            Handle to the new memoryset in the OrcaCloud

        Examples:
            >>> LabeledMemoryset.from_list("my_memoryset", [
            ...     {"value": "hello", "label": 0, "tag": "tag1"},
            ...     {"value": "world", "label": 1, "tag": "tag2"},
            ... ])
        """
        datasource = Datasource.from_list(f"{name}_datasource", data, if_exists=kwargs.get("if_exists", "error"))
        kwargs["background"] = background
        return cls.create(name, datasource, **kwargs)

    @overload
    @classmethod
    def from_dict(
        cls,
        name: str,
        data: dict,
        *,
        background: Literal[True],
        **kwargs: Any,
    ) -> Job[Self]:
        pass

    @overload
    @classmethod
    def from_dict(
        cls,
        name: str,
        data: dict,
        *,
        background: Literal[False] = False,
        **kwargs: Any,
    ) -> Self:
        pass

    @classmethod
    def from_dict(
        cls,
        name: str,
        data: dict,
        *,
        background: bool = False,
        **kwargs: Any,
    ) -> Self | Job[Self]:
        """
        Create a new memoryset from a dictionary of columns in the OrcaCloud

        This will automatically create a [`Datasource`][orca_sdk.Datasource] with the same name
        appended with `_datasource` and use that as the datasource for the memoryset.

        All columns from the datasource that are not specified in the `value_column`,
        `label_column`, or `source_id_column` will be stored as metadata in the memoryset.

        Params:
            name: Name for the new memoryset (must be unique)
            data: Dictionary of columns to create the memoryset from
            background: Whether to run the operation in the background
            kwargs: Additional parameters for creating the memoryset. See
                [`create`][orca_sdk.LabeledMemoryset.create] attributes for details.

        Returns:
            Handle to the new memoryset in the OrcaCloud

        Examples:
            >>> LabeledMemoryset.from_dict("my_memoryset", {
            ...     "value": ["hello", "world"],
            ...     "label": [0, 1],
            ...     "tag": ["tag1", "tag2"],
            ... })
        """
        datasource = Datasource.from_dict(f"{name}_datasource", data, if_exists=kwargs.get("if_exists", "error"))
        kwargs["background"] = background
        return cls.create(name, datasource, **kwargs)

    @overload
    @classmethod
    def from_pandas(
        cls,
        name: str,
        dataframe: pd.DataFrame,
        *,
        background: Literal[True],
        **kwargs: Any,
    ) -> Job[Self]:
        pass

    @overload
    @classmethod
    def from_pandas(
        cls,
        name: str,
        dataframe: pd.DataFrame,
        *,
        background: Literal[False] = False,
        **kwargs: Any,
    ) -> Self:
        pass

    @classmethod
    def from_pandas(
        cls,
        name: str,
        dataframe: pd.DataFrame,
        *,
        background: bool = False,
        **kwargs: Any,
    ) -> Self | Job[Self]:
        """
        Create a new memoryset from a pandas [`DataFrame`][pandas.DataFrame] in the OrcaCloud

        This will automatically create a [`Datasource`][orca_sdk.Datasource] with the same name
        appended with `_datasource` and use that as the datasource for the memoryset.

        All columns that are not specified to be used as `value_column`, `label_column`, or
        `source_id_column` will be stored as metadata in the memoryset.

        Params:
            name: Name for the new memoryset (must be unique)
            dataframe: Dataframe to create the memoryset from
            background: Whether to run the operation in the background
            kwargs: Additional parameters for creating the memoryset. See
                [`create`][orca_sdk.LabeledMemoryset.create] attributes for details.

        Returns:
            Handle to the new memoryset in the OrcaCloud
        """
        datasource = Datasource.from_pandas(f"{name}_datasource", dataframe, if_exists=kwargs.get("if_exists", "error"))
        kwargs["background"] = background
        return cls.create(name, datasource, **kwargs)

    @overload
    @classmethod
    def from_arrow(
        cls,
        name: str,
        pyarrow_table: pa.Table,
        *,
        background: Literal[True],
        **kwargs: Any,
    ) -> Job[Self]:
        pass

    @overload
    @classmethod
    def from_arrow(
        cls,
        name: str,
        pyarrow_table: pa.Table,
        *,
        background: Literal[False] = False,
        **kwargs: Any,
    ) -> Self:
        pass

    @classmethod
    def from_arrow(
        cls,
        name: str,
        pyarrow_table: pa.Table,
        *,
        background: bool = False,
        **kwargs: Any,
    ) -> Self | Job[Self]:
        """
        Create a new memoryset from a PyArrow [`Table`][pyarrow.Table] in the OrcaCloud

        This will automatically create a [`Datasource`][orca_sdk.Datasource] with the same name
        appended with `_datasource` and use that as the datasource for the memoryset.

        All columns that are not specified to be used as `value_column`, `label_column`, or
        `source_id_column` will be stored as metadata in the memoryset.

        Params:
            name: Name for the new memoryset (must be unique)
            pyarrow_table: PyArrow table to create the memoryset from
            background: Whether to run the operation in the background
            kwargs: Additional parameters for creating the memoryset. See
                [`create`][orca_sdk.LabeledMemoryset.create] attributes for details.

        Returns:
            Handle to the new memoryset in the OrcaCloud
        """
        datasource = Datasource.from_arrow(
            f"{name}_datasource", pyarrow_table, if_exists=kwargs.get("if_exists", "error")
        )
        kwargs["background"] = background
        return cls.create(name, datasource, **kwargs)

    @overload
    @classmethod
    def from_disk(
        cls,
        name: str,
        file_path: str | PathLike,
        *,
        background: Literal[True],
        **kwargs: Any,
    ) -> Job[Self]:
        pass

    @overload
    @classmethod
    def from_disk(
        cls,
        name: str,
        file_path: str | PathLike,
        *,
        background: Literal[False] = False,
        **kwargs: Any,
    ) -> Self:
        pass

    @classmethod
    def from_disk(
        cls,
        name: str,
        file_path: str | PathLike,
        *,
        background: bool = False,
        **kwargs: Any,
    ) -> Self | Job[Self]:
        """
        Create a new memoryset from a file on disk in the OrcaCloud

        This will automatically create a [`Datasource`][orca_sdk.Datasource] with the same name
        appended with `_datasource` and use that as the datasource for the memoryset.

        All columns from the datasource that are not specified in the `value_column`,
        `label_column`, or `source_id_column` will be stored as metadata in the memoryset.

        Params:
            name: Name for the new memoryset (must be unique)
            file_path: Path to the file on disk to create the memoryset from. The file type will
                be inferred from the file extension. The following file types are supported:

                - .pkl: [`Pickle`][pickle] files containing lists of dictionaries or dictionaries of columns
                - .json/.jsonl: [`JSON`][json] and [`JSON`] Lines files
                - .csv: [`CSV`][csv] files
                - .parquet: [`Parquet`][pyarrow.parquet.ParquetFile] files
                - dataset directory: Directory containing a saved HuggingFace [`Dataset`][datasets.Dataset]
            background: Whether to run the operation in the background
            kwargs: Additional parameters for creating the memoryset. See
                [`create`][orca_sdk.LabeledMemoryset.create] attributes for details.

        Returns:
            Handle to the new memoryset in the OrcaCloud
        """
        datasource = Datasource.from_disk(f"{name}_datasource", file_path, if_exists=kwargs.get("if_exists", "error"))
        kwargs["background"] = background
        return cls.create(name, datasource, **kwargs)

    @classmethod
    def open(cls, name: str) -> Self:
        """
        Get a handle to a memoryset in the OrcaCloud

        Params:
            name: Name or unique identifier of the memoryset

        Returns:
            Handle to the existing memoryset in the OrcaCloud

        Raises:
            LookupError: If the memoryset does not exist
        """
        metadata = get_memoryset(name)
        return cls(metadata)

    @classmethod
    def exists(cls, name_or_id: str) -> bool:
        """
        Check if a memoryset exists in the OrcaCloud

        Params:
            name_or_id: Name or id of the memoryset

        Returns:
            True if the memoryset exists, False otherwise
        """
        try:
            cls.open(name_or_id)
            return True
        except LookupError:
            return False

    @classmethod
    def all(cls) -> list[Self]:
        """
        Get a list of handles to all memorysets in the OrcaCloud

        Returns:
            List of handles to all memorysets in the OrcaCloud
        """
        return [cls(metadata) for metadata in list_memorysets(type=cls.memory_type)]

    @classmethod
    def drop(cls, name_or_id: str, if_not_exists: DropMode = "error"):
        """
        Delete a memoryset from the OrcaCloud

        Params:
            name_or_id: Name or id of the memoryset
            if_not_exists: What to do if the memoryset does not exist, defaults to `"error"`.
                Other options are `"ignore"` to do nothing if the memoryset does not exist.

        Raises:
            LookupError: If the memoryset does not exist and if_not_exists is `"error"`
        """
        try:
            delete_memoryset(name_or_id)
            logging.info(f"Deleted memoryset {name_or_id}")
        except LookupError:
            if if_not_exists == "error":
                raise

    def set(self, *, name: str = UNSET, description: str | None = UNSET, label_names: list[str] = UNSET):
        """
        Update editable attributes of the memoryset

        Note:
            If a field is not provided, it will default to [UNSET][orca_sdk.UNSET] and not be updated.

        Params:
            description: Value to set for the description
            name: Value to set for the name
            label_names: Value to replace existing label names with
        """
        update_memoryset(
            self.id,
            body=MemorysetUpdate(
                name=name if name is not UNSET else CLIENT_UNSET,
                description=description if description is not UNSET else CLIENT_UNSET,
                label_names=label_names if label_names is not UNSET else CLIENT_UNSET,
            ),
        )
        self.refresh()

    @overload
    def clone(
        self,
        name: str,
        *,
        embedding_model: PretrainedEmbeddingModel | FinetunedEmbeddingModel | None = None,
        max_seq_length_override: int | None = None,
        prompt: str | None = None,
        if_exists: CreateMode = "error",
        background: Literal[True],
    ) -> Job[Self]:
        pass

    @overload
    def clone(
        self,
        name: str,
        *,
        embedding_model: PretrainedEmbeddingModel | FinetunedEmbeddingModel | None = None,
        max_seq_length_override: int | None = None,
        prompt: str | None = None,
        if_exists: CreateMode = "error",
        background: Literal[False] = False,
    ) -> Self:
        pass

    def clone(
        self,
        name: str,
        *,
        embedding_model: PretrainedEmbeddingModel | FinetunedEmbeddingModel | None = None,
        max_seq_length_override: int | None = None,
        prompt: str | None = None,
        if_exists: CreateMode = "error",
        background: bool = False,
    ) -> Self | Job[Self]:
        """
        Create a clone of the memoryset with a new name

        Params:
            name: Name for the new memoryset (must be unique)
            embedding_model: Optional new embedding model to use for re-embedding the memory values
                value is longer than this it will be truncated, will default to the model's max
                sequence length if not provided
            document_prompt_override: Optional custom document prompt to use for the cloned memoryset.
                If not provided, will use the source memoryset's document prompt.
            query_prompt_override: Optional custom query prompt to use for the cloned memoryset.
                If not provided, will use the source memoryset's query prompt.
            if_exists: What to do if a memoryset with the same name already exists, defaults to
                `"error"`. Other option is `"open"` to open the existing memoryset.

        Returns:
            Handle to the cloned memoryset in the OrcaCloud

        Examples:
            >>> memoryset = LabeledMemoryset.open("my_memoryset")
            >>> finetuned_embedding_model = PretrainedEmbeddingModel.GTE_BASE.finetune(
            ...     "gte_base_finetuned", my_memoryset
            ... )
            >>> new_memoryset = memoryset.clone(
            ...     "my_memoryset_finetuned", embedding_model=finetuned_embedding_model,
            ... )

            >>> # Clone with custom prompts
            >>> new_memoryset = memoryset.clone(
            ...     "my_memoryset_with_prompts",
            ...     document_prompt_override="Represent this document for retrieval:",
            ...     query_prompt_override="Represent this query for retrieval:",
            ... )
        """
        if self.exists(name):
            if if_exists == "error":
                raise ValueError(f"Memoryset with name {name} already exists")
            elif if_exists == "open":
                existing = self.open(name)
                for attribute in {"embedding_model"}:
                    if locals()[attribute] is not None and locals()[attribute] != getattr(existing, attribute):
                        raise ValueError(f"Memoryset with name {name} already exists with a different {attribute}.")
                return existing

        metadata = clone_memoryset(
            self.id,
            body=CloneMemorysetRequest(
                name=name,
                pretrained_embedding_model_name=(
                    embedding_model._model_name if isinstance(embedding_model, PretrainedEmbeddingModel) else None
                ),
                finetuned_embedding_model_id=(
                    embedding_model.id if isinstance(embedding_model, FinetunedEmbeddingModel) else None
                ),
                max_seq_length_override=max_seq_length_override,
                prompt=prompt,
            ),
        )
        job = Job(
            metadata.insertion_task_id,
            lambda: self.open(metadata.id),
        )
        return job if background else job.result()

    def refresh(self, throttle: float = 0):
        """
        Refresh the information about the memoryset from the OrcaCloud

        Params:
            throttle: Minimum time in seconds between refreshes
        """
        current_time = datetime.now()
        # Skip refresh if last refresh was too recent
        if (current_time - self._last_refresh) < timedelta(seconds=throttle):
            return

        self.__dict__.update(self.open(self.id).__dict__)
        self._last_refresh = current_time

    def __len__(self) -> int:
        """Get the number of memories in the memoryset"""
        self.refresh(throttle=5)
        return self.length

    @overload
    def __getitem__(self, index: int | str) -> MemoryT:
        pass

    @overload
    def __getitem__(self, index: slice) -> list[MemoryT]:
        pass

    def __getitem__(self, index: int | slice | str) -> MemoryT | list[MemoryT]:
        """
        Get memories from the memoryset by index or memory id

        Params:
            index: Index or memory to retrieve or slice of memories to retrieve or unique
                identifier of the memory to retrieve

        Returns:
            Memory or memories from the memoryset

        Raises:
            LookupError: If the id is not found or the index is out of bounds

        Examples:
            Retrieve the first memory in the memoryset:
            >>> memoryset[0]
            LabeledMemory({ label: <positive: 1>, value: 'I am happy' })

            Retrieve the last memory in the memoryset:
            >>> memoryset[-1]
            LabeledMemory({ label: <negative: 0>, value: 'I am sad' })

            Retrieve a slice of memories in the memoryset:
            >>> memoryset[1:3]
            [
                LabeledMemory({ label: <positive: 1>, value: 'I am happy' }),
                LabeledMemory({ label: <negative: 0>, value: 'I am sad' }),
            ]

            Retrieve a memory by id:
            >>> memoryset["0195019a-5bc7-7afb-b902-5945ee1fb766"]
            LabeledMemory({ label: <positive: 1>, value: 'I am happy' })
        """
        if isinstance(index, int):
            return self.query(offset=len(self) + index if index < 0 else index, limit=1)[0]
        elif isinstance(index, str):
            return self.get(index)
        elif isinstance(index, slice):
            start = 0 if index.start is None else (len(self) + index.start) if index.start < 0 else index.start
            stop = len(self) if index.stop is None else (len(self) + index.stop) if index.stop < 0 else index.stop
            return self.query(offset=start, limit=stop - start)
        else:
            raise ValueError(f"Invalid index type: {type(index)}")

    @overload
    def search(self, query: str, *, count: int = 1, prompt: str | None = None) -> list[MemoryLookupT]:
        pass

    @overload
    def search(self, query: list[str], *, count: int = 1, prompt: str | None = None) -> list[list[MemoryLookupT]]:
        pass

    def search(
        self, query: str | list[str], *, count: int = 1, prompt: str | None = None
    ) -> list[MemoryLookupT] | list[list[MemoryLookupT]]:
        """
        Search for memories that are semantically similar to the query

        Params:
            query: Query to lookup memories in the memoryset, can be a single query or a list
            count: Number of memories to return for each query
            prompt: Optional prompt for query embedding during search.
                If not provided, the memoryset's default query prompt will be used if available.

        Returns:
            List of memories from the memoryset that match the query. If a single query is provided,
                the return value is a list containing a single list of memories. If a list of
                queries is provided, the return value is a list of lists of memories.

        Examples:
            Search for similar memories:
            >>> memoryset.search("I am happy", count=2)
            [
                LabeledMemoryLookup({ label: <positive: 1>, value: 'I am happy' }),
                LabeledMemoryLookup({ label: <positive: 1>, value: 'I am content' }),
            ]

            Search with custom query prompt for instruction-following models:
            >>> memoryset.search("I am happy", count=2, query_prompt="Represent this query for sentiment retrieval:")
            [
                LabeledMemoryLookup({ label: <positive: 1>, value: 'I am happy' }),
                LabeledMemoryLookup({ label: <positive: 1>, value: 'I am content' }),
            ]

            Search for similar memories for multiple queries:
            >>> memoryset.search(["I am happy", "I am sad"], count=1)
            [
                [
                    LabeledMemoryLookup({ label: <positive: 1>, value: 'I am happy' }),
                ],
                [
                    LabeledMemoryLookup({ label: <negative: 0>, value: 'I am sad' }),
                ],
            ]
        """
        response = memoryset_lookup_gpu(
            name_or_id=self.id,
            body=LookupRequest(
                query=query if isinstance(query, list) else [query],
                count=count,
                prompt=prompt,
            ),
        )
        lookups = [
            [
                cast(
                    MemoryLookupT,
                    (
                        LabeledMemoryLookup(self.id, lookup_response)
                        if isinstance(lookup_response, LabeledMemoryLookupResponse)
                        else ScoredMemoryLookup(self.id, lookup_response)
                    ),
                )
                for lookup_response in batch
            ]
            for batch in response
        ]
        return lookups if isinstance(query, list) else lookups[0]

    def query(
        self,
        offset: int = 0,
        limit: int = 100,
        filters: list[FilterItemTuple] = [],
        with_feedback_metrics: bool = False,
        sort: list[TelemetrySortItem] | None = None,
    ) -> list[MemoryT]:
        """
        Query the memoryset for memories that match the filters

        Params:
            offset: The offset of the first memory to return
            limit: The maximum number of memories to return
            filters: List of filters to apply to the query.
            with_feedback_metrics: Whether to include feedback metrics in the response

        Returns:
            List of memories from the memoryset that match the filters

        Examples:
            >>> memoryset.query(filters=[("label", "==", 0)], limit=2)
            [
                LabeledMemory({ label: <positive: 1>, value: "I am happy" }),
                LabeledMemory({ label: <negative: 0>, value: "I am sad" }),
            ]
        """
        parsed_filters = [
            _parse_filter_item_from_tuple(filter) if isinstance(filter, tuple) else filter for filter in filters
        ]

        if with_feedback_metrics:
            return [
                cast(
                    MemoryT,
                    (
                        LabeledMemory(self.id, memory)
                        if isinstance(memory, LabeledMemoryWithFeedbackMetrics)
                        else ScoredMemory(self.id, memory)
                    ),
                )
                for memory in list_memories_with_feedback(
                    body=TelemetryMemoriesRequest(
                        memoryset_id=self.id,
                        offset=offset,
                        limit=limit,
                        filters=parsed_filters,
                        sort=[_parse_sort_item_from_tuple(item) for item in sort] if sort else None,
                    ),
                ).items
            ]

        if any(isinstance(filter, TelemetryFilterItem) for filter in parsed_filters):
            raise ValueError("Feedback metrics are only supported when the with_feedback_metrics flag is set to True")

        if sort:
            logging.warning("Sorting is not supported when with_feedback_metrics is False. Sort value will be ignored.")

        return [
            cast(
                MemoryT,
                (
                    LabeledMemory(self.id, memory)
                    if isinstance(memory, LabeledMemoryResponse)
                    else ScoredMemory(self.id, memory)
                ),
            )
            for memory in query_memoryset(
                self.id,
                body=ListMemoriesRequest(
                    offset=offset,
                    limit=limit,
                    filters=cast(list[FilterItem], parsed_filters),
                ),
            )
        ]

    def insert(self, items: Iterable[dict[str, Any]] | dict[str, Any]) -> None:
        """
        Insert memories into the memoryset

        Params:
            items: List of memories to insert into the memoryset. This should be a list of
                dictionaries with the following keys:

                - `value`: Value of the memory
                - `label`: Label of the memory
                - `score`: Score of the memory
                - `source_id`: Optional unique ID of the memory in a system of reference
                - `...`: Any other metadata to store for the memory

        Examples:
            >>> memoryset.insert([
            ...     {"value": "I am happy", "label": 1, "source_id": "user_123", "tag": "happy"},
            ...     {"value": "I am sad", "label": 0, "source_id": "user_124", "tag": "sad"},
            ... ])
        """
        insert_memories_gpu(
            self.id,
            body=(
                cast(
                    list[LabeledMemoryInsert] | list[ScoredMemoryInsert],
                    [
                        _parse_memory_insert(memory, type=self.memory_type)
                        for memory in (cast(list[dict[str, Any]], [items]) if isinstance(items, dict) else items)
                    ],
                )
            ),
        )
        self.refresh()

    @overload
    def get(self, memory_id: str) -> MemoryT:  # type: ignore -- this takes precedence
        pass

    @overload
    def get(self, memory_id: Iterable[str]) -> list[MemoryT]:
        pass

    def get(self, memory_id: str | Iterable[str]) -> MemoryT | list[MemoryT]:
        """
        Fetch a memory or memories from the memoryset

        Params:
            memory_id: Unique identifier of the memory or memories to fetch

        Returns:
            Memory or list of memories from the memoryset

        Raises:
            LookupError: If no memory with the given id is found

        Examples:
            Fetch a single memory:
            >>> memoryset.get("0195019a-5bc7-7afb-b902-5945ee1fb766")
            LabeledMemory({ label: <positive: 1>, value: 'I am happy' })

            Fetch multiple memories:
            >>> memoryset.get([
            ...     "0195019a-5bc7-7afb-b902-5945ee1fb766",
            ...     "019501a1-ea08-76b2-9f62-95e4800b4841",
            ... ])
            [
                LabeledMemory({ label: <positive: 1>, value: 'I am happy' }),
                LabeledMemory({ label: <negative: 0>, value: 'I am sad' }),
            ]
        """
        if isinstance(memory_id, str):
            response = get_memory(self.id, memory_id)
            return cast(
                MemoryT,
                (
                    LabeledMemory(self.id, response)
                    if isinstance(response, LabeledMemoryResponse)
                    else ScoredMemory(self.id, response)
                ),
            )
        else:
            response = get_memories(self.id, body=GetMemoriesRequest(memory_ids=list(memory_id)))
            return [
                cast(
                    MemoryT,
                    (
                        LabeledMemory(self.id, memory)
                        if isinstance(memory, LabeledMemoryResponse)
                        else ScoredMemory(self.id, memory)
                    ),
                )
                for memory in response
            ]

    @overload
    def update(self, updates: dict[str, Any]) -> MemoryT:
        pass

    @overload
    def update(self, updates: Iterable[dict[str, Any]]) -> list[MemoryT]:
        pass

    def update(self, updates: dict[str, Any] | Iterable[dict[str, Any]]) -> MemoryT | list[MemoryT]:
        """
        Update one or multiple memories in the memoryset

        Params:
            updates: List of updates to apply to the memories. Each update should be a dictionary
                with the following keys:

                - `memory_id`: Unique identifier of the memory to update (required)
                - `value`: Optional new value of the memory
                - `label`: Optional new label of the memory
                - `source_id`: Optional new source ID of the memory
                - `...`: Optional new values for metadata properties

        Returns:
            Updated memory or list of updated memories

        Examples:
            Update a single memory:
            >>> memoryset.update(
            ...     {
            ...         "memory_id": "019501a1-ea08-76b2-9f62-95e4800b4841",
            ...         "tag": "happy",
            ...     },
            ... )

            Update multiple memories:
            >>> memoryset.update(
            ...     {"memory_id": m.memory_id, "label": 2}
            ...     for m in memoryset.query(filters=[("tag", "==", "happy")])
            ... )
        """
        response = update_memories_gpu(
            self.id,
            body=cast(
                list[LabeledMemoryUpdate] | list[ScoredMemoryUpdate],
                [
                    _parse_memory_update(update, type=self.memory_type)
                    for update in (cast(list[dict[str, Any]], [updates]) if isinstance(updates, dict) else updates)
                ],
            ),
        )
        updated_memories = [
            cast(
                MemoryT,
                (
                    LabeledMemory(self.id, memory)
                    if isinstance(memory, LabeledMemoryResponse)
                    else ScoredMemory(self.id, memory)
                ),
            )
            for memory in response
        ]
        return updated_memories[0] if isinstance(updates, dict) else updated_memories

    def get_cascading_edits_suggestions(
        self,
        memory: MemoryT,
        *,
        old_label: int,
        new_label: int,
        max_neighbors: int = 50,
        max_validation_neighbors: int = 10,
        similarity_threshold: float | None = None,
        only_if_has_old_label: bool = True,
        exclude_if_new_label: bool = True,
        suggestion_cooldown_time: float = 3600.0 * 24.0,  # 1 day
        label_confirmation_cooldown_time: float = 3600.0 * 24.0 * 7,  # 1 week
    ) -> list[CascadingEditSuggestion]:
        """
        Suggests cascading edits for a given memory based on nearby points with similar labels.

        This function is triggered after a user changes a memory's label. It looks for nearby
        candidates in embedding space that may be subject to similar relabeling and returns them
        as suggestions. The system uses scoring heuristics, label filters, and cooldown tracking
        to reduce noise and improve usability.

        Params:
            memory: The memory whose label was just changed.
            old_label: The label this memory used to have.
            new_label: The label it was changed to.
            max_neighbors: Maximum number of neighbors to consider.
            max_validation_neighbors: Maximum number of neighbors to use for label suggestion.
            similarity_threshold: If set, only include neighbors with a lookup score above this threshold.
            only_if_has_old_label: If True, only consider neighbors that have the old label.
            exclude_if_new_label: If True, exclude neighbors that already have the new label.
            suggestion_cooldown_time: Minimum time (in seconds) since the last suggestion for a neighbor
                to be considered again.
            label_confirmation_cooldown_time: Minimum time (in seconds) since a neighbor's label was confirmed
                to be considered for suggestions.
            _current_time: Optional override for the current timestamp (useful for testing).

        Returns:
            A list of CascadingEditSuggestion objects, each containing a neighbor and the suggested new label.
        """

        return suggest_cascading_edits(
            name_or_id=self.id,
            memory_id=memory.memory_id,
            body=CascadeEditSuggestionsRequest(
                old_label=old_label,
                new_label=new_label,
                max_neighbors=max_neighbors,
                max_validation_neighbors=max_validation_neighbors,
                similarity_threshold=similarity_threshold,
                only_if_has_old_label=only_if_has_old_label,
                exclude_if_new_label=exclude_if_new_label,
                suggestion_cooldown_time=suggestion_cooldown_time,
                label_confirmation_cooldown_time=label_confirmation_cooldown_time,
            ),
        )

    def delete(self, memory_id: str | Iterable[str]) -> None:
        """
        Delete memories from the memoryset

        Params:
            memory_id: unique identifiers of the memories to delete

        Examples:
            Delete a single memory:
            >>> memoryset.delete("0195019a-5bc7-7afb-b902-5945ee1fb766")

            Delete multiple memories:
            >>> memoryset.delete([
            ...     "0195019a-5bc7-7afb-b902-5945ee1fb766",
            ...     "019501a1-ea08-76b2-9f62-95e4800b4841",
            ... )

        """
        memory_ids = [memory_id] if isinstance(memory_id, str) else list(memory_id)
        delete_memories(self.id, body=DeleteMemoriesRequest(memory_ids=memory_ids))
        logging.info(f"Deleted {len(memory_ids)} memories from memoryset.")
        self.refresh()

    @overload
    def analyze(
        self,
        *analyses: Iterable[dict[str, Any] | str],
        lookup_count: int = 15,
        clear_metrics: bool = False,
        background: Literal[True],
    ) -> Job[dict]:
        pass

    @overload
    def analyze(
        self,
        *analyses: Iterable[dict[str, Any] | str],
        lookup_count: int = 15,
        clear_metrics: bool = False,
        background: Literal[False] = False,
    ) -> dict:
        pass

    def analyze(
        self,
        *analyses: Iterable[dict[str, Any] | str],
        lookup_count: int = 15,
        clear_metrics: bool = False,
        background: bool = False,
    ) -> Job[dict] | dict:
        """
        Run analyses on the memoryset to find duplicates, clusters, mislabelings, and more

        The results of the analysis will be stored in the [`LabeledMemory.metrics`][orca_sdk.LabeledMemory]
        attribute of each memory in the memoryset. Overall memoryset metrics will be returned as a dictionary.

        Params:
            analyses: List of analysis to run on the memoryset, can either be just the name of an
                analysis or a dictionary with a name property and additional config. The available
                analyses are:

                - **`"duplicate"`**: Find potentially duplicate memories in the memoryset
                - **`"cluster"`**: Cluster the memories in the memoryset
                - **`"label"`**: Analyze the labels to find potential mislabelings
                - **`"neighbor"`**: Analyze the neighbors to populate anomaly scores
                - **`"projection"`**: Create a 2D projection of the embeddings for visualization

            lookup_count: Number of memories to lookup for each memory in the memoryset
            clear_metrics: Whether to clear any existing metrics from the memories before running the analysis

        Returns:
            dictionary with aggregate metrics for each analysis that was run

        Raises:
            ValueError: If an invalid analysis name is provided

        Examples:
            Run label and duplicate analysis:
            >>> memoryset.analyze("label", {"name": "duplicate", "possible_duplicate_threshold": 0.99})
            { "duplicate": { "num_duplicates": 10 },
              "label": {
                "label_metrics": [{
                    "label": 0,
                    "label_name": "negative",
                    "average_lookup_score": 0.95,
                    "memory_count": 100,
                }, {
                    "label": 1,
                    "label_name": "positive",
                    "average_lookup_score": 0.90,
                    "memory_count": 100,
                }]
                "neighbor_prediction_accuracy": 0.95,
                "mean_neighbor_label_confidence": 0.95,
                "mean_neighbor_label_entropy": 0.95,
                "mean_neighbor_predicted_label_ambiguity": 0.95,
              }
            }

            Remove all exact duplicates:
            >>> memoryset.delete(
            ...     m.memory_id
            ...     for m in memoryset.query(
            ...         filters=[("metrics.is_duplicate", "==", True)]
            ...     )
            ... )

            Display label analysis to review potential mislabelings:
            >>> memoryset.display_label_analysis()
        """

        # Get valid analysis names from MemorysetAnalysisConfigs
        valid_analysis_names = {
            field.name for field in fields(MemorysetAnalysisConfigs) if field.name != "additional_properties"
        }

        configs: dict[str, dict] = {}
        for analysis in analyses:
            if isinstance(analysis, str):
                error_msg = (
                    f"Invalid analysis name: {analysis}. Valid names are: {', '.join(sorted(valid_analysis_names))}"
                )
                if analysis not in valid_analysis_names:
                    raise ValueError(error_msg)
                configs[analysis] = {}
            else:
                name = analysis.pop("name")  # type: ignore
                error_msg = f"Invalid analysis name: {name}. Valid names are: {', '.join(sorted(valid_analysis_names))}"
                if name not in valid_analysis_names:
                    raise ValueError(error_msg)
                configs[name] = analysis  # type: ignore

        analysis = analyze_memoryset(
            self.id,
            body=MemorysetAnalysisRequest(
                configs=MemorysetAnalysisConfigs.from_dict(configs),
                lookup_count=lookup_count,
                clear_metrics=clear_metrics,
            ),
        )
        job = Job(
            analysis.task_id,
            lambda: (r := get_analysis(self.id, analysis.task_id).results) and r.to_dict(),
        )
        return job if background else job.result()

    def get_potential_duplicate_groups(self):
        """Group potential duplicates in the memoryset"""
        response = potential_duplicate_groups(self.name)
        return response

    @overload
    @staticmethod
    def run_embedding_evaluation(
        datasource: Datasource,
        *,
        value_column: str = "value",
        label_column: str = "label",
        source_id_column: str | None = None,
        neighbor_count: int = 5,
        embedding_models: list[str] | None = None,
        background: Literal[True],
    ) -> Job[dict]:
        pass

    @overload
    @staticmethod
    def run_embedding_evaluation(
        datasource: Datasource,
        *,
        value_column: str = "value",
        label_column: str = "label",
        source_id_column: str | None = None,
        neighbor_count: int = 5,
        embedding_models: list[str] | None = None,
        background: Literal[False] = False,
    ) -> dict:
        pass

    @staticmethod
    def run_embedding_evaluation(
        datasource: Datasource,
        *,
        value_column: str = "value",
        label_column: str = "label",
        source_id_column: str | None = None,
        neighbor_count: int = 5,
        embedding_models: list[str] | None = None,
        background: bool = False,
    ) -> Job[dict] | dict:
        """
        Test the quality of embeddings for the datasource by computing metrics such as prediction accuracy.

        Params:
            datasource: The datasource to run the embedding evaluation on
            value_column: Name of the column in the datasource that contains the memory values
            label_column: Name of the column in the datasource that contains the memory labels,
                these must be contiguous integers starting from 0
            source_id_column: Optional name of the column in the datasource that contains the ids in
                the system of reference
            neighbor_count: The number of neighbors to select for prediction
            embedding_models: Optional list of embedding model keys to evaluate, if not provided all
                available embedding models will be used

        Returns:
            A dictionary containing the results of the embedding evaluation
        """

        if embedding_models is not None:
            embedding_model_enums: list[PretrainedEmbeddingModelName | str] | None = [
                PretrainedEmbeddingModelName(model) for model in embedding_models
            ]
        else:
            embedding_model_enums: list[PretrainedEmbeddingModelName | str] | None = None

        request = EmbeddingEvaluationRequest(
            value_column=value_column,
            label_column=label_column,
            source_id_column=source_id_column,
            neighbor_count=neighbor_count,
            embedding_models=embedding_model_enums,
        )

        response = create_embedding_evaluation(name_or_id=datasource.id, body=request)
        job = Job(
            response.task_id,
            lambda: (r := get_embedding_evaluation(datasource.id, response.task_id).result) and r.to_dict(),
        )
        return job if background else job.result()


class LabeledMemoryset(_Memoryset[LabeledMemory, LabeledMemoryLookup]):
    """
    A Handle to a collection of memories with labels in the OrcaCloud

    Attributes:
        id: Unique identifier for the memoryset
        name: Unique name of the memoryset
        description: Description of the memoryset
        label_names: Names for the class labels in the memoryset
        length: Number of memories in the memoryset
        embedding_model: Embedding model used to embed the memory values for semantic search
        created_at: When the memoryset was created, automatically generated on create
        updated_at: When the memoryset was last updated, automatically updated on updates
    """

    label_names: list[str]
    memory_type: MemoryType = MemoryType.LABELED

    def __init__(self, metadata: MemorysetMetadata):
        super().__init__(metadata)
        assert metadata.label_names is not None
        self.label_names = metadata.label_names

    def __eq__(self, other) -> bool:
        return isinstance(other, LabeledMemoryset) and self.id == other.id

    @classmethod
    def create(cls, name: str, datasource: Datasource, *, label_column: str | None = "label", **kwargs):
        return super().create(name, datasource, label_column=label_column, score_column=None, **kwargs)

    def display_label_analysis(self):
        """Display a UI to review and act upon the label analysis results"""
        from ._utils.analysis_ui import display_suggested_memory_relabels

        display_suggested_memory_relabels(self)


class ScoredMemoryset(_Memoryset[ScoredMemory, ScoredMemoryLookup]):
    """
    A Handle to a collection of memories with scores in the OrcaCloud

    Attributes:
        id: Unique identifier for the memoryset
        name: Unique name of the memoryset
        description: Description of the memoryset
        length: Number of memories in the memoryset
        embedding_model: Embedding model used to embed the memory values for semantic search
        created_at: When the memoryset was created, automatically generated on create
        updated_at: When the memoryset was last updated, automatically updated on updates
    """

    memory_type: MemoryType = MemoryType.SCORED

    def __eq__(self, other) -> bool:
        return isinstance(other, ScoredMemoryset) and self.id == other.id

    @classmethod
    def create(cls, name: str, datasource: Datasource, *, score_column: str | None = "score", **kwargs):
        return super().create(name, datasource, score_column=score_column, label_column=None, **kwargs)
