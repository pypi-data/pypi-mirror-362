"""
Manager for users collection.
"""

from typing import Any, Dict, List, Optional, Union

from testzeus_sdk.client import TestZeusClient
from testzeus_sdk.models.users import Users

from .base import BaseManager, record_to_dict


class UsersManager(BaseManager):
    """
    Manager for Users resources
    """

    def __init__(self, client: TestZeusClient) -> None:
        """
        Initialize the Users manager

        Args:
            client: TestZeus client instance
        """
        super().__init__(client, "users", Users)

    async def find_by_email(self, email: str) -> Optional[Users]:
        """
        Find a user by email address.

        Args:
            email: User email address

        Returns:
            User instance if found, None otherwise
        """
        await self.client.ensure_authenticated()

        try:
            filter_str = f'email = "{email}"'
            result = self.client.pb.collection("users").get_first_list_item(filter_str)
            return Users(record_to_dict(result))
        except Exception as e:
            print(f"Warning: Error finding user by email ({email}): {str(e)}")
            return None

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
        }

        return convert_name_refs_to_ids(self.client, data, ref_fields)
