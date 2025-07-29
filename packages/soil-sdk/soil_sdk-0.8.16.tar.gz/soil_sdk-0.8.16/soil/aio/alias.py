"""Package that contains calls for soil alias data structures"""

from typing import Any, cast

from soil.aio.api import set_alias
from soil.data_structure import DataStructure
from soil.types import DEFAULT_TIMEOUT, SerializableDataStructure


async def alias(
    name: str,
    data_ref: DataStructure | SerializableDataStructure,
    roles: list[str] | None = None,
    extras: dict[str, Any] | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> None:
    """Set an alias to a data reference asynchronously"""
    # Force to get an id if there is none yet.
    data_ref = cast(DataStructure, data_ref)
    if data_ref.id is None:
        await data_ref.async_get_id(timeout=timeout)
    assert isinstance(data_ref.id, str)
    await set_alias(name, data_ref.id, roles, extras)
