"""
Manager for tenants collection.
"""

from typing import Any, Dict, List, Optional, Union

from testzeus_sdk.client import TestZeusClient
from testzeus_sdk.models.tenants import Tenants

from .base import BaseManager


class TenantsManager(BaseManager):
    """
    Manager for Tenants resources
    """

    def __init__(self, client: TestZeusClient) -> None:
        """
        Initialize the Tenants manager

        Args:
            client: TestZeus client instance
        """
        super().__init__(client, "tenants", Tenants)

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
            "default_agent_config": "pbc_383599117",
        }

        return convert_name_refs_to_ids(self.client, data, ref_fields)
