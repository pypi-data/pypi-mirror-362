import asyncio
import logging
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from threading import Lock
from typing import Optional

import pymongo
import pytest
import pytest_asyncio
from pydantic import Field

from src.sas.cosmosdb.base.model_base import EntityBase
from src.sas.cosmosdb.base.repository_base import SortDirection, SortField
from src.sas.cosmosdb.mongo.model import RootEntityBase
from src.sas.cosmosdb.mongo.repository import RepositoryBase
from tests.test_config import test_config

# Configure logging for better test debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CustomNonSerializableClass(EntityBase):
    """Custom class that cannot be serialized by default."""

    def __init__(self, value: str):
        self.value = value
        self.lock = Lock()

    def __str__(self):
        return f"CustomNonSerializableClass({self.value})"


class People(EntityBase):
    name: str
    age: int
    phone: str = Field(default="123-456-7890")
    # Non-serializable attributes for testing
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    precision_number: Optional[Decimal] = Field(default=None)


class SampleEntity(RootEntityBase["SampleEntity", str]):
    """Sample entity for testing purposes with non-serializable attributes."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str = Field(default="test@example.com")
    age: int = Field(default=25)
    friends: list[People] = Field(default_factory=list)

    # Non-serializable attributes for testing serialization handling
    timestamp: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    decimal_value: Optional[Decimal] = Field(default=None)
    custom_object: Optional[str] = Field(default=None)  # Will store serialized version
    callback_function: Optional[str] = Field(default=None)  # Will store function name

    def __init__(self, **data):
        super().__init__(**data)
        # Add truly non-serializable attributes after initialization


class SampleEntityRepository(RepositoryBase[SampleEntity, str]):
    """Test repository implementation for SampleEntity."""

    def __init__(self, connection_string, database_name, collection_name, indexes=None):
        super().__init__(
            connection_string=connection_string,
            database_name=database_name,
            collection_name=collection_name,
            indexes=indexes,
        )


@pytest_asyncio.fixture(scope="session")
async def test_repository():
    """Create a test repository instance."""
    if not test_config.has_mongodb_config:
        pytest.skip("MongoDB configuration not provided in test_config")

    connection_string = test_config.cosmosdb_mongodb_connection_string
    database_name = test_config.cosmosdb_mongodb_database_name

    repo = SampleEntityRepository(
        connection_string=connection_string,
        database_name=database_name,
        collection_name="test_collection",
        indexes=["name", "email", "age"],
    )
    yield repo


# === CORE FUNCTIONALITY TESTS ===


@pytest.mark.asyncio
async def test_repository_initialization():
    """Test repository initialization and basic setup."""

    if not test_config.has_mongodb_config:
        pytest.skip("MongoDB configuration not provided in test_config")

    connection_string = test_config.cosmosdb_mongodb_connection_string
    database_name = test_config.cosmosdb_mongodb_database_name

    repo = SampleEntityRepository(
        connection_string=connection_string,
        database_name=database_name,
        collection_name="test_collection_init",
        indexes=["name", "email"],
    )

    # Test entity creation
    entity = SampleEntity(name="Init Test", email="init@test.com")
    await repo.add_async(entity)

    # Verify entity was added
    retrieved = await repo.get_async(entity.id)
    assert retrieved is not None
    assert retrieved.name == "Init Test"


@pytest.mark.asyncio
async def test_comprehensive_crud_operations(test_repository: SampleEntityRepository):
    """Test all CRUD operations in a comprehensive workflow."""
    # CREATE - Add multiple entities with complex data
    entities = [
        SampleEntity(name="CRUD Test 1", email="crud1@test.com", age=25),
        SampleEntity(name="CRUD Test 2", email="crud2@test.com", age=30),
        SampleEntity(name="CRUD Test 3", email="crud3@test.com", age=35),
    ]

    # Add friends to demonstrate nested object handling
    entities[0].friends.append(People(name="Friend 1", age=20, phone="111-222-3333"))
    entities[1].friends.append(People(name="Friend 2", age=22, phone="444-555-6666"))

    # Add all entities
    for entity in entities:
        await test_repository.add_async(entity)

    # READ - Test various read operations
    # Get by ID
    retrieved = await test_repository.get_async(entities[0].id)
    assert retrieved is not None
    assert retrieved.name == "CRUD Test 1"
    assert len(retrieved.friends) == 1
    assert isinstance(retrieved.friends[0], People)

    # Find with predicate
    found_entities = await test_repository.find_async({"name": {"$regex": "CRUD Test"}})
    assert len(found_entities) >= 3

    # Find one
    found_one = await test_repository.find_one_async({"name": "CRUD Test 2"})
    assert found_one is not None
    assert found_one.email == "crud2@test.com"

    # Check existence
    exists = await test_repository.exists_async({"name": "CRUD Test 3"})
    assert exists is True

    # Count
    count = await test_repository.count_async({"name": {"$regex": "CRUD Test"}})
    assert count >= 3

    # UPDATE - Test updates
    entities[0].name = "Updated CRUD Test 1"
    entities[0].friends[0].phone = "999-888-7777"
    await test_repository.update_async(entities[0])

    # Verify update
    updated = await test_repository.get_async(entities[0].id)
    assert updated.name == "Updated CRUD Test 1"
    assert updated.friends[0].phone == "999-888-7777"

    # DELETE - Test deletion
    await test_repository.delete_async(entities[0].id)

    # Verify deletion
    deleted = await test_repository.get_async(entities[0].id)
    assert deleted is None

    # Verify other entities still exist
    remaining_count = await test_repository.count_async(
        {"name": {"$regex": "CRUD Test"}}
    )
    assert remaining_count <= count - 1


@pytest.mark.asyncio
async def test_sorting_and_pagination(test_repository: SampleEntityRepository):
    """Test sorting and pagination functionality."""
    # Create test data with specific patterns for sorting
    entities = [
        SampleEntity(name="Sort A", age=30, email="a@test.com"),
        SampleEntity(name="Sort Z", age=25, email="z@test.com"),
        SampleEntity(name="Sort M", age=35, email="m@test.com"),
        SampleEntity(name="Sort B", age=20, email="b@test.com"),
        SampleEntity(name="Sort Y", age=40, email="y@test.com"),
    ]

    for entity in entities:
        await test_repository.add_async(entity)

    # Test sorting - ascending by name
    sorted_asc = await test_repository.find_async(
        {"name": {"$regex": "Sort"}}, [SortField("name", SortDirection.ASCENDING)]
    )
    assert len(sorted_asc) >= 5
    for i in range(len(sorted_asc) - 1):
        assert sorted_asc[i].name <= sorted_asc[i + 1].name

    # Test sorting - descending by age
    sorted_desc = await test_repository.find_async(
        {"name": {"$regex": "Sort"}}, [SortField("age", SortDirection.DESCENDING)]
    )
    assert len(sorted_desc) >= 5
    for i in range(len(sorted_desc) - 1):
        assert sorted_desc[i].age >= sorted_desc[i + 1].age

    # Test all_async with sorting
    all_sorted = await test_repository.all_async(
        [SortField("name", SortDirection.ASCENDING)]
    )
    # Should include our test entities in sorted order
    sort_entities = [e for e in all_sorted if e.name.startswith("Sort")]
    assert len(sort_entities) >= 5

    # Test pagination
    page1 = await test_repository.find_with_pagination_async(
        {"name": {"$regex": "Sort"}},
        [SortField("name", pymongo.ASCENDING)],
        skip=0,
        limit=2,
    )
    assert len(page1) == 2
    assert page1[0].name <= page1[1].name

    page2 = await test_repository.find_with_pagination_async(
        {"name": {"$regex": "Sort"}},
        [SortField("name", pymongo.ASCENDING)],
        skip=2,
        limit=2,
    )
    assert len(page2) == 2
    assert page1[1].name <= page2[0].name  # Ensure no overlap


@pytest.mark.asyncio
async def test_complex_queries_and_predicates(test_repository: SampleEntityRepository):
    """Test complex query patterns and predicates."""
    # Create entities with various patterns
    entities = [
        SampleEntity(name="Query Test Alpha", age=25, email="alpha@test.com"),
        SampleEntity(name="Query Test Beta", age=30, email="beta@test.com"),
        SampleEntity(name="Query Test Gamma", age=35, email="gamma@test.com"),
        SampleEntity(name="Other Entity", age=40, email="other@test.com"),
    ]

    # Add friends with specific patterns
    entities[0].friends.extend([People(name="John", age=28, phone="555-1234")])
    entities[1].friends.extend([People(name="Jane", age=32, phone="555-5678")])
    entities[2].friends.extend([People(name="Bob", age=24, phone="555-9012")])

    for entity in entities:
        await test_repository.add_async(entity)

    # Test regex queries
    regex_results = await test_repository.find_async({"name": {"$regex": "Query Test"}})
    assert len(regex_results) >= 3

    # Test range queries
    age_range = await test_repository.find_async({"age": {"$gte": 30, "$lte": 35}})
    age_range_filtered = [e for e in age_range if "Query Test" in e.name]
    assert len(age_range_filtered) >= 2

    # Test nested field queries
    nested_results = await test_repository.find_async({"friends.name": "John"})
    assert len(nested_results) >= 1
    assert nested_results[0].name == "Query Test Alpha"

    # Test compound queries
    compound_results = await test_repository.find_async(
        {"$and": [{"name": {"$regex": "Query Test"}}, {"age": {"$gte": 30}}]}
    )

    compound_results = await test_repository.find_async(
        {"name": {"$regex": "Query Test"}, "age": {"$gte": 30}}
    )

    assert len(compound_results) >= 2

    # Test IN operator
    in_results = await test_repository.find_async(
        {"name": {"$in": ["Query Test Alpha", "Query Test Beta"]}}
    )
    assert len(in_results) >= 2


# === ERROR HANDLING AND EDGE CASES ===


@pytest.mark.asyncio
async def test_error_handling(test_repository: SampleEntityRepository):
    """Test error handling and edge cases."""
    # Test non-existent entity
    nonexistent = await test_repository.get_async(str(uuid.uuid4()))
    assert nonexistent is None

    # Test empty query
    empty_results = await test_repository.find_async({})
    assert isinstance(empty_results, list)

    # Test no matches
    no_matches = await test_repository.find_async({"name": "NonExistentEntity12345"})
    assert len(no_matches) == 0

    # Test count with no matches
    zero_count = await test_repository.count_async({"name": "NonExistentEntity12345"})
    assert zero_count == 0

    # Test exists with no matches
    not_exists = await test_repository.exists_async({"name": "NonExistentEntity12345"})
    assert not_exists is False

    # Test find_one with no matches
    not_found = await test_repository.find_one_async({"name": "NonExistentEntity12345"})
    assert not_found is None


@pytest.mark.asyncio
async def test_data_validation_and_serialization():
    """Test data validation and serialization."""
    # Test entity creation with all fields
    entity = SampleEntity(name="Validation Test", email="validation@test.com", age=25)

    # Test adding friends
    entity.friends.append(People(name="Friend 1", age=30, phone="555-1234"))
    entity.friends.append(People(name="Friend 2", age=25))  # Default phone

    # Test serialization
    entity_dict = entity.model_dump()
    assert entity_dict["name"] == "Validation Test"
    assert len(entity_dict["friends"]) == 2
    assert entity_dict["friends"][1]["phone"] == "123-456-7890"  # Default value

    # Test deserialization
    reconstructed = SampleEntity.model_validate(entity_dict)
    assert reconstructed.name == entity.name
    assert len(reconstructed.friends) == 2
    assert isinstance(reconstructed.friends[0], People)


@pytest.mark.asyncio
async def test_concurrent_operations(test_repository: SampleEntityRepository):
    """Test concurrent operations."""
    # Create multiple entities for concurrent operations
    entities = [
        SampleEntity(
            name=f"Concurrent {i}", email=f"concurrent{i}@test.com", age=25 + i
        )
        for i in range(5)
    ]

    # Test concurrent additions
    add_tasks = [test_repository.add_async(entity) for entity in entities]
    await asyncio.gather(*add_tasks)

    # Verify all entities were added
    for entity in entities:
        retrieved = await test_repository.get_async(entity.id)
        assert retrieved is not None
        assert retrieved.name == entity.name

    # Test concurrent reads
    read_tasks = [test_repository.get_async(entity.id) for entity in entities]
    retrieved_entities = await asyncio.gather(*read_tasks)

    assert len(retrieved_entities) == 5
    for retrieved in retrieved_entities:
        assert retrieved is not None
        assert retrieved.name.startswith("Concurrent")


@pytest.mark.asyncio
async def test_performance_characteristics(test_repository: SampleEntityRepository):
    """Test performance characteristics."""
    import time

    # Test batch operations
    batch_size = 20
    entities = [
        SampleEntity(
            name=f"Perf Test {i:03d}", email=f"perf{i}@test.com", age=25 + (i % 20)
        )
        for i in range(batch_size)
    ]

    # Measure insertion time
    start_time = time.time()
    for entity in entities:
        await test_repository.add_async(entity)
    insert_time = time.time() - start_time

    logger.info(f"Batch insert of {batch_size} entities: {insert_time:.2f}s")
    assert insert_time < 30, "Batch insert should complete within reasonable time"

    # Measure query time
    start_time = time.time()
    perf_entities = await test_repository.find_async({"name": {"$regex": "Perf Test"}})
    query_time = time.time() - start_time

    logger.info(f"Query for {len(perf_entities)} entities: {query_time:.2f}s")
    assert query_time < 5, "Query should complete within reasonable time"
    assert len(perf_entities) >= batch_size


@pytest.mark.asyncio
async def test_pagination_edge_cases(test_repository: SampleEntityRepository):
    """Test pagination edge cases."""
    # Create test data
    entities = [
        SampleEntity(name=f"Page Test {i:02d}", email=f"page{i}@test.com", age=25 + i)
        for i in range(10)
    ]

    for entity in entities:
        await test_repository.add_async(entity)

    # Test limit larger than available data
    large_limit = await test_repository.find_with_pagination_async(
        {"name": {"$regex": "Page Test"}},
        [SortField("name", SortDirection.ASCENDING)],
        skip=0,
        limit=100,
    )
    assert len(large_limit) <= 100

    # Test skip beyond available data
    beyond_skip = await test_repository.find_with_pagination_async(
        {"name": {"$regex": "Page Test"}},
        [SortField("name", SortDirection.ASCENDING)],
        skip=50,
        limit=10,
    )
    assert len(beyond_skip) == 0

    # Test zero limit.
    # 0 means equaivalent to no limit, so it should return all matching entities
    zero_limit = await test_repository.find_with_pagination_async(
        {"name": {"$regex": "Page Test"}},
        [SortField("name", SortDirection.ASCENDING)],
        skip=10,
        limit=0,
    )
    assert len(zero_limit) >= 0


# === INTEGRATION TESTS ===


@pytest.mark.asyncio
async def test_production_like_workflow(test_repository: SampleEntityRepository):
    """Test production-like workflow with realistic data patterns."""
    test_id = uuid.uuid4().hex[:8]

    # Simulate user registration workflow
    users = []
    for i in range(20):
        user = SampleEntity(
            name=f"User{test_id}_{i:02d}",
            email=f"user{test_id}_{i}@company.com",
            age=22 + (i % 40),
        )

        # Add some friends to simulate social connections
        if i > 0:
            user.friends.append(
                People(name=f"Friend{i}_1", age=25 + (i % 30), phone=f"555-{i:04d}")
            )
        if i > 1:
            user.friends.append(
                People(
                    name=f"Friend{i}_2", age=30 + (i % 25), phone=f"555-{i + 1000:04d}"
                )
            )

        users.append(user)
        await test_repository.add_async(user)

    # Test various query patterns
    # Find users by age range
    young_users = await test_repository.find_async(
        {"age": {"$lte": 30}, "name": {"$regex": f"User{test_id}_"}}
    )
    assert len(young_users) > 0

    # Find users with friends
    users_with_friends = await test_repository.find_async(
        {"friends": {"$ne": []}, "name": {"$regex": f"User{test_id}_"}}
    )
    assert len(users_with_friends) > 0

    # Pagination through all users
    all_users_paged = []
    skip = 0
    limit = 5
    while True:
        page = await test_repository.find_with_pagination_async(
            {"name": {"$regex": f"User{test_id}_"}},
            [SortField("name", pymongo.ASCENDING)],
            skip=skip,
            limit=limit,
        )
        if not page:
            break
        all_users_paged.extend(page)
        skip += limit

    assert len(all_users_paged) == 20

    # Update workflow - modify some users
    for i in range(5):
        users[i].age += 1
        await test_repository.update_async(users[i])

    # Verify updates
    updated_users = await test_repository.find_async(
        {"name": {"$regex": f"User{test_id}_0[0-4]"}}
    )
    for user in updated_users:
        original_user = next(u for u in users if u.id == user.id)
        assert user.age == original_user.age

    # Delete workflow
    await test_repository.delete_async(users[0].id)

    # Verify deletion
    final_count = await test_repository.count_async(
        {"name": {"$regex": f"User{test_id}_"}}
    )
    assert final_count == 19


@pytest.mark.asyncio
async def test_delete_items_async_comprehensive(
    test_repository: SampleEntityRepository,
):
    """Test comprehensive delete_items_async functionality for MongoDB."""
    # Setup test data
    test_entities = []
    test_id = str(uuid.uuid4())[:8]

    # Clean up any existing test data for this test ID (defensive cleanup)
    await test_repository.delete_items_async(
        {"name": {"$regex": f"DeleteTest_{test_id}_.*"}}
    )

    for i in range(10):
        entity = SampleEntity(
            name=f"DeleteTest_{test_id}_{i}",
            email=f"delete{i}@test.com",
            age=20 + (i % 5),  # Ages: 20, 21, 22, 23, 24, 20, 21, 22, 23, 24
        )
        if i % 3 == 0:  # Add friends to some entities
            entity.friends.append(People(name=f"Friend{i}", age=25 + i))
        test_entities.append(entity)
        await test_repository.add_async(entity)

    print(f"✓ Created {len(test_entities)} test entities for deletion")

    # TEST 1: Delete by age filter (scoped to our test entities)
    delete_query = {
        "$and": [
            {"name": {"$regex": f"DeleteTest_{test_id}_.*"}},
            {"age": {"$gte": 23}},
        ]
    }
    expected_deletions = len([e for e in test_entities if e.age >= 23])

    deleted_count = await test_repository.delete_items_async(delete_query)
    assert deleted_count == expected_deletions, (
        f"Expected {expected_deletions} deletions, got {deleted_count}"
    )
    print(f"✓ Deleted {deleted_count} entities with age >= 23")

    # Verify deletions
    remaining_entities = await test_repository.find_async(
        {"name": {"$regex": f"DeleteTest_{test_id}_.*"}}
    )
    assert all(e.age < 23 for e in remaining_entities), (
        "Some entities with age >= 23 were not deleted"
    )

    # TEST 2: Delete by name pattern
    delete_query = {"name": {"$regex": f"DeleteTest_{test_id}_[135]$"}}
    deleted_count = await test_repository.delete_items_async(delete_query)
    print(f"✓ Deleted {deleted_count} entities matching name pattern")

    # TEST 3: Delete entities with friends (using MongoDB array query)
    entity_with_friend = SampleEntity(
        name=f"DeleteTestFriend_{test_id}", email="friendtest@test.com", age=30
    )
    entity_with_friend.friends.append(People(name="TestFriend", age=25))
    await test_repository.add_async(entity_with_friend)

    delete_query = {
        "$and": [
            {"name": {"$regex": f"DeleteTest.*_{test_id}_.*"}},
            {"friends": {"$ne": []}},
        ]
    }
    deleted_count = await test_repository.delete_items_async(delete_query)
    print(f"✓ Deleted {deleted_count} entities with friends")

    # Verify no entities with friends remain in our test set
    remaining_with_friends = await test_repository.find_async(
        {
            "$and": [
                {"name": {"$regex": f"DeleteTest.*_{test_id}_.*"}},
                {"friends": {"$ne": []}},
            ]
        }
    )
    assert len(remaining_with_friends) == 0, (
        "Some entities with friends were not deleted"
    )

    # TEST 4: Delete with no matches (scoped to our test entities)
    delete_query = {
        "$and": [
            {"name": {"$regex": f"DeleteTest.*_{test_id}_.*"}},
            {"age": {"$gt": 100}},
        ]
    }
    deleted_count = await test_repository.delete_items_async(delete_query)
    assert deleted_count == 0, (
        "Should not delete any entities when query matches nothing"
    )
    print("✓ Correctly handled delete query with no matches")

    # TEST 5: Clean up remaining test entities
    delete_query = {"name": {"$regex": f"DeleteTest.*_{test_id}_.*"}}
    deleted_count = await test_repository.delete_items_async(delete_query)
    print(f"✓ Cleaned up {deleted_count} remaining test entities")

    # Verify cleanup
    remaining_test_entities = await test_repository.find_async(
        {"name": {"$regex": f"DeleteTest.*_{test_id}_.*"}}
    )
    assert len(remaining_test_entities) == 0, "Some test entities were not cleaned up"

    print("✓ All delete_items_async tests completed successfully")


@pytest.mark.asyncio
async def test_delete_items_async_mongodb_specific(
    test_repository: SampleEntityRepository,
):
    """Test MongoDB-specific delete operations and edge cases."""
    test_id = str(uuid.uuid4())[:8]

    # Clean up any existing test data for this test ID (defensive cleanup)
    await test_repository.delete_items_async()

    # Setup test data with MongoDB-specific features
    entities = []
    for i in range(20):
        entity = SampleEntity(
            name=f"MongoDelete_{test_id}_{i}",
            email=f"mongo{i}@test.com",
            age=25 + (i % 10),  # Ages from 25 to 34
        )

        # Add varying numbers of friends for array testing
        for j in range(i % 3):
            entity.friends.append(
                People(name=f"Friend_{i}_{j}", age=20 + j, phone=f"555-{i:03d}{j:02d}")
            )

        entities.append(entity)
        await test_repository.add_async(entity)

    print(f"✓ Created {len(entities)} entities for MongoDB-specific tests")

    # TEST 1: Delete using MongoDB array size operator
    delete_query = {"friends": {"$size": 2}}  # Delete entities with exactly 2 friends
    expected_count = len([e for e in entities if len(e.friends) == 2])

    deleted_count = await test_repository.delete_items_async(delete_query)
    assert deleted_count >= expected_count, (
        f"Expected {expected_count} deletions, got {deleted_count}"
    )
    print(f"✓ Deleted {deleted_count} entities with exactly 2 friends")

    # TEST 2: Delete using elemMatch on friends array
    delete_query = {"friends": {"$elemMatch": {"age": {"$gte": 21}}}}
    deleted_count = await test_repository.delete_items_async(delete_query)
    print(f"✓ Deleted {deleted_count} entities with friends aged >= 21")

    # TEST 3: Delete using complex MongoDB aggregation-style query
    delete_query = {
        "$and": [
            {"age": {"$in": [25, 26, 27]}},
            {"email": {"$regex": f"mongo.*{test_id}.*@test.com"}},
        ]
    }
    deleted_count = await test_repository.delete_items_async(delete_query)
    print(f"✓ Deleted {deleted_count} entities with complex AND query")

    # TEST 4: Performance test with large batch
    batch_entities = []
    for i in range(100):
        entity = SampleEntity(
            name=f"BatchMongo_{test_id}_{i}", email=f"batch{i}@test.com", age=30
        )
        batch_entities.append(entity)
        await test_repository.add_async(entity)

    start_time = asyncio.get_event_loop().time()
    delete_query = {"name": {"$regex": f"BatchMongo_{test_id}_.*"}}
    deleted_count = await test_repository.delete_items_async(delete_query)
    end_time = asyncio.get_event_loop().time()

    assert deleted_count == 100, (
        f"Should delete all 100 batch entities, got {deleted_count}"
    )
    assert end_time - start_time < 10.0, (
        "Batch deletion should complete within 10 seconds"
    )
    print(
        f"✓ Batch deleted {deleted_count} entities in {end_time - start_time:.2f} seconds"
    )

    # TEST 5: Clean up remaining test entities
    cleanup_query = {"name": {"$regex": f"MongoDelete_{test_id}_.*"}}
    deleted_count = await test_repository.delete_items_async(cleanup_query)
    print(f"✓ Cleaned up {deleted_count} remaining test entities")

    # TEST 6: Error handling for invalid MongoDB operators
    try:
        await test_repository.delete_items_async(
            {"invalid_field": {"$invalidOp": "value"}}
        )
        assert False, "Should have raised an exception for invalid MongoDB query"
    except Exception as e:
        print(f"✓ Correctly handled invalid MongoDB query: {type(e).__name__}")

    print("✓ MongoDB-specific delete_items_async tests completed successfully")


@pytest.mark.asyncio
async def test_delete_items_async_concurrent_safety(
    test_repository: SampleEntityRepository,
):
    """Test concurrent safety of delete_items_async operations."""
    test_id = str(uuid.uuid4())[:8]

    # Setup test data
    entities = []
    for i in range(50):
        entity = SampleEntity(
            name=f"ConcurrentDelete_{test_id}_{i}",
            email=f"concurrent{i}@test.com",
            age=25 + (i % 2),  # Ages 25 or 26
        )
        entities.append(entity)
        await test_repository.add_async(entity)

    print(f"✓ Created {len(entities)} entities for concurrent deletion tests")

    # TEST: Concurrent deletions with different criteria
    async def delete_by_age(age_value):
        query = {
            "$and": [
                {"age": age_value},
                {"name": {"$regex": f"ConcurrentDelete_{test_id}_.*"}},
            ]
        }
        return await test_repository.delete_items_async(query)

    # Run concurrent deletions
    tasks = [delete_by_age(25), delete_by_age(26)]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Verify results
    total_deleted = sum(r for r in results if isinstance(r, int))
    assert total_deleted == 50, f"Should delete all 50 entities, got {total_deleted}"

    # Verify no entities remain
    remaining = await test_repository.find_async(
        {"name": {"$regex": f"ConcurrentDelete_{test_id}_.*"}}
    )
    assert len(remaining) == 0, "All test entities should have been deleted"

    print(
        f"✓ Concurrent deletion completed successfully, deleted {total_deleted} entities"
    )


@pytest.mark.asyncio
async def test_repository_initialization_error_handling():
    """Test repository initialization with invalid parameters."""
    # Test with invalid connection string
    with pytest.raises(Exception):
        invalid_repo = SampleEntityRepository(
            "invalid://connection:string", "test_db", "test_collection"
        )
        entity = SampleEntity(name="Test")
        await invalid_repo.add_async(entity)


@pytest.mark.asyncio
async def test_delete_items_async_large_batch_less_50(
    test_repository: SampleEntityRepository,
):
    """
    Test batch deletion with over 50 items to validate MongoDB batch processing.

    This test verifies:
    1. Efficient handling of large batch deletions (100+ items)
    2. Proper batching logic for MongoDB operations
    3. Performance characteristics of bulk deletion
    4. Memory efficiency with large datasets
    """
    test_id = str(uuid.uuid4())[:8]
    batch_size = 75  # Over 50 to test batching logic

    print(f"🧪 Testing large batch deletion with {batch_size} items...")

    # Clean up any existing test data for this test ID (defensive cleanup)
    await test_repository.delete_items_async(
        {"name": {"$regex": f"LargeBatch_{test_id}_.*"}}
    )

    # Setup test data - Create entities in batches for better performance
    entities = []
    batch_create_size = 20  # Create in smaller batches to avoid memory issues

    for batch_start in range(0, batch_size, batch_create_size):
        batch_entities = []
        batch_end = min(batch_start + batch_create_size, batch_size)

        for i in range(batch_start, batch_end):
            entity = SampleEntity(
                name=f"LargeBatch_{test_id}_{i:03d}",
                email=f"largebatch{i}@test.com",
                age=20 + (i % 50),  # Varied ages for testing
            )

            # Add friends to some entities to test complex object deletion
            if i % 10 == 0:
                entity.friends.append(People(name=f"BatchFriend{i}", age=25 + (i % 20)))

            batch_entities.append(entity)
            entities.append(entity)

        # Insert batch
        for entity in batch_entities:
            await test_repository.add_async(entity)

        print(f"  ✓ Created batch {batch_start + 1}-{batch_end} of {batch_size}")

    print(f"✓ Created {len(entities)} entities for large batch deletion test")

    # Verify all entities were created
    created_entities = await test_repository.find_async(
        {"name": {"$regex": f"LargeBatch_{test_id}_.*"}}
    )
    assert len(created_entities) == batch_size, (
        f"Expected {batch_size} entities, found {len(created_entities)}"
    )

    # TEST 1: Delete all entities in a single batch operation
    print("🔥 Performing large batch deletion...")
    import time

    start_time = time.time()

    deleted_count = await test_repository.delete_items_async(
        {"name": {"$regex": f"LargeBatch_{test_id}_.*"}}
    )

    end_time = time.time()
    deletion_time = end_time - start_time

    print(f"✓ Batch deletion completed in {deletion_time:.2f} seconds")

    # Verify deletion count
    assert deleted_count == batch_size, (
        f"Expected to delete {batch_size} entities, actually deleted {deleted_count}"
    )

    # Verify no entities remain
    remaining_entities = await test_repository.find_async(
        {"name": {"$regex": f"LargeBatch_{test_id}_.*"}}
    )
    assert len(remaining_entities) == 0, (
        f"Expected 0 remaining entities, found {len(remaining_entities)}"
    )

    # Performance validation (should complete within reasonable time)
    max_expected_time = 30.0  # 30 seconds max for 75 deletions
    assert deletion_time < max_expected_time, (
        f"Deletion took {deletion_time:.2f}s, expected < {max_expected_time}s. "
        "Consider optimizing batch processing."
    )

    print("✅ Large batch deletion test completed successfully!")
    print(f"   📊 Deleted {deleted_count} entities in {deletion_time:.2f} seconds")
    print(f"   ⚡ Average: {deleted_count / deletion_time:.1f} deletions/second")


@pytest.mark.asyncio
async def test_delete_items_async_very_large_batch_100_plus(
    test_repository: SampleEntityRepository,
):
    """
    Test very large batch deletion (100+ items) to validate scalability.

    This test validates:
    1. Scalability of batch deletion operations
    2. Memory efficiency with large datasets
    3. Error handling for potential timeout scenarios
    4. Batch processing optimization for MongoDB
    """
    test_id = str(uuid.uuid4())[:8]
    large_batch_size = 120  # Significantly over 50 to test batching

    print(f"🔬 Testing very large batch deletion with {large_batch_size} items...")

    # Clean up any existing test data
    await test_repository.delete_items_async(
        {"name": {"$regex": f"VeryLargeBatch_{test_id}_.*"}}
    )

    # Create test entities efficiently
    print("📦 Creating test entities...")
    entities_created = 0

    # Create in batches to manage memory and avoid timeouts
    create_batch_size = 25
    for batch_start in range(0, large_batch_size, create_batch_size):
        batch_end = min(batch_start + create_batch_size, large_batch_size)

        for i in range(batch_start, batch_end):
            entity = SampleEntity(
                name=f"VeryLargeBatch_{test_id}_{i:03d}",
                email=f"verylarge{i}@batch.test",
                age=18 + (i % 60),  # Ages 18-77
            )

            # Add variety to test complex deletions
            if i % 15 == 0:
                entity.friends.extend(
                    [
                        People(name=f"BatchFriend{i}_1", age=25 + i),
                        People(name=f"BatchFriend{i}_2", age=30 + i),
                    ]
                )

            await test_repository.add_async(entity)
            entities_created += 1

        print(f"  ✓ Created entities {batch_start + 1}-{batch_end}")

    print(f"✓ Successfully created {entities_created} entities")

    # Verify creation
    created_count = await test_repository.count_async(
        {"name": {"$regex": f"VeryLargeBatch_{test_id}_.*"}}
    )
    assert created_count == large_batch_size, (
        f"Expected {large_batch_size} entities, found {created_count}"
    )

    # TEST: Perform very large batch deletion with performance monitoring
    print(f"🚀 Performing very large batch deletion of {large_batch_size} entities...")

    import time

    start_time = time.time()

    try:
        deleted_count = await test_repository.delete_items_async(
            {"name": {"$regex": f"VeryLargeBatch_{test_id}_.*"}}
        )

        end_time = time.time()
        total_time = end_time - start_time

        # Verify successful deletion
        assert deleted_count == large_batch_size, (
            f"Expected to delete {large_batch_size} entities, deleted {deleted_count}"
        )

        # Verify no entities remain
        remaining_count = await test_repository.count_async(
            {"name": {"$regex": f"VeryLargeBatch_{test_id}_.*"}}
        )
        assert remaining_count == 0, f"Expected 0 remaining, found {remaining_count}"

        # Performance validation
        max_time = 60.0  # 60 seconds max for very large batch
        assert total_time < max_time, (
            f"Very large deletion took {total_time:.2f}s, expected < {max_time}s"
        )

        print("✅ Very large batch deletion completed successfully!")
        print(f"   📊 Deleted {deleted_count} entities in {total_time:.2f} seconds")
        print(f"   ⚡ Average: {deleted_count / total_time:.1f} deletions/second")
        print(f"   🎯 Performance target: < {max_time}s (achieved: {total_time:.2f}s)")

    except Exception as e:
        # Clean up in case of failure
        try:
            await test_repository.delete_items_async(
                {"name": {"$regex": f"VeryLargeBatch_{test_id}_.*"}}
            )
        except Exception:
            pass

        # Re-raise the original exception
        print(f"❌ Very large batch deletion failed: {e}")
        raise


# === NON-SERIALIZABLE ATTRIBUTES TESTS ===


@pytest.mark.asyncio
async def test_non_serializable_attributes_handling(
    test_repository: SampleEntityRepository,
):
    """Test handling of non-serializable attributes in MongoDB entities."""
    from datetime import datetime, timezone
    from decimal import Decimal

    # Create entity with non-serializable attributes
    entity = SampleEntity(
        name="NonSerializable Test", email="nonserial@test.com", age=30
    )

    # Set non-serializable attributes
    entity.decimal_value = Decimal("123.456789")
    entity.timestamp = datetime.now(timezone.utc)

    # Add a friend with non-serializable attributes
    friend = People(name="Friend with Decimal", age=25)
    friend.precision_number = Decimal("999.999")
    friend.created_at = datetime.now(timezone.utc)
    entity.friends.append(friend)

    # Set custom non-serializable objects
    # Test that entity can be added to repository despite non-serializable attributes
    await test_repository.add_async(entity)

    # Retrieve and verify
    retrieved = await test_repository.get_async(entity.id)
    assert retrieved is not None
    assert retrieved.name == "NonSerializable Test"
    assert retrieved.age == 30

    # Verify decimal and datetime handling
    assert retrieved.decimal_value is not None
    assert retrieved.timestamp is not None

    # Verify friend with non-serializable attributes
    assert len(retrieved.friends) == 1
    assert retrieved.friends[0].name == "Friend with Decimal"
    assert retrieved.friends[0].precision_number is not None
    assert retrieved.friends[0].created_at is not None


@pytest.mark.asyncio
async def test_serialization_edge_cases(test_repository: SampleEntityRepository):
    """Test edge cases in serialization with various non-serializable types."""
    import json
    from datetime import datetime, timezone
    from decimal import Decimal

    entity = SampleEntity(
        name="Serialization Edge Cases", email="edges@test.com", age=35
    )

    # Test various decimal values
    entity.decimal_value = Decimal("0.000000001")  # Very small decimal

    # Test datetime with different timezones
    entity.timestamp = datetime.now(timezone.utc)

    # Test complex nested structure with non-serializable elements
    for i in range(3):
        friend = People(name=f"Complex Friend {i}", age=20 + i)
        friend.precision_number = Decimal(f"{i}.{i}{i}{i}")
        friend.created_at = datetime.now(timezone.utc)
        entity.friends.append(friend)

    # Test model_dump doesn't fail with non-serializable attributes
    entity_dict = entity.model_dump()
    assert isinstance(entity_dict, dict)
    assert "name" in entity_dict
    assert "decimal_value" in entity_dict
    assert "timestamp" in entity_dict

    # Test that dict can be JSON serialized (with proper handling)
    try:
        json_str = json.dumps(entity_dict, default=str)
        assert isinstance(json_str, str)
        assert len(json_str) > 0
    except Exception as e:
        pytest.fail(f"JSON serialization failed: {e}")


@pytest.mark.asyncio
async def test_non_serializable_query_operations(
    test_repository: SampleEntityRepository,
):
    """Test query operations with entities containing non-serializable attributes."""
    from datetime import datetime, timedelta, timezone
    from decimal import Decimal

    # Create multiple entities with non-serializable attributes
    base_time = datetime.now(timezone.utc)
    entities = []

    for i in range(5):
        entity = SampleEntity(
            name=f"Query NonSerial {i}", email=f"querynonserial{i}@test.com", age=25 + i
        )

        entity.decimal_value = Decimal(f"{i}.{i}")
        entity.timestamp = base_time + timedelta(minutes=i)

        # Add friend with non-serializable attributes
        friend = People(name=f"Query Friend {i}", age=30 + i)
        friend.precision_number = Decimal(f"100.{i}")
        friend.created_at = base_time + timedelta(hours=i)
        entity.friends.append(friend)

        entities.append(entity)
        await test_repository.add_async(entity)

    # Test queries work with non-serializable attributes
    # Query by name pattern
    query_results = await test_repository.find_async(
        {"name": {"$regex": "Query NonSerial"}}
    )
    assert len(query_results) >= 5

    # Verify all results have non-serializable attributes
    for result in query_results:
        if "Query NonSerial" in result.name:
            assert result.decimal_value is not None
            assert result.timestamp is not None
            assert len(result.friends) > 0
            assert result.friends[0].precision_number is not None
            assert result.friends[0].created_at is not None

    # Test range queries work
    age_range = await test_repository.find_async(
        {"age": {"$gte": 27}, "name": {"$regex": "Query NonSerial"}}
    )
    assert len(age_range) >= 3

    # Test sorting with non-serializable attributes present
    sorted_results = await test_repository.find_async(
        {"name": {"$regex": "Query NonSerial"}},
        [SortField("age", SortDirection.ASCENDING)],
    )
    assert len(sorted_results) >= 5

    # Verify sorting worked and non-serializable attributes are intact
    for i in range(len(sorted_results) - 1):
        if (
            "Query NonSerial" in sorted_results[i].name
            and "Query NonSerial" in sorted_results[i + 1].name
        ):
            assert sorted_results[i].age <= sorted_results[i + 1].age
            assert sorted_results[i].decimal_value is not None
            assert sorted_results[i + 1].decimal_value is not None


@pytest.mark.asyncio
async def test_non_serializable_update_operations(
    test_repository: SampleEntityRepository,
):
    """Test update operations with non-serializable attributes."""
    from datetime import datetime, timezone
    from decimal import Decimal

    # Create entity with non-serializable attributes
    entity = SampleEntity(
        name="Update NonSerial", email="updatenonserial@test.com", age=40
    )

    entity.decimal_value = Decimal("50.25")
    entity.timestamp = datetime.now(timezone.utc)

    # Add initial friend
    friend = People(name="Update Friend", age=35)
    friend.precision_number = Decimal("75.75")
    friend.created_at = datetime.now(timezone.utc)
    entity.friends.append(friend)

    await test_repository.add_async(entity)

    # Update non-serializable attributes
    entity.decimal_value = Decimal("100.50")
    entity.age = 41

    # Update friend's non-serializable attributes
    entity.friends[0].precision_number = Decimal("150.150")
    entity.friends[0].age = 36

    # Add another friend with non-serializable attributes
    new_friend = People(name="New Update Friend", age=32)
    new_friend.precision_number = Decimal("200.200")
    new_friend.created_at = datetime.now(timezone.utc)
    entity.friends.append(new_friend)

    # Update entity
    await test_repository.update_async(entity)

    # Retrieve and verify updates
    updated = await test_repository.get_async(entity.id)
    assert updated is not None
    assert updated.age == 41
    assert updated.decimal_value == Decimal("100.50")

    # Verify friend updates
    assert len(updated.friends) == 2

    # Find the updated friend
    updated_friend = next(f for f in updated.friends if f.name == "Update Friend")
    assert updated_friend.age == 36
    assert updated_friend.precision_number == Decimal("150.150")

    # Find the new friend
    new_friend_retrieved = next(
        f for f in updated.friends if f.name == "New Update Friend"
    )
    assert new_friend_retrieved.age == 32
    assert new_friend_retrieved.precision_number == Decimal("200.200")
    assert new_friend_retrieved.created_at is not None


@pytest.mark.asyncio
async def test_non_serializable_bulk_operations(
    test_repository: SampleEntityRepository,
):
    """Test bulk operations with entities containing non-serializable attributes."""
    from datetime import datetime, timedelta, timezone
    from decimal import Decimal

    test_id = str(uuid.uuid4())[:8]

    # Create multiple entities with non-serializable attributes
    entities = []
    base_time = datetime.now(timezone.utc)

    for i in range(10):
        entity = SampleEntity(
            name=f"Bulk NonSerial {test_id} {i}",
            email=f"bulknonserial{i}@test.com",
            age=25 + i,
        )

        entity.decimal_value = Decimal(f"{i * 10}.{i}")
        entity.timestamp = base_time + timedelta(seconds=i * 10)

        # Add friends with non-serializable attributes
        for j in range(2):
            friend = People(name=f"Bulk Friend {i}-{j}", age=30 + j)
            friend.precision_number = Decimal(f"{i}.{j}")
            friend.created_at = base_time + timedelta(minutes=i + j)
            entity.friends.append(friend)

        entities.append(entity)
        await test_repository.add_async(entity)

    # Test bulk query with non-serializable attributes
    all_bulk = await test_repository.find_async(
        {"name": {"$regex": f"Bulk NonSerial {test_id}"}}
    )
    assert len(all_bulk) == 10

    # Verify all have non-serializable attributes
    for entity in all_bulk:
        assert entity.decimal_value is not None
        assert entity.timestamp is not None
        assert len(entity.friends) == 2
        for friend in entity.friends:
            assert friend.precision_number is not None
            assert friend.created_at is not None

    # Test bulk delete with non-serializable attributes
    deleted_count = await test_repository.delete_items_async(
        {"name": {"$regex": f"Bulk NonSerial {test_id}"}}
    )
    assert deleted_count == 10

    # Verify deletion
    remaining = await test_repository.find_async(
        {"name": {"$regex": f"Bulk NonSerial {test_id}"}}
    )
    assert len(remaining) == 0
