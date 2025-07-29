"""
Model for tenants collection.
"""

import datetime
from typing import Any, Dict, List, Optional

from .base import BaseModel


class Tenants(BaseModel):
    """
    Tenants model for tenants collection
    """

    def __init__(self, data: Dict[str, Any]):
        """
        Initialize a Tenants instance

        Args:
            data: Dictionary containing model data
        """
        super().__init__(data)
        self.password = data.get("password")
        self.tokenKey = data.get("tokenKey")
        self.email = data.get("email")
        self.emailVisibility = data.get("emailVisibility")
        self.verified = data.get("verified")
        self.description = data.get("description")
        self.is_active = data.get("is_active")
        self.default_agent_config = data.get("default_agent_config")
