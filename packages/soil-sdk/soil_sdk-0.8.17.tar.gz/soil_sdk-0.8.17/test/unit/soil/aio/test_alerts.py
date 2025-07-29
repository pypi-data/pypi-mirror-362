import unittest
from unittest.mock import patch

from soil.aio import alerts


class TestAioAlerts(unittest.IsolatedAsyncioTestCase):
    @patch("soil.aio.alerts.create_event")
    async def test_event(self, mock_create_event):
        mock_create_event.return_value = {"status": "success"}

        result = await alerts.event("test_key", "test_value")

        mock_create_event.assert_called_once_with("test_key", "test_value")
        self.assertEqual(result, {"status": "success"})

    @patch("soil.aio.alerts.create_alert")
    async def test_alert(self, mock_create_alert):
        mock_create_alert.return_value = {"alert_id": "123"}

        alert_config = {"type": "test_alert", "threshold": 100}
        result = await alerts.alert(alert_config)

        mock_create_alert.assert_called_once_with(alert_config)
        self.assertEqual(result, {"alert_id": "123"})


if __name__ == "__main__":
    unittest.main()
