"""
SAS Cosmos DB Helper Library

A comprehensive Python library for working with Azure Cosmos DB using both MongoDB and SQL APIs.
Built with enterprise-grade architecture and modern Python best practices.

This library provides:
- Type-safe entity models with Pydantic
- Repository pattern for clean architecture
- Support for both MongoDB and SQL APIs
- Async/await throughout
- Comprehensive error handling
- Generic inheritance and type constraints

Example usage:

    from sas.cosmosdb.sql import RootEntityBase, RepositoryBase

    class MyEntity(RootEntityBase['MyEntity', str]):
        name: str
        value: int

    class MyRepository(RepositoryBase[MyEntity, str]):
        # Implementation...
"""

__version__ = "0.1.3"

# Import base classes
from .base.model_base import EntityBase
from .base.repository_base import RepositoryBase, SortDirection, SortField

# Import MongoDB API classes
from .mongo.model import RootEntityBase as MongoRootEntityBase
from .mongo.repository import RepositoryBase as MongoRepositoryBase

# Import SQL API classes
from .sql.model import RootEntityBase as SQLRootEntityBase
from .sql.repository import RepositoryBase as SQLRepositoryBase

# Main exports for the package
__all__ = [
    # Version
    "__version__",
    # Base classes
    "EntityBase",
    "RepositoryBase",
    "SortDirection",
    "SortField",
    # SQL API (aliased for convenience)
    "SQLRootEntityBase",
    "SQLRepositoryBase",
    # MongoDB API (aliased for convenience)
    "MongoRootEntityBase",
    "MongoRepositoryBase",
]

# Create convenient aliases for the most commonly used classes
# This allows users to import directly from sas.cosmosdb
RootEntityBase = SQLRootEntityBase  # Default to SQL API for backwards compatibility
