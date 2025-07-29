"""Types used by soil library"""

# pylint:disable=unnecessary-ellipsis
from enum import StrEnum
from typing import (
    Dict,
    List,
    Literal,
    NotRequired,
    Protocol,
    Self,
    Type,
    TypedDict,
    TypeVar,
)

from numpy import ndarray
from pandas import DataFrame

from soil.storage.base_storage import BaseStorage

DEFAULT_TIMEOUT = 60 * 60

Plan = List[Dict[str, str]]

_TypedDict = TypeVar("_TypedDict", bound=TypedDict)  # type: ignore
type DataObject = dict | list | ndarray | DataFrame | _TypedDict


class GetModule(TypedDict):
    """Type for GET modules/:moduleId"""

    is_package: bool
    public_api: List[str]
    package_type: str


class GetModuleHash(TypedDict):
    """Type for GET modules/"""

    name: str
    hash: str


type ExperimentStatuses = Literal["WAITING", "EXECUTING", "DONE", "ERROR"]


class Experiment(TypedDict):
    """Type for GET experiments/:experimentId"""

    _id: str
    app_id: str
    outputs: Dict[str, str]
    experiment_status: ExperimentStatuses
    experiment_group: NotRequired[str]
    status: Dict[str, ExperimentStatuses]
    created_at: int


class Result(TypedDict):
    """Type for GET results/:resultId"""

    _id: str
    type: str


class _TypedDict(TypedDict):
    """Makes pyright happy"""

    pass


class SerializableDataStructure[Storage: BaseStorage, MetadataDict: _TypedDict](
    Protocol
):
    """Data Strucutre base protocol"""

    metadata: MetadataDict

    def serialize(self) -> Storage:
        """Serializes the DS."""
        ...

    @classmethod
    def deserialize(
        cls: Type[Self],
        storage: Storage,
        metadata: MetadataDict,
    ) -> "SerializableDataStructure[Storage, MetadataDict]":
        """Deserialize DS method."""
        ...


class DataStructure(Protocol):
    """Data Structure Protocol"""

    @property
    def metadata(self) -> dict:
        """Get the metadata of the DS"""
        ...

    @property
    def data(self) -> dict:
        """Get the data of the DS"""
        ...

    def get_data(self, **kwargs) -> dict:
        """Get the data of the DS"""
        ...


type JobStatuses = ExperimentStatuses


class Job(Protocol):
    """Job Protocol"""

    @property
    def group(self) -> str:
        """Get the group of the job"""
        ...

    @property
    def created_at(self) -> str:
        """Get the created at of the job"""
        ...

    @property
    def status(self) -> JobStatuses:
        """Get the status of the job"""
        ...

    @property
    def data(self) -> DataStructure:
        """Get the data of the job"""
        ...


class TypeLog(StrEnum):
    """Types of Logs."""

    PROCESSED = "processed"
    NOT_CONSISTENT = "not_consistent"
    NOT_PROCESSED = "not_processed"


class SaveGraphStateRequest(TypedDict):
    """Request to save the graph state"""

    id: str
    title: str
    user_question: str
    remaining_steps: int
    project_id: str
    next_node: str
    user_roles: list[str]
    user_id: str
    question_interpretation: str
    evaluation: str
    action_plan: list[str]
    message_id: str | None
    retries: int


class GraphStateResponse(TypedDict):
    """Graph state response."""

    id: str
    user_question: str
    remaining_steps: int
    project_id: str
    case_mix_store_id: str
    dataset_alias: str
    next_node: str
    title: str
    created_at: str
    updated_at: str
    question_interpretation: str
    evaluation: str
    action_plan: list[str]
    message_id: str | None
    retries: int


class StoredGraphState(TypedDict):
    """Graph state."""

    id: str
    user_question: str
    remaining_steps: int
    project_id: str
    dataset_id: str
    next_node: str


class PipelineForRequest(TypedDict):
    """Pipeline for request."""

    id: str
    model_id: str
    prompt_version: str
    explanation: str
    description: str
    type: str


class Project(TypedDict):
    """Project of the super agent."""

    id: str
    name: str


class Dataset(TypedDict):
    """Dataset context"""

    alias: str
    name: str


class Pipeline(TypedDict):
    """Pipeline context"""

    id: str
    name: str
    type: str
    description: str | None
    explanation: str | None
    model_id: str | None
    prompt_version: str | None


class Subset(TypedDict):
    """Filter context"""

    id: str
    pipeline: Pipeline
    subsets: list["Subset"]
    pipelines: list[Pipeline]


class Context(TypedDict):
    """Context of the super agent."""

    project: Project
    root: Subset
    dataset: Dataset


class CreateGraphLogRequest(TypedDict):
    """Create graph log request."""

    id: NotRequired[str]
    user_id: str
    node: str
    log: str
