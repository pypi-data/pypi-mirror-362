"""
Base model class for TestZeus entities.
"""

import datetime
from typing import Any, Dict, List, Optional


class BaseModel:
    """
    Base model class for all TestZeus entities.

    This class provides common functionality for all entity models,
    including data validation and conversion.
    """

    def __init__(self, data: Dict[str, Any]):
        """
        Initialize a model with data from the API.

        Args:
            data: Dictionary containing model data
        """
        self.id = data.get("id")
        self.created = data.get("created")
        self.updated = data.get("updated")
        self.data = data

    @staticmethod
    def _parse_date(date_str: Optional[str]) -> Optional[datetime.datetime]:
        """
        Parse date string from API to Python datetime.

        Args:
            date_str: Date string from API

        Returns:
            Parsed datetime or None
        """
        if not date_str:
            return None

        try:
            return datetime.datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except (ValueError, TypeError):
            return None

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert model to dictionary representation.

        Returns:
            Dictionary representation of the model
        """
        return self.data.copy()
