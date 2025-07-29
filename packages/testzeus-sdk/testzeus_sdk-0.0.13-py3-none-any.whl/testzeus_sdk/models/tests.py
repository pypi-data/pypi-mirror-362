"""
Model for tests collection.
"""

import datetime
from typing import Any, Dict, List, Optional

from .base import BaseModel


class Tests(BaseModel):
    """
    Tests model for tests collection
    """

    def __init__(self, data: Dict[str, Any]):
        """
        Initialize a Tests instance

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
        self.test_design = data.get("test_design")
        self.test_params = data.get("test_params")
        self.test_data = data.get("test_data")
        self.test_feature = data.get("test_feature")
        self.tags = data.get("tags")
        self.environment = data.get("environment")
