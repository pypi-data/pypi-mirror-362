"""
Soil package.
"""

from soil import aio, connectors, errors, finder, types
from soil.alerts import alerts
from soil.alias import alias
from soil.data import data
from soil.data_structure import DataStructure
from soil.decorator import decorator
from soil.dictionary import dictionary
from soil.job import job
from soil.logger import logger, logger_extra_kwarg, set_file_status
from soil.modulify import modulify
from soil.task import task, task_wait

finder.upload_modules()

__all__ = [
    "modulify",
    "data_structures",
    "DataStructure",
    "modules",
    "data",
    "alias",
    "logger",
    "connectors",
    "decorator",
    "task",
    "task_wait",
    "alerts",
    "dictionary",
    "errors",
    "types",
    "logger_extra_kwarg",
    "set_file_status",
    "job",
    "aio",
]
