"""
Type stubs for the TestManager class.
"""

from typing import Any, Dict, List, Literal, Optional, TypedDict, Union

from testzeus_sdk.client import TestZeusClient
from testzeus_sdk.managers.base import BaseManager
from testzeus_sdk.models.test import Test

class TestManager(BaseManager[Test]):
    """
    Manager class for TestZeus test entities.

    This class provides CRUD operations and specialized methods
    for working with test entities.
    """

    def __init__(self, client: TestZeusClient) -> None: ...
    async def create(self, data: Dict[str, Any]) -> Test: ...
    async def create_test(
        self,
        name: str,
        test_feature: str,
        status: Literal["draft", "ready", "deleted"] = ...,
        test_data: Optional[List[str]] = ...,
        tags: Optional[List[str]] = ...,
        environment: Optional[str] = ...,
    ) -> Test: ...
    async def update(self, id_or_name: str, data: Dict[str, Any]) -> Test: ...
    async def update_test(
        self,
        id_or_name: str,
        name: Optional[str] = ...,
        test_feature: Optional[str] = ...,
        status: Optional[Literal["draft", "ready", "deleted"]] = ...,
        test_data: Optional[List[str]] = ...,
        tags: Optional[List[str]] = ...,
        environment: Optional[str] = ...,
    ) -> Test: ...
    async def run_test(
        self,
        id_or_name: str,
        environment: Optional[str] = ...,
        tags: Optional[List[str]] = ...,
        modified_by: Optional[str] = ...,
        tenant: Optional[str] = ...,
    ) -> Dict[str, Any]: ...
    async def run_test_with_email(
        self,
        id_or_name: str,
        user_email: str,
        environment: Optional[str] = ...,
        tags: Optional[List[str]] = ...,
        tenant: Optional[str] = ...,
    ) -> Dict[str, Any]: ...
    async def add_tags(self, id_or_name: str, tags: List[str]) -> Test: ...
    def _process_references(self, data: Dict[str, Any]) -> Dict[str, Any]: ...
