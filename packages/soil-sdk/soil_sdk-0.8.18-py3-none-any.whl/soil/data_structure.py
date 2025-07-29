"""Module that implements a Data Structure"""

import json
import os
from typing import Any, Dict, Optional, Tuple, Union, cast

from soil import api, errors
from soil.aio import api as aio_api
from soil.pipeline import Pipeline
from soil.types import DEFAULT_TIMEOUT, DataObject

try:
    import numpy  # type: ignore

    NUMPY_ENABLED = True
except ModuleNotFoundError:
    NUMPY_ENABLED = False
try:
    import pandas  # type: ignore

    PANDAS_ENABLED = True
except ModuleNotFoundError:
    PANDAS_ENABLED = False


DS_NAMESPACE = "soil.data_structures.predefined."


class DataStructure[D: DataObject]:
    """Data Structure class"""

    def __init__(  # noqa: D107
        self,
        did: Optional[str] = None,
        sym_id: Optional[str] = None,
        data: Optional[D] = None,
        metadata: Optional[Dict[str, Any]] = None,
        pipeline: Optional[Pipeline] = None,
        dstype: Optional[str] = None,
    ):
        self.id = did  # Result id
        self.sym_id = sym_id  # Symbolic id used in the pipeline
        self.data = cast(D, data)
        self.metadata = metadata
        self.pipeline = pipeline
        self.dstype = dstype

    async def async_get_data(
        self, **kwargs: Dict[str, Any]
    ) -> Dict[Union[str, int], Any]:
        """Asynchronously invoke the get_data() method from the data structure in the cloud."""
        result_id = await self.async_get_id()
        result = await aio_api.get_result_data(
            result_id, query={k: json.dumps(v) for k, v in kwargs.items()}
        )
        self.metadata = result["metadata"]
        self.dstype = result["type"]
        return _unserialize_data(result["type"], result["results"])

    async def async_get_id(self, timeout: int = DEFAULT_TIMEOUT) -> str:
        """Asynchronously get the result ID."""
        if self.id is None:
            if not self.pipeline:
                raise errors.DataStructurePipelineNotFound(
                    "Data structure has no pipeline to run."
                )
            results = await self.pipeline.async_run(timeout=timeout)
            assert isinstance(self.sym_id, str)
            self.id = results[self.sym_id]
        return self.id

    async def async_get_metadata(self) -> Dict[str, Any]:
        """Asynchronously get the metadata of the data structure."""
        if self.metadata:
            return self.metadata

        result_id = await self.async_get_id()
        result = await aio_api.get_result(result_id)
        self.dstype = result["type"]
        self.metadata = result["metadata"]
        return self.metadata

    def get_data(self, **kwargs: Dict[str, Any]) -> Dict[Union[str, int], Any]:
        """Invoke the get_data() method from the data structure in the cloud."""  # noqa: D402
        result_id = self.get_id()
        result = api.get_result_data(
            result_id, query={k: json.dumps(v) for k, v in kwargs.items()}
        )
        self.metadata = result["metadata"]
        self.dstype = result["type"]
        return _unserialize_data(result["type"], result["results"])

    def export(self, path: str, **kwargs: Dict[str, Any]) -> str:
        """Export a result to a file. The file will be stored in the folder
        and returns the file_path.
        """
        result_id = self.get_id()
        file_path = os.path.join(path, "result.zip")
        api.export_result(result_id, file_path, **kwargs)
        return file_path

    def get_id(self, timeout: int = DEFAULT_TIMEOUT) -> str:
        """Invoke the get_data() method from the data structure in the cloud."""
        result_id = self.id
        if result_id is None:
            if not self.pipeline:
                raise errors.DataStructurePipelineNotFound(
                    "Data structure has no pipeline to run."
                )
            results = self.pipeline.run(timeout=timeout)  # run
            assert isinstance(self.sym_id, str)
            result_id = results[self.sym_id]
            self.id = result_id
        return result_id

    def __getattribute__(self, name: str) -> Any:  # noqa: D105
        if name in ("data", "metadata"):
            if (object.__getattribute__(self, "data") and name == "data") or (
                object.__getattribute__(self, "metadata") and name == "metadata"
            ):
                return object.__getattribute__(self, name)
            result_id = self.id
            if not self.pipeline and result_id is None:
                raise errors.DataStructurePipelineNotFound(
                    "Data structure has no pipeline to run."
                )
            if result_id is None:
                assert isinstance(self.pipeline, Pipeline)
                assert isinstance(self.sym_id, str)
                results = self.pipeline.run()
                result_id = results[self.sym_id]
                self.id = result_id
            if name == "data":
                result = api.get_result_data(result_id)
                self.dstype = result["type"]
                self.data = _unserialize_data(result["type"], result["results"])
            elif name == "metadata":
                result = api.get_result(result_id)
                self.dstype = result["type"]
            self.dstype = result["type"]
            self.metadata = result["metadata"]
        return object.__getattribute__(self, name)


def _unserialize_data(dtype: str, data: Any) -> Any:
    if dtype == "data_structures.predefined.ndarray.Ndarray":
        return numpy.array(data)
    if dtype == "data_structures.predefined.pd_data_frame.PdDataFrame":
        return pandas.DataFrame(data=data)
    return data


def get_data_structure_name_and_serialize(data_object: Any) -> Tuple[str, str]:
    """Get the data structure and serialize it."""
    data_type = type(data_object)
    if data_type == dict:  # noqa: E721
        return DS_NAMESPACE + "dict.Dict", json.dumps(data_object)
    if data_type == list:  # noqa: E721
        return DS_NAMESPACE + "list.List", json.dumps(data_object)
    if NUMPY_ENABLED and data_type == numpy.ndarray:
        return DS_NAMESPACE + "ndarray.Ndarray", json.dumps(data_object.tolist())
    if PANDAS_ENABLED and data_type == pandas.core.frame.DataFrame:
        return DS_NAMESPACE + "pd_data_frame.PdDataFrame", data_object.to_json()
    raise errors.DataStructureType(f"Unrecognised type: {data_type}")
