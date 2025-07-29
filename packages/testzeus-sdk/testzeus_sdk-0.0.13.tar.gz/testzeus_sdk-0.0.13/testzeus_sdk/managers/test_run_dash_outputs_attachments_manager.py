"""
Manager for test_run_dash_outputs_attachments collection.
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import httpx

from testzeus_sdk.client import TestZeusClient
from testzeus_sdk.models.test_run_dash_outputs_attachments import (
    TestRunDashOutputsAttachments,
)

from .base import BaseManager

logger = logging.getLogger(__name__)


class TestRunDashOutputsAttachmentsManager(BaseManager):
    """
    Manager for TestRunDashOutputsAttachments resources
    """

    def __init__(self, client: TestZeusClient) -> None:
        """
        Initialize the TestRunDashOutputsAttachments manager

        Args:
            client: TestZeus client instance
        """
        super().__init__(client, "test_run_dash_outputs_attachments", TestRunDashOutputsAttachments)

    def _process_references(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process name-based references to ID-based references

        Args:
            data: Entity data with potential name-based references

        Returns:
            Processed data with ID-based references
        """
        from testzeus_sdk.utils.helpers import convert_name_refs_to_ids

        # Define which fields are relations and what collections they reference
        ref_fields = {
            "tenant": "pbc_138639755",
            "modified_by": "_pb_users_auth_",
            "test_run_dash": "pbc_2189187333",
            "test_run_dash_output": "pbc_2691161507",
            "test_run_dash_output_steps": "pbc_1861708698",
            "tags": "pbc_1219621782",
        }

        return convert_name_refs_to_ids(self.client, data, ref_fields)

    async def download_attachment(self, id_or_name: str, output_dir: str = ".") -> Optional[str]:
        """
        Download an attachment file by its ID or name.

        Args:
            id_or_name: ID or name of the attachment
            output_dir: Directory where the file should be downloaded to (defaults to current directory)

        Returns:
            Path to the downloaded file as string if successful, None otherwise
        """
        await self.client.ensure_authenticated()

        try:
            # Get the attachment record first
            attachment = await self.get_one(id_or_name)
            if not attachment or not attachment.file:
                logger.error(f"No file found for attachment {id_or_name}")
                return None

            # Get the file name from the attachment
            file_name = attachment.file
            if isinstance(file_name, dict) and "file" in file_name:
                file_name = file_name["file"]
            elif isinstance(file_name, list) and len(file_name) > 0:
                file_name = file_name[0]

            # Create output path
            output_path = Path(output_dir) / file_name

            # Get the file download URL with authentication token
            file_token = self.client.get_file_token()
            url = f"{self.client.base_url}/api/files/{self.collection_name}/{attachment.id}/{file_name}?token={file_token}"

            # Download the file
            async with httpx.AsyncClient() as client:
                async with client.stream("GET", url, follow_redirects=True) as response:
                    response.raise_for_status()

                    # Ensure the output directory exists
                    output_path.parent.mkdir(parents=True, exist_ok=True)

                    # Write the file in chunks
                    with open(output_path, "wb") as f:
                        async for chunk in response.aiter_bytes():
                            f.write(chunk)

            logger.info(f"Downloaded file to {output_path}")
            return str(output_path)

        except Exception as e:
            logger.error(f"Failed to download attachment {id_or_name}: {str(e)}")
            return None
