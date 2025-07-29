"""
CTRF (Common Test Report Format) reporter for TestZeus SDK.

This module provides functionality to generate CTRF reports from TestZeus test runs.
"""

import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from testzeus_sdk.client import TestZeusClient
from testzeus_sdk.managers.test_run_manager import TestRunManager
from testzeus_sdk.utils.helpers import get_project_info
from testzeus_sdk.utils.gerkin_parser import GherkinParser


class CTRFReporter:
    """
    Generate CTRF (Common Test Report Format) reports from TestZeus test runs.
    
    This class can convert TestZeus test run data into standardized CTRF format
    for compatibility with various test reporting tools.
    """
    
    # CTRF specification version
    SPEC_VERSION = "1.0.0"
    
    # Status mapping from TestZeus to CTRF
    STATUS_MAPPING = {
        "pass": "pass",
        "fail": "fail",
        "error": "error",
        "skip": "skip",
        "executing": "pending",
        "unknown": "unknown"
    }
    
    
    def __init__(self, client: TestZeusClient):
        """
        Initialize the CTRF reporter.
        
        Args:
            client: TestZeus client instance
        """
        self.client = client
        self.tool_name, self.tool_version = get_project_info()
        self.test_run_manager = TestRunManager(client)
        self.gherkin_parser = GherkinParser()
    
    async def generate_report(
        self, 
        test_run_id_or_name: str, 
        include_attachments: bool = True,
        include_environment: bool = True
    ) -> Dict[str, Any]:
        """
        Generate a CTRF report from a TestZeus test run.
        
        Args:
            test_run_id_or_name: Test run ID or name
            include_attachments: Whether to include attachments in the report
            include_environment: Whether to include environment information
            
        Returns:
            CTRF report dictionary
        """
        # Get expanded test run data
        expanded_data = await self.test_run_manager.get_expanded(test_run_id_or_name)
        
        # Extract components
        test_run = expanded_data["test_run"]
        test_run_dashs = expanded_data["test_run_dashs"]
        test_run_dash_outputs = expanded_data["test_run_dash_outputs"]
        test_run_dash_output_steps = expanded_data["test_run_dash_output_steps"]
        test_run_dash_outputs_attachments = expanded_data["test_run_dash_outputs_attachments"]
        
        # Generate tests from test_run_dashs (each dash becomes a single test)
        tests = []
        for test_run_dash in test_run_dashs:
            test_item = await self._generate_test_from_dash(
                test_run_dash,
                test_run_dash_outputs,
                test_run_dash_output_steps,
                test_run_dash_outputs_attachments if include_attachments else [],
                test_run
            )
            tests.append(test_item)
        
        # Generate CTRF report
        ctrf_report = {
            "reportFormat": "CTRF",
            "specVersion": self.SPEC_VERSION,
            "results": {
                "tool": self._generate_tool_info(),
                "summary": self._generate_summary(tests),
                "tests": tests
            }
        }
        
        # Add environment information if requested
        if include_environment:
            environment_info = await self._generate_environment_info(test_run)
            if environment_info:
                ctrf_report["results"]["environment"] = environment_info
        
        return ctrf_report
    
    async def generate_report_from_multiple_runs(
        self, 
        test_run_ids_or_names: List[str],
        include_attachments: bool = True,
        include_environment: bool = True
    ) -> Dict[str, Any]:
        """
        Generate a CTRF report from multiple TestZeus test runs.
        
        Args:
            test_run_ids_or_names: List of test run IDs or names
            include_attachments: Whether to include attachments in the report
            include_environment: Whether to include environment information
            
        Returns:
            Combined CTRF report dictionary
        """
        all_tests = []
        environment_info = None
        earliest_start = None
        latest_stop = None
        
        for test_run_id_or_name in test_run_ids_or_names:
            # Get expanded test run data
            expanded_data = await self.test_run_manager.get_expanded(test_run_id_or_name)
            
            # Extract components
            test_run = expanded_data["test_run"]
            test_run_dashs = expanded_data["test_run_dashs"]
            test_run_dash_outputs = expanded_data["test_run_dash_outputs"]
            test_run_dash_output_steps = expanded_data["test_run_dash_output_steps"]
            test_run_dash_outputs_attachments = expanded_data["test_run_dash_outputs_attachments"]
            
            # Generate tests from test_run_dashs
            for test_run_dash in test_run_dashs:
                test_item = await self._generate_test_from_dash(
                    test_run_dash,
                    test_run_dash_outputs,
                    test_run_dash_output_steps,
                    test_run_dash_outputs_attachments if include_attachments else [],
                    test_run
                )
                all_tests.append(test_item)
            
            # Get environment info from first test run
            if include_environment and environment_info is None:
                environment_info = await self._generate_environment_info(test_run)
            
            # Track timing from test run
            if test_run.get("start_time"):
                start_time = self._parse_timestamp(test_run["start_time"])
                if earliest_start is None or start_time < earliest_start:
                    earliest_start = start_time
            
            if test_run.get("end_time"):
                end_time = self._parse_timestamp(test_run["end_time"])
                if latest_stop is None or end_time > latest_stop:
                    latest_stop = end_time
        
        # Generate combined summary
        summary = self._generate_summary(all_tests)
        if earliest_start:
            summary["start"] = int(earliest_start.timestamp())
        if latest_stop:
            summary["stop"] = int(latest_stop.timestamp())
        
        # Generate combined CTRF report
        ctrf_report = {
            "reportFormat": "CTRF",
            "specVersion": self.SPEC_VERSION,
            "results": {
                "tool": self._generate_tool_info(),
                "summary": summary,
                "tests": all_tests
            }
        }
        
        # Add environment information if available
        if environment_info:
            ctrf_report["results"]["environment"] = environment_info
        
        return ctrf_report
    
    def _generate_tool_info(self) -> Dict[str, Any]:
        """Generate tool information for CTRF report."""
        return {
            "name": self.tool_name,
            "version": self.tool_version,
            "type": "test-automation",
        }
    
    def _generate_summary(self, tests: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary statistics for CTRF report."""
        total_tests = len(tests)
        passed = 0
        failed = 0
        pending = 0
        skipped = 0
        other = 0
        
        for test in tests:
            status = test.get("status", "unknown")
            
            if status == "pass":
                passed += 1
            elif status == "fail":
                failed += 1
            elif status == "error":
                failed += 1
            elif status == "skip":
                skipped += 1
            elif status == "pending":
                pending += 1
            else:
                other += 1
        
        return {
            "tests": total_tests,
            "passed": passed,
            "failed": failed,
            "pending": pending,
            "skipped": skipped,
            "other": other
        }
    
    async def _generate_test_from_dash(
        self, 
        test_run_dash: Dict[str, Any],
        test_run_dash_outputs: List[Dict[str, Any]],
        test_run_dash_output_steps: List[Dict[str, Any]], 
        attachments: List[Dict[str, Any]],
        test_run: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate a single CTRF test item from a TestZeus test run dash."""
        
        # Parse Gherkin feature content from dash_feature
        feature_content = test_run_dash.get("dash_feature", "")
        
        # Parse using the new GherkinParser
        parsed_feature = None
        all_steps = []
        
        if feature_content:
            try:
                parsed_feature = self.gherkin_parser.parse(feature_content)
                # Extract all steps from all scenarios
                for scenario in parsed_feature.scenarios:
                    all_steps.extend(scenario.steps)
            except Exception as e:
                # If parsing fails, create a fallback structure
                print(f"Warning: Failed to parse Gherkin content: {e}")
                all_steps = []
        
        # Get dash timing
        dash_start_time = test_run_dash.get("start_time")
        dash_end_time = test_run_dash.get("end_time")
        dash_duration = self._calculate_duration(dash_start_time, dash_end_time)
        
        # Map dash status to CTRF status
        dash_status = self._map_status(test_run_dash.get("test_status", "unknown"))
        
        # Filter outputs and steps related to this dash
        related_outputs = [
            output for output in test_run_dash_outputs 
            if output.get("test_run_dash") == test_run_dash.get("id")
        ]
        
        related_steps = []
        for output in related_outputs:
            output_steps = [
                step for step in test_run_dash_output_steps
                if step.get("test_run_dash_output") == output.get("id")
            ]
            related_steps.extend(output_steps)
        
        # Filter attachments related to this dash
        related_attachments = [
            attachment for attachment in attachments
            if attachment.get("test_run_dash") == test_run_dash.get("id")
        ]
        
        # Create the main test item
        test_item = {
            "name": test_run_dash.get("name", "Unknown Test"),
            "status": dash_status,
            "duration": dash_duration
        }
        
        # Add timing information
        if dash_start_time:
            test_item["start"] = int(self._parse_timestamp(dash_start_time).timestamp())
        if dash_end_time:
            test_item["stop"] = int(self._parse_timestamp(dash_end_time).timestamp())
        
        # Add threadId from workflow_run_id
        if test_run_dash.get("workflow_run_id"):
            test_item["threadId"] = test_run_dash["workflow_run_id"]
        
        # Add parameters with test_data
        test_data_id = test_run.get("test_data")
        if test_data_id:
            parameters = {}
            data_content = await self.client.test_data.get_one(test_data_id[0])
            parameters["test_data"] = data_content.data_content
            test_item["parameters"] = parameters
            
        # Add attachments if available
        if related_attachments:
            test_item["attachments"] = self._format_attachments(related_attachments)
        
        # Generate steps array from parsed Gherkin steps
        steps = []
        
        if all_steps:
            for i, gherkin_step in enumerate(all_steps):
                # Determine step status based on overall dash status and execution steps
                step_status = self._determine_step_status(dash_status, i, len(all_steps), related_steps)
                
                # Format step name with keyword and text
                step_name = f"{gherkin_step.type.value} {gherkin_step.text}"
                
                step_item = {
                    "name": step_name,
                    "status": step_status
                }
                
                steps.append(step_item)
        
        # Add steps array to test item
        test_item["steps"] = steps
        
        # Add extra object with all IDs
        extra = {
            "tenantid": test_run.get("tenant"),
            "test_run_id": test_run.get("id"),
            "test_run_dash_id": test_run_dash.get("id"),
            "agent_config_id": test_run.get("config"),
        }
        
        if test_run.get("test_data"):
            extra["test_data_id"] = test_run.get("test_data")
        
        # Add feature name and scenario name if available
        if parsed_feature:
            extra["feature_name"] = parsed_feature.name
            
            # Add scenario names (combine multiple scenarios if present)
            if parsed_feature.scenarios:
                scenario_names = [scenario.name for scenario in parsed_feature.scenarios]
                if len(scenario_names) == 1:
                    extra["scenario_name"] = scenario_names[0]
                else:
                    extra["scenario_names"] = scenario_names
        
        # Remove None values from extra
        test_item["extra"] = {k: v for k, v in extra.items() if v is not None}
        
        return test_item
    
    def _determine_step_status(self, dash_status: str, step_index: int, total_steps: int, execution_steps: List[Dict[str, Any]]) -> str:
        """Determine the status of a Gherkin step based on dash status and execution steps."""
        
        # If dash failed, determine which steps likely failed
        if dash_status == "fail":
            # Check execution steps for failure information
            failed_steps = [step for step in execution_steps if step.get("is_passed") is False]
            
            if failed_steps:
                # If we have specific failure information, fail the last steps
                if step_index >= total_steps - len(failed_steps):
                    return "fail"
                else:
                    return "pass"
            else:
                # If no specific failure info, fail the last step
                if step_index == total_steps - 1:
                    return "fail"
                else:
                    return "pass"
        
        # If dash passed, all steps passed
        elif dash_status == "pass":
            return "pass"
        
        # For other statuses, return the same status
        else:
            return dash_status
    
    def _map_status(self, status: str) -> str:
        """Map TestZeus status to CTRF status."""
        return self.STATUS_MAPPING.get(status, "unknown")
    
    def _calculate_duration(self, start_time: str, end_time: str) -> float:
        """Calculate duration in milliseconds."""
        if start_time and end_time:
            try:
                start = self._parse_timestamp(start_time)
                end = self._parse_timestamp(end_time)
                return (end - start).total_seconds() * 1000  # Convert to milliseconds
            except:
                pass
        
        return 0.0
    
    def _format_attachments(self, attachments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format attachments for CTRF report."""
        formatted_attachments = []
        
        for attachment in attachments:
            attachment_item = {
                "name": attachment.get("name", "unknown")
            }
            
            # Add content type if available
            if attachment.get("file_type"):
                attachment_item["contentType"] = attachment["file_type"]
            
            # Note: We don't include the actual data here as it might be large
            # The data can be retrieved separately using the attachment ID
            attachment_item["path"] = attachment.get('file', 'unknown')
            
            formatted_attachments.append(attachment_item)
        
        return formatted_attachments
    
    async def _generate_environment_info(self, test_run: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate environment information for CTRF report."""
        environment_id = test_run.get("environment")
        if not environment_id:
            return None
        
        try:
            environment = await self.client.environment.get_one(environment_id)
            return {
                "appName": environment.name,
                "extra": {
                    "environment_id": environment_id,
                    "environment_status": environment.status,
                    "environment_metadata": environment.metadata
                }
            }
        except:
            return None
    
    def _parse_timestamp(self, timestamp: Union[str, int, float]) -> datetime:
        """Parse timestamp string to datetime object."""
        if isinstance(timestamp, str):
            try:
                # Try ISO format first
                return datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            except:
                try:
                    # Try common formats
                    return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                except:
                    return datetime.now()
        elif isinstance(timestamp, (int, float)):
            return datetime.fromtimestamp(timestamp)
        else:
            return datetime.now()
    
    async def save_report(self, report: Dict[str, Any], filename: str) -> str:
        """
        Save CTRF report to a JSON file.
        
        Args:
            report: CTRF report dictionary
            filename: Output filename
            
        Returns:
            Path to the saved file
        """
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        return filename
    
    async def generate_and_save_report(
        self, 
        test_run_id_or_name: str, 
        filename: str,
        include_attachments: bool = True,
        include_environment: bool = True
    ) -> str:
        """
        Generate and save a CTRF report from a TestZeus test run.
        
        Args:
            test_run_id_or_name: Test run ID or name
            filename: Output filename
            include_attachments: Whether to include attachments in the report
            include_environment: Whether to include environment information
            
        Returns:
            Path to the saved file
        """
        report = await self.generate_report(test_run_id_or_name, include_attachments, include_environment)
        return await self.save_report(report, filename)
    
    async def generate_and_save_report_from_multiple_runs(
        self, 
        test_run_ids_or_names: List[str], 
        filename: str,
        include_attachments: bool = True,
        include_environment: bool = True
    ) -> str:
        """
        Generate and save a CTRF report from multiple TestZeus test runs.
        
        Args:
            test_run_ids_or_names: List of test run IDs or names
            filename: Output filename
            include_attachments: Whether to include attachments in the report
            include_environment: Whether to include environment information
            
        Returns:
            Path to the saved file
        """
        report = await self.generate_report_from_multiple_runs(test_run_ids_or_names, include_attachments, include_environment)
        return await self.save_report(report, filename)
    
    async def get_test_data(self, test_data_id: str) -> Dict[str, Any]:
        """Get test data for a test run."""
        test_data = await self.client.test_data.get_one(test_data_id)
        return test_data.get("data")