"""
Tag model class for TestZeus tag entities.
"""

from typing import Any, Dict, Optional

from testzeus_sdk.models.base import BaseModel


class Tag(BaseModel):
    """
    Model class for TestZeus tag entities.

    This class represents tag entities in TestZeus, which can be
    used to categorize and organize other entities.
    """

    def __init__(self, data: Dict[str, Any]):
        """
        Initialize a Tag model with data from the API.

        Args:
            data: Dictionary containing tag data
        """
        super().__init__(data)

        # Extract common fields
        self.name = data.get("name")
        self.tenant = data.get("tenant")
        self.modified_by = data.get("modified_by")
        self.value = data.get("value")
