# pylint: disable=missing-docstring,line-too-long,broad-exception-raised, unnecessary-ellipsis
import unittest
from dataclasses import dataclass
from json import dumps, loads
from typing import Dict, NamedTuple, Optional, Self, Type, TypedDict
from unittest.mock import MagicMock, call, patch
from urllib.parse import parse_qs, urlparse

import soil
from soil.data_structure import DataStructure
from soil.storage.base_storage import BaseStorage


class MockHttpResponse(NamedTuple):
    """Soil configuration class"""

    status_code: int
    text: str

    def json(self) -> dict:
        return loads(self.text)


def set_id(self: DataStructure, timeout: int) -> None:
    self.id = "mock_id"
    self.timeout = timeout  # type:ignore[reportAttributeAccessIssue]


# pylint: disable=unused-argument
def mock_http_patch(
    url: str,
    *,
    headers: Optional[Dict[str, str]] = None,
    json: Optional[Dict[str, str]] = None,
    timeout: int,
) -> MockHttpResponse:
    assert json is not None
    return MockHttpResponse(status_code=200, text=dumps({}))


# pylint: disable=unused-argument
def mock_http_post(
    url: str,
    *,
    headers: Optional[Dict[str, str]] = None,
    json: Optional[Dict[str, str]] = None,
    timeout: int,
) -> MockHttpResponse:
    assert json is not None
    url_parts = urlparse(url)
    if url_parts.path == "/v2/results/":
        response = {"_id": "mock_id", "type": json["type"]}
        return MockHttpResponse(status_code=201, text=dumps(response))
    if url_parts.path == "/v2/states/":
        return MockHttpResponse(status_code=200, text=dumps({}))
    raise Exception("mock http case not found")


# pylint: disable=unused-argument
def mock_http_get(
    url: str, *, headers: Optional[Dict[str, str]] = None, timeout: int
) -> MockHttpResponse:
    url_parts = urlparse(url)
    query_params = parse_qs(url_parts.query)
    if url_parts.path == "/v2/states/" and query_params["name"][0] == "test_alias":
        return MockHttpResponse(status_code=200, text=dumps([]))
    raise Exception("mock http case not found")


# pylint: disable=unused-argument
def mock_http_get2(
    url: str, *, headers: Optional[Dict[str, str]] = None, timeout: int
) -> MockHttpResponse:
    url_parts = urlparse(url)
    query_params = parse_qs(url_parts.query)
    if url_parts.path == "/v2/states/" and query_params["name"][0] == "valid_alias":
        return MockHttpResponse(status_code=200, text=dumps([{"_id": "alias_id"}]))
    if url_parts.path == "/v2/states/alias_id/":
        result = {
            "_id": "alias_id",
            "state": {"result_id": "non_existing_alias_but_valid_id"},
        }
        return MockHttpResponse(status_code=200, text=dumps(result))
    raise Exception("mock http case not found")


def mock_http_get3(
    url: str, *, headers: Optional[Dict[str, str]] = None, timeout: int
) -> MockHttpResponse:
    if url == "test_auth_url/api/application/test_auth_app_id":
        return MockHttpResponse(
            status_code=200,
            text=dumps(
                {"application": {"roles": [{"name": "test"}, {"name": "test1"}]}}
            ),
        )
    raise Exception("mock http case not found")


def mock_http_post2(
    url: str,
    *,
    headers: Optional[Dict[str, str]] = None,
    json: dict | None = None,
    timeout: int,
) -> MockHttpResponse:
    if url == "test_auth_url/api/application/test_auth_app_id/role":
        return MockHttpResponse(status_code=200, text="ack")
    raise Exception("mock http case not found")


