"""Module that defines a Pipeline."""

# To prevent Pipeline not defined: https://stackoverflow.com/a/49872353/3481480
from __future__ import annotations

import asyncio
import copy
import datetime
import logging
from time import sleep, time
from typing import Any, Dict, List, Optional

from soil import api, errors
from soil.aio import api as aio_api
from soil.logger import logger as soil_logger
from soil.types import DEFAULT_TIMEOUT, Experiment, Plan

# How much should wait between api calls
# Remember ES takes some time to index logs
SLEEP_TIME = 1
logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class Pipeline:
    """A Pipeline stores the transformations and dependencies to obtain certain results."""

    def __init__(self, plan: Optional[Plan] = None) -> None:  # noqa: D107
        self.plan = plan if plan is not None else []
        self.experiment: Optional[Experiment] = None
        self.finished = False

    def run(self, timeout: int = DEFAULT_TIMEOUT) -> Dict[str, str]:
        """Run the Pipeline (blocking call until the experiment finishes or timesout"""
        if self.finished and self.experiment:
            return self.experiment["outputs"]
        if self.experiment is None:
            experiment = api.create_experiment(self.plan)
            self.experiment = experiment
        status = api.get_experiment(experiment["_id"])["experiment_status"]
        start_date = datetime.datetime.now().astimezone().isoformat()
        max_time = time() + timeout
        while status not in ["DONE", "ERROR"]:
            if time() > max_time:
                raise errors.ExperimentTimeoutError("Pipeline timed out")
            sleep(SLEEP_TIME)
            logs = api.get_experiment_logs(experiment["_id"], start_date)
            _print_logs(logs)
            if len(logs) > 0:
                start_date = logs[0]["date"]
            status = api.get_experiment(experiment["_id"])["experiment_status"]
        sleep(SLEEP_TIME)
        logs = api.get_experiment_logs(experiment["_id"], start_date)
        _print_logs(logs)
        if status == "ERROR":
            raise errors.ExperimentError("Pipeline failed")
        logger.debug("experiment_done: %s", experiment["_id"])
        self.finished = True
        return experiment["outputs"]

    def add_transformation(self, transformation: Dict[str, str]) -> Pipeline:
        """Add a new transformation to the Pipeline, returns a new Pipeline
        containing the plan of the old Pipeline plus the transformation.
        """
        new_plan = [*self.plan, transformation]
        return Pipeline(plan=new_plan)

    @staticmethod
    def merge_pipelines(*pipelines: Pipeline) -> Pipeline:
        """Merges all the Pipelines passed into a new Pipeline that is returned."""
        merged_plan: Plan = sum([p.plan for p in pipelines], [])  # noqa: RUF017
        # Remove repeated
        merged_plan = [
            i for n, i in enumerate(merged_plan) if i not in merged_plan[n + 1 :]
        ]
        return Pipeline(plan=merged_plan)

    async def async_run(self, timeout: int = DEFAULT_TIMEOUT) -> Dict[str, str]:
        """Run the Pipeline asynchronously until the experiment finishes or times out."""
        if self.finished and self.experiment:
            return self.experiment["outputs"]
        if self.experiment is None:
            self.experiment = await aio_api.create_experiment(self.plan)

        status = (await aio_api.get_experiment(self.experiment["_id"]))[
            "experiment_status"
        ]
        start_date = datetime.datetime.now().astimezone().isoformat()
        max_time = time() + timeout

        while status not in ["DONE", "ERROR"]:
            if time() > max_time:
                raise errors.ExperimentTimeoutError("Pipeline timed out")
            await asyncio.sleep(SLEEP_TIME)
            logs = await aio_api.get_experiment_logs(self.experiment["_id"], start_date)
            _print_logs(logs)
            if logs:
                start_date = logs[0]["date"]
            status = (await aio_api.get_experiment(self.experiment["_id"]))[
                "experiment_status"
            ]

        await asyncio.sleep(SLEEP_TIME)
        logs = await aio_api.get_experiment_logs(self.experiment["_id"], start_date)
        _print_logs(logs)

        if status == "ERROR":
            raise errors.ExperimentError("Pipeline failed")
        logger.debug("experiment_done: %s", self.experiment["_id"])
        self.finished = True
        return self.experiment["outputs"]


def _print_logs(logs: List[Dict[str, Any]]) -> None:
    for log in logs[::-1]:
        level = getattr(logging, log["level"], logging.INFO)
        nlog = copy.copy(log)
        del nlog["message"]
        soil_logger.log(level, "%s - %s", nlog["date"], log["message"], extra=nlog)
