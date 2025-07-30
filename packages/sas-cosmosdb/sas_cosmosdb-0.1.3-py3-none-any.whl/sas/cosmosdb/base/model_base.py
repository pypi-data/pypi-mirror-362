"""
Base model for Cosmos DB entities.

Provides a Pydantic-based base class for entities, enforcing required 'id' and 'partition_key' properties.
Supports type-safe entity and key definitions for both MongoDB and SQL APIs.
"""

from pydantic import BaseModel, ConfigDict


class EntityBase(BaseModel):
    """
    Base model for entities, providing required 'id' and 'partition_key' properties.
    Inherit from this class to define models with type-safe entity and key support.

    Features provided by Pydantic BaseModel:
    - Automatic validation and serialization
    - JSON schema generation
    - Field validation and transformation
    - Computed fields and custom validators
    """

    # Pydantic v2 configuration using model_config
    model_config = ConfigDict(
        # Allow arbitrary types (useful for Azure SDK types)
        arbitrary_types_allowed=True,
        # Validate assignment (validate when setting attributes)
        validate_assignment=True,
        # Use enum values instead of names in serialization
        use_enum_values=True,
        # Exclude None values from serialization
        exclude_none=True,
        # Allow population by field name or alias
        populate_by_name=True,
        # Allow additional attributes not defined in the model (for backward compatibility)
        extra="allow",
    )
