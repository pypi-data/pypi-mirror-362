"""
Manager for test_run_dashs collection.
"""

from typing import Any, Dict, List, Optional, Union

from testzeus_sdk.client import TestZeusClient
from testzeus_sdk.models.test_run_dashs import TestRunDashs

from .base import BaseManager


class TestRunDashsManager(BaseManager):
    """
    Manager for TestRunDashs resources
    """

    def __init__(self, client: TestZeusClient) -> None:
        """
        Initialize the TestRunDashs manager

        Args:
            client: TestZeus client instance
        """
        super().__init__(client, "test_run_dashs", TestRunDashs)

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
            "test_run": "pbc_872419316",
            "tags": "pbc_1219621782",
        }

        return convert_name_refs_to_ids(self.client, data, ref_fields)

    def get_expanded(self, test_run_id: str) -> Dict[str, Any]:
        """
        Get complete expanded tree of a test run with all details

        Args:
            test_run_id: Test run ID

        Returns:
            Complete test run tree with all details
        """
        from testzeus_sdk.utils.helpers import expand_test_run_tree

        return expand_test_run_tree(self.client, test_run_id)

    def cancel(self, test_run_id: str) -> bool:
        """
        Cancel a test run

        Args:
            test_run_id: Test run ID

        Returns:
            True if successful
        """
        return self.update(test_run_id, {"status": "cancelled"})
