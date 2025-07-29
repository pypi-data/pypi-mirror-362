"""Package that contains calls for soil get dictionary"""

from typing import Any, Dict

from soil.aio.api import create_dictionary, get_dictionary


async def dictionary(
    name: str, language: str, content: Dict[str, str] | None = None
) -> Dict[str, Any]:
    """Create or get a dictionary asynchronously"""
    if content is None:
        assert isinstance(name, str)
        assert isinstance(language, str)
        return await get_dictionary(name, language)
    return await create_dictionary(name, language, content)
