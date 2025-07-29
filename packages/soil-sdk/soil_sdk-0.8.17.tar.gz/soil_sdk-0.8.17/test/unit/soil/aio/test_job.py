import unittest
from unittest.mock import AsyncMock, patch

from soil.aio.job import job
from soil.data_structure import DataStructure
from soil.job import _Job
from soil.pipeline import Pipeline


class TestJob(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_experiment = {
            "_id": "mock_experiment_id",
            "outputs": {"mock_sym_id": "mock_result_id"},
            "created_at": 1609459200000,  # 2021-01-01 00:00:00 UTC
        }

    def create_data_structure(self):
        pipeline = Pipeline()
        pipeline.plan = "mock_plan"  # pyright:ignore[reportAttributeAccessIssue]
        return DataStructure(sym_id="mock_sym_id", pipeline=pipeline)

    async def test_job_function(self):
        data_structure = self.create_data_structure()

        with patch(
            "soil.aio.job.create_experiment", new_callable=AsyncMock
        ) as mock_create_experiment:
            mock_create_experiment.return_value = self.mock_experiment

            result = await job(
                data_structure, group="test_group", description="test_description"
            )

            self.assertIsInstance(result, _Job)
            self.assertEqual(result.experiment_id, "mock_experiment_id")  # pyright:ignore[reportAttributeAccessIssue]
            self.assertEqual(result.result_id, "mock_result_id")  # pyright:ignore[reportAttributeAccessIssue]
            self.assertEqual(result._created_at, "2021-01-01T00:00:00+00:00")  # pyright:ignore[reportAttributeAccessIssue]
            self.assertEqual(result._group, "test_group")  # pyright:ignore[reportAttributeAccessIssue]

            mock_create_experiment.assert_called_once_with(
                "mock_plan",
                experiment_group="test_group",
                description="test_description",
            )

    async def test_job_function_default_description(self):
        data_structure = self.create_data_structure()

        with patch(
            "soil.aio.job.create_experiment", new_callable=AsyncMock
        ) as mock_create_experiment:
            mock_create_experiment.return_value = self.mock_experiment

            result = await job(data_structure, group="test_group")

            self.assertIsInstance(result, _Job)
            self.assertEqual(result.experiment_id, "mock_experiment_id")  # pyright:ignore[reportAttributeAccessIssue]
            self.assertEqual(result.result_id, "mock_result_id")  # pyright:ignore[reportAttributeAccessIssue]
            self.assertEqual(result._created_at, "2021-01-01T00:00:00+00:00")  # pyright:ignore[reportAttributeAccessIssue]
            self.assertEqual(result._group, "test_group")  # pyright:ignore[reportAttributeAccessIssue]

            mock_create_experiment.assert_called_once_with(
                "mock_plan", experiment_group="test_group", description=None
            )

    async def test_job_function_missing_pipeline(self):
        data_structure = DataStructure(sym_id="mock_sym_id")

        with self.assertRaises(ValueError) as context:
            await job(data_structure, group="test_group")

        self.assertEqual(str(context.exception), "Pipeline plan is required")

    async def test_job_function_missing_sym_id(self):
        pipeline = Pipeline()
        pipeline.plan = "mock_plan"  # pyright:ignore[reportAttributeAccessIssue]
        data_structure = DataStructure(pipeline=pipeline)

        with self.assertRaises(ValueError) as context:
            await job(data_structure, group="test_group")

        self.assertEqual(str(context.exception), "sym_id is required")


if __name__ == "__main__":
    unittest.main()
