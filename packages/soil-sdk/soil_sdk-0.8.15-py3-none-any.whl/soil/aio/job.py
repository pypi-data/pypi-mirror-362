"""Asynchronous Job module"""

from datetime import UTC, datetime

from soil.aio.api import create_experiment
from soil.data_structure import DataStructure
from soil.data_structure import DataStructure as InternalDataStructure
from soil.job import _Job
from soil.types import Job


async def _new_job(
    data_structure: InternalDataStructure,
    group: str,
    description: dict | str | None = None,
) -> Job:
    if data_structure.pipeline is None:
        raise ValueError("Pipeline plan is required")
    if data_structure.sym_id is None:
        raise ValueError("sym_id is required")
    experiment = await create_experiment(
        data_structure.pipeline.plan,
        experiment_group=group,
        description=description,
    )
    return _Job(
        experiment_id=experiment["_id"],
        result_id=experiment["outputs"][data_structure.sym_id],
        _created_at=datetime.fromtimestamp(
            experiment["created_at"] / 1000, tz=UTC
        ).isoformat(),
        _group=group,
    )


async def job(
    data_object: DataStructure, *, group: str, description: dict | str | None = None
) -> Job:
    """Creates a non-blocking job at soil."""
    return await _new_job(data_object, group=group, description=description)
