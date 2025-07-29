"""Exports the soil logger"""

import importlib
import logging
import logging.handlers
import os
import sqlite3
import sys
from os.path import exists
from typing import LiteralString, cast

from psycopg_pool import ConnectionPool

from soil.types import TypeLog

_SOIL_LOGGER = "soil_logger"
TABLE_NAME = "processed_files"
PROCESSED_FILES_DB = "/rain-data/processed_files.db"
DB_POOL = None


if not exists(PROCESSED_FILES_DB):
    PROCESSED_FILES_DB = None

try:
    sys.path.insert(1, "/rain/config")
    config = importlib.import_module(os.environ["PY_ENV"])
    if config.db_credentials is not None:
        DB_POOL = ConnectionPool(
            " ".join([f"{k}={v}" for k, v in config.db_credentials.items()])
        )
except (ModuleNotFoundError, AttributeError, KeyError):
    pass


def _get_connection():
    if DB_POOL is not None:
        return DB_POOL.connection()
    return sqlite3.connect(PROCESSED_FILES_DB)


def _transform_query(query: str) -> str:
    if DB_POOL is None:
        return query.replace("%s", "?")
    return query


logger = logging.getLogger(_SOIL_LOGGER)  # pylint: disable=invalid-name


def logger_extra_kwarg(*, type_log: TypeLog, file_name: str) -> dict[str, str]:
    """Creates the extra kwarg for the logger."""
    return {
        HashFileHandler.type_log: type_log.value,
        HashFileHandler.hashfile: file_name,
    }


def set_file_status(*, status: TypeLog, file_hash: str, message_status: str) -> None:
    """Updates the status of the file hash."""
    logger.info(
        message_status, extra=logger_extra_kwarg(type_log=status, file_name=file_hash)
    )


class HashFileHandler(logging.StreamHandler):
    """Handler of logs to store file to sqlite."""

    type_log = "type"
    hashfile = "file"
    state_name_column = "state_description"
    message_column = "message"

    def emit(self, record: logging.LogRecord) -> None:
        """Emits the log record."""
        type_log = cast(TypeLog | None, getattr(record, "type", None))
        hashfile = cast(str | None, getattr(record, "file", None))
        if (
            type_log is not None
            and hashfile is not None
            and type_log in [*TypeLog]
            and (PROCESSED_FILES_DB is not None or DB_POOL is not None)
        ):
            self._process_file_in_storage(
                hashfile=hashfile, type_log=type_log, message=record.getMessage()
            )

    def _process_file_in_storage(self, **kwargs) -> None:
        """Process the file hash to update the DB."""
        with _get_connection() as connection:
            cursor = connection.cursor()
            self._update_hashfile(cursor=cursor, table_name=TABLE_NAME, **kwargs)

    def _update_hashfile(
        self,
        *,
        cursor: sqlite3.Cursor,
        table_name: LiteralString,
        hashfile: str,
        type_log: TypeLog,
        message: str,
    ) -> None:
        cursor.execute(
            _transform_query(
                f"UPDATE {table_name} "  # nosec
                f"SET {self.state_name_column} = %s, {self.message_column} = %s "
                f"WHERE file_name = %s and "
                f"({self.state_name_column} IS NULL or {self.state_name_column} = %s)"
            ),
            (type_log, message, hashfile, TypeLog.NOT_PROCESSED.value),
        )


logger.addHandler(HashFileHandler())
