# pylint:disable=missing-module-docstring,missing-class-docstring,missing-function-docstring
# pylint:disable=import-outside-toplevel
import logging
import sqlite3
import unittest
from pathlib import Path
from unittest.mock import Mock, call, patch

from soil.logger import set_file_status
from soil.types import TypeLog

_TEST_LOGGER = "test_logger"
PROCESSED_FILES_DB = "test/processed_files.db"


@patch("soil.logger.PROCESSED_FILES_DB", new=PROCESSED_FILES_DB)
@patch("soil.logger._SOIL_LOGGER", new=_TEST_LOGGER)
class TestHashfileLogger(unittest.TestCase):
    @staticmethod
    def _init_storage():
        """Checks if the state files are writeable."""
        path = Path(PROCESSED_FILES_DB)
        if not path.parent.exists():
            path.mkdir(parents=True, exist_ok=True)

        with sqlite3.connect(PROCESSED_FILES_DB) as connection:
            connection.execute("DROP TABLE IF EXISTS processed_files")
            connection.execute(
                """
                CREATE TABLE processed_files (
                    file_name VARCHAR PRIMARY KEY,
                    date VARCHAR NOT NULL,
                    size int NOT NULL,
                    datatype VARCHAR NOT NULL,
                    state VARCHAR CHECK( state IN ('WAITING','PROCESSED','ERROR') ) NOT NULL,
                    state_description VARCHAR,
                    message VARCHAR
                )
                """
            )

    @staticmethod
    def _store_file_db(hexdigest, date, size, datatype):
        with sqlite3.connect(PROCESSED_FILES_DB) as connection:
            connection.execute(
                """
                INSERT INTO processed_files (file_name, date, size, datatype, state)
                VALUES (?,?,?,?,?)
                """,
                (hexdigest, date, size, datatype, "WAITING"),
            )

    def test_logs_handler(self):
        # importing inside method because of patch test_logger
        from soil.logger import logger, logger_extra_kwarg

        TestHashfileLogger._init_storage()
        file = "hash_file_1"
        file_2 = "hash_file_2"
        file_3 = "hash_file_3"
        TestHashfileLogger._store_file_db(file, "2022-02-02", 1, "test1")
        TestHashfileLogger._store_file_db(file_2, "2022-02-02", 1, "test1")
        TestHashfileLogger._store_file_db(file_3, "2022-02-02", 1, "test1")
        logger.setLevel(logging.DEBUG)
        logger.debug(
            "%s has been processed successfully!",
            file,
            extra=logger_extra_kwarg(type_log=TypeLog.PROCESSED, file_name=file),
        )
        logger.debug(
            "%s has been processed successfully!",
            "file_not_existent",
            extra=logger_extra_kwarg(
                type_log=TypeLog.PROCESSED, file_name="file_not_existent"
            ),
        )
        logger.debug(
            "%s data not consistent!",
            file_2,
            extra=logger_extra_kwarg(type_log=TypeLog.NOT_CONSISTENT, file_name=file_2),
        )
        logger.debug(
            "%s has been processed successfully!",
            file_2,
            extra=logger_extra_kwarg(type_log=TypeLog.PROCESSED, file_name=file_2),
        )
        logger.debug(
            "%s error",
            file_3,
            extra=logger_extra_kwarg(type_log=TypeLog.NOT_PROCESSED, file_name=file_3),
        )
        logger.debug(
            "%s processed!",
            file_3,
            extra=logger_extra_kwarg(type_log=TypeLog.PROCESSED, file_name=file_3),
        )
        with sqlite3.connect(PROCESSED_FILES_DB) as connection:
            results = connection.execute(
                """
                    SELECT *
                    FROM processed_files
                """
            ).fetchall()
        self.assertListEqual(
            [
                (
                    file,
                    "2022-02-02",
                    1,
                    "test1",
                    "WAITING",
                    "processed",
                    f"{file} has been processed successfully!",
                ),
                (
                    file_2,
                    "2022-02-02",
                    1,
                    "test1",
                    "WAITING",
                    "not_consistent",
                    f"{file_2} data not consistent!",
                ),
                (
                    file_3,
                    "2022-02-02",
                    1,
                    "test1",
                    "WAITING",
                    "processed",
                    f"{file_3} processed!",
                ),
            ],
            results,
        )

    @patch("soil.logger.logger")
    def test_set_file_status(self, mocked_logger: Mock) -> None:
        set_file_status(
            status=TypeLog.NOT_PROCESSED, file_hash="123", message_status="test_message"
        )
        self.assertListEqual(
            mocked_logger.info.call_args_list,
            [call("test_message", extra={"type": "not_processed", "file": "123"})],
        )
