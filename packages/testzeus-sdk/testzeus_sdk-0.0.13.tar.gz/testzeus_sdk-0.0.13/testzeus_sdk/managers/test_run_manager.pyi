"""
Type stubs for the TestRunManager class.
"""

from typing import Any, Dict, List, Optional, Union

from testzeus_sdk.client import TestZeusClient
from testzeus_sdk.managers.base import BaseManager
from testzeus_sdk.models.test_run import TestRun

class TestRunManager(BaseManager[TestRun]):
    """
    Manager class for TestZeus test run entities.

    This class provides CRUD operations and specialized methods
    for working with test run entities.
    """

    def __init__(self, client: TestZeusClient) -> None: ...
    async def create_and_start(
        self,
        name: str,
        test: str,
        modified_by: Optional[str] = ...,
        tenant: Optional[str] = ...,
    ) -> TestRun: ...
    async def create_and_start_with_email(
        self,
        name: str,
        test: str,
        user_email: str,
        tenant: Optional[str] = ...,
    ) -> TestRun: ...
    async def cancel(
        self,
        id_or_name: str,
        modified_by: Optional[str] = ...,
        tenant: Optional[str] = ...,
    ) -> TestRun: ...
    async def cancel_with_email(
        self,
        id_or_name: str,
        user_email: str,
        tenant: Optional[str] = ...,
    ) -> TestRun: ...
    async def get_expanded(self, id_or_name: str) -> Dict[str, Any]: ...
    async def download_all_attachments(
        self,
        id_or_name: str,
        output_dir: str = ...,
    ) -> List[str]: ...
    def _process_references(self, data: Dict[str, Any]) -> Dict[str, Any]: ...
