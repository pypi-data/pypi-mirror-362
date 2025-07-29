"""
Model for test_run_dash_output_steps collection.
"""

import datetime
from typing import Any, Dict, List, Optional

from .base import BaseModel


class TestRunDashOutputSteps(BaseModel):
    """
    TestRunDashOutputSteps model for test_run_dash_output_steps collection
    """

    def __init__(self, data: Dict[str, Any]):
        """
        Initialize a TestRunDashOutputSteps instance

        Args:
            data: Dictionary containing model data
        """
        super().__init__(data)
        self.metadata = data.get("metadata")
        self.name = data.get("name")
        self.status = data.get("status")
        self.tenant = data.get("tenant")
        self.modified_by = data.get("modified_by")
        self.test_run_dash_output = data.get("test_run_dash_output")
        self.end_time = data.get("end_time")
        self.step = data.get("step")
        self.execution_helper = data.get("execution_helper")
        self.is_assert = data.get("is_assert")
        self.is_passed = data.get("is_passed")
        self.assert_summary = data.get("assert_summary")
        self.is_terminated = data.get("is_terminated")
        self.is_completed = data.get("is_completed")
        self.final_response = data.get("final_response")
        self.step_result = data.get("step_result")
        self.tags = data.get("tags")
        self.start_time = data.get("start_time")
