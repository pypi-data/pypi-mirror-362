"""
Manager for test_runs_stage collection.
"""

from typing import Any, Dict, List, Optional, Union

from testzeus_sdk.client import TestZeusClient
from testzeus_sdk.models.test_runs_stage import TestRunsStage

from .base import BaseManager


class TestRunsStageManager(BaseManager):
    """
    Manager for TestRunsStage resources
    """

    def __init__(self, client: TestZeusClient) -> None:
        """
        Initialize the TestRunsStage manager

        Args:
            client: TestZeus client instance
        """
        super().__init__(client, "test_runs_stage", TestRunsStage)

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
            "test": "pbc_3643163317",
            "config": "pbc_383599117",
            "test_data": "pbc_3433119540",
            "test_device": "pbc_1845990100",
            "tags": "pbc_1219621782",
            "environment": "pbc_3067608406",
        }

        return convert_name_refs_to_ids(self.client, data, ref_fields)
