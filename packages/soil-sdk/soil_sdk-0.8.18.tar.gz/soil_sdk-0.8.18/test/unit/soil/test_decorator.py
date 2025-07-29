# pylint: disable=missing-docstring,line-too-long, unused-argument
# type: ignore

import unittest
from unittest.mock import MagicMock

from soil import decorator

train = MagicMock(name="train")
my_model = MagicMock(name="my_model")


def trainable(module):
    def dec(**model_params):
        def train_fn(**train_params):
            def inner_module(*data):
                return train(
                    *data, module=module, model_params=model_params, **train_params
                )

            return inner_module

        return train_fn

    return dec


class TestDecorator(unittest.TestCase):
    def setUp(self):
        train.reset_mock()
        my_model.reset_mock()

    def test_no_depth(self):
        with self.assertRaises(ValueError):
            decorator()(trainable)
        train.assert_not_called()
        my_model.assert_not_called()

    def test_show_calls(self):
        my_trainable = decorator(depth=3)(trainable)
        assert my_trainable(__show_calls=True) == (trainable, [])
        train.assert_not_called()
        my_model.assert_not_called()

    def test_show_calls_2(self):
        my_trainable = decorator(depth=3)(trainable)
        assert my_trainable(__show_calls=True) == (trainable, [])
        train.assert_not_called()
        my_model.assert_not_called()

    def test_show_calls_3(self):
        my_trainable = decorator(depth=3)(trainable)(my_model)
        assert my_trainable(__show_calls=True) == (trainable, [((my_model,), {})])
        train.assert_not_called()
        my_model.assert_not_called()

    def test_show_calls_4(self):
        my_trainable = decorator(depth=3)(trainable)(my_model)(test=1)
        assert my_trainable(__show_calls=True) == (
            trainable,
            [((my_model,), {}), ((), {"test": 1})],
        )
        train.assert_not_called()
        my_model.assert_not_called()

    def test_show_calls_5(self):
        my_trainable = decorator(depth=3)(trainable)(my_model)(test=1)(["bla"])
        assert my_trainable(__show_calls=True) == (
            trainable,
            [((my_model,), {}), ((), {"test": 1}), ((["bla"],), {})],
        )
        train.assert_not_called()
        my_model.assert_not_called()

    def test_show_calls_6(self):
        my_trainable = decorator(depth=3)(trainable)(my_model)(test=1)(test2="3")(
            "other"
        )
        # pylint:disable=protected-access
        assert my_trainable._extract_mock_name() == "train()"
        train.assert_called_once_with(
            "other", module=my_model, test2="3", model_params={"test": 1}
        )
        my_model.assert_not_called()
