"""
Test manager class for TestZeus test operations.
"""

import datetime
from typing import Any, Dict, List, Literal, Optional, TypedDict

from typing_extensions import NotRequired

from testzeus_sdk.client import TestZeusClient
from testzeus_sdk.managers.base import BaseManager
from testzeus_sdk.models.test import Test
from testzeus_sdk.utils.helpers import get_id_by_name


class TestManager(BaseManager[Test]):
    """
    Manager class for TestZeus test entities.

    This class provides CRUD operations and specialized methods
    for working with test entities.
    """

    def __init__(self, client: TestZeusClient) -> None:
        """
        Initialize a TestManager.

        Args:
            client: TestZeus client instance
        """
        super().__init__(client, "tests", Test)

    async def create(self, data: Dict[str, Any]) -> Test:
        """
        Create a new Test entity.

        Args:
            data: Test data

        Returns:
            Test: The created Test instance.
        """
        return await super().create(data)

    # Helper method to create a test with individual fields
    async def create_test(
        self,
        name: str,
        test_feature: str,
        status: Literal["draft", "ready", "deleted"] = "draft",
        test_data: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        environment: Optional[str] = None,
        execution_mode: Optional[Literal["lenient", "strict"]] = "lenient",
    ) -> Test:
        """
        Create a new Test entity with individual fields.

        This method creates a new test record using the provided data.
        If the 'status' field is not specified, it defaults to 'draft'.

        Args:
            name (str): Name of the test. Required and Unique
            test_feature (str): Associated test feature. Required.
            status (str, optional): Status ('draft' by default).
            test_data (List[str], optional): Test data IDs.
            tags (List[str], optional): Tag IDs.
            environment (str, optional): Environment ID.

        Returns:
            Test: The created Test instance.
        """
        data = {
            "name": name,
            "status": status,
            "test_feature": test_feature,
            "test_data": test_data,
            "tags": tags,
            "environment": environment,
            "execution_mode": execution_mode,
            "metadata": {},
            "test_params": {},
        }

        return await self.create(data)

    async def update(self, id_or_name: str, data: Dict[str, Any]) -> Test:
        """
        Update an existing Test entity.

        Args:
            id_or_name: Test ID or name
            data: Updated test data

        Returns:
            Test: The updated Test instance.
        """
        return await super().update(id_or_name, data)

    # Helper method to update test with individual fields
    async def update_test(
        self,
        id_or_name: str,
        name: Optional[str] = None,
        test_feature: Optional[str] = None,
        status: Optional[Literal["draft", "ready", "deleted"]] = None,
        test_data: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        environment: Optional[str] = None,
        execution_mode: Optional[Literal["lenient", "strict"]] = None,
    ) -> Test:
        """
        Update an existing Test entity with individual fields.

        Args:
            id_or_name: Test ID or name
            name (str, optional): Name of the test.
            test_feature (str, optional): Associated test feature.
            status (str, optional): Status.
            test_data (List[str], optional): Test data IDs.
            tags (List[str], optional): Tag IDs.
            environment (str, optional): Environment ID.

        Returns:
            Test: The updated Test instance.
        """
        data = {
            key: value
            for key, value in {
                "name": name,
                "test_feature": test_feature,
                "status": status,
                "test_data": test_data,
                "tags": tags,
                "environment": environment,
                "execution_mode": execution_mode,
            }.items()
            if value is not None
        }

        return await self.update(id_or_name, data)

    async def run_test(
        self,
        id_or_name: str,
        execution_mode: Optional[Literal["lenient", "strict"]] = "lenient",
        modified_by: Optional[str] = None,
        tenant: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create and start a test run for a test.

        Args:
            id_or_name: Test ID or name
            environment: Environment name or ID (optional)
            tags: List of tag names or IDs (optional)
            modified_by: User ID who is modifying the test run (optional)
            tenant: Tenant ID to associate with this test run (optional)

        Returns:
            Created test run data
        """
        # Get the test
        test = await self.get_one(id_or_name)

        # Import here to avoid circular imports
        from testzeus_sdk.managers.test_run_manager import TestRunManager

        test_run_manager = TestRunManager(self.client)
        run_name = f"Run of {test.name}"
        test_run = await test_run_manager.create_and_start(run_name, str(test.id), modified_by=modified_by, tenant=tenant, execution_mode=execution_mode)
        return test_run

    async def add_tags(self, id_or_name: str, tags: List[str]) -> Test:
        """
        Add tags to a test.

        Args:
            id_or_name: Test ID or name
            tags: List of tag names or IDs

        Returns:
            Updated test instance
        """
        # Get the test
        test = await self.get_one(id_or_name)

        # Process tags
        tag_ids = []
        current_tags = test.tags or []

        # Add existing tags
        if isinstance(current_tags, list):
            tag_ids.extend(current_tags)

        # Process new tags
        for tag in tags:
            if self._is_valid_id(tag):
                if tag not in tag_ids:
                    tag_ids.append(tag)
            else:
                tag_id = get_id_by_name(self.client, "tags", tag)
                if tag_id and tag_id not in tag_ids:
                    tag_ids.append(tag_id)

        # Update the test with the new tags
        update_data = {"tags": tag_ids}
        return await self.update(str(test.id), update_data)

    def _process_references(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process name-based references to ID-based references.

        Args:
            data: Test data with potential name-based references

        Returns:
            Processed data with ID-based references
        """
        result = data.copy()
        tenant_id = self.client.get_tenant_id()

        # Process config reference
        if "config" in result and isinstance(result["config"], str) and not self._is_valid_id(result["config"]):
            config_id = get_id_by_name(self.client, "agent_configs", result["config"], tenant_id)
            if config_id:
                result["config"] = config_id

        # Process test_design reference
        if "test_design" in result and isinstance(result["test_design"], str) and not self._is_valid_id(result["test_design"]):
            design_id = get_id_by_name(self.client, "test_designs", result["test_design"], tenant_id)
            if design_id:
                result["test_design"] = design_id

        # Process test_data references
        if "test_data" in result and isinstance(result["test_data"], list):
            data_ids = []
            for data_item in result["test_data"]:
                if isinstance(data_item, str):
                    if self._is_valid_id(data_item):
                        data_ids.append(data_item)
                    else:
                        data_id = get_id_by_name(self.client, "test_data", data_item, tenant_id)
                        if data_id:
                            data_ids.append(data_id)
            result["test_data"] = data_ids

        # Process tags references
        if "tags" in result and isinstance(result["tags"], list):
            tag_ids = []
            for tag in result["tags"]:
                if isinstance(tag, str):
                    if self._is_valid_id(tag):
                        tag_ids.append(tag)
                    else:
                        tag_id = get_id_by_name(self.client, "tags", tag, tenant_id)
                        if tag_id:
                            tag_ids.append(tag_id)
            result["tags"] = tag_ids

        return result

    async def run_test_with_email(
        self,
        id_or_name: str,
        user_email: str,
        environment: Optional[str] = None,
        tags: Optional[List[str]] = None,
        tenant: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create and start a test run for a test, using a user's email address.

        Args:
            id_or_name: Test ID or name
            user_email: Email address of the user who is modifying the test run
            environment: Environment name or ID (optional)
            tags: List of tag names or IDs (optional)
            tenant: Tenant ID to associate with this test run (optional)

        Returns:
            Created test run data
        """
        # Look up the user ID from the email
        user = await self.client.users.find_by_email(user_email)
        if not user:
            raise ValueError(f"Could not find user with email: {user_email}")

        # Use the user ID to run the test
        return await self.run_test(
            id_or_name=id_or_name,
            environment=environment,
            tags=tags,
            modified_by=str(user.id),
            tenant=tenant,
        )
