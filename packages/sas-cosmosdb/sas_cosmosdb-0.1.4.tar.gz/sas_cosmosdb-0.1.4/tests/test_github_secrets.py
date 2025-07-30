"""
Demonstration of GitHub Secrets Integration for Cosmos DB Tests

This module shows how to use GitHub secrets for connection strings in integration tests.
"""

import uuid

import pytest
import pytest_asyncio
from pydantic import Field

from src.sas.cosmosdb.sql.model import RootEntityBase
from src.sas.cosmosdb.sql.repository import RepositoryBase
from tests.test_config import (
    integration_test,
    requires_sql,
    skip_if_no_mongodb,
    skip_if_no_sql,
    test_config,
)


class DemoEntity(RootEntityBase["DemoEntity", str]):
    """Demo entity for testing GitHub secrets integration."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(default="GitHub Secrets Test")
    value: str = Field(default="demo")


class DemoRepository(RepositoryBase[DemoEntity, str]):
    """Demo repository for testing GitHub secrets integration."""

    def __init__(self, connection_string: str, database_name: str):
        super().__init__(
            connection_string=connection_string,
            database_name=database_name,
            container_name="DemoContainer",
            use_managed_identity=True,
        )

    def _document_to_entity(self, document: dict) -> DemoEntity:
        """Convert document to entity."""
        clean_document = {
            k: v
            for k, v in document.items()
            if not k.startswith("_") or k == "_partitionKey"
        }
        return DemoEntity(**clean_document)


@pytest_asyncio.fixture(scope="session")
async def demo_sql_repository():
    """Create a demo SQL repository using GitHub secrets."""
    if not test_config.has_sql_config:
        pytest.skip("SQL API connection string not available")

    connection_info = test_config.get_sql_connection_info()
    repo = DemoRepository(
        connection_info["connection_string"], connection_info["database_name"]
    )
    yield repo
    if hasattr(repo, "_client") and repo._client:
        await repo._client.close()


class TestGitHubSecretsIntegration:
    """Demonstrate GitHub secrets integration."""

    def test_config_availability(self):
        """Test that demonstrates how configuration is checked."""
        print(f"MongoDB config available: {test_config.has_mongodb_config}")
        print(f"SQL config available: {test_config.has_sql_config}")
        print(f"Azure auth available: {test_config.has_azure_auth}")

        # This test always passes to show configuration state
        assert True

    @skip_if_no_sql()
    def test_sql_connection_info(self):
        """Test that only runs if SQL connection is available."""
        connection_info = test_config.get_sql_connection_info()

        # Verify connection info structure (without exposing secrets)
        assert "service_location" in connection_info
        assert "database_name" in connection_info
        assert "container_name" in connection_info
        assert "connection_string" in connection_info

        # Verify service location is not empty
        assert connection_info["connection_string"] is not None
        assert len(connection_info["connection_string"]) > 0

        print("✓ SQL connection info available and properly structured")

    @skip_if_no_mongodb()
    def test_mongodb_connection_info(self):
        """Test that only runs if MongoDB connection is available."""
        connection_info = test_config.get_mongodb_connection_info()

        # Verify connection info structure (without exposing secrets)
        assert "connection_string" in connection_info
        assert "database_name" in connection_info

        # Verify connection string is not empty
        assert connection_info["connection_string"] is not None
        assert len(connection_info["connection_string"]) > 0

        print("✓ MongoDB connection info available and properly structured")

    @integration_test()
    @requires_sql()
    @pytest.mark.asyncio
    async def test_sql_repository_with_github_secrets(self, demo_sql_repository):
        """Integration test using SQL repository with GitHub secrets."""
        repo = demo_sql_repository

        # Initialize repository
        await repo._ensure_initialized()
        assert repo._is_initialized.is_set()

        # Create and save a demo entity
        entity = DemoEntity(
            id=str(uuid.uuid4()), name="GitHub Secrets Test", value="integration"
        )
        await repo.add_async(entity)
        saved_entity = await repo.get_async(entity.id)

        assert saved_entity.id is not None
        assert saved_entity.name == "GitHub Secrets Test"
        assert saved_entity.value == "integration"

        # Clean up
        await repo.delete_async(saved_entity.id)

        print("✓ SQL repository integration test with GitHub secrets completed")

    @pytest.mark.unit
    def test_unit_test_example(self):
        """Example unit test that always runs."""
        # Unit tests don't require connection strings
        entity = DemoEntity(id="test-id", name="Unit Test", value="no-secrets-needed")

        assert entity.id == "test-id"
        assert entity.name == "Unit Test"
        assert entity.value == "no-secrets-needed"

        print("✓ Unit test completed (no secrets required)")


# Example of using environment variables directly (for local development)
def test_environment_variables_example():
    """Example showing how environment variables are used."""
    import os

    # These would be set by GitHub Actions or local .env file
    mongodb_conn = os.getenv("COSMOSDB_MONGODB_CONNECTION_STRING")
    sql_conn = os.getenv("COSMOSDB_SQL_LOCATION")

    print(f"MongoDB connection available: {mongodb_conn is not None}")
    print(f"SQL connection available: {sql_conn is not None}")

    if test_config.has_mongodb_config and mongodb_conn is None:
        print(f"MongoDB connection string: {mongodb_conn}")
        os.environ["COSMOSDB_MONGODB_CONNECTION_STRING"] = (
            test_config.cosmosdb_mongodb_connection_string
        )
        mongodb_conn = os.getenv("COSMOSDB_MONGODB_CONNECTION_STRING")

    if test_config.has_sql_config and sql_conn is None:
        print(f"SQL connection string: {sql_conn}")
        os.environ["COSMOSDB_SQL_LOCATION"] = test_config.cosmosdb_sql_location
        sql_conn = os.getenv("COSMOSDB_SQL_LOCATION")

    # Test configuration uses these same environment variables

    assert test_config.has_mongodb_config == (mongodb_conn is not None)
    assert test_config.has_sql_config == (sql_conn is not None)

    print("✓ Environment variable integration verified")
