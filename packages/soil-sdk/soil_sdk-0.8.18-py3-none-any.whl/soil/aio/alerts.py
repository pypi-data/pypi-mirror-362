"""Package that contains calls for the alerts system."""

from typing import Any, Dict

from soil.aio.api import create_alert, create_event


async def event(key: str, value: Any) -> Any:
    """Creates an event asynchronously."""
    return await create_event(key, value)


async def alert(alert_config: Dict) -> Any:
    """Creates an alert asynchronously."""
    return await create_alert(alert_config)
