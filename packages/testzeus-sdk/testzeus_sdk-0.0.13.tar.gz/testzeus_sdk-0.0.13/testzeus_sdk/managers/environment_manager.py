"""
Environment manager class for TestZeus environment operations.
"""

from typing import Any, Dict, List, Literal, Optional, Text, Union

from pocketbase.client import FileUpload

from testzeus_sdk.client import TestZeusClient
from testzeus_sdk.managers.base import BaseManager
from testzeus_sdk.models.environment import Environment
from testzeus_sdk.utils.helpers import get_id_by_name


class EnvironmentManager(BaseManager[Environment]):
    """
    Manager class for TestZeus environment entities.

    This class provides CRUD operations and specialized methods
    for working with environment entities.
    """

    def __init__(self, client: TestZeusClient) -> None:
        """
        Initialize an EnvironmentManager.

        Args:
            client: TestZeus client instance
        """
        super().__init__(client, "environment", Environment)

    async def create(self, data: Dict[str, Any]) -> Environment:
        """
        Create a new environment.

        Args:
            data: Environment data

        Returns:
            Created environment instance
        """
        return await super().create(data)

    async def create_environment(
        self,
        name: Text,
        status: Literal["draft", "ready", "deleted"] = "draft",
        supporting_data_files: Optional[Text] = None,
        data: Optional[Text] = None,
        tags: Optional[List[Text]] = None,
    ) -> Environment:
        """
        Create a new environment with individual fields.

        Args:
            name: Name of the environment
            status: Status ('draft' by default)
            supporting_data_files: Path to supporting data files
            data: Environment data
            tags: List of tag IDs

        Returns:
            Created environment instance
        """
        env_data: Dict[str, Any] = {
            "name": name,
            "status": status,
            "data": data,
            "tags": tags,
            "metadata": {},
        }

        # Check for supporting_data_files and upload if present
        if supporting_data_files:
            filename = supporting_data_files
            env_data["supporting_data_files"] = FileUpload(filename, open(filename, "rb"))

        return await self.create(env_data)

    async def update(self, id_or_name: Text, data: Dict[str, Any]) -> Environment:
        """
        Update an existing environment.

        Args:
            id_or_name: Environment ID or name
            data: Updated environment data

        Returns:
            Updated environment instance
        """
        return await super().update(id_or_name, data)

    async def update_environment(
        self,
        id_or_name: Text,
        name: Optional[Text] = None,
        status: Optional[Literal["draft", "ready", "deleted"]] = None,
        supporting_data_files: Optional[Text] = None,
        env_data: Optional[Text] = None,
        tags: Optional[List[Text]] = None,
    ) -> Environment:
        """
        Update an existing environment with individual fields.

        Args:
            id_or_name: Environment ID or name
            name: Name of the environment
            status: Status
            supporting_data_files: Path to supporting data files
            env_data: Environment data
            tags: List of tag IDs

        Returns:
            Updated environment instance
        """
        update_data: Dict[str, Any] = {}
        if name:
            update_data["name"] = name
        if status:
            update_data["status"] = status
        if env_data:
            update_data["data"] = env_data
        if tags:
            update_data["tags"] = tags

        # Check for supporting_data_files and upload if present
        if supporting_data_files:
            filename = supporting_data_files
            update_data["supporting_data_files+"] = FileUpload(filename, open(filename, "rb"))

        return await self.update(id_or_name, update_data)

    async def add_file(self, id_or_name: str, file_name: str) -> Environment:
        """
        Add a file to an environment.
        """
        file = FileUpload(file_name, open(file_name, "rb"))
        return await self.update(id_or_name, {"supporting_data_files+": file})

    async def remove_file(self, id_or_name: str, file_name: str) -> Environment:
        """
        Remove a file from an environment.
        """
        environment = await self.get_one(id_or_name)
        if environment.supporting_data_files:
            for file in environment.supporting_data_files:
                if file_name.split("/")[-1].split(".")[0] in file:
                    file_name = file
                    break
        return await self.update(id_or_name, {"supporting_data_files-": file_name})

    async def remove_all_files(self, id_or_name: str) -> Environment:
        """
        Remove all files from an environment.
        """
        return await self.update(id_or_name, {"supporting_data_files": None})

    async def add_tags(self, id_or_name: str, tags: List[str]) -> Environment:
        """
        Add tags to an environment.

        Args:
            id_or_name: Environment ID or name
            tags: List of tag names or IDs

        Returns:
            Updated environment instance
        """
        # Get the environment
        environment = await self.get_one(id_or_name)

        # Process tags
        tag_ids = []
        current_tags = environment.tags or []

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

        # Update the environment
        return await self.update(str(environment.id), {"tags": tag_ids})

    def _process_references(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process name-based references to ID-based references.

        Args:
            data: Environment data with potential name-based references

        Returns:
            Processed data with ID-based references
        """
        result = data.copy()
        tenant_id = self.client.get_tenant_id()

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
