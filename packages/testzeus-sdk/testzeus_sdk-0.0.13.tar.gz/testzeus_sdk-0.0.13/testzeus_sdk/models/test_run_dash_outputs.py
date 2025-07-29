"""
Model for test_run_dash_outputs collection.
"""

import datetime
from typing import Any, Dict, List, Optional

from .base import BaseModel


class TestRunDashOutputs(BaseModel):
    """
    TestRunDashOutputs model for test_run_dash_outputs collection
    """

    def __init__(self, data: Dict[str, Any]):
        """
        Initialize a TestRunDashOutputs instance

        Args:
            data: Dictionary containing model data
        """
        super().__init__(data)
        self.metadata = data.get("metadata")
        self.name = data.get("name")
        self.status = data.get("status")
        self.tenant = data.get("tenant")
        self.modified_by = data.get("modified_by")
        self.test_run_dash = data.get("test_run_dash")
        self.execution_plan = data.get("execution_plan")
        self.tags = data.get("tags")
