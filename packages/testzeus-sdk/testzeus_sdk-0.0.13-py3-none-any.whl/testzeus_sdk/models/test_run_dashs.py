"""
Model for test_run_dashs collection.
"""

import datetime
from typing import Any, Dict, List, Optional

from .base import BaseModel


class TestRunDashs(BaseModel):
    """
    TestRunDashs model for test_run_dashs collection
    """

    def __init__(self, data: Dict[str, Any]):
        """
        Initialize a TestRunDashs instance

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
        self.end_time = data.get("end_time")
        self.dash_feature = data.get("dash_feature")
        self.test_status = data.get("test_status")
        self.workflow_run_id = data.get("workflow_run_id")
        self.tags = data.get("tags")
        self.start_time = data.get("start_time")
