"""
Type stubs for the helper functions in the TestZeus SDK.
"""

from typing import Any, Dict, List, Optional, Union

from testzeus_sdk.client import TestZeusClient

def get_id_by_name(client: TestZeusClient, collection: str, name: str, tenant_id: Optional[str] = ...) -> Optional[str]: ...
def expand_test_run_tree(client: TestZeusClient, test_run_id: str) -> Dict[str, Any]: ...
def convert_name_refs_to_ids(client: TestZeusClient, data: Dict[str, Any], ref_fields: Dict[str, str]) -> Dict[str, Any]: ...
