"""Module for Object Storage"""

from dataclasses import dataclass
from typing import Any, Dict, Optional

from soil.storage.base_storage import BaseStorage


@dataclass
class ObjectStorage(BaseStorage):
    """Implements basic Object Storage using s3 api. If there are no s3 credentials
    it fallsback to disk. Before storing the data they are compressed with zlib.

    Example:
    -------
        class ObjectDS(DataStructure):
        def serialize(self):
            obj_storage = ObjectStorage()
            obj_storage.put_object(json.dumps(self.data).encode('utf-8'))
            return obj_storage

        @staticmethod
        def deserialize(obj_storage: ObjectStorage, metadata):
            raw_data = obj_storage.get_object()
            data = json.loads(raw_data.decode('utf-8'))
            return ObjectDS(data, metadata, storage=obj_storage)

        def get_data(self):
            return self.data

    Attributes:
    ----------
        path: str = '': An optional folder to store the data to.
        obj_name: Optional[str]: The obj_name can optionally be provided. Otherwise
            a unique name will be generated. Caution! Existing data for the same app
            will be overwritten if the same name is used twice.
        metadata: Optional[Dict[str, Any]]: Experimental. Metadata to be stored in the s3 storage.

    """

    path: str = ""
    obj_name: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def put_object(self, obj: bytes) -> None:
        """Compressess an object and stores it."""

    def get_object(self) -> bytes:
        """Gets the object back and decompresses it."""
