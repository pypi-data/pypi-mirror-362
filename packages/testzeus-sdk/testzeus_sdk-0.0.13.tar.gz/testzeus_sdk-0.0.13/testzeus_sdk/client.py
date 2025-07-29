"""
Main client class for TestZeus SDK.
"""

import asyncio
import json
import os
from typing import Any, Dict, List, Optional, Union

import aiohttp
from pocketbase import PocketBase


class TestZeusClient:
    """
    Client for interacting with TestZeus API.

    This client wraps the PocketBase client and provides access to all TestZeus
    functionality through specialized managers for each entity type.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
    ):
        """
        Initialize the TestZeus client

        Args:
            base_url: TestZeus API base URL
            email: User email for authentication
            password: User password for authentication
        """
        default_url = "https://pb.prod.testzeus.app"
        self.base_url = base_url or os.environ.get("TESTZEUS_BASE_URL", default_url)
        if self.base_url:
            self.base_url = self.base_url.rstrip("/")
        self.email = email or os.environ.get("TESTZEUS_EMAIL")
        self.password = password or os.environ.get("TESTZEUS_PASSWORD")

        # Initialize the PocketBase client
        self.pb = PocketBase(self.base_url or default_url)  # Ensure non-None value is passed

        # Auth token and session
        self.token: Optional[str] = None
        self.session: Optional[aiohttp.ClientSession] = None
        self._authenticated = False

        # Import here to avoid circular imports
        # Import new managers
        from testzeus_sdk.managers.agent_configs_manager import AgentConfigsManager
        from testzeus_sdk.managers.environment_manager import EnvironmentManager
        from testzeus_sdk.managers.tag_manager import TagManager
        from testzeus_sdk.managers.tenant_consumption_logs_manager import (
            TenantConsumptionLogsManager,
        )
        from testzeus_sdk.managers.tenant_consumption_manager import (
            TenantConsumptionManager,
        )
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

        # Initialize managers
        self.tests = TestManager(self)
        self.test_runs = TestRunManager(self)
        self.test_data = TestDataManager(self)
        self.environments = EnvironmentManager(self)
        self.tags = TagManager(self)
        self.users = UsersManager(self)

        # Initialize new managers
        self.agent_configs = AgentConfigsManager(self)
        self.test_devices = TestDeviceManager(self)
        self.test_designs = TestDesignsManager(self)
        self.test_run_dashs = TestRunDashsManager(self)
        self.test_run_dash_outputs = TestRunDashOutputsManager(self)
        self.test_run_dash_output_steps = TestRunDashOutputStepsManager(self)
        self.tenant_consumption = TenantConsumptionManager(self)
        self.tenant_consumption_logs = TenantConsumptionLogsManager(self)
        self.test_run_dash_outputs_attachments = TestRunDashOutputsAttachmentsManager(self)

    async def __aenter__(self) -> "TestZeusClient":
        """Context manager entry point"""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[Exception],
        exc_tb: Optional[asyncio.Task],
    ) -> None:
        """Context manager exit point"""
        if self.session and not self.session.closed:
            await self.session.close()
            self.session = None

    async def ensure_authenticated(self) -> None:
        """
        Ensure the client is authenticated before making API calls
        """
        if self._authenticated:
            # Make sure PocketBase client has the token
            if self.token and not self.pb.auth_store.token:
                self.pb.auth_store.save(self.token, None)
            return

        if self.session is None:
            self.session = aiohttp.ClientSession()

        if self.email and self.password:
            # Username/password authentication
            await self.authenticate(self.email, self.password)
        else:
            raise ValueError("Authentication credentials not provided. " "Set email/password via constructor or environment variables.")

    async def authenticate(self, email: str, password: str) -> str:
        """
        Authenticate with email and password

        Args:
            email: User email
            password: User password

        Returns:
            Authentication token
        """
        if self.session is None:
            self.session = aiohttp.ClientSession()

        # First authenticate with PocketBase client
        try:
            auth_data = self.pb.collection("users").auth_with_password(email, password)
            self.token = auth_data.token
            self._authenticated = True

            # Extract and store tenant information if available
            if hasattr(auth_data.record, "tenant"):
                # Store tenant information for future use
                tenant_id = getattr(auth_data.record, "tenant")
                if tenant_id:
                    self._store_tenant_info(tenant_id)

            return self.token or ""  # Return empty string if token is None
        except Exception as e:
            # Fallback to our own authentication if PocketBase client fails
            if self.session is None:  # Double-check session exists
                self.session = aiohttp.ClientSession()

            auth_url = f"{self.base_url}/api/collections/users/auth-with-password"
            auth_payload = {
                "identity": email,
                "password": password,
            }

            async with self.session.post(auth_url, json=auth_payload) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise ValueError(f"Authentication failed: {error_text}")

                data = await response.json()
                self.token = data.get("token")

                if not self.token:
                    raise ValueError("Authentication succeeded but no token was returned")

                # Extract and store tenant information if available
                if data.get("record") and data["record"].get("tenant"):
                    tenant_id = data["record"]["tenant"]
                    self._store_tenant_info(tenant_id)

                    # Save auth data to PocketBase client
                    self.pb.auth_store.save(self.token, data.get("record"))

                self._authenticated = True
                return self.token

    def _store_tenant_info(self, tenant_id: str) -> None:
        """
        Internal method to store tenant information safely

        Args:
            tenant_id: The tenant ID to store
        """
        # Use PocketBase's auth store to save tenant info if possible
        if self.pb.auth_store.model:
            # Try to set the tenant attribute, safely handling read-only properties
            try:
                if not hasattr(self.pb.auth_store.model, "tenant"):
                    object.__setattr__(self.pb.auth_store.model, "tenant", tenant_id)
                elif getattr(self.pb.auth_store.model, "tenant") != tenant_id:
                    object.__setattr__(self.pb.auth_store.model, "tenant", tenant_id)
            except (AttributeError, TypeError):
                # If we can't set it directly, store it separately
                self._tenant_id = tenant_id
        else:
            # Store tenant ID separately if model is not available
            self._tenant_id = tenant_id

    def _get_headers(self) -> Dict[str, str]:
        """
        Get headers for API requests

        Returns:
            Dictionary of HTTP headers
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        if self.token:
            # Token auth from login
            headers["Authorization"] = f"Bearer {self.token}"

        return headers

    async def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
    ) -> Any:
        """
        Make an API request

        Args:
            method: HTTP method (GET, POST, PATCH, DELETE)
            endpoint: API endpoint (starting with /)
            params: Query parameters
            json_data: JSON body for POST/PATCH requests
            data: Form data for POST requests

        Returns:
            API response as dictionary
        """
        await self.ensure_authenticated()

        if self.session is None:
            self.session = aiohttp.ClientSession()

        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()

        async with self.session.request(
            method=method,
            url=url,
            params=params,
            json=json_data,
            data=data,
            headers=headers,
        ) as response:
            response_text = await response.text()

            if not response_text:
                # Handle empty responses
                if 200 <= response.status < 300:
                    return {}
                else:
                    raise ValueError(f"Request failed with status {response.status}: Empty response")

            try:
                import json as json_module

                response_json = json_module.loads(response_text)
            except ValueError:
                if 200 <= response.status < 300:
                    # Success with non-JSON response
                    return {"data": response_text}
                else:
                    # Error with non-JSON response
                    raise ValueError(f"Request failed with status {response.status}: {response_text}")

            # Check for error response
            if not (200 <= response.status < 300):
                error_message = response_json.get("message", response_json) if isinstance(response_json, dict) else response_text
                raise ValueError(f"Request failed with status {response.status}: {error_message}")

            return response_json

    def is_authenticated(self) -> bool:
        """
        Check if the client is authenticated

        Returns:
            True if authenticated
        """
        return self._authenticated and self.token is not None

    def logout(self) -> None:
        """
        Logout and clear authentication state
        """
        self.token = None
        self._authenticated = False

    def get_tenant_id(self) -> str:
        """
        Get the current tenant ID

        Returns:
            Tenant ID or default tenant ID if not authenticated
        """
        # Default tenant ID if model is None
        DEFAULT_TENANT_ID = "pbc_138639755"

        if not self._authenticated:
            return DEFAULT_TENANT_ID

        try:
            # First check if we have stored it separately
            if hasattr(self, "_tenant_id"):
                return self._tenant_id

            # Then check if it's in the auth store model
            if self.pb.auth_store.model and hasattr(self.pb.auth_store.model, "tenant"):
                tenant_id = getattr(self.pb.auth_store.model, "tenant")
                if tenant_id:
                    return str(tenant_id)  # Ensure we return a string

            # If we couldn't get tenant from model, log a message and return default
            print("Warning: Using default tenant ID. Tenant information was not extracted during login.")
            return DEFAULT_TENANT_ID
        except Exception as e:
            # Fallback to default tenant ID if any issue occurs
            print(f"Warning: Error getting tenant ID: {str(e)}. Using default.")
            return DEFAULT_TENANT_ID

    def get_user_id(self) -> str:
        """
        Get the current User ID

        Returns:
            User ID or empty string if not authenticated or not implemented
        """
        try:
            if self.pb.auth_store.model and hasattr(self.pb.auth_store.model, "id"):
                return self.pb.auth_store.model.id
            return ""
        except Exception:
            return ""

    def get_file_token(self) -> str:
        """
        Get the current file token
        """
        return self.pb.get_file_token()

    def set_tenant_id(self, tenant_id: str) -> None:
        """
        Explicitly set the tenant ID to use for operations

        Args:
            tenant_id: The tenant ID to use
        """
        # Store tenant ID using the safe method
        self._store_tenant_info(tenant_id)

        # Print confirmation message
        print(f"Tenant ID set to: {tenant_id}")
