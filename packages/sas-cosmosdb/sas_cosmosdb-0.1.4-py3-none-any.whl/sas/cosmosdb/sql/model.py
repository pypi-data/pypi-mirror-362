import hashlib
import json
import threading
from abc import ABC
from typing import Any, Dict, Generic, TypeVar

from pydantic import computed_field

from ..base.model_base import EntityBase

"""
Cosmos DB SQL API entity models.

Defines abstract base classes for SQL API entities, including partition key logic and thread-safe caching.
"""

TEntity = TypeVar("TEntity", bound=EntityBase)
TKey = TypeVar("TKey")


class EntityBase(EntityBase, ABC):
    """
    Abstract base model for entities in CosmosDB SQL API.
    Inherit from this class to define models with type-safe entity and key support.

    Features provided by Pydantic BaseModel:
    - Automatic validation and serialization
    - JSON schema generation
    - Field validation and transformation
    - Computed fields and custom validators
    """

    # No additional fields or methods needed here, just for type safety
    pass


class RootEntityBase(EntityBase, ABC, Generic[TEntity, TKey]):
    """
    Abstract base model for root entities, providing required 'id' and computed 'partition_key' properties.
    Implements thread-safe, lazy partition key computation and conversion to CosmosDB storage dict.

    Features provided by Pydantic BaseModel:
    - Automatic validation and serialization
    - JSON schema generation
    - Field validation and transformation
    - Computed fields and custom validators
    """

    id: TKey

    # Alternative approach using PrivateAttr (automatically excluded from serialization)
    # _partition_key_value: Optional[str] = PrivateAttr(default=None)
    # _partition_key_lock: threading.Lock = PrivateAttr(default_factory=threading.Lock)

    def __init__(self, **data):
        super().__init__(**data)
        # Current approach: Use object.__setattr__ to avoid Pydantic field detection
        # These won't be included in model_dump() by default
        object.__setattr__(self, "_partition_key_value", None)
        object.__setattr__(self, "_partition_key_lock", threading.Lock())

    @computed_field
    @property
    def _partitionKey(self) -> str:
        """
        Computed read-only partition key based on entity ID.
        Uses lazy evaluation with thread-safe caching for optimal performance.

        Thread safety: This implementation is thread-safe using double-checked locking pattern.
        The first access will compute and cache the value, subsequent accesses return the cached value.

        Override get_partition_key_from_id() in subclasses for custom partition key logic.
        """
        # Fast path: if already computed, return cached value (thread-safe read)
        if self._partition_key_value is not None:
            return self._partition_key_value

        # Thread-safe computation with double-checked locking
        with self._partition_key_lock:
            # Double-check pattern: another thread might have computed it while we were waiting
            if self._partition_key_value is not None:
                return self._partition_key_value

            # Compute and cache the partition key
            self._partition_key_value = self.get_partition_key_from_id(self.id)
            return self._partition_key_value

    def to_cosmos_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary suitable for CosmosDB storage.

        Returns:
            dict: Dictionary with all model fields and computed partition key.
        """
        # Use model_dump with alias=True to get JSON field names
        # Explicitly exclude private attributes that shouldn't be serialized
        data = self.model_dump(
            by_alias=True,
            mode="json",
            exclude_none=False,
            exclude={"_partition_key_value", "_partition_key_lock"},
        )

        # Ensure required CosmosDB fields
        if self._partitionKey:
            data["_partitionKey"] = self._partitionKey

        return data

    @staticmethod
    def get_partition_key_from_id(id: TKey, number_of_partitions: int = 1000) -> str:
        """
        Create Partition Key from Entity ID.
        Uses SHA256 hash of the id, mapped to a partition number by modulo.

        Args:
            id: The entity's unique identifier.
            number_of_partitions: Logical partition count (default 1000).
        Returns:
            str: Partition key as a zero-padded string.
        """
        # Create SHA256 hash from id (more secure than SHA1)
        hash_bytes = hashlib.sha256(str(id).encode("utf-8")).digest()

        # Convert first 4 bytes to uint32
        int_hashed_val = int.from_bytes(
            hash_bytes[:4], byteorder="little", signed=False
        )

        # Calculate partition key
        range_val = number_of_partitions - 1
        length = len(str(range_val))

        key = str(int_hashed_val % number_of_partitions)
        return key.zfill(length)
