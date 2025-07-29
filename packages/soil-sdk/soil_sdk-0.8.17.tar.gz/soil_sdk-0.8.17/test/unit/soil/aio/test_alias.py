import unittest
from unittest.mock import AsyncMock, patch

from soil import errors
from soil.aio.alias import alias
from soil.data_structure import DataStructure
from soil.types import DEFAULT_TIMEOUT


class TestAlias(unittest.IsolatedAsyncioTestCase):
    async def test_alias_1(self):
        # Mock dependencies
        mock_data_ref = AsyncMock(spec=DataStructure)
        mock_data_ref.id = None

        def mock_set_id(**kwargs):
            mock_data_ref.id = "test_id"
            return mock_data_ref.id

        mock_data_ref.async_get_id.side_effect = mock_set_id

        with patch(
            "soil.aio.alias.set_alias", new_callable=AsyncMock
        ) as mock_set_alias:
            # Test alias function
            await alias(
                "test_name",
                mock_data_ref,
                roles=["role1", "role2"],
                extras={"key": "value"},
            )

            # Assert that async_get_id was called
            mock_data_ref.async_get_id.assert_called_once_with(timeout=DEFAULT_TIMEOUT)

            # Assert that set_alias was called with correct arguments
            mock_set_alias.assert_called_once_with(
                "test_name", "test_id", ["role1", "role2"], {"key": "value"}
            )

    async def test_alias_with_existing_id(self):
        # Mock dependencies
        mock_data_ref = AsyncMock(spec=DataStructure)
        mock_data_ref.id = "existing_id"

        with patch(
            "soil.aio.alias.set_alias", new_callable=AsyncMock
        ) as mock_set_alias:
            # Test alias function
            await alias("test_name", mock_data_ref)

            # Assert that async_get_id was not called
            mock_data_ref.async_get_id.assert_not_called()

            # Assert that set_alias was called with correct arguments
            mock_set_alias.assert_called_once_with(
                "test_name", "existing_id", None, None
            )

    async def test_alias_with_invalid_data_ref(self):
        mock_data_ref = DataStructure()
        with self.assertRaises(errors.DataStructurePipelineNotFound):
            await alias("test_name", mock_data_ref)


if __name__ == "__main__":
    unittest.main()
