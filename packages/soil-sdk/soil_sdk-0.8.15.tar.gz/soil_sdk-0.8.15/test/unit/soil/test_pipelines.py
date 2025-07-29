# pylint: disable=missing-docstring,line-too-long,unused-argument,no-member,too-many-locals
# type: ignore

import unittest
from unittest.mock import Mock, patch

import soil
from soil import errors, modulify
from soil.data_structure import DataStructure


class List:
    # pylint:disable=too-few-public-methods
    pass


@modulify(output_types=lambda *input_types, **args: [List])
def merge_list(data1, data2):
    pass


@modulify()
def merge_list_with_signature(data1, data2) -> tuple[DataStructure]:
    pass


@modulify()
def merge_list_with_signature_error(data1, data2) -> DataStructure:
    pass


@modulify
def merge_list_with_signature_error_2(data1, data2):
    pass


@modulify
def split_list(data) -> tuple[list, list]:
    pass


@modulify
def one_to_one(data, **kwargs) -> tuple[list]:
    pass


def soil_data_patch(name):
    return DataStructure(name)


@patch("soil.data", side_effect=soil_data_patch)
@patch(
    "soil.utils.uuid4",
    side_effect=list(range(1111, 1111 * 1000, 1111)),
)
@patch("soil.api.create_experiment")
@patch("soil.api.get_experiment")
@patch("soil.api.get_experiment_logs")
@patch("soil.api.get_result_data")
@patch("soil.pipeline.sleep", new=lambda x: None)
class TestPipelines(unittest.TestCase):
    # pylint:disable=too-many-function-args

    @patch("soil.api.get_result")
    def test_pipeline_simple(
        self,
        get_result_mock,
        get_result_data_mock,
        experiment_logs_mock,
        get_experiment_mock,
        create_experiment_mock,
        random_int_patch,
        mock_data_patch,
    ):
        data_ref_1 = soil.data("data_ref_1")
        data_ref_2 = soil.data("data_ref_2")
        (result,) = merge_list(data_ref_1, data_ref_2)
        get_experiment_mock.side_effect = [
            {"experiment_status": "EXECUTING"},
            {"experiment_status": "DONE"},
        ]
        experiment_logs_mock.return_value = []

        _data = result.metadata

        assert len(experiment_logs_mock.call_args_list) == 2
        assert len(get_result_data_mock.call_args_list) == 0
        assert len(get_result_mock.call_args_list) == 1
        assert len(get_experiment_mock.call_args_list) == 2
        create_experiment_mock.assert_called_once_with(
            [
                {
                    "id": "unit.soil.test_pipelines.merge_list-2222",
                    "module": "unit.soil.test_pipelines.merge_list",
                    "inputs": ["data_ref_1", "data_ref_2"],
                    "outputs": ["unit/soil/test_pipelines/merge_list-1111-0"],
                    "args": {},
                }
            ]
        )

    @patch("soil.api.get_result")
    @patch("soil.pipeline.time")
    def test_pipeline_timeout(
        self,
        time_mock,
        get_result_mock,
        get_result_data_mock,
        experiment_logs_mock,
        get_experiment_mock: Mock,
        create_experiment_mock,
        random_int_patch,
        mock_data_patch,
    ):
        time_mock.side_effect = [0, 50, 3601, 3801]
        data_ref_1 = soil.data("data_ref_1")
        data_ref_2 = soil.data("data_ref_2")
        (result,) = merge_list(data_ref_1, data_ref_2)
        get_experiment_mock.return_value = {"experiment_status": "EXECUTING"}
        experiment_logs_mock.return_value = []

        with self.assertRaises(errors.ExperimentTimeoutError):
            result.pipeline.run(timeout=3800)
        self.assertEqual(get_experiment_mock.call_count, 3)

    @patch("soil.api.get_result")
    def test_pipeline_simple_with_signature(
        self,
        get_result_mock,
        get_result_data_mock,
        experiment_logs_mock,
        get_experiment_mock,
        create_experiment_mock,
        *_unused_mocks,
    ):
        data_ref_1 = soil.data("data_ref_1")
        data_ref_2 = soil.data("data_ref_2")
        (result,) = merge_list_with_signature(data_ref_1, data_ref_2)
        get_experiment_mock.side_effect = [
            {"experiment_status": "EXECUTING"},
            {"experiment_status": "DONE"},
        ]
        experiment_logs_mock.return_value = []

        _data = result.metadata

        assert len(experiment_logs_mock.call_args_list) == 2
        assert len(get_result_data_mock.call_args_list) == 0
        assert len(get_result_mock.call_args_list) == 1
        assert len(get_experiment_mock.call_args_list) == 2
        create_experiment_mock.assert_called_once_with(
            [
                {
                    "id": "unit.soil.test_pipelines.merge_list_with_signature-2222",
                    "module": "unit.soil.test_pipelines.merge_list_with_signature",
                    "inputs": ["data_ref_1", "data_ref_2"],
                    "outputs": [
                        "unit/soil/test_pipelines/merge_list_with_signature-1111-0"
                    ],
                    "args": {},
                }
            ]
        )

    @patch("soil.api.get_result")
    def test_pipeline_simple_with_signature_raise_error(
        self,
        *_unused_mocks,
    ):
        data_ref_1 = soil.data("data_ref_1")
        data_ref_2 = soil.data("data_ref_2")
        with self.assertRaises(ValueError):
            merge_list_with_signature_error(data_ref_1, data_ref_2)

        with self.assertRaises(ValueError):
            merge_list_with_signature_error_2(data_ref_1, data_ref_2)

    def test_pipeline_split(
        self,
        get_result_data_mock,
        experiment_logs_mock,
        get_experiment_mock,
        create_experiment_mock,
        random_int_patch,
        mock_data_patch,
    ):
        data_ref_1 = soil.data("data_ref_1")
        data_ref_2 = soil.data("data_ref_2")
        (result1, result2) = split_list(data_ref_1, data_ref_2)
        get_experiment_mock.side_effect = [{"experiment_status": "DONE"}]
        experiment_logs_mock.return_value = []

        _data = result1.data
        _data = result2.data

        assert len(experiment_logs_mock.call_args_list) == 1
        assert len(get_result_data_mock.call_args_list) == 2
        assert len(get_experiment_mock.call_args_list) == 1

        create_experiment_mock.assert_called_once_with(
            [
                {
                    "id": "unit.soil.test_pipelines.split_list-2222",
                    "module": "unit.soil.test_pipelines.split_list",
                    "inputs": ["data_ref_1", "data_ref_2"],
                    "outputs": [
                        "unit/soil/test_pipelines/split_list-1111-0",
                        "unit/soil/test_pipelines/split_list-1111-1",
                    ],
                    "args": {},
                }
            ]
        )

    def test_pipeline_split_merge(
        self,
        get_result_data_mock,
        experiment_logs_mock,
        get_experiment_mock,
        create_experiment_mock,
        random_int_patch,
        mock_data_patch,
    ):
        data_ref_1 = soil.data("data_ref_1")
        (res_1, res_2) = split_list(data_ref_1)
        (result1,) = merge_list(res_1, res_2)
        get_experiment_mock.side_effect = [{"experiment_status": "DONE"}]
        experiment_logs_mock.return_value = []

        _data = result1.get_data()

        assert len(experiment_logs_mock.call_args_list) == 1
        assert len(get_result_data_mock.call_args_list) == 1
        assert len(get_experiment_mock.call_args_list) == 1

        create_experiment_mock.assert_called_once_with(
            [
                {
                    "id": "unit.soil.test_pipelines.split_list-2222",
                    "module": "unit.soil.test_pipelines.split_list",
                    "inputs": ["data_ref_1"],
                    "outputs": [
                        "unit/soil/test_pipelines/split_list-1111-0",
                        "unit/soil/test_pipelines/split_list-1111-1",
                    ],
                    "args": {},
                },
                {
                    "id": "unit.soil.test_pipelines.merge_list-4444",
                    "module": "unit.soil.test_pipelines.merge_list",
                    "inputs": [
                        "unit/soil/test_pipelines/split_list-1111-0",
                        "unit/soil/test_pipelines/split_list-1111-1",
                    ],
                    "outputs": ["unit/soil/test_pipelines/merge_list-3333-0"],
                    "args": {},
                },
            ]
        )

    def test_pipeline_complex_split_merge(
        self,
        get_result_data_mock,
        experiment_logs_mock,
        get_experiment_mock,
        create_experiment_mock,
        random_int_patch,
        mock_data_patch,
    ):
        data_ref_1 = soil.data("data_ref_1")
        (res_1, res_2) = split_list(data_ref_1)
        (res_11, res_12) = split_list(res_1)
        (res_21, res_22) = split_list(res_2)
        (result1,) = merge_list(res_11, res_21)
        (result2,) = merge_list(res_12, res_22)
        (result,) = merge_list(result1, result2)
        get_experiment_mock.side_effect = [{"experiment_status": "DONE"}]
        experiment_logs_mock.return_value = []

        _data = result.get_data()

        assert len(experiment_logs_mock.call_args_list) == 1
        assert len(get_result_data_mock.call_args_list) == 1
        assert len(get_experiment_mock.call_args_list) == 1

        create_experiment_mock.assert_called_once_with(
            [
                {
                    "id": "unit.soil.test_pipelines.merge_list-8888",
                    "module": "unit.soil.test_pipelines.merge_list",
                    "inputs": [
                        "unit/soil/test_pipelines/split_list-3333-0",
                        "unit/soil/test_pipelines/split_list-5555-0",
                    ],
                    "outputs": ["unit/soil/test_pipelines/merge_list-7777-0"],
                    "args": {},
                },
                {
                    "id": "unit.soil.test_pipelines.split_list-4444",
                    "module": "unit.soil.test_pipelines.split_list",
                    "inputs": ["unit/soil/test_pipelines/split_list-1111-0"],
                    "outputs": [
                        "unit/soil/test_pipelines/split_list-3333-0",
                        "unit/soil/test_pipelines/split_list-3333-1",
                    ],
                    "args": {},
                },
                {
                    "id": "unit.soil.test_pipelines.split_list-2222",
                    "module": "unit.soil.test_pipelines.split_list",
                    "inputs": ["data_ref_1"],
                    "outputs": [
                        "unit/soil/test_pipelines/split_list-1111-0",
                        "unit/soil/test_pipelines/split_list-1111-1",
                    ],
                    "args": {},
                },
                {
                    "id": "unit.soil.test_pipelines.split_list-6666",
                    "module": "unit.soil.test_pipelines.split_list",
                    "inputs": ["unit/soil/test_pipelines/split_list-1111-1"],
                    "outputs": [
                        "unit/soil/test_pipelines/split_list-5555-0",
                        "unit/soil/test_pipelines/split_list-5555-1",
                    ],
                    "args": {},
                },
                {
                    "id": "unit.soil.test_pipelines.merge_list-11110",
                    "module": "unit.soil.test_pipelines.merge_list",
                    "inputs": [
                        "unit/soil/test_pipelines/split_list-3333-1",
                        "unit/soil/test_pipelines/split_list-5555-1",
                    ],
                    "outputs": ["unit/soil/test_pipelines/merge_list-9999-0"],
                    "args": {},
                },
                {
                    "id": "unit.soil.test_pipelines.merge_list-13332",
                    "module": "unit.soil.test_pipelines.merge_list",
                    "inputs": [
                        "unit/soil/test_pipelines/merge_list-7777-0",
                        "unit/soil/test_pipelines/merge_list-9999-0",
                    ],
                    "outputs": ["unit/soil/test_pipelines/merge_list-12221-0"],
                    "args": {},
                },
            ]
        )
        # print(create_experiment_mock.call_args_list)

    @patch("soil.alias.set_alias")
    def test_pipeline_iterations(
        self,
        mock_set_alias,
        get_result_data_mock,
        experiment_logs_mock,
        get_experiment_mock,
        create_experiment_mock,
        random_int_patch,
        mock_data_patch,
    ):
        result = soil.data("data_ref_1")

        for i in range(4):
            experiment_logs_mock.return_value = []
            create_experiment_mock.return_value = {
                "_id": "aaaa",
                "outputs": {
                    "unit/soil/test_pipelines/one_to_one-1111-0": "okok",
                    "unit/soil/test_pipelines/one_to_one-3333-0": "blabla",
                    "unit/soil/test_pipelines/one_to_one-5555-0": "blabla",
                    "unit/soil/test_pipelines/one_to_one-7777-0": "blabla",
                },
            }
            get_experiment_mock.side_effect = [{"experiment_status": "DONE"}]
            (result2,) = one_to_one(result, index=i)
            self.assertEqual(len(result2.pipeline.plan), 1)
            soil.alias("result", result2)

        for i in range(4):
            experiment_logs_mock.return_value = []
            create_experiment_mock.return_value = {
                "_id": "aaaa",
                "outputs": {
                    "unit/soil/test_pipelines/one_to_one-9999-0": "blabla",
                    "unit/soil/test_pipelines/one_to_one-12221-0": "blabla",
                    "unit/soil/test_pipelines/one_to_one-14443-0": "blabla",
                    "unit/soil/test_pipelines/one_to_one-16665-0": "blabla",
                },
            }
            get_experiment_mock.side_effect = [{"experiment_status": "DONE"}]
            (result,) = one_to_one(result, index=i)
            # This is correct results in soil are immutable
            self.assertEqual(len(result.pipeline.plan), i + 1)
            soil.alias("result", result)
