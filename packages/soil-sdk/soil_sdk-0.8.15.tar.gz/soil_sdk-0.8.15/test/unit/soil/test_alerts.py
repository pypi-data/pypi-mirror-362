# pylint: disable=missing-docstring,line-too-long

import unittest
from json import dumps
from typing import Dict, NamedTuple, Optional
from unittest.mock import MagicMock, patch

import soil


class MockHttpResponse(NamedTuple):
    """Soil configuration class"""

    status_code: int
    text: str


# pylint: disable=unused-argument
def mock_http_post(
    url: str,
    *,
    headers: Optional[Dict[str, str]] = None,
    json: Optional[Dict[str, str]] = None,
    timeout: int,
) -> MockHttpResponse:
    assert json is not None
    response = "ok"
    return MockHttpResponse(status_code=201, text=dumps(response))


class TestAlerts(unittest.TestCase):
    @patch("soil.api.session.post", side_effect=mock_http_post)
    def test_create_event(self, mock_post: MagicMock) -> None:
        soil.alerts.event("test_key", "test_value")
        mock_post.assert_called_once_with(
            "http://test_host.test/v2/alerts/events/",
            json={"key": "test_key", "value": "test_value"},
            timeout=30,
        )

    @patch("soil.api.session.post", side_effect=mock_http_post)
    def test_create_alert(self, mock_post: MagicMock) -> None:
        alert_config = {
            "role": "test_alerts",
            "event_id": "test_event1",
            "condition": {"type": "any"},
        }
        soil.alerts.alert(alert_config)
        mock_post.assert_called_once_with(
            "http://test_host.test/v2/alerts/alerts/",
            json=alert_config,
            timeout=30,
        )
