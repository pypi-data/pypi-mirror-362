"""
MongoDB API implementation for SAS CosmosDB Library

This module provides MongoDB-specific implementations for Cosmos DB operations,
including repositories and models designed for the MongoDB API.
"""

from .model import RootEntityBase, EntityBase
from .repository import RepositoryBase

__all__ = ["RootEntityBase", "EntityBase", "RepositoryBase"]
