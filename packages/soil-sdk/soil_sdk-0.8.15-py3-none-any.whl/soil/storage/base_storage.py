"""Module for BaseStorage"""

from dataclasses import dataclass
from typing import Any, Type, TypeVar

StorageClass = TypeVar("StorageClass")


@dataclass
class BaseStorage:
    """Abstract class that implements serialize and deserialize methods for storage classes."""

    def serialize(self) -> dict[str, Any]:
        """Serializes the storage object. In general it shouldn't be used from a module."""

    @classmethod
    def deserialize(
        cls: Type[StorageClass], serialized_storage_object: dict[str, Any]
    ) -> StorageClass:
        """Takes a serialized storage object and returns an instance."""
