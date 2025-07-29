"""
Model for test_designs collection.
"""

import datetime
from typing import Any, Dict, List, Optional

from .base import BaseModel


class TestDesigns(BaseModel):
    """
    TestDesigns model for test_designs collection
    """

    def __init__(self, data: Dict[str, Any]):
        """
        Initialize a TestDesigns instance

        Args:
            data: Dictionary containing model data
        """
        super().__init__(data)
        self.metadata = data.get("metadata")
        self.name = data.get("name")
        self.status = data.get("status")
        self.tenant = data.get("tenant")
        self.modified_by = data.get("modified_by")
        self.config = data.get("config")
        self.design_params = data.get("design_params")
        self.source_data = data.get("source_data")
        self.tags = data.get("tags")
