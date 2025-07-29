"""
Type stubs for the Test model.
"""

from typing import Any, Dict, List, Optional, Union

from testzeus_sdk.models.base import BaseModel

class Test(BaseModel):
    """
    Model class for TestZeus test entities.

    This class represents a test entity in TestZeus, which contains
    test definitions, features, and configurations.
    """

    name: Optional[str]
    status: Optional[str]
    tenant: Optional[str]
    modified_by: Optional[str]
    config: Optional[str]
    test_design: Optional[str]
    test_params: Optional[Dict[str, Any]]
    test_data: Optional[List[str]]
    test_feature: Optional[str]
    tags: Optional[List[str]]
    metadata: Optional[Dict[str, Any]]
    expand: Optional[Dict[str, Any]]

    def __init__(self, data: Dict[str, Any]) -> None: ...
    def is_ready(self) -> bool: ...
    def is_draft(self) -> bool: ...
    def is_deleted(self) -> bool: ...
