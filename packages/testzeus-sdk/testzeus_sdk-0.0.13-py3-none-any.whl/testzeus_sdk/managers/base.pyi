"""
Type stubs for the BaseManager class.
"""

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from testzeus_sdk.client import TestZeusClient
from testzeus_sdk.models.base import BaseModel

T = TypeVar("T", bound=BaseModel)

def record_to_dict(record: Any) -> Dict[str, Any]: ...

class BaseManager(Generic[T]):
    """
    Base manager class for all TestZeus entities.

    This class provides common CRUD operations for all entity types.
    """

    client: TestZeusClient
    collection_name: str
    model_class: Type[T]

    def __init__(self, client: TestZeusClient, collection_name: str, model_class: Type[T]) -> None: ...
    async def get_list(
        self,
        page: int = ...,
        per_page: int = ...,
        filters: Optional[Dict[str, Any]] = ...,
        sort: Optional[Union[str, List[str]]] = ...,
        expand: Optional[Union[str, List[str]]] = ...,
    ) -> Dict[str, Any]: ...
    async def get_one(self, id_or_name: str, expand: Optional[Union[str, List[str]]] = ...) -> T: ...
    async def create(self, data: Dict[str, Any]) -> T: ...
    async def update(self, id_or_name: str, data: Dict[str, Any]) -> T: ...
    async def delete(self, id_or_name: str) -> bool: ...
    def _process_references(self, data: Dict[str, Any]) -> Dict[str, Any]: ...
    async def _get_id_from_name_or_id(self, id_or_name: str) -> str: ...
    @staticmethod
    def _is_valid_id(id_str: str) -> bool: ...
    @staticmethod
    def _build_filter_string(filters: Dict[str, Any]) -> str: ...