class TestAlias(unittest.TestCase):
    @patch("soil.api.session.get", side_effect=mock_http_get)
    @patch("soil.api.session.post", side_effect=mock_http_post)
    @patch("soil.api.session.patch", side_effect=mock_http_patch)
    def test_alias_new(
        self, mock_patch: MagicMock, mock_post: MagicMock, mock_get: MagicMock
    ) -> None:
        data = soil.data([1, 2, 3, 4])
        soil.alias("test_alias", data)
        mock_get.assert_has_calls(
            [
                call(
                    "http://test_host.test/v2/states/?name=test_alias&with-roles",
                    timeout=30,
                )
            ]
        )
        mock_post.assert_has_calls(
            [
                call(
                    "http://test_host.test/v2/results/",
                    json={
                        "type": "soil.data_structures.predefined.list.List",
                        "data": "[1, 2, 3, 4]",
                        "metadata": None,
                    },
                    timeout=30,
                ),
                call(
                    "http://test_host.test/v2/states/",
                    json={
                        "name": "test_alias",
                        "state": {"alias": "test_alias", "result_id": "mock_id"},
                    },
                    timeout=30,
                ),
            ]
        )
        assert mock_patch.call_count == 0

    @patch("soil.api.session.get", side_effect=mock_http_get)
    @patch("soil.api.session.post", side_effect=mock_http_post)
    @patch("soil.api.session.patch", side_effect=mock_http_patch)
    def test_alias_new_with_type_hint(
        self, mock_patch: MagicMock, mock_post: MagicMock, mock_get: MagicMock
    ) -> None:
        @dataclass(kw_only=True)
        class MockClass:
            class Metadata(TypedDict):
                test: str

            metadata: "MockClass.Metadata"
            storage: BaseStorage

            def serialize(self) -> BaseStorage:
                """Serializes the DS."""
                ...

            @classmethod
            def deserialize(
                cls: Type[Self],
                storage: BaseStorage,
                metadata: "MockClass.Metadata",
            ) -> Self:
                """Deserialize DS method."""
                ...

        data = soil.data([1, 2, 3, 4], return_type=MockClass)
        soil.alias("test_alias", data)
        mock_get.assert_has_calls(
            [
                call(
                    "http://test_host.test/v2/states/?name=test_alias&with-roles",
                    timeout=30,
                )
            ]
        )
        mock_post.assert_has_calls(
            [
                call(
                    "http://test_host.test/v2/results/",
                    json={
                        "type": "soil.data_structures.predefined.list.List",
                        "data": "[1, 2, 3, 4]",
                        "metadata": None,
                    },
                    timeout=30,
                ),
                call(
                    "http://test_host.test/v2/states/",
                    json={
                        "name": "test_alias",
                        "state": {"alias": "test_alias", "result_id": "mock_id"},
                    },
                    timeout=30,
                ),
            ]
        )
        assert mock_patch.call_count == 0

    @patch("soil.api.session.get", side_effect=mock_http_get2)
    @patch("soil.api.session.post", side_effect=mock_http_post)
    @patch("soil.api.session.patch", side_effect=mock_http_patch)
    def test_alias_existing(
        self, mock_patch: MagicMock, mock_post: MagicMock, mock_get: MagicMock
    ) -> None:
        data = soil.data([1, 2, 3, 4])
        soil.alias("valid_alias", data)
        mock_get.assert_has_calls(
            [
                call(
                    "http://test_host.test/v2/states/?name=valid_alias&with-roles",
                    timeout=30,
                ),
                call(
                    "http://test_host.test/v2/states/alias_id/",
                    timeout=30,
                ),
            ]
        )
        mock_post.assert_has_calls(
            [
                call(
                    "http://test_host.test/v2/results/",
                    json={
                        "type": "soil.data_structures.predefined.list.List",
                        "data": "[1, 2, 3, 4]",
                        "metadata": None,
                    },
                    timeout=30,
                )
            ]
        )
        mock_patch.assert_has_calls(
            [
                call(
                    "http://test_host.test/v2/states/alias_id/",
                    json={
                        "name": "valid_alias",
                        "state": {"alias": "valid_alias", "result_id": "mock_id"},
                    },
                    timeout=30,
                )
            ]
        )

    @patch("soil.api.session.get", side_effect=mock_http_get2)
    @patch("soil.api.session.post", side_effect=mock_http_post)
    @patch("soil.api.session.patch", side_effect=mock_http_patch)
    def test_alias_data_structure(
        self, mock_patch: MagicMock, mock_post: MagicMock, mock_get: MagicMock
    ) -> None:
        with patch.object(
            DataStructure, "get_id", side_effect=set_id, autospec=True
        ) as mock_get_data:
            data = DataStructure(dstype="data_structures.some.test.type")
            soil.alias("valid_alias", data)
            assert mock_get_data.call_count == 1
        mock_get.assert_has_calls(
            [
                call(
                    "http://test_host.test/v2/states/?name=valid_alias&with-roles",
                    timeout=30,
                ),
                call(
                    "http://test_host.test/v2/states/alias_id/",
                    timeout=30,
                ),
            ]
        )
        assert mock_post.call_count == 0
        mock_patch.assert_has_calls(
            [
                call(
                    "http://test_host.test/v2/states/alias_id/",
                    json={
                        "name": "valid_alias",
                        "state": {"alias": "valid_alias", "result_id": "mock_id"},
                    },
                    timeout=30,
                )
            ]
        )
        self.assertEqual(mock_get_data.call_args_list[0][1]["timeout"], 3600)

    @patch("soil.api.session.get", side_effect=mock_http_get2)
    @patch("soil.api.session.post", side_effect=mock_http_post)
    @patch("soil.api.session.patch", side_effect=mock_http_patch)
    def test_alias_data_structure_timeout(
        self, mock_patch: MagicMock, mock_post: MagicMock, mock_get: MagicMock
    ) -> None:
        with patch.object(
            DataStructure, "get_id", side_effect=set_id, autospec=True
        ) as mock_get_data:
            data = DataStructure(dstype="data_structures.some.test.type")
            soil.alias("valid_alias", data, timeout=15)
            assert mock_get_data.call_count == 1
        mock_get.assert_has_calls(
            [
                call(
                    "http://test_host.test/v2/states/?name=valid_alias&with-roles",
                    timeout=30,
                ),
                call(
                    "http://test_host.test/v2/states/alias_id/",
                    timeout=30,
                ),
            ]
        )
        assert mock_post.call_count == 0
        mock_patch.assert_has_calls(
            [
                call(
                    "http://test_host.test/v2/states/alias_id/",
                    json={
                        "name": "valid_alias",
                        "state": {"alias": "valid_alias", "result_id": "mock_id"},
                    },
                    timeout=30,
                )
            ]
        )
        self.assertEqual(mock_get_data.call_args_list[0][1]["timeout"], 15)

    @patch("soil.api.requests.post", side_effect=mock_http_post2)
    @patch("soil.api.requests.get", side_effect=mock_http_get3)
    @patch("soil.api.session.get", side_effect=mock_http_get2)
    @patch("soil.api.session.post", side_effect=mock_http_post)
    @patch("soil.api.session.patch", side_effect=mock_http_patch)
    def test_alias_roles(
        self,
        mock_patch: MagicMock,
        mock_post: MagicMock,
        mock_get: MagicMock,
        mock_requests_get: MagicMock,
        mock_requests_post: MagicMock,
    ) -> None:
        with patch.object(
            DataStructure, "get_id", side_effect=set_id, autospec=True
        ) as mock_get_data:
            data = DataStructure(dstype="data_structures.some.test.type")
            soil.alias("valid_alias", data, roles=["test"])
            assert mock_get_data.call_count == 1
        mock_get.assert_has_calls(
            [
                call(
                    "http://test_host.test/v2/states/?name=valid_alias&with-roles",
                    timeout=30,
                ),
                call(
                    "http://test_host.test/v2/states/alias_id/",
                    timeout=30,
                ),
            ]
        )
        assert mock_post.call_count == 0
        mock_patch.assert_has_calls(
            [
                call(
                    "http://test_host.test/v2/states/alias_id/",
                    json={
                        "name": "valid_alias",
                        "state": {"alias": "valid_alias", "result_id": "mock_id"},
                        "roles": ["test"],
                    },
                    timeout=30,
                ),
                call(
                    "http://test_host.test/v2/results/mock_id/",
                    json={"roles": ["test"]},
                    timeout=30,
                ),
            ]
        )
        self.assertListEqual(
            mock_requests_get.call_args_list,
            [
                call(
                    "test_auth_url/api/application/test_auth_app_id",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": "TEST_APP_INFO_API_KEY",
                    },
                    timeout=15,
                )
            ],
        )
        self.assertListEqual(mock_requests_post.call_args_list, [])

    @patch("soil.api.requests.post", side_effect=mock_http_post2)
    @patch("soil.api.requests.get", side_effect=mock_http_get3)
    @patch("soil.api.session.get", side_effect=mock_http_get)
    @patch("soil.api.session.post", side_effect=mock_http_post)
    @patch("soil.api.session.patch", side_effect=mock_http_patch)
    def test_alias_new_with_roles(
        self,
        mock_patch: MagicMock,
        mock_post: MagicMock,
        mock_get: MagicMock,
        mock_requests_get: MagicMock,
        mock_requests_post: MagicMock,
    ) -> None:
        data = soil.data([1, 2, 3, 4])
        soil.alias("test_alias", data, roles=["test1", "test2"])
        mock_get.assert_has_calls(
            [
                call(
                    "http://test_host.test/v2/states/?name=test_alias&with-roles",
                    timeout=30,
                )
            ]
        )
        mock_post.assert_has_calls(
            [
                call(
                    "http://test_host.test/v2/results/",
                    json={
                        "type": "soil.data_structures.predefined.list.List",
                        "data": "[1, 2, 3, 4]",
                        "metadata": None,
                    },
                    timeout=30,
                ),
                call(
                    "http://test_host.test/v2/states/",
                    json={
                        "name": "test_alias",
                        "state": {"alias": "test_alias", "result_id": "mock_id"},
                        "roles": ["test1", "test2"],
                    },
                    timeout=30,
                ),
            ]
        )
        mock_patch.assert_has_calls(
            [
                call(
                    "http://test_host.test/v2/results/mock_id/",
                    json={"roles": ["test1", "test2"]},
                    timeout=30,
                )
            ]
        )
        self.assertListEqual(
            mock_requests_get.call_args_list,
            [
                call(
                    "test_auth_url/api/application/test_auth_app_id",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": "TEST_APP_INFO_API_KEY",
                    },
                    timeout=15,
                ),
                call(
                    "test_auth_url/api/application/test_auth_app_id",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": "TEST_APP_INFO_API_KEY",
                    },
                    timeout=15,
                ),
            ],
        )
        self.assertListEqual(
            mock_requests_post.call_args_list,
            [
                call(
                    "test_auth_url/api/application/test_auth_app_id/role",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": "TEST_APP_INFO_API_KEY",
                    },
                    json={"role": {"name": "test2"}},
                    timeout=15,
                )
            ],
        )

    @patch("soil.api.requests.post", side_effect=mock_http_post2)
    @patch("soil.api.requests.get", side_effect=mock_http_get3)
    @patch("soil.api.session.get", side_effect=mock_http_get2)
    @patch("soil.api.session.post", side_effect=mock_http_post)
    @patch("soil.api.session.patch", side_effect=mock_http_patch)
    def test_alias_roles_and_extras(
        self,
        mock_patch: MagicMock,
        mock_post: MagicMock,
        mock_get: MagicMock,
        mock_requests_get: MagicMock,
        mock_requests_post: MagicMock,
    ) -> None:
        with patch.object(
            DataStructure, "get_id", side_effect=set_id, autospec=True
        ) as mock_get_data:
            data = DataStructure(dstype="data_structures.some.test.type")
            soil.alias("valid_alias", data, roles=["test"], extras={"name": "My Data"})
            assert mock_get_data.call_count == 1
        mock_get.assert_has_calls(
            [
                call(
                    "http://test_host.test/v2/states/?name=valid_alias&with-roles",
                    timeout=30,
                ),
                call(
                    "http://test_host.test/v2/states/alias_id/",
                    timeout=30,
                ),
            ]
        )
        assert mock_post.call_count == 0
        mock_patch.assert_has_calls(
            [
                call(
                    "http://test_host.test/v2/states/alias_id/",
                    json={
                        "name": "valid_alias",
                        "state": {
                            "alias": "valid_alias",
                            "result_id": "mock_id",
                            "extras": {"name": "My Data"},
                        },
                        "roles": ["test"],
                    },
                    timeout=30,
                ),
                call(
                    "http://test_host.test/v2/results/mock_id/",
                    json={"roles": ["test"]},
                    timeout=30,
                ),
            ]
        )
        self.assertListEqual(
            mock_requests_get.call_args_list,
            [
                call(
                    "test_auth_url/api/application/test_auth_app_id",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": "TEST_APP_INFO_API_KEY",
                    },
                    timeout=15,
                )
            ],
        )
        self.assertListEqual(mock_requests_post.call_args_list, [])
