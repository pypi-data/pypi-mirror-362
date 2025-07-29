"""
Base manager class for TestZeus entity operations.
"""

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from testzeus_sdk.client import TestZeusClient
from testzeus_sdk.models.base import BaseModel

T = TypeVar("T", bound=BaseModel)


def record_to_dict(record: Any) -> Dict[str, Any]:
    """
    Convert a PocketBase Record to a dictionary.
    Attempts multiple approaches to ensure compatibility with different PocketBase libraries.
    """
    if hasattr(record, "to_dict") and callable(record.to_dict):
        return record.to_dict()
    elif hasattr(record, "export") and callable(record.export):
        return record.export()
    elif hasattr(record, "__dict__"):
        return record.__dict__
    else:
        # As a last resort, try converting all attributes to a dict
        return {key: getattr(record, key) for key in dir(record) if not key.startswith("_") and not callable(getattr(record, key))}


class BaseManager(Generic[T]):
    """
    Base manager class for all TestZeus entities.

    This class provides common CRUD operations for all entity types.
    """

    def __init__(self, client: TestZeusClient, collection_name: str, model_class: Type[T]) -> None:
        """
        Initialize a manager for a specific entity type.

        Args:
            client: TestZeus client instance
            collection_name: Name of the PocketBase collection
            model_class: Model class for this entity type
        """
        self.client = client
        self.collection_name = collection_name
        self.model_class = model_class

    async def get_list(
        self,
        page: int = 1,
        per_page: int = 30,
        filters: Optional[Dict[str, Any]] = None,
        sort: Optional[Union[str, List[str]]] = None,
        expand: Optional[Union[str, List[str]]] = None,
    ) -> Dict[str, Any]:
        """
        Get a list of entities with optional filtering.

        Args:
            page: Page number (1-based)
            per_page: Number of items per page
            filters: Dictionary of filter conditions
            sort: Field(s) to sort by (prefix with '-' for descending order)
            expand: Related collection(s) to expand

        Returns:
            Dictionary containing items and pagination info
        """
        await self.client.ensure_authenticated()
        filter_str = self._build_filter_string(filters) if filters else None

        # Prepare the sort parameter
        sort_str = None
        if sort:
            if isinstance(sort, list):
                sort_str = ",".join(sort)
            else:
                sort_str = sort

        # Prepare the expand parameter
        expand_str = None
        if expand:
            if isinstance(expand, list):
                expand_str = ",".join(expand)
            else:
                expand_str = expand

        result = self.client.pb.collection(self.collection_name).get_list(
            page,
            per_page,
            query_params={"filter": filter_str, "sort": sort_str, "expand": expand_str},
        )

        # Convert items to model instances
        items = [self.model_class(record_to_dict(item)) for item in result.items]

        return {
            "items": items,
            "page": result.page,
            "per_page": result.per_page,
            "total_items": result.total_items,
            "total_pages": result.total_pages,
        }

    async def get_one(self, id_or_name: str, expand: Optional[Union[str, List[str]]] = None) -> T:
        """
        Get a single entity by ID or name.

        Args:
            id_or_name: Entity ID or name
            expand: Fields to expand in the response

        Returns:
            Entity model instance
        """
        await self.client.ensure_authenticated()

        expand_str = None
        if expand:
            if isinstance(expand, list):
                expand_str = ",".join(expand)
            else:
                expand_str = expand

        # Check if the provided string is an ID or name
        if self._is_valid_id(id_or_name):
            result = self.client.pb.collection(self.collection_name).get_one(id_or_name, query_params={"expand": expand_str})
        else:
            # Assume it's a name and try to find it
            tenant_id = self.client.get_tenant_id()
            if not tenant_id:
                raise ValueError("User must be authenticated with a tenant to find by name")

            filter_str = f'name = "{id_or_name}" && tenant = "{tenant_id}"'
            try:
                result = self.client.pb.collection(self.collection_name).get_first_list_item(filter_str)
            except Exception as e:
                raise ValueError(f"Could not find {self.collection_name} with name: {id_or_name}") from e

        return self.model_class(record_to_dict(result))

    async def get_first_item(self, filters: Optional[Dict[str, Any]] = None) -> T:
        """
        Get the first item from the collection based on optional filters.

        Args:
            filters: Dictionary of filter conditions

        Returns:
            First item from the collection
        """
        await self.client.ensure_authenticated()
        filter_str = self._build_filter_string(filters) if filters else None
        result = self.client.pb.collection(self.collection_name).get_first_list_item(filter_str)
        return self.model_class(record_to_dict(result))

    async def check_duplicate(self, data: Dict[str, Any]) -> Optional[T]:
        """
        Check if a record with the same name exists in the current tenant.

        Args:
            data: Entity data to check for duplicates

        Returns:
            Existing record if found, None otherwise
        """
        await self.client.ensure_authenticated()
        tenant_id = self.client.get_tenant_id()

        if not tenant_id:
            return None

        if "name" not in data:
            return None

        try:
            filter_str = f'name = "{data["name"]}" && tenant = "{tenant_id}"'
            result = self.client.pb.collection(self.collection_name).get_first_list_item(filter_str)
            return self.model_class(record_to_dict(result))
        except Exception:
            return None

    async def create(self, data: Dict[str, Any]) -> T:
        """
        Create a new entity.

        Args:
            data: Entity data

        Returns:
            Created entity model instance

        Raises:
            ValueError: If a record with the same name already exists or if creation fails
        """
        await self.client.ensure_authenticated()

        # Check for duplicate records
        existing_record = await self.check_duplicate(data)
        if existing_record:
            raise ValueError(f"A {self.collection_name} record with name '{data.get('name')}' already exists in this tenant. Choose a different name.")

        # Add tenant if not provided
        if "tenant" not in data:
            tenant_id = self.client.get_tenant_id()
            if tenant_id:
                data["tenant"] = tenant_id

        # Add modified_by if not provided
        if "modified_by" not in data and self.client.is_authenticated():
            data["modified_by"] = self.client.get_user_id()

        # Process name-based references
        processed_data = self._process_references(data)

        try:
            result = self.client.pb.collection(self.collection_name).create(processed_data)
            return self.model_class(record_to_dict(result))
        except Exception as e:
            # Provide more information about the error
            raise ValueError(f"Failed to create {self.collection_name}: {str(e)}") from e

    async def update(self, id_or_name: str, data: Dict[str, Any]) -> T:
        """
        Update an existing entity.

        Args:
            id_or_name: Entity ID or name
            data: Updated entity data

        Returns:
            Updated entity model instance
        """
        await self.client.ensure_authenticated()
        # Add tenant if not provided
        if "tenant" not in data:
            tenant_id = self.client.get_tenant_id()
            if tenant_id:
                data["tenant"] = tenant_id
            else:
                print(f"Warning: No tenant ID available when updating {self.collection_name}")

        # Add modified_by if not provided
        if "modified_by" not in data and self.client.is_authenticated():
            data["modified_by"] = self.client.get_user_id()

        # Process name-based references
        processed_data = self._process_references(data)

        # Get the ID if a name was provided
        try:
            entity_id = await self._get_id_from_name_or_id(id_or_name)
            result = self.client.pb.collection(self.collection_name).update(entity_id, processed_data)
            return self.model_class(record_to_dict(result))
        except Exception as e:
            # Provide more information about the error
            raise ValueError(f"Failed to update {self.collection_name} {id_or_name}: {str(e)}") from e

    async def delete(self, id_or_name: str) -> bool:
        """
        Delete an entity.

        Args:
            id_or_name: Entity ID or name

        Returns:
            True if deletion was successful
        """
        await self.client.ensure_authenticated()
        # Get the ID if a name was provided
        entity_id = await self._get_id_from_name_or_id(id_or_name)

        return self.client.pb.collection(self.collection_name).delete(entity_id)

    def _process_references(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process name-based references to ID-based references.

        This is a placeholder that should be overridden by subclasses
        to handle entity-specific reference fields.

        Args:
            data: Entity data with potential name-based references

        Returns:
            Processed data with ID-based references
        """
        # Base implementation does nothing
        return data.copy()

    async def _get_id_from_name_or_id(self, id_or_name: str) -> str:
        """
        Get entity ID from name or ID.

        Args:
            id_or_name: Entity ID or name

        Returns:
            Entity ID
        """
        if self._is_valid_id(id_or_name):
            return id_or_name

        # Try to find the entity by name
        try:
            entity = await self.get_one(id_or_name)
            if entity and hasattr(entity, "id"):
                return str(entity.id)
            raise ValueError(f"Entity found but has no ID: {id_or_name}")
        except Exception as e:
            raise ValueError(f"Could not find {self.collection_name} with name: {id_or_name}") from e

    @staticmethod
    def _is_valid_id(id_str: str) -> bool:
        """
        Check if a string is a valid ID.

        For PocketBase, IDs are typically 15 characters alphanumeric.

        Args:
            id_str: String to check

        Returns:
            True if string is a valid ID
        """
        return len(id_str) == 15 and id_str.isalnum()

    @staticmethod
    def _build_filter_string(filters: Dict[str, Any]) -> str:
        """
        Build a filter string from a dictionary of filters.
        
        Supports all PocketBase operators and logical conditions:
        - Simple format: {"field": "value"} -> field = "value"  
        - Complex format: {"field": {"operator": ">=", "value": 10}} -> field >= 10
        - List format: {"field": ["val1", "val2"]} -> (field = "val1" || field = "val2")
        - Array operators: {"field": {"operator": "?=", "value": ["val1", "val2"]}} -> (field ?= "val1" || field ?= "val2")
        - Logical grouping: {"$and": [...], "$or": [...]}

        Supports all PocketBase operators and logical conditions:
        - Simple format: {"field": "value"} -> field = "value"
        - Complex format: {"field": {"operator": ">=", "value": 10}} -> field >= 10
        - List format: {"field": ["val1", "val2"]} -> (field = "val1" || field = "val2")
        - Array operators: {"field": {"operator": "?=", "value": ["val1", "val2"]}} -> (field ?= "val1" || field ?= "val2")
        - Logical grouping: {"$and": [...], "$or": [...]}

        Args:
            filters: Dictionary of filter conditions

        Returns:
            Filter string for PocketBase API
        """

        def _format_value(value: Any) -> str:
            """Format a value for the filter string."""
            if isinstance(value, bool):
                return str(value).lower()
            elif isinstance(value, (int, float)):
                return str(value)
            elif value is None:
                return "null"
            else:
                # Escape quotes in string values
                escaped_value = str(value).replace('"', '\\"')
                return f'"{escaped_value}"'

        def _build_condition(field: str, value: Any) -> str:
            """Build a single filter condition."""
            if isinstance(value, dict) and "operator" in value:
                # Complex format: {"operator": ">=", "value": 10}
                operator = value["operator"]
                operand = value["value"]
                if operator in ["?=", "?!=", "?>", "?>=", "?<", "?<=", "?~", "?!~"] and isinstance(operand, list):
                    # Array operators with list values
                    sub_conditions = [f"{field} {operator} {_format_value(item)}" for item in operand]
                    return f"({' || '.join(sub_conditions)})"
                else:
                    return f"{field} {operator} {_format_value(operand)}"

            elif isinstance(value, list):
                # Simple list format: ["val1", "val2"] -> (field = "val1" || field = "val2")
                or_conditions = [f"{field} = {_format_value(item)}" for item in value]
                return f"({' || '.join(or_conditions)})"

            else:
                # Simple format: "value" -> field = "value"
                return f"{field} = {_format_value(value)}"

        def _process_filters(filter_dict: Dict[str, Any]) -> List[str]:
            """Process a filter dictionary and return list of conditions."""
            conditions = []
            for key, value in filter_dict.items():
                if key == "$and":
                    # AND grouping
                    if isinstance(value, list):
                        and_conditions = []
                        for sub_filter in value:
                            if isinstance(sub_filter, dict):
                                sub_conditions = _process_filters(sub_filter)
                                if sub_conditions:
                                    and_conditions.extend(sub_conditions)
                        if and_conditions:
                            if len(and_conditions) == 1:
                                conditions.append(and_conditions[0])
                            else:
                                conditions.append(f"({' && '.join(and_conditions)})")

                elif key == "$or":
                    # OR grouping
                    if isinstance(value, list):
                        or_conditions = []
                        for sub_filter in value:
                            if isinstance(sub_filter, dict):
                                sub_conditions = _process_filters(sub_filter)
                                if sub_conditions:
                                    or_conditions.extend(sub_conditions)
                        if or_conditions:
                            if len(or_conditions) == 1:
                                conditions.append(or_conditions[0])
                            else:
                                conditions.append(f"({' || '.join(or_conditions)})")

                else:
                    # Regular field condition
                    conditions.append(_build_condition(key, value))

            return conditions

        conditions = _process_filters(filters)
        return " && ".join(conditions)
