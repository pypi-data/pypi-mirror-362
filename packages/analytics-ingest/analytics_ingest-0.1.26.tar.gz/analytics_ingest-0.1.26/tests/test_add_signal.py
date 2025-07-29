import unittest
import time
from unittest.mock import patch, MagicMock

from analytics_ingest.ingest_client import AnalyticsIngestClient
from analytics_ingest.internal.utils.batching import Batcher
from analytics_ingest.internal.utils.mutations import GraphQLMutations
from factories import configuration_factory, message_factory, signal_factory


class TestAnalyticsIngestClient(unittest.TestCase):
    def setUp(self):
        self.config = configuration_factory()
        self.client = AnalyticsIngestClient(
            device_id=self.config['device_id'],
            vehicle_id=self.config['vehicle_id'],
            fleet_id=self.config['fleet_id'],
            org_id=self.config['organization_id'],
            graphql_endpoint="http://0.0.0.0:8092/graphql",
            batch_size=5,
            batch_interval_seconds=2,
        )

    def tearDown(self):
        self.client.close()

    def test_create_batches_valid(self):
        data = list(range(10))
        batches = Batcher.create_batches(data, 4)
        self.assertEqual(len(batches), 3)
        self.assertEqual(batches[0], [0, 1, 2, 3])

    def test_create_batches_invalid_type(self):
        with self.assertRaises(TypeError):
            Batcher.create_batches("bad_data", 3)

    def test_create_batches_invalid_batch_size(self):
        with self.assertRaises(ValueError):
            Batcher.create_batches([1, 2, 3], 0)

    def test_add_signal_missing_data_key(self):
        variables = [
            {
                "name": "Speed",
                "unit": "km/h",
                "messageName": "SpeedMsg",
                "networkName": "CAN",
                "ecuName": "TestECU",
            }
        ]
        self.client.add_signal(variables)
        time.sleep(3)

        self.assertGreaterEqual(len(self.client.signal_buffer), 1)

    @patch("analytics_ingest.internal.utils.graphql_executor.requests.post")
    def test_create_configuration_failure_invalid_endpoint(self, mock_post):
        mock_post.side_effect = Exception("Invalid endpoint")
        with self.assertRaises(Exception):
            _ = AnalyticsIngestClient(
                device_id=1,
                vehicle_id=1,
                fleet_id=1,
                org_id=1,
                graphql_endpoint="http://invalid",
            )

    def test_executor_fails_on_bad_graphql(self):
        with self.assertRaises(RuntimeError):
            self.client.executor.execute("invalid graphql")

    def test_graphql_configuration_success(self):
        variables = {
            "input": {
                "deviceId": self.config['device_id'],
                "fleetId": self.config['fleet_id'],
                "organizationId": self.config['organization_id'],
                "vehicleId": self.config['vehicle_id'],
            }
        }
        response = self.client.executor.execute(
            GraphQLMutations.create_configuration(), variables
        )
        self.assertIn("data", response)
        self.assertIn("createConfiguration", response["data"])


if __name__ == "__main__":
    unittest.main()
