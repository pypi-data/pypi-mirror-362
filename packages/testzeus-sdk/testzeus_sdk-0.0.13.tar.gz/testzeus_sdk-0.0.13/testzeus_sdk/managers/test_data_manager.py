"""
TestData manager class for TestZeus test data operations.
"""

from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

from pocketbase.client import FileUpload

from testzeus_sdk.client import TestZeusClient
from testzeus_sdk.managers.base import BaseManager
from testzeus_sdk.models.test_data import TestData
from testzeus_sdk.utils.helpers import get_id_by_name


class TestDataManager(BaseManager[TestData]):
    """
    Manager class for TestZeus test data entities.

    This class provides CRUD operations and specialized methods
    for working with test data entities.
    """

    def __init__(self, client: TestZeusClient) -> None:
        """
        Initialize a TestDataManager.

        Args:
            client: TestZeus client instance
        """
        super().__init__(client, "test_data", TestData)

    def create(self, data: Dict[str, Any]) -> TestData:
        """
        Create a new test data entity.

        Args:
            data: Test data with potentially name-based references

        Returns:
            Created test data instance
        """
        # Set default status if not provided
        if "status" not in data:
            data["status"] = "draft"

        # Set default type if not provided
        if "type" not in data:
            data["type"] = "test"

        return super().create(data)

    async def create_test_data(
        self,
        name: str,
        status: Literal["draft", "ready", "deleted"] = "draft",
        type: Literal["test", "design", "run"] = "test",
        content: str = None,
        supporting_data_files: str = None,
        tags: List[str] = None,
    ) -> TestData:
        """
        Create a new test data entity.

        Args:
            name: Name of the test data
            status: Status of the test data
            type: Type of the test data
            data: Data of the test data
            supporting_data_files: Supporting data files of the test data
            tags: Tags of the test data

        Returns:
            Created test data instance
        """
        data = {
            "name": name,
            "status": status,
            "type": type,
            "metadata": {},
        }
        if content:
            data["data"] = content
        if supporting_data_files:
            filename = supporting_data_files
            data["supporting_data_files"] = FileUpload(filename, open(filename, "rb"))
        if tags:
            data["tags"] = tags

        return await self.create(data)

    async def update_test_data(
        self,
        id_or_name: str,
        name: str = None,
        status: Literal["draft", "ready", "deleted"] = None,
        type: Literal["test", "design", "run"] = None,
        content: str = None,
        supporting_data_files: str = None,
        tags: List[str] = None,
        cached_prompt_details: str = None,
    ) -> TestData:
        """
        Update a test data entity.
        """
        data = {}
        if name:
            data["name"] = name
        if status:
            data["status"] = status
        if type:
            data["type"] = type
        if content:
            data["data"] = content
        if supporting_data_files:
            filename = supporting_data_files
            data["supporting_data_files+"] = FileUpload(filename, open(filename, "rb"))
        if tags:
            data["tags"] = tags
        if cached_prompt_details:
            data["cached_prompt_details"] = cached_prompt_details

        return await self.update(id_or_name, data)

    async def add_file(self, id_or_name: str, file_name: str) -> TestData:
        """
        Add a file to a test data entity.
        """
        file = FileUpload(file_name, open(file_name, "rb"))
        return await self.update(id_or_name, {"supporting_data_files+": file})

    async def remove_file(self, id_or_name: str, file_name: str) -> TestData:
        """
        Remove a file from a test data entity.
        """
        test_data = await self.get_one(id_or_name)
        if test_data.supporting_data_files:
            for file in test_data.supporting_data_files:
                if file_name.split("/")[-1].split(".")[0] in file:
                    file_name = file
                    break
        return await self.update(id_or_name, {"supporting_data_files-": file_name})

    async def remove_all_files(self, id_or_name: str) -> TestData:
        """
        Remove all files from a test data entity.
        """
        return await self.update(id_or_name, {"supporting_data_files": None})

    async def download_all_files(self, id_or_name: str, output_dir: str = "downloads") -> List[Path]:
        """
        Download all supporting files from a test data collection.

        Args:
            id_or_name (str): The ID or name of the test data collection
            output_dir (str, optional): Directory to save the downloaded files. Defaults to "downloads".

        Returns:
            List[str]: List of paths to the downloaded files
        """
        from pathlib import Path

        import httpx

        # Create output directory if it doesn't exist
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        downloaded_files = []
        test_data = await self.get_one(id_or_name)

        if not test_data.supporting_data_files:
            return downloaded_files

        file_token = self.client.get_file_token()

        async with httpx.AsyncClient() as client:
            for filename in test_data.supporting_data_files:
                if not filename:
                    continue

                file_path = output_path / filename
                url = f"{self.client.base_url}/api/files/{self.collection_name}/{test_data.id}/{filename}?token={file_token}"

                async with client.stream("GET", url, follow_redirects=True) as response:
                    response.raise_for_status()

                    with open(file_path, "wb") as f:
                        async for chunk in response.aiter_bytes():
                            f.write(chunk)

                downloaded_files.append(file_path)

        return downloaded_files

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
