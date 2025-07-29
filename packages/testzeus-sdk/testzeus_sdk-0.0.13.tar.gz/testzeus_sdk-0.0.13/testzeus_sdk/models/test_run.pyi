"""
Type stubs for the TestRun model.
"""

import datetime
from typing import Any, Dict, List, Optional

from testzeus_sdk.models.base import BaseModel

class TestRun(BaseModel):
    """
    Model class for TestZeus test run entities.

    This class represents a test run entity in TestZeus, which contains
    information about a test execution instance.
    """

    name: Optional[str]
    status: Optional[str]
    tenant: Optional[str]
    modified_by: Optional[str]
    test: Optional[str]
    start_time: Optional[datetime.datetime]
    end_time: Optional[datetime.datetime]
    test_status: Optional[str]
    workflow_run_id: Optional[str]
    tags: Optional[List[str]]
    metadata: Optional[Dict[str, Any]]
    dash_feature: Optional[str]

    def __init__(self, data: Dict[str, Any]) -> None: ...
    def is_running(self) -> bool: ...
    def is_completed(self) -> bool: ...
    def is_failed(self) -> bool: ...
    def is_crashed(self) -> bool: ...
    def is_cancelled(self) -> bool: ...
    def is_pending(self) -> bool: ...
    def get_duration(self) -> Optional[float]: ...
