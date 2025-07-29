"""
Model for test_run_reports collection.
"""

import datetime
from typing import Any, Dict, List, Optional

from .base import BaseModel


class TestRunReports(BaseModel):
    """
    TestRunReports model for test_run_reports collection
    """

    def __init__(self, data: Dict[str, Any]):
        """
        Initialize a TestRunReports instance

        Args:
            data: Dictionary containing model data
        """
        super().__init__(data)
        self.metadata = data.get("metadata")
        self.name = data.get("name")
        self.status = data.get("status")
        self.tenant = data.get("tenant")
        self.modified_by = data.get("modified_by")
        self.test_run = data.get("test_run")
        self.output_data = data.get("output_data")
        self.result = data.get("result")
        self.tags = data.get("tags")
