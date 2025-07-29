"""
Environment model class for TestZeus environment entities.
"""

from typing import Any, Dict, List

from testzeus_sdk.models.base import BaseModel


class Environment(BaseModel):
    """
    Model class for TestZeus environment entities.

    This class represents environment entities in TestZeus, which can be
    used to define test environments and their configurations.
    """

    def __init__(self, data: Dict[str, Any]):
        """
        Initialize an Environment model with data from the API.

        Args:
            data: Dictionary containing environment data
        """
        super().__init__(data)

        # Extract common fields
        self.name: str = data.get("name")
        self.status: str = data.get("status")
        self.tenant: str = data.get("tenant")
        self.modified_by: str = data.get("modified_by")
        self.supporting_data_files: List[str] = data.get("supporting_data_files")
        self.data_content: str = data.get("data")
        self.tags: List[str] = data.get("tags")
        self.metadata: str = data.get("metadata")
        self.skip_process: bool = data.get("skip_process")
        self.cached_prompt_details: str = data.get("cached_prompt_details")

    def is_ready(self) -> bool:
        """
        Check if the environment is ready for use.

        Returns:
            True if environment is in ready status
        """
        return self.status == "ready"

    def is_draft(self) -> bool:
        """
        Check if the environment is in draft status.

        Returns:
            True if environment is in draft status
        """
        return self.status == "draft"

    def is_deleted(self) -> bool:
        """
        Check if the environment is deleted.

        Returns:
            True if environment is deleted
        """
        return self.status == "deleted"
