"""
Test configuration module for managing connection strings and test settings.
"""

import os
from typing import Optional

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))


class TestConfig(BaseSettings):
    """Configuration for tests with support for environment variables and GitHub secrets."""

    # MongoDB Configuration
    cosmosdb_mongodb_connection_string: Optional[str] = Field(
        default=None,
        description="MongoDB connection string for Cosmos DB",
        json_schema_extra={
            "env": "COSMOSDB_MONGODB_CONNECTION_STRING",
            "example": "mongodb://<username>:<password>@<host>:<port>/<database>",
        },
    )
    cosmosdb_mongodb_database_name: str = Field(
        default="test_db",
        description="MongoDB database name for tests",
        json_schema_extra={
            "env": "COSMOSDB_MONGODB_DATABASE_NAME",
            "example": "test_db",
        },
    )

    # SQL API Configuration
    cosmosdb_sql_location: Optional[str] = Field(
        default=None,
        description="SQL API location for Cosmos DB",
        json_schema_extra={
            "env": "COSMOSDB_SQL_LOCATION",
            "example": "https://<your-account>.documents.azure.com:443/",
        },
    )
    cosmosdb_sql_database_name: str = Field(
        default="test_db",
        description="SQL database name for tests",
        json_schema_extra={
            "env": "COSMOSDB_SQL_DATABASE_NAME",
            "example": "test_db",
        },
    )
    cosmosdb_sql_container_name: str = Field(
        default="test_container",
        description="SQL container name for tests",
        json_schema_extra={
            "env": "COSMOSDB_SQL_CONTAINER_NAME",
            "example": "test_container",
        },
    )

    cosmosdb_sql_connection_string: Optional[str] = Field(
        default=None,
        description="SQL API connection string for Cosmos DB",
        json_schema_extra={
            "env": "COSMOSDB_SQL_CONNECTION_STRING",
            "example": "AccountEndpoint=https://<your-account>.documents.azure.com:443/;AccountKey=<your-key>;",
        },
    )

    # Azure Authentication (optional)
    azure_client_id: Optional[str] = Field(
        default=None,
        description="Azure client ID for authentication",
        json_schema_extra={"env": "AZURE_CLIENT_ID", "example": "<your-client-id>"},
    )
    azure_client_secret: Optional[str] = Field(
        default=None,
        description="Azure client secret for authentication",
        json_schema_extra={
            "env": "AZURE_CLIENT_SECRET",
            "example": "<your-client-secret>",
        },
    )
    azure_tenant_id: Optional[str] = Field(
        default=None,
        description="Azure tenant ID for authentication",
        json_schema_extra={"env": "AZURE_TENANT_ID", "example": "<your-tenant-id>"},
    )

    # Test Configuration
    test_type: str = Field(
        default="unit",
        description="Type of tests to run: unit or integration",
        json_schema_extra={"env": "TEST_TYPE", "example": "unit"},
    )

    run_integration_tests: bool = Field(
        default=False,
        description="Whether to run integration tests",
        json_schema_extra={"env": "RUN_INTEGRATION_TESTS", "example": False},
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def has_mongodb_config(self) -> bool:
        """Check if MongoDB configuration is available."""
        return self.cosmosdb_mongodb_connection_string is not None

    @property
    def has_sql_config(self) -> bool:
        """Check if SQL API configuration is available."""
        return self.cosmosdb_sql_location is not None

    @property
    def has_azure_auth(self) -> bool:
        """Check if Azure authentication is configured."""
        return all(
            [self.azure_client_id, self.azure_client_secret, self.azure_tenant_id]
        )

    def get_mongodb_connection_info(self) -> dict:
        """Get MongoDB connection information."""
        if not self.has_mongodb_config:
            raise ValueError("MongoDB connection string not configured")

        return {
            "connection_string": self.cosmosdb_mongodb_connection_string,
            "database_name": self.cosmosdb_mongodb_database_name,
        }

    def get_sql_connection_info(self) -> dict:
        """Get SQL API connection information."""
        if not self.has_sql_config:
            raise ValueError("SQL API location not configured")

        return {
            "service_location": self.cosmosdb_sql_location,
            "database_name": self.cosmosdb_sql_database_name,
            "container_name": self.cosmosdb_sql_container_name,
            "connection_string": self.cosmosdb_sql_connection_string,
        }

    def get_azure_credentials(self) -> dict:
        """Get Azure authentication credentials."""
        if not self.has_azure_auth:
            raise ValueError("Azure authentication not configured")

        return {
            "client_id": self.azure_client_id,
            "client_secret": self.azure_client_secret,
            "tenant_id": self.azure_tenant_id,
        }


# Global test configuration instance
test_config = TestConfig()


def skip_if_no_mongodb():
    """Decorator to skip tests if MongoDB connection is not available."""
    import pytest

    return pytest.mark.skipif(
        not test_config.has_mongodb_config,
        reason="MongoDB connection string not available",
    )


def skip_if_no_sql():
    """Decorator to skip tests if SQL API connection is not available."""
    import pytest

    return pytest.mark.skipif(
        not test_config.has_sql_config, reason="SQL API connection string not available"
    )


def skip_if_no_azure_auth():
    """Decorator to skip tests if Azure authentication is not available."""
    import pytest

    return pytest.mark.skipif(
        not test_config.has_azure_auth, reason="Azure authentication not configured"
    )


def integration_test():
    """Decorator to mark tests as integration tests."""
    import pytest

    return pytest.mark.integration


def requires_mongodb():
    """Decorator to mark tests that require MongoDB connection."""
    import pytest

    return pytest.mark.integration and skip_if_no_mongodb()


def requires_sql():
    """Decorator to mark tests that require SQL API connection."""
    import pytest

    return pytest.mark.integration and skip_if_no_sql()


def requires_azure_auth():
    """Decorator to mark tests that require Azure authentication."""
    import pytest

    return pytest.mark.integration and skip_if_no_azure_auth()
