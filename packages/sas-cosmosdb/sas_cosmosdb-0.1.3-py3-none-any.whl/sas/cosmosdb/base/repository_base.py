import enum
from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, TypeVar

from .model_base import EntityBase

"""
Base repository abstraction for Cosmos DB.

Defines generic repository interfaces and sort helpers for both MongoDB and SQL APIs.
Provides type-safe CRUD operations and sorting utilities.

This module contains the foundational classes that enable consistent repository patterns
across different Cosmos DB APIs while maintaining type safety and flexibility.

Examples:
    Creating a custom repository:
    
    ```python
    from sas.cosmosdb.base import RepositoryBase, EntityBase, SortField, SortDirection
    
    class Product(EntityBase):
        name: str
        price: float
        category: str
    
    class ProductRepository(RepositoryBase[Product, str]):
        async def get_async(self, key: str) -> Optional[Product]:
            # Implementation specific to your chosen API (SQL or MongoDB)
            pass
            
        async def find_async(self, predicate: Dict[str, Any]) -> List[Product]:
            # Implementation specific to your chosen API
            pass
    ```
    
    Using sort fields:
    
    ```python
    # Single field sorting
    sort_by_price = SortField("price", SortDirection.ASCENDING)
    
    # Multiple field sorting
    sort_fields = [
        SortField("category", SortDirection.ASCENDING),
        SortField("price", SortDirection.DESCENDING),
        SortField("name", SortDirection.ASCENDING)
    ]
    
    products = await repo.find_async(
        {"category": "electronics"},
        sort_fields=sort_fields
    )
    ```
"""

# Type variables with constraints for better type safety
TEntity = TypeVar("TEntity", bound=EntityBase)  # Must inherit from EntityBase
TKey = TypeVar("TKey")  # Any type for the key


class SortDirection(enum.IntEnum):
    ASCENDING = 1
    DESCENDING = -1


class SortField:
    def __init__(self, field_name: str, order: SortDirection = SortDirection.ASCENDING):
        """
        Represents a field to sort by and its direction.

        Args:
            field_name: The name of the field to sort by.
            order: The sort direction (ascending or descending).

        Examples:
            Basic sorting:

            ```python
            # Sort by name in ascending order (default)
            name_sort = SortField("name")

            # Sort by price in descending order
            price_sort = SortField("price", SortDirection.DESCENDING)

            # Sort by date in ascending order (explicit)
            date_sort = SortField("createdDate", SortDirection.ASCENDING)
            ```

            Multiple field sorting:

            ```python
            # Sort by category first, then by price (high to low), then by name
            sort_fields = [
                SortField("category", SortDirection.ASCENDING),
                SortField("price", SortDirection.DESCENDING),
                SortField("name", SortDirection.ASCENDING)
            ]

            # Use in repository queries
            products = await repo.find_async(
                {"inStock": True},
                sort_fields=sort_fields
            )
            ```

            Nested field sorting:

            ```python
            # Sort by nested field
            address_sort = SortField("address.city", SortDirection.ASCENDING)

            # Sort by array element (MongoDB API)
            tag_sort = SortField("tags.priority", SortDirection.DESCENDING)
            ```
        """
        self.field_name = field_name
        self.order = order

    def __repr__(self):
        return f"{self.field_name} ({'ASCENDING' if self.order == SortDirection.ASCENDING else 'DESCENDING'})"


class RepositoryBase(ABC, Generic[TEntity, TKey]):
    @abstractmethod
    async def get_async(self, key: TKey) -> Optional[TEntity]:
        """
        Retrieve an entity by its key.

        Args:
            key: The entity's key value.
        Returns:
            The entity if found, else None.
        """
        raise NotImplementedError("This method must be implemented in a subclass.")

    @abstractmethod
    async def find_async(
        self,
        predicate: Dict[str, Any],
        sort_fields: List[SortField] = [],
    ) -> List[TEntity]:
        """
        Find entities matching a predicate.

        Args:
            predicate: Query conditions
            sort_fields: Fields to sort by (optional)
        Returns:
            List of matching entities.
        Raises:
            ValueError: If sort_order is provided but sort_fields is empty
        """
        raise NotImplementedError("This method must be implemented in a subclass.")

    @abstractmethod
    async def add_async(self, entity: TEntity) -> None:
        """
        Add a new entity.

        Args:
            entity: The entity to add.
        """
        raise NotImplementedError("This method must be implemented in a subclass.")

    @abstractmethod
    async def update_async(self, entity: TEntity) -> None:
        """
        Update an existing entity.

        Args:
            entity: The entity to update.
        """
        raise NotImplementedError("This method must be implemented in a subclass.")

    @abstractmethod
    async def delete_async(self, key: TKey) -> None:
        """
        Delete an entity by its key.

        Args:
            key: The entity's key value.
        """
        raise NotImplementedError("This method must be implemented in a subclass.")

    @abstractmethod
    async def delete_items_async(self, predicate: Dict[str, Any]) -> int:
        """
        Delete all entities matching the predicate.

        Args:
            predicate: Query conditions (same format as find_async).

        Returns:
            The number of entities deleted.

        Raises:
            ValueError: If the predicate is invalid.
            Exception: For any deletion errors.

        Notes:
            - Subclasses should implement batching for large deletes.
            - Partial failures should be logged and surfaced.
            - Returns 0 if no entities matched.
        """
        raise NotImplementedError("This method must be implemented in a subclass.")

    @abstractmethod
    async def all_async(
        self, sort_fields: Optional[List[SortField]] = None
    ) -> List[TEntity]:
        """Retrieve all entities.

        Args:
            sort_fields: Fields to sort by (optional)

        Raises:
            ValueError: If sort_fields is provided but sort_order is empty
        """
        raise NotImplementedError("This method must be implemented in a subclass.")

    @abstractmethod
    async def find_with_pagination_async(
        self,
        predicate: Dict[str, Any],
        sort_fields: List[SortField] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[TEntity]:
        """Find entities with pagination support."""
        raise NotImplementedError("This method must be implemented in a subclass.")

    @abstractmethod
    async def count_async(self, predicate: Dict[str, Any] = None) -> int:
        """Count entities matching a predicate."""
        raise NotImplementedError("This method must be implemented in a subclass.")

    @abstractmethod
    async def find_one_async(self, predicate: Dict[str, Any]) -> Optional[TEntity]:
        """Find a single entity matching a predicate."""
        raise NotImplementedError("This method must be implemented in a subclass.")

    @abstractmethod
    async def exists_async(self, predicate: Dict[str, Any]) -> bool:
        """Check if any entity exists matching a predicate."""
        raise NotImplementedError("This method must be implemented in a subclass.")

    # Helper methods for entity/document conversion
    def _entity_to_document(self, entity: TEntity) -> Dict[str, Any]:
        """Convert entity to Cosmos DB document."""
        document = entity.to_cosmos_dict()

        return document

    def _document_to_entity(self, document: Dict[str, Any]) -> TEntity:
        """Convert Cosmos DB document to entity."""
        # Create a new entity instance from the document
        return self.__orig_bases__[0].__args__[0](**document)

    async def _cursor_to_entities(self, cursor) -> List[TEntity]:
        """Convert Cosmos DB cursor to list of entities using async iteration."""
        entities = []
        async for document in cursor:
            entities.append(self._document_to_entity(document))
        return entities
