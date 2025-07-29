"""
Manager for test_designs collection.
"""

from typing import Any, Dict, List, Optional, Union

from testzeus_sdk.client import TestZeusClient
from testzeus_sdk.models.test_designs import TestDesigns

from .base import BaseManager


class TestDesignsManager(BaseManager):
    """
    Manager for TestDesigns resources
    """

    def __init__(self, client: TestZeusClient) -> None:
        """
        Initialize the TestDesigns manager

        Args:
            client: TestZeus client instance
        """
        super().__init__(client, "test_designs", TestDesigns)

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
            "source_data": "pbc_3433119540",
            "tags": "pbc_1219621782",
        }

        return convert_name_refs_to_ids(self.client, data, ref_fields)
