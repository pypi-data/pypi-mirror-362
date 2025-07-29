"""
Manager for tests collection.
"""

from typing import Any, Dict, List, Optional, Union

from testzeus_sdk.client import TestZeusClient
from testzeus_sdk.models.tests import Tests

from .base import BaseManager


class TestsManager(BaseManager):
    """
    Manager for Tests resources
    """

    def __init__(self, client: TestZeusClient) -> None:
        """
        Initialize the Tests manager

        Args:
            client: TestZeus client instance
        """
        super().__init__(client, "tests", Tests)

    def _process_references(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process name-based references to ID-based references

        Args:
            data: Entity data with potential name-based references

        Returns:
            Processed data with ID-based references
        """
        from testzeus_sdk.utils.helpers import convert_name_refs_to_ids

        # Define which fields are relations and what collections they reference
        ref_fields = {
            "tenant": "pbc_138639755",
            "modified_by": "_pb_users_auth_",
            "config": "pbc_383599117",
            "test_design": "pbc_3066241075",
            "test_data": "pbc_3433119540",
            "tags": "pbc_1219621782",
            "environment": "pbc_3067608406",
        }

        return convert_name_refs_to_ids(self.client, data, ref_fields)

    def run_test(self, test_id: str, environment_id: Optional[str] = None) -> Any:
        """
        Run a test

        Args:
            test_id: Test ID or name
            environment_id: Environment ID (optional)

        Returns:
            Test run result
        """
        # Convert name to ID if needed
        if not self._is_valid_id(test_id):
            test = self.get_one(test_id)
            if not test:
                raise ValueError(f"Test not found: {test_id}")
            test_id = test.id

        data = {"test": test_id}
        if environment_id:
            data["environment"] = environment_id

        # Use the test runs manager to create a run
        return self.client.test_runs.create(data)
