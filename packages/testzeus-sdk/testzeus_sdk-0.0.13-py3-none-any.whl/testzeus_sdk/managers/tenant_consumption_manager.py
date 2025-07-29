"""
Manager for tenant_consumption collection.
"""

from typing import Any, Dict, List, Optional, Union

from testzeus_sdk.client import TestZeusClient
from testzeus_sdk.models.tenant_consumption import TenantConsumption

from .base import BaseManager


class TenantConsumptionManager(BaseManager):
    """
    Manager for TenantConsumption resources
    """

    def __init__(self, client: TestZeusClient) -> None:
        """
        Initialize the TenantConsumption manager

        Args:
            client: TestZeus client instance
        """
        super().__init__(client, "tenant_consumption", TenantConsumption)

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
            "tags": "pbc_1219621782",
        }

        return convert_name_refs_to_ids(self.client, data, ref_fields)
