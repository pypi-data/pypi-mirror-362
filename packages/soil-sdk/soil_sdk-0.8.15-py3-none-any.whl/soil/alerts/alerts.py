"""Package that contains calls for the alerts system."""

from typing import Any, Dict

from soil import api


def event(key: str, value: Any) -> Any:
    """Creates an event."""
    return api.create_event(key, value)


def alert(alert_config: Dict) -> Any:
    """Creates an alert."""
    return api.create_alert(alert_config)
