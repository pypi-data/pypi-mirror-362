from abc import ABC
from typing import Any, Dict, Generic, TypeVar

from ..base.model_base import EntityBase

"""
Cosmos DB MongoDB API entity models.

Defines abstract base classes for MongoDB API entities, including conversion to CosmosDB storage dict.
"""

TKey = TypeVar("TKey")
TEntity = TypeVar("TEntity", bound=EntityBase)


class EntityBase(EntityBase, ABC):
    """
    Abstract base model for entities in CosmosDB MongoDB API.

    EntityBase is a specialized subclass of Pydantic's BaseModel designed specifically
    for Azure Cosmos DB entities using the MongoDB API. It leverages all of Pydantic's
    powerful features while providing MongoDB-specific functionality.

    Purpose:
    - Serves as the foundation for all CosmosDB MongoDB entity models
    - Provides automatic data validation and serialization through Pydantic
    - Enables type-safe entity definitions with full IDE support
    - Used for nested/embedded entities that don't require independent storage

    Key Features from Pydantic BaseModel:
    - Automatic validation and serialization/deserialization
    - JSON schema generation for API documentation
    - Field validation with custom validators and constraints
    - Computed fields and property-based fields
    - Type conversion and coercion
    - Alias support for field name mapping

    Use Case:
    - Inherit from this class for nested entities (e.g., Address, ContactInfo)
    - Entities that are always embedded within other entities
    - Entities that don't need independent querying or storage
    """

    # No additional fields or methods needed here, just for type safety
    pass


class RootEntityBase(EntityBase, ABC, Generic[TEntity, TKey]):
    """
    Abstract base model for root entities in CosmosDB MongoDB API.

    RootEntityBase extends EntityBase with CosmosDB MongoDB-specific features required for
    entities that are stored independently in CosmosDB collections. It provides
    essential functionality for data conversion and integration with the CosmosDB MongoDB API.

    Purpose:
    - Serves as the base class for all independently stored entities
    - Handles entity-to-dictionary and dictionary-to-entity conversion
    - Enables seamless integration with CosmosDB MongoDB API operations
    - Supports type-safe repository patterns with generic type parameters
    - Provides MongoDB-specific document storage optimization

    Key Features:
    - Seamless conversion between entity objects and MongoDB document format
    - Type-safe generic parameters for entity type and key type
    - Integration with repository pattern for CRUD operations
    - Optimized for MongoDB document storage and querying
    - Support for MongoDB-specific operations and indexing

    CosmosDB MongoDB-Specific Features:
    - to_cosmos_dict(): Converts entity to MongoDB document format
    - Optimized for MongoDB collection storage
    - Compatible with MongoDB query operations and indexing
    - Support for MongoDB-specific data types and operations

    Inherited Pydantic Features:
    - All EntityBase features (validation, serialization, etc.)
    - JSON schema generation for API documentation
    - Field validation with custom validators and constraints
    - Computed fields and property-based fields

    Type Parameters:
    - TEntity: The entity class type (used for type safety and IDE support)
    - TKey: The type of the entity's primary key (str, int, UUID, etc.)

    Use Case:
    - Inherit from this class for root entities (e.g., Customer, Order, Product)
    - Entities that are stored independently in CosmosDB collections
    - Entities that can be queried and accessed directly
    - Entities that serve as aggregate roots in domain-driven design
    """

    id: TKey

    def to_cosmos_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary suitable for CosmosDB storage.

        Returns:
            dict: Dictionary with all model fields using JSON field names.
        """
        # Use model_dump with alias=True to get JSON field names
        return self.model_dump(by_alias=True, exclude_none=False, mode="json")
