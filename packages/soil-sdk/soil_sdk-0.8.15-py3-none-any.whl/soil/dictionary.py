"""Package that contains calls for soil get dictionary"""

from typing import Any, Dict, Optional

from soil.api import create_dictionary, get_dictionary


def dictionary(
    name: str, language: str, content: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """Create or get a dictionary"""
    if content is None:
        assert isinstance(name, str)
        assert isinstance(language, str)
        return get_dictionary(name, language)
    return create_dictionary(name, language, content)
