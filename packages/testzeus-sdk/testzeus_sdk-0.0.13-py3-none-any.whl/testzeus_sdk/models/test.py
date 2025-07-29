"""
Test model class for TestZeus test entities.
"""

from typing import Any, Dict, List, Optional

from testzeus_sdk.models.base import BaseModel


class Test(BaseModel):
    """
    Model class for TestZeus test entities.

    This class represents a test entity in TestZeus, which contains
    test definitions, features, and configurations.
    """

    def __init__(self, data: Dict[str, Any]):
        """
        Initialize a Test model with data from the API.

        Args:
            data: Dictionary containing test data
        """
        super().__init__(data)

        # Extract common fields
        self.name = data.get("name")
        self.status = data.get("status")
        self.tenant = data.get("tenant")
        self.modified_by = data.get("modified_by")
        self.config = data.get("config")
        self.test_design = data.get("test_design")
        self.test_params = data.get("test_params")
        self.test_data = data.get("test_data")
        self.test_feature = data.get("test_feature")
        self.tags = data.get("tags")
        self.metadata = data.get("metadata")
        self.expand = data.get("expand")
        self.execution_mode = data.get("execution_mode")

    def is_ready(self) -> bool:
        """
        Check if the test is ready for execution.

        Returns:
            True if test is in ready status
        """
        return self.status == "ready"

    def is_draft(self) -> bool:
        """
        Check if the test is in draft status.

        Returns:
            True if test is in draft status
        """
        return self.status == "draft"

    def is_deleted(self) -> bool:
        """
        Check if the test is deleted.

        Returns:
            True if test is deleted
        """
        return self.status == "deleted"
