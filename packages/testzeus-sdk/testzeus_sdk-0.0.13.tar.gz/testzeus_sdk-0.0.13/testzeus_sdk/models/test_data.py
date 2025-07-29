"""
TestData model class for TestZeus test data entities.
"""

from typing import Any, Dict, List, Optional

from testzeus_sdk.models.base import BaseModel


class TestData(BaseModel):
    """
    Model class for TestZeus test data entities.

    This class represents test data entities in TestZeus, which can be
    used for test inputs, configurations, or reference data.
    """

    def __init__(self, data: Dict[str, Any]):
        """
        Initialize a TestData model with data from the API.

        Args:
            data: Dictionary containing test data
        """
        super().__init__(data)

        # Extract common fields
        self.name = data.get("name")
        self.status = data.get("status")
        self.tenant = data.get("tenant")
        self.modified_by = data.get("modified_by")
        self.type = data.get("type")
        self.supporting_data_files = data.get("supporting_data_files")
        self.data_content = data.get("data")
        self.tags = data.get("tags")
        self.metadata = data.get("metadata")
        self.cached_prompt_details = data.get("cached_prompt_details")

    def is_ready(self) -> bool:
        """
        Check if the test data is ready for use.

        Returns:
            True if test data is in ready status
        """
        return self.status == "ready"

    def is_draft(self) -> bool:
        """
        Check if the test data is in draft status.

        Returns:
            True if test data is in draft status
        """
        return self.status == "draft"

    def is_deleted(self) -> bool:
        """
        Check if the test data is deleted.

        Returns:
            True if test data is deleted
        """
        return self.status == "deleted"

    def get_data_value(self) -> Any:
        """
        Get the test data value.

        Returns:
            Test data value
        """
        return self.data_content
