"""
Model for tenant_consumption_logs collection.
"""

import datetime
from typing import Any, Dict, List, Optional

from .base import BaseModel


class TenantConsumptionLogs(BaseModel):
    """
    TenantConsumptionLogs model for tenant_consumption_logs collection
    """

    def __init__(self, data: Dict[str, Any]):
        """
        Initialize a TenantConsumptionLogs instance

        Args:
            data: Dictionary containing model data
        """
        super().__init__(data)
        self.tenant = data.get("tenant")
        self.execution_id = data.get("execution_id")
        self.execution_type = data.get("execution_type")
        self.is_processed = data.get("is_processed")
        self.updated_by = data.get("updated_by")
        self.is_completed = data.get("is_completed")
        self.steps_consumed = data.get("steps_consumed")
        self.tags = data.get("tags")
