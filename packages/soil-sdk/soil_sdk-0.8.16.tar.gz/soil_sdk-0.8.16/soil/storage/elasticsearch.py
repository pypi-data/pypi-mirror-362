"""Module for Elasticsearch storage"""

from dataclasses import dataclass
from typing import Any, Dict, Iterable, Optional

from soil.storage.base_storage import BaseStorage


@dataclass
class Elasticsearch(BaseStorage):
    """Class that implements Elasticsearch storage.

    Attributes
    ----------
        index: str: The index name to store the data to. It will be
            automatically prefixed with the app_id.

    """

    index: str

    def search(
        self, body: Dict[str, Any], auto_scroll: bool = True, **kwargs: Any
    ) -> Any:
        """Perform a search in elasticsearch in the idnex self.index.

        Attributes
        ----------
            body: The body of the search
            auto_scroll: If an auto_scroll has to be done.

        Returns: if auto_scroll is true it will return a tuple with a generator
            with the results as first element and metadata as second element.
            Otherwise it will return everything together.

        """

    # def insert(self, document: Dict[Any, Any], doc_id: Optional[str] = None) -> None:
    #     """Insert a document in the index."""

    def create_index(self, schema: Optional[Dict[str, Any]] = None) -> None:
        """Creates an index with the schema or an empty schema.
        If the index already exists it does nothing.
        """

    def delete_index(self) -> None:
        """Deletes the index"""

    def bulk(self, actions: Iterable[Any]) -> Any:
        """Performs bulk operations to the index only."""
