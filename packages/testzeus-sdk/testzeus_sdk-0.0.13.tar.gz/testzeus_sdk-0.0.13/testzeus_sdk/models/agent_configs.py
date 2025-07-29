"""
Model for agent_configs collection.
"""

import datetime
from typing import Any, Dict, List, Optional

from .base import BaseModel


class AgentConfigs(BaseModel):
    """
    AgentConfigs model for agent_configs collection
    """

    def __init__(self, data: Dict[str, Any]):
        """
        Initialize a AgentConfigs instance

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
        self.deleted = data.get("deleted")
        self.llm_config = data.get("llm_config")
        self.tags = data.get("tags")
