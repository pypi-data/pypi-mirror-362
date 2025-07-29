"""Defines soil.data()"""

from typing import (
    Any,
    Dict,
    Optional,
    Type,
    cast,
    overload,
)

from soil import errors
from soil.api import get_alias, get_result, upload_data
from soil.data_structure import DataStructure, get_data_structure_name_and_serialize
from soil.types import DataObject, SerializableDataStructure


@overload
def data(
    data_object: str,
    metadata: None = None,
    *,
    return_type: None = None,
) -> DataStructure: ...


@overload
def data[G: SerializableDataStructure](
    data_object: str,
    metadata: None = None,
    *,
    return_type: Type[G],
) -> G: ...


@overload
def data[G: SerializableDataStructure](
    data_object: str,
    metadata: None = None,
    *,
    return_type: G,
) -> G: ...


@overload
def data[D: DataObject](
    data_object: D,
    metadata: dict[str, Any] | None = None,
    *,
    return_type: None = None,
) -> DataStructure[D]: ...


@overload
def data[G: SerializableDataStructure](
    data_object: DataObject,
    metadata: dict[str, Any] | None = None,
    *,
    return_type: Type[G],
) -> G: ...


@overload
def data[G: SerializableDataStructure](
    data_object: DataObject,
    metadata: dict[str, Any] | None = None,
    *,
    return_type: G,
) -> G: ...


def data[D: DataObject, G: SerializableDataStructure](  # pyright: ignore[reportInconsistentOverload]
    data_object: str | D,
    metadata: dict[str, Any] | None = None,
    *,
    return_type: Type[G] | G | None = None,
) -> G | DataStructure | DataStructure[D]:
    """Load data from the cloud or mark it as uploadable"""
    if return_type is None:
        cast_return_type = DataStructure
    elif isinstance(return_type, type):
        cast_return_type = return_type
    else:
        # return_type is a union type instance
        cast_return_type = (
            type(return_type) if hasattr(return_type, "__class__") else return_type
        )
    if isinstance(data_object, str):
        # Data object is an id or an alias
        try:
            data_object = _load_data_alias(data_object)
        except errors.DataNotFound:
            pass
        return cast(cast_return_type, _load_data_id(data_object))  # pyright: ignore
    return cast(
        cast_return_type,  # pyright: ignore
        _upload_data(data_object, metadata),
    )


def _upload_data(
    data_object: Any, metadata: Optional[Dict[str, Any]] = None
) -> DataStructure:
    ds_name, serialized = get_data_structure_name_and_serialize(data_object)
    result = upload_data(ds_name, serialized, metadata)
    ds = DataStructure(result["_id"], dstype=result["type"])
    return ds


def _load_datastructure(did: str, dtype: str) -> DataStructure:
    # TODO: dynamically load a data structure
    return DataStructure(did, dstype=dtype)


def _load_data_alias(alias: str) -> str:
    return get_alias(alias)["state"]["result_id"]


def _load_data_id(data_id: str) -> DataStructure:
    result = get_result(data_id)
    return _load_datastructure(result["_id"], result["type"])
