"""
Model for tenant_consumption collection.
"""

import datetime
from typing import Any, Dict, List, Optional

from .base import BaseModel


class TenantConsumption(BaseModel):
    """
    TenantConsumption model for tenant_consumption collection
    """

    def __init__(self, data: Dict[str, Any]):
        """
        Initialize a TenantConsumption instance

        Args:
            data: Dictionary containing model data
        """
        super().__init__(data)
        self.tenant = data.get("tenant")
        self.plan_tenure_type = data.get("plan_tenure_type")
        self.test_run_dash_unit_value = data.get("test_run_dash_unit_value")
        self.test_design_unit_value = data.get("test_design_unit_value")
        self.max_credit_test_runs_dash = data.get("max_credit_test_runs_dash")
        self.max_credit_test_designs = data.get("max_credit_test_designs")
        self.used_credit_test_runs_dash = data.get("used_credit_test_runs_dash")
        self.used_credit_test_designs = data.get("used_credit_test_designs")
        self.max_allowed_users = data.get("max_allowed_users")
        self.used_users = data.get("used_users")
        self.test_run_step_unit_value = data.get("test_run_step_unit_value")
        self.tags = data.get("tags")
