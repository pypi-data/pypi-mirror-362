# pylint: disable=missing-docstring,line-too-long, unused-argument, redefined-outer-name
# type: ignore

import unittest
from unittest.mock import patch

from pandas import Timestamp

import soil
from soil import decorator, modulify, task
from soil.data_structure import DataStructure


@modulify(output_types=lambda *input_types, **args: [input_types[0]])
def train(*data, module=None, model_params=None, **kwargs):
    (res,) = task(module)(*data, **model_params)
    return [res]


@decorator(depth=3)
def trainable(module):
    def decorator(**model_params):
        def train_fn(**train_params):
            def inner_module(*data):
                return train(
                    *data, module=module, model_params=model_params, **train_params
                )

            return inner_module

        return train_fn

    return decorator


@trainable
@modulify(output_types=lambda *input_types, **args: [input_types[0]])
def my_model(*data, **my_model_params):
    if "p3" in my_model_params:
        return task(my_model_params["p3"](cross_validation=True))(*data)
    return data


@modulify(output_types=lambda *input_types, **args: [input_types[0]])
def my_model2(*data, **my_model_params):
    return data


@modulify
def my_model3(*data, **my_model_params) -> tuple[DataStructure]:
    return data


def test_fn1():
    pass


def test_fn2():
    pass


def mock_soil_data_fn(data):
    return DataStructure("test_id")


