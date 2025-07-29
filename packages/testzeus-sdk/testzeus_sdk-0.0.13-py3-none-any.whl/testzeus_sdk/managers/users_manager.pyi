"""
Type stubs for the UsersManager class.
"""

from typing import Any, Dict, List, Optional

from testzeus_sdk.client import TestZeusClient
from testzeus_sdk.managers.base import BaseManager
from testzeus_sdk.models.users import Users

class UsersManager(BaseManager[Users]):
    """
    Manager for Users resources
    """

    def __init__(self, client: TestZeusClient) -> None: ...
    async def find_by_email(self, email: str) -> Optional[Users]: ...
    def _process_references(self, data: Dict[str, Any]) -> Dict[str, Any]: ...
