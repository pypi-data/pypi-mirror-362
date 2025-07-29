"""
Model for test_device collection.
"""

import datetime
from typing import Any, Dict, List, Optional

from .base import BaseModel


class TestDevice(BaseModel):
    """
    TestDevice model for test_device collection
    """

    def __init__(self, data: Dict[str, Any]):
        """
        Initialize a TestDevice instance

        Args:
            data: Dictionary containing model data
        """
        super().__init__(data)
        self.metadata = data.get("metadata")
        self.name = data.get("name")
        self.status = data.get("status")
        self.tenant = data.get("tenant")
        self.modified_by = data.get("modified_by")
        self.supporting_data_files = data.get("supporting_data_files")
        self.operating_system = data.get("operating_system")
        self.browser_type = data.get("browser_type")
        self.browser_channel = data.get("browser_channel")
        self.browser_version = data.get("browser_version")
        self.browser_path = data.get("browser_path")
        self.browser_viewport = data.get("browser_viewport")
        self.browser_locale = data.get("browser_locale")
        self.browser_timezone = data.get("browser_timezone")
        self.browser_geolocation = data.get("browser_geolocation")
        self.headless = data.get("headless")
        self.record_video = data.get("record_video")
        self.take_screenshots = data.get("take_screenshots")
        self.capture_network = data.get("capture_network")
        self.enable_playwright_tracing = data.get("enable_playwright_tracing")
        self.enable_browser_logs = data.get("enable_browser_logs")
        self.deleted = data.get("deleted")
        self.device_information = data.get("device_information")
        self.tags = data.get("tags")