class TestUtils(unittest.TestCase):
    @patch("soil.data")
    def test_build_arguments_1(self, mock_soil_data):
        mock_soil_data.side_effect = mock_soil_data_fn
        data = soil.data([{"test": [1, 2, 3]}])
        (res,) = my_model(test_param=1)(cross_validation=True)(data)
        plan = res.pipeline.plan
        first = plan[0]
        args = first["args"]
        expected_args = {
            "module": {
                "__soil_arg_type": "decorated",
                "module": "soil.modulify",
                "name": "modulify",
                "calls": [
                    {
                        "args": [],
                        "kwargs": {"output_types": {"__soil_arg_type": "lambda"}},
                    },
                    {
                        "args": [
                            {
                                "__soil_arg_type": "function",
                                "module": "unit.soil.test_utils",
                                "name": "my_model",
                            }
                        ],
                        "kwargs": {},
                    },
                ],
            },
            "model_params": {"test_param": 1},
            "cross_validation": True,
        }
        assert first["module"] == "unit.soil.test_utils.train"
        assert args == expected_args

    @patch("soil.data")
    def test_build_arguments_2(self, mock_soil_data):
        mock_soil_data.side_effect = mock_soil_data_fn
        data = soil.data([{"test": "test"}])
        (res,) = my_model(test_param=[test_fn1, test_fn2])(cross_validation=True)(data)
        plan = res.pipeline.plan
        first = plan[0]
        args = first["args"]
        expected = {
            "cross_validation": True,
            "model_params": {
                "test_param": [
                    {
                        "__soil_arg_type": "function",
                        "module": "unit.soil.test_utils",
                        "name": "test_fn1",
                    },
                    {
                        "__soil_arg_type": "function",
                        "module": "unit.soil.test_utils",
                        "name": "test_fn2",
                    },
                ]
            },
            "module": {
                "__soil_arg_type": "decorated",
                "calls": [
                    {
                        "args": [],
                        "kwargs": {"output_types": {"__soil_arg_type": "lambda"}},
                    },
                    {
                        "args": [
                            {
                                "__soil_arg_type": "function",
                                "module": "unit.soil.test_utils",
                                "name": "my_model",
                            }
                        ],
                        "kwargs": {},
                    },
                ],
                "module": "soil.modulify",
                "name": "modulify",
            },
        }
        assert args == expected

    @patch("soil.data")
    def test_build_arguments_3(self, mock_soil_data):
        mock_soil_data.side_effect = mock_soil_data_fn
        data = soil.data([{"test": "test"}])
        (res,) = my_model(test_param=my_model2)(cross_validation=True)(data)
        plan = res.pipeline.plan
        first = plan[0]
        args = first["args"]
        expected = {
            "cross_validation": True,
            "model_params": {
                "test_param": {
                    "__soil_arg_type": "decorated",
                    "calls": [
                        {
                            "args": [],
                            "kwargs": {"output_types": {"__soil_arg_type": "lambda"}},
                        },
                        {
                            "args": [
                                {
                                    "__soil_arg_type": "function",
                                    "module": "unit.soil.test_utils",
                                    "name": "my_model2",
                                }
                            ],
                            "kwargs": {},
                        },
                    ],
                    "module": "soil.modulify",
                    "name": "modulify",
                }
            },
            "module": {
                "__soil_arg_type": "decorated",
                "calls": [
                    {
                        "args": [],
                        "kwargs": {"output_types": {"__soil_arg_type": "lambda"}},
                    },
                    {
                        "args": [
                            {
                                "__soil_arg_type": "function",
                                "module": "unit.soil.test_utils",
                                "name": "my_model",
                            }
                        ],
                        "kwargs": {},
                    },
                ],
                "module": "soil.modulify",
                "name": "modulify",
            },
        }
        assert args == expected

    @patch("soil.data")
    def test_build_arguments_4(self, mock_soil_data):
        mock_soil_data.side_effect = mock_soil_data_fn
        data = soil.data([{"test": "test"}])
        (res,) = my_model(test_param=trainable(my_model2))(cross_validation=True)(data)
        plan = res.pipeline.plan
        first = plan[0]
        args = first["args"]
        expected = {
            "cross_validation": True,
            "model_params": {
                "test_param": {
                    "__soil_arg_type": "decorated",
                    "calls": [
                        {
                            "args": [
                                {
                                    "__soil_arg_type": "decorated",
                                    "calls": [
                                        {
                                            "args": [],
                                            "kwargs": {
                                                "output_types": {
                                                    "__soil_arg_type": "lambda"
                                                }
                                            },
                                        },
                                        {
                                            "args": [
                                                {
                                                    "__soil_arg_type": "function",
                                                    "module": "unit.soil.test_utils",
                                                    "name": "my_model2",
                                                }
                                            ],
                                            "kwargs": {},
                                        },
                                    ],
                                    "module": "soil.modulify",
                                    "name": "modulify",
                                }
                            ],
                            "kwargs": {},
                        }
                    ],
                    "module": "unit.soil.test_utils",
                    "name": "trainable",
                }
            },
            "module": {
                "__soil_arg_type": "decorated",
                "calls": [
                    {
                        "args": [],
                        "kwargs": {"output_types": {"__soil_arg_type": "lambda"}},
                    },
                    {
                        "args": [
                            {
                                "__soil_arg_type": "function",
                                "module": "unit.soil.test_utils",
                                "name": "my_model",
                            }
                        ],
                        "kwargs": {},
                    },
                ],
                "module": "soil.modulify",
                "name": "modulify",
            },
        }
        assert args == expected

    @patch("soil.data")
    def test_build_arguments_5(self, mock_soil_data):
        mock_soil_data.side_effect = mock_soil_data_fn
        data = soil.data([{"test": "test"}])
        (res,) = my_model(test_param=my_model)(cross_validation=True)(data)
        plan = res.pipeline.plan
        first = plan[0]
        args = first["args"]
        expected = {
            "cross_validation": True,
            "model_params": {
                "test_param": {
                    "__soil_arg_type": "decorated",
                    "calls": [
                        {
                            "args": [
                                {
                                    "__soil_arg_type": "decorated",
                                    "calls": [
                                        {
                                            "args": [],
                                            "kwargs": {
                                                "output_types": {
                                                    "__soil_arg_type": "lambda"
                                                }
                                            },
                                        },
                                        {
                                            "args": [
                                                {
                                                    "__soil_arg_type": "function",
                                                    "module": "unit.soil.test_utils",
                                                    "name": "my_model",
                                                }
                                            ],
                                            "kwargs": {},
                                        },
                                    ],
                                    "module": "soil.modulify",
                                    "name": "modulify",
                                }
                            ],
                            "kwargs": {},
                        }
                    ],
                    "module": "unit.soil.test_utils",
                    "name": "trainable",
                }
            },
            "module": {
                "__soil_arg_type": "decorated",
                "calls": [
                    {
                        "args": [],
                        "kwargs": {"output_types": {"__soil_arg_type": "lambda"}},
                    },
                    {
                        "args": [
                            {
                                "__soil_arg_type": "function",
                                "module": "unit.soil.test_utils",
                                "name": "my_model",
                            }
                        ],
                        "kwargs": {},
                    },
                ],
                "module": "soil.modulify",
                "name": "modulify",
            },
        }
        assert args == expected

    @patch("soil.data")
    def test_build_arguments_6(self, mock_soil_data):
        mock_soil_data.side_effect = mock_soil_data_fn
        data = soil.data([{"test": "test"}])
        (res,) = my_model(test_param=my_model(f1=2, t1=test_fn1))(
            cross_validation=True
        )(data)
        plan = res.pipeline.plan
        first = plan[0]
        args = first["args"]
        expected = {
            "cross_validation": True,
            "model_params": {
                "test_param": {
                    "__soil_arg_type": "decorated",
                    "calls": [
                        {
                            "args": [
                                {
                                    "__soil_arg_type": "decorated",
                                    "calls": [
                                        {
                                            "args": [],
                                            "kwargs": {
                                                "output_types": {
                                                    "__soil_arg_type": "lambda"
                                                }
                                            },
                                        },
                                        {
                                            "args": [
                                                {
                                                    "__soil_arg_type": "function",
                                                    "module": "unit.soil.test_utils",
                                                    "name": "my_model",
                                                }
                                            ],
                                            "kwargs": {},
                                        },
                                    ],
                                    "module": "soil.modulify",
                                    "name": "modulify",
                                }
                            ],
                            "kwargs": {},
                        },
                        {
                            "args": [],
                            "kwargs": {
                                "f1": 2,
                                "t1": {
                                    "__soil_arg_type": "function",
                                    "module": "unit.soil.test_utils",
                                    "name": "test_fn1",
                                },
                            },
                        },
                    ],
                    "module": "unit.soil.test_utils",
                    "name": "trainable",
                }
            },
            "module": {
                "__soil_arg_type": "decorated",
                "calls": [
                    {
                        "args": [],
                        "kwargs": {"output_types": {"__soil_arg_type": "lambda"}},
                    },
                    {
                        "args": [
                            {
                                "__soil_arg_type": "function",
                                "module": "unit.soil.test_utils",
                                "name": "my_model",
                            }
                        ],
                        "kwargs": {},
                    },
                ],
                "module": "soil.modulify",
                "name": "modulify",
            },
        }
        assert args == expected

    @patch("soil.data")
    def test_build_arguments_7(self, mock_soil_data):
        mock_soil_data.side_effect = mock_soil_data_fn
        data = soil.data([{"test": "test"}])
        (res,) = my_model(test_param=my_model(f1=2, t1=test_fn1)(another=1))(
            cross_validation=True
        )(data)
        plan = res.pipeline.plan
        first = plan[0]
        args = first["args"]
        expected = {
            "cross_validation": True,
            "model_params": {
                "test_param": {
                    "__soil_arg_type": "decorated",
                    "calls": [
                        {
                            "args": [
                                {
                                    "__soil_arg_type": "decorated",
                                    "calls": [
                                        {
                                            "args": [],
                                            "kwargs": {
                                                "output_types": {
                                                    "__soil_arg_type": "lambda"
                                                }
                                            },
                                        },
                                        {
                                            "args": [
                                                {
                                                    "__soil_arg_type": "function",
                                                    "module": "unit.soil.test_utils",
                                                    "name": "my_model",
                                                }
                                            ],
                                            "kwargs": {},
                                        },
                                    ],
                                    "module": "soil.modulify",
                                    "name": "modulify",
                                }
                            ],
                            "kwargs": {},
                        },
                        {
                            "args": [],
                            "kwargs": {
                                "f1": 2,
                                "t1": {
                                    "__soil_arg_type": "function",
                                    "module": "unit.soil.test_utils",
                                    "name": "test_fn1",
                                },
                            },
                        },
                        {"args": [], "kwargs": {"another": 1}},
                    ],
                    "module": "unit.soil.test_utils",
                    "name": "trainable",
                }
            },
            "module": {
                "__soil_arg_type": "decorated",
                "calls": [
                    {
                        "args": [],
                        "kwargs": {"output_types": {"__soil_arg_type": "lambda"}},
                    },
                    {
                        "args": [
                            {
                                "__soil_arg_type": "function",
                                "module": "unit.soil.test_utils",
                                "name": "my_model",
                            }
                        ],
                        "kwargs": {},
                    },
                ],
                "module": "soil.modulify",
                "name": "modulify",
            },
        }
        assert args == expected

    @patch("soil.data")
    def test_build_arguments_8(self, mock_soil_data):
        mock_soil_data.side_effect = mock_soil_data_fn
        data = soil.data([{"test": "test"}])
        (res,) = my_model(
            test_param=trainable(my_model2)(f1=2, t1=test_fn1)(another=1)
        )(cross_validation=True)(data)
        plan = res.pipeline.plan
        first = plan[0]
        args = first["args"]
        expected = {
            "cross_validation": True,
            "model_params": {
                "test_param": {
                    "__soil_arg_type": "decorated",
                    "calls": [
                        {
                            "args": [
                                {
                                    "__soil_arg_type": "decorated",
                                    "calls": [
                                        {
                                            "args": [],
                                            "kwargs": {
                                                "output_types": {
                                                    "__soil_arg_type": "lambda"
                                                }
                                            },
                                        },
                                        {
                                            "args": [
                                                {
                                                    "__soil_arg_type": "function",
                                                    "module": "unit.soil.test_utils",
                                                    "name": "my_model2",
                                                }
                                            ],
                                            "kwargs": {},
                                        },
                                    ],
                                    "module": "soil.modulify",
                                    "name": "modulify",
                                }
                            ],
                            "kwargs": {},
                        },
                        {
                            "args": [],
                            "kwargs": {
                                "f1": 2,
                                "t1": {
                                    "__soil_arg_type": "function",
                                    "module": "unit.soil.test_utils",
                                    "name": "test_fn1",
                                },
                            },
                        },
                        {"args": [], "kwargs": {"another": 1}},
                    ],
                    "module": "unit.soil.test_utils",
                    "name": "trainable",
                }
            },
            "module": {
                "__soil_arg_type": "decorated",
                "calls": [
                    {
                        "args": [],
                        "kwargs": {"output_types": {"__soil_arg_type": "lambda"}},
                    },
                    {
                        "args": [
                            {
                                "__soil_arg_type": "function",
                                "module": "unit.soil.test_utils",
                                "name": "my_model",
                            }
                        ],
                        "kwargs": {},
                    },
                ],
                "module": "soil.modulify",
                "name": "modulify",
            },
        }
        assert args == expected

    @patch("soil.data")
    def test_build_arguments_9(self, mock_soil_data):
        mock_soil_data.side_effect = mock_soil_data_fn
        data = soil.data([{"test": "test"}])
        (res,) = my_model(
            test_param=trainable(my_model2)(f1=2, t1=my_model(test=1))(another=1)
        )(cross_validation=True)(data)
        plan = res.pipeline.plan
        first = plan[0]
        args = first["args"]
        expected = {
            "cross_validation": True,
            "model_params": {
                "test_param": {
                    "__soil_arg_type": "decorated",
                    "calls": [
                        {
                            "args": [
                                {
                                    "__soil_arg_type": "decorated",
                                    "calls": [
                                        {
                                            "args": [],
                                            "kwargs": {
                                                "output_types": {
                                                    "__soil_arg_type": "lambda"
                                                }
                                            },
                                        },
                                        {
                                            "args": [
                                                {
                                                    "__soil_arg_type": "function",
                                                    "module": "unit.soil.test_utils",
                                                    "name": "my_model2",
                                                }
                                            ],
                                            "kwargs": {},
                                        },
                                    ],
                                    "module": "soil.modulify",
                                    "name": "modulify",
                                }
                            ],
                            "kwargs": {},
                        },
                        {
                            "args": [],
                            "kwargs": {
                                "f1": 2,
                                "t1": {
                                    "__soil_arg_type": "decorated",
                                    "calls": [
                                        {
                                            "args": [
                                                {
                                                    "__soil_arg_type": "decorated",
                                                    "calls": [
                                                        {
                                                            "args": [],
                                                            "kwargs": {
                                                                "output_types": {
                                                                    "__soil_arg_type": "lambda"
                                                                }
                                                            },
                                                        },
                                                        {
                                                            "args": [
                                                                {
                                                                    "__soil_arg_type": "function",
                                                                    "module": "unit.soil.test_utils",
                                                                    "name": "my_model",
                                                                }
                                                            ],
                                                            "kwargs": {},
                                                        },
                                                    ],
                                                    "module": "soil.modulify",
                                                    "name": "modulify",
                                                }
                                            ],
                                            "kwargs": {},
                                        },
                                        {"args": [], "kwargs": {"test": 1}},
                                    ],
                                    "module": "unit.soil.test_utils",
                                    "name": "trainable",
                                },
                            },
                        },
                        {"args": [], "kwargs": {"another": 1}},
                    ],
                    "module": "unit.soil.test_utils",
                    "name": "trainable",
                }
            },
            "module": {
                "__soil_arg_type": "decorated",
                "calls": [
                    {
                        "args": [],
                        "kwargs": {"output_types": {"__soil_arg_type": "lambda"}},
                    },
                    {
                        "args": [
                            {
                                "__soil_arg_type": "function",
                                "module": "unit.soil.test_utils",
                                "name": "my_model",
                            }
                        ],
                        "kwargs": {},
                    },
                ],
                "module": "soil.modulify",
                "name": "modulify",
            },
        }
        assert args == expected

    @patch("soil.data")
    def test_build_arguments_10(self, mock_soil_data):
        self.maxDiff = None
        mock_soil_data.side_effect = mock_soil_data_fn
        data = soil.data([{"test": "test"}])
        (res,) = my_model(test_param=my_model(f1=2, t1=my_model(test=1))(another=1))(
            cross_validation=True
        )(data)
        plan = res.pipeline.plan
        first = plan[0]
        args = first["args"]
        expected = {
            "cross_validation": True,
            "model_params": {
                "test_param": {
                    "__soil_arg_type": "decorated",
                    "calls": [
                        {
                            "args": [
                                {
                                    "__soil_arg_type": "decorated",
                                    "calls": [
                                        {
                                            "args": [],
                                            "kwargs": {
                                                "output_types": {
                                                    "__soil_arg_type": "lambda"
                                                }
                                            },
                                        },
                                        {
                                            "args": [
                                                {
                                                    "__soil_arg_type": "function",
                                                    "module": "unit.soil.test_utils",
                                                    "name": "my_model",
                                                }
                                            ],
                                            "kwargs": {},
                                        },
                                    ],
                                    "module": "soil.modulify",
                                    "name": "modulify",
                                }
                            ],
                            "kwargs": {},
                        },
                        {
                            "args": [],
                            "kwargs": {
                                "f1": 2,
                                "t1": {
                                    "__soil_arg_type": "decorated",
                                    "calls": [
                                        {
                                            "args": [
                                                {
                                                    "__soil_arg_type": "decorated",
                                                    "calls": [
                                                        {
                                                            "args": [],
                                                            "kwargs": {
                                                                "output_types": {
                                                                    "__soil_arg_type": "lambda"
                                                                }
                                                            },
                                                        },
                                                        {
                                                            "args": [
                                                                {
                                                                    "__soil_arg_type": "function",
                                                                    "module": "unit.soil.test_utils",
                                                                    "name": "my_model",
                                                                }
                                                            ],
                                                            "kwargs": {},
                                                        },
                                                    ],
                                                    "module": "soil.modulify",
                                                    "name": "modulify",
                                                }
                                            ],
                                            "kwargs": {},
                                        },
                                        {"args": [], "kwargs": {"test": 1}},
                                    ],
                                    "module": "unit.soil.test_utils",
                                    "name": "trainable",
                                },
                            },
                        },
                        {"args": [], "kwargs": {"another": 1}},
                    ],
                    "module": "unit.soil.test_utils",
                    "name": "trainable",
                }
            },
            "module": {
                "__soil_arg_type": "decorated",
                "calls": [
                    {
                        "args": [],
                        "kwargs": {"output_types": {"__soil_arg_type": "lambda"}},
                    },
                    {
                        "args": [
                            {
                                "__soil_arg_type": "function",
                                "module": "unit.soil.test_utils",
                                "name": "my_model",
                            }
                        ],
                        "kwargs": {},
                    },
                ],
                "module": "soil.modulify",
                "name": "modulify",
            },
        }
        self.assertDictEqual(args, expected)

    @patch("soil.data")
    def test_build_arguments_11(self, mock_soil_data):
        mock_soil_data.side_effect = mock_soil_data_fn
        data = soil.data([{"test": "test"}])
        param = Timestamp("2020-02-02 02:02:02+01:00").tz_convert("Europe/Madrid")
        param1 = Timestamp("2020-02-02 02:02:02+02:00")
        param2 = Timestamp("2020-02-02 02:02:02")
        (res,) = my_model3(
            data, test_param=param, test_param_1=param1, test_param_2=param2
        )
        plan = res.pipeline.plan
        first = plan[0]
        args = first["args"]
        expected = {
            "test_param": {
                "_object": "Timestamp",
                "_constructor_params": {
                    "positional_args": ["2020-02-02T02:02:02+01:00"],
                    "keywords_args": {"tz": "Europe/Madrid"},
                },
            },
            "test_param_1": {
                "_object": "Timestamp",
                "_constructor_params": {
                    "positional_args": ["2020-02-02T02:02:02+02:00"],
                    "keywords_args": {},
                },
            },
            "test_param_2": {
                "_object": "Timestamp",
                "_constructor_params": {
                    "positional_args": ["2020-02-02T02:02:02"],
                    "keywords_args": {},
                },
            },
        }
        self.assertDictEqual(args, expected)
