"""
Model for tags collection.
"""

import datetime
from typing import Any, Dict, List, Optional

from .base import BaseModel


class Tags(BaseModel):
    """
    Tags model for tags collection
    """

    def __init__(self, data: Dict[str, Any]):
        """
        Initialize a Tags instance

        Args:
            data: Dictionary containing model data
        """
        super().__init__(data)
        self.name = data.get("name")
        self.tenant = data.get("tenant")
        self.modified_by = data.get("modified_by")
        self.value = data.get("value")
