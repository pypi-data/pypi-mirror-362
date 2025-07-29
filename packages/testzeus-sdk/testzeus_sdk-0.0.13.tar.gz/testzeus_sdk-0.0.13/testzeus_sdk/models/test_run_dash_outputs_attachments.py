"""
Model for test_run_dash_outputs_attachments collection.
"""

import datetime
from typing import Any, Dict, List, Optional

from .base import BaseModel


class TestRunDashOutputsAttachments(BaseModel):
    """
    TestRunDashOutputsAttachments model for test_run_dash_outputs_attachments collection
    """

    def __init__(self, data: Dict[str, Any]):
        """
        Initialize a TestRunDashOutputsAttachments instance

        Args:
            data: Dictionary containing model data
        """
        super().__init__(data)
        self.metadata = data.get("metadata")
        self.name = data.get("name")
        self.tenant = data.get("tenant")
        self.modified_by = data.get("modified_by")
        self.test_run_dash = data.get("test_run_dash")
        self.test_run_dash_output = data.get("test_run_dash_output")
        self.file = data.get("file")
        self.file_type = data.get("file_type")
        self.test_run_dash_output_steps = data.get("test_run_dash_output_steps")
        self.tags = data.get("tags")
