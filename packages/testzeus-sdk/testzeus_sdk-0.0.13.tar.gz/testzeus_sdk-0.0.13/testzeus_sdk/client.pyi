"""
Type stubs for the TestZeus client.
"""

import asyncio
from typing import Any, Dict, List, Optional, Union

import aiohttp
from pocketbase import PocketBase

from testzeus_sdk.managers.agent_configs_manager import AgentConfigsManager
from testzeus_sdk.managers.environment_manager import EnvironmentManager
from testzeus_sdk.managers.tag_manager import TagManager
from testzeus_sdk.managers.tenant_consumption_logs_manager import (
    TenantConsumptionLogsManager,
)
from testzeus_sdk.managers.tenant_consumption_manager import TenantConsumptionManager
from testzeus_sdk.managers.test_data_manager import TestDataManager
from testzeus_sdk.managers.test_designs_manager import TestDesignsManager
from testzeus_sdk.managers.test_device_manager import TestDeviceManager
from testzeus_sdk.managers.test_manager import TestManager
from testzeus_sdk.managers.test_run_dash_output_steps_manager import (
    TestRunDashOutputStepsManager,
)
from testzeus_sdk.managers.test_run_dash_outputs_attachments_manager import (
    TestRunDashOutputsAttachmentsManager,
)
from testzeus_sdk.managers.test_run_dash_outputs_manager import (
    TestRunDashOutputsManager,
)
from testzeus_sdk.managers.test_run_dashs_manager import TestRunDashsManager
from testzeus_sdk.managers.test_run_manager import TestRunManager
from testzeus_sdk.managers.users_manager import UsersManager

class TestZeusClient:
    """
    Client for interacting with TestZeus API.

    This client wraps the PocketBase client and provides access to all TestZeus
    functionality through specialized managers for each entity type.
    """

    base_url: str
    email: Optional[str]
    password: Optional[str]
    pb: PocketBase
    token: Optional[str]
    session: Optional[aiohttp.ClientSession]
    _authenticated: bool
    _tenant_id: str

    # Manager instances
    tests: TestManager
    test_runs: TestRunManager
    test_data: TestDataManager
    environments: EnvironmentManager
    tags: TagManager
    users: UsersManager
    agent_configs: AgentConfigsManager
    test_devices: TestDeviceManager
    test_designs: TestDesignsManager
    test_run_dashs: TestRunDashsManager
    test_run_dash_outputs: TestRunDashOutputsManager
    test_run_dash_output_steps: TestRunDashOutputStepsManager
    tenant_consumption: TenantConsumptionManager
    tenant_consumption_logs: TenantConsumptionLogsManager
    test_run_dash_outputs_attachments: TestRunDashOutputsAttachmentsManager

    def __init__(
        self,
        base_url: Optional[str] = ...,
        email: Optional[str] = ...,
        password: Optional[str] = ...,
    ) -> None: ...
    async def __aenter__(self) -> "TestZeusClient": ...
    async def __aexit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[Exception],
        exc_tb: Optional[asyncio.Task],
    ) -> None: ...
    async def ensure_authenticated(self) -> None: ...
    async def authenticate(self, email: str, password: str) -> str: ...
    def _store_tenant_info(self, tenant_id: str) -> None: ...
    def _get_headers(self) -> Dict[str, str]: ...
    async def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = ...,
        json_data: Optional[Dict[str, Any]] = ...,
        data: Optional[Any] = ...,
    ) -> Any: ...
    def is_authenticated(self) -> bool: ...
    def logout(self) -> None: ...
    def get_tenant_id(self) -> str: ...
    def get_user_id(self) -> str: ...
    def get_file_token(self) -> str: ...
    def set_tenant_id(self, tenant_id: str) -> None: ...
