# ''' Package for Elastic Search Connector '''  # noqa: D100
# This package is deprecated and can be removed.
# from typing import Iterable
# from typing import Any, Optional


# class ElasticSearchDBObject:
#     ''' Represents an Elastic Search Data Base Object. '''
#     # pylint: disable=unused-argument,redefined-builtin
#     def bulk(self, actions: Iterable[Any]) -> Any:
#         ''' Performs actions in bulk as defined in the ES bulk API.'''

#     def query(self, query: Any, random_sorting: bool = False) -> Any:
#         ''' Launches a query to ES. Returns the query.'''

#     def insert(self, document: Any, id: Optional[str] = None) -> Any:
#         ''' Inserts a document to ES. '''

#     def update_query(self, new_partial_query: Any) -> Any:
#         ''' Updates a query without executing it.'''


# def create_db_object(index: str, force_rewrite: bool = False) -> ElasticSearchDBObject:
#     ''' Obtains an Elastic Search DB object. Only works on cloud.'''
#     # pylint: disable=unused-argument
#     return ElasticSearchDBObject()
