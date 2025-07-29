import unittest
from unittest.mock import patch

from soil.aio.dictionary import dictionary


class TestDictionary(unittest.IsolatedAsyncioTestCase):
    @patch("soil.aio.dictionary.get_dictionary")
    async def test_get_dictionary(self, mock_get_dictionary):
        mock_get_dictionary.return_value = {"key": "value"}
        result = await dictionary("test_dict", "en")
        mock_get_dictionary.assert_called_once_with("test_dict", "en")
        self.assertEqual(result, {"key": "value"})

    @patch("soil.aio.dictionary.create_dictionary")
    async def test_create_dictionary(self, mock_create_dictionary):
        mock_create_dictionary.return_value = {"status": "created"}
        content = {"word1": "definition1", "word2": "definition2"}
        result = await dictionary("new_dict", "fr", content)
        mock_create_dictionary.assert_called_once_with("new_dict", "fr", content)
        self.assertEqual(result, {"status": "created"})

    async def test_invalid_input(self):
        with self.assertRaises(AssertionError):
            await dictionary(
                123,  # pyright:ignore[reportArgumentType]
                "en",
            )  # Invalid name type

        with self.assertRaises(AssertionError):
            await dictionary(
                "test_dict",
                123,  # pyright:ignore[reportArgumentType] Invalid language type
            )


if __name__ == "__main__":
    unittest.main()
