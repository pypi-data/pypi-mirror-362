"""
Type stubs for the BaseModel class.
"""

import datetime
from typing import Any, Dict, Generic, List, Optional, TypeVar

def record_to_dict(record: Any) -> Dict[str, Any]: ...

T = TypeVar("T", bound="BaseModel")

class BaseModel:
    """
    Base model class for all TestZeus entities.

    This class provides common functionality for all entity models,
    including data validation and conversion.
    """

    id: Optional[str]
    created: Optional[datetime.datetime]
    updated: Optional[datetime.datetime]
    data: Dict[str, Any]

    def __init__(self, data: Dict[str, Any]) -> None: ...
    @staticmethod
    def _parse_date(date_str: Optional[str]) -> Optional[datetime.datetime]: ...
    def to_dict(self) -> Dict[str, Any]: ...
