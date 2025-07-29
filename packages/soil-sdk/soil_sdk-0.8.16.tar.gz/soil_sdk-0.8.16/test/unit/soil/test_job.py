import unittest
from dataclasses import dataclass
from datetime import UTC, datetime
from json import dumps, loads
from unittest.mock import Mock, patch
from urllib.parse import parse_qs, urlparse

from soil import job
from soil.job import _Job
from soil.types import Experiment


class TestJob(unittest.TestCase):
    @patch("soil.job.create_experiment")
    def test_job_create(self, mock_create_experiment: Mock):
        mock_create_experiment.return_value = Experiment(
            _id="my_experiment",
            status={"my_output": "DONE"},
            experiment_status="DONE",
            app_id="my_app",
            outputs={"my_datastructure": "my_output"},
            created_at=1640995200 * 1000,
        )
        plan_mocked = Mock()
        data_object_mocked = Mock(
            sym_id="my_datastructure", pipeline=Mock(plan=plan_mocked)
        )
        my_job = job(
            data_object=data_object_mocked,
            group="job_group1",
            description={"unit_id": "my_unit", "target": "my_target"},
        )
        mock_create_experiment.assert_called_once_with(
            plan_mocked,
            experiment_group="job_group1",
            description={"unit_id": "my_unit", "target": "my_target"},
        )

        self.assertEqual(
            my_job,
            _Job(  # pyright:ignore[reportAbstractUsage]
                experiment_id="my_experiment",
                result_id="my_output",
                _group="job_group1",
                _created_at=datetime.fromtimestamp(1640995200, tz=UTC).isoformat(),
            ),
        )

    @patch("soil.api.session.post")
    def test_job_create_with_description(
        self,
        mock_post: Mock,
    ):
        mock_post.return_value = MockHttpResponse(
            status_code=200,
            text=dumps(
                {
                    "experiment": {
                        "_id": "my_experiment",
                        "outputs": {"my_datastructure": "my_output"},
                        "created_at": 1640995200 * 1000,
                    }
                }
            ),
        )

        plan_mocked = Mock()
        data_object_mocked = Mock(
            sym_id="my_datastructure", pipeline=Mock(plan=plan_mocked)
        )
        my_job = job(
            data_object=data_object_mocked,
            group="job_group1",
            description={"unit_id": "my_unit", "target": "my_target"},
        )
        self.assertEqual(
            my_job,
            _Job(  # pyright:ignore[reportAbstractUsage]
                experiment_id="my_experiment",
                result_id="my_output",
                _group="job_group1",
                _created_at=datetime.fromtimestamp(1640995200, tz=UTC).isoformat(),
            ),
        )

        mock_post.assert_called_once_with(
            "http://test_host.test/v2/experiments/",
            json={
                "experiment": {
                    "name": "",
                    "description": {"unit_id": "my_unit", "target": "my_target"},
                    "plan": plan_mocked,
                    "experiment_group": "job_group1",
                }
            },
            timeout=30,
        )

    @patch("soil.api.session.post")
    def test_job_create_no_description(
        self,
        mock_post: Mock,
    ):
        mock_post.return_value = MockHttpResponse(
            status_code=200,
            text=dumps(
                {
                    "experiment": {
                        "_id": "my_experiment",
                        "outputs": {"my_datastructure": "my_output"},
                        "created_at": 1640995200 * 1000,
                    }
                }
            ),
        )

        plan_mocked = Mock()
        data_object_mocked = Mock(
            sym_id="my_datastructure", pipeline=Mock(plan=plan_mocked)
        )
        my_job = job(
            data_object=data_object_mocked,
            group="job_group1",
        )
        self.assertEqual(
            my_job,
            _Job(  # pyright:ignore[reportAbstractUsage]
                experiment_id="my_experiment",
                result_id="my_output",
                _group="job_group1",
                _created_at=datetime.fromtimestamp(1640995200, tz=UTC).isoformat(),
            ),
        )

        mock_post.assert_called_once_with(
            "http://test_host.test/v2/experiments/",
            json={
                "experiment": {
                    "name": "",
                    "description": "",
                    "plan": plan_mocked,
                    "experiment_group": "job_group1",
                }
            },
            timeout=30,
        )


@dataclass
class MockHttpResponse:
    """Soil configuration class"""

    status_code: int
    text: str

    def json(self) -> dict:
        return loads(self.text)


# pylint: disable=unused-argument
def mock_http_patch(
    url: str,
    *,
    headers: dict[str, str] | None = None,
    json: dict[str, str] | None = None,
    timeout: int,
) -> MockHttpResponse:
    assert url == "http://test_host.test/v2/states/mock_id/"
    assert json == {"name": "backtest", "state": {}}
    return MockHttpResponse(status_code=200, text=dumps({"hello": json}))


# pylint: disable=unused-argument
def mock_http_post_(
    url: str,
    *,
    headers: dict[str, str] | None = None,
    json: dict[str, str] | None = None,
    timeout: int,
) -> MockHttpResponse:
    url_parts = urlparse(url)
    assert url_parts.path == "/v2/states/"
    assert json == {"name": "backtest", "state": {}}
    return MockHttpResponse(status_code=200, text=dumps({}))


# pylint: disable=unused-argument
def mock_http_get(
    url: str, *, headers: dict[str, str] | None = None, timeout: int
) -> MockHttpResponse:
    url_parts = urlparse(url)
    query_params = parse_qs(url_parts.query)
    if url_parts.path == "/v2/states/" and query_params["name"][0] == "backtest":
        return MockHttpResponse(
            status_code=200,
            text=dumps([{"_id": "mock_id", "name": "backtest", "state": "mock_state"}]),
        )
    raise Exception("mock http case not found")
