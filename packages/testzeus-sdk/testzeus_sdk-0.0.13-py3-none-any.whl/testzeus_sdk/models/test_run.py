"""
TestRun model class for TestZeus test run entities.
"""

from typing import Any, Dict, Optional

from testzeus_sdk.models.base import BaseModel


class TestRun(BaseModel):
    """
    Model class for TestZeus test run entities.

    This class represents a test run entity in TestZeus, which contains
    information about a test execution instance.
    """

    def __init__(self, data: Dict[str, Any]):
        """
        Initialize a TestRun model with data from the API.

        Args:
            data: Dictionary containing test run data
        """
        super().__init__(data)

        self.name = data.get("name")
        self.status = data.get("status")
        self.tenant = data.get("tenant")
        self.modified_by = data.get("modified_by")
        self.test = data.get("test")
        self.start_time = self._parse_date(data.get("start_time"))
        self.end_time = self._parse_date(data.get("end_time"))
        self.config = data.get("config")
        self.test_params = data.get("test_params")
        self.test_data = data.get("test_data")
        self.test_feature = data.get("test_feature")
        self.test_status = data.get("test_status")
        self.tags = data.get("tags")
        self.environment = data.get("environment")
        self.metadata = data.get("metadata")
        self.execution_mode = data.get("execution_mode")

    def is_running(self) -> bool:
        """
        Check if the test run is currently running.

        Returns:
            True if test run is in running status
        """
        return self.status == "running"

    def is_completed(self) -> bool:
        """
        Check if the test run has completed.

        Returns:
            True if test run is in completed status
        """
        return self.status == "completed"

    def is_failed(self) -> bool:
        """
        Check if the test run has failed.

        Returns:
            True if test run is in failed status
        """
        return self.status == "failed"

    def is_crashed(self) -> bool:
        """
        Check if the test run has crashed.

        Returns:
            True if test run is in crashed status
        """
        return self.status == "crashed"

    def is_cancelled(self) -> bool:
        """
        Check if the test run was cancelled.

        Returns:
            True if test run is in cancelled status
        """
        return self.status == "cancelled"

    def is_pending(self) -> bool:
        """
        Check if the test run is pending.

        Returns:
            True if test run is in pending status
        """
        return self.status == "pending"

    def get_duration(self) -> Optional[float]:
        """
        Calculate the duration of the test run in seconds.

        Returns:
            Duration in seconds or None if not possible to calculate
        """
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None
