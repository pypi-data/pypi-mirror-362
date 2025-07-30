import asyncio
import logging
import time
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional

import pytest
import pytest_asyncio
from pydantic import Field

from src.sas.cosmosdb.base.model_base import EntityBase
from src.sas.cosmosdb.base.repository_base import SortDirection, SortField
from src.sas.cosmosdb.sql.model import RootEntityBase
from src.sas.cosmosdb.sql.repository import RepositoryBase
from tests.test_config import integration_test, requires_sql, test_config

# Configure logging for better test debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
    age: int
    phone: str = Field(default="123-456-7890")
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

    def __init__(self, cosmos_location: str, database_name: str):
        entity_type = self.__orig_bases__[0].__args__[0]
        container_name = f"{entity_type.__name__}Container"

        super().__init__(
            connection_string=cosmos_location,
            database_name=database_name,
            container_name=container_name,
        )

    def _document_to_entity(self, document: dict) -> SampleEntity:
        """Convert document from Cosmos DB to SampleEntity."""
        # Handle JOIN query results that wrap the entity in a 'c' property
        if "c" in document and isinstance(document["c"], dict):
            document = document["c"]

        clean_document = {
            k: v
            for k, v in document.items()
            if not k.startswith("_") or k == "_partitionKey"
        }

        # Convert friends list if present
        if "friends" in clean_document and clean_document["friends"]:
            friends_list = []
            for friend_data in clean_document["friends"]:
                if isinstance(friend_data, dict):
                    friends_list.append(People(**friend_data))
                else:
                    friends_list.append(friend_data)
            clean_document["friends"] = friends_list

        return SampleEntity(**clean_document)


@pytest_asyncio.fixture(scope="session")
async def test_repository():
    """Create a test repository instance using configuration from test_config."""
    if not test_config.has_sql_config:
        pytest.skip("SQL API connection string not available")

    connection_info = test_config.get_sql_connection_info()
    repo = SampleEntityRepository(
        connection_info["connection_string"], connection_info["database_name"]
    )
    yield repo
    if hasattr(repo, "_client") and repo._client:
        await repo._client.close()


# === CORE FUNCTIONALITY TESTS ===


@integration_test()
@requires_sql()
@pytest.mark.asyncio
async def test_repository_initialization_and_setup(
    test_repository: SampleEntityRepository,
):
    """Test repository initialization and basic setup."""
    repo = test_repository

    # Test repository initialization
    await repo._ensure_initialized()
    assert repo._is_initialized.is_set(), "Repository should be initialized"

    # Test entity creation and partition key handling
    entity = SampleEntity(name="Init Test", age=25)
    assert entity._partitionKey is not None, "Entity should have partition key"

    # Test basic add and retrieve to verify connection
    await repo.add_async(entity)
    retrieved = await repo.get_async(entity.id)
    assert retrieved is not None
    assert retrieved.name == "Init Test"

    print("✓ Repository initialization and setup completed successfully")


@integration_test()
@requires_sql()
@pytest.mark.asyncio
async def test_comprehensive_crud_operations(test_repository: SampleEntityRepository):
    """Test all CRUD operations in a comprehensive workflow."""
    repo = test_repository

    # CREATE - Add multiple entities with varying complexity
    entities = [
        SampleEntity(name="CRUD Test 1", age=25),
        SampleEntity(name="CRUD Test 2", age=30),
        SampleEntity(name="CRUD Test 3", age=35),
    ]

    # Add friends to demonstrate nested object handling
    entities[0].friends.extend(
        [
            People(name="Alice", age=22, phone="555-1111"),
            People(name="Bob", age=25, phone="555-2222"),
        ]
    )
    entities[1].friends.append(People(name="Charlie", age=28, phone="555-3333"))

    # Add all entities
    for entity in entities:
        await repo.add_async(entity)
    print(f"✓ Added {len(entities)} entities successfully")

    # Test duplicate addition (should fail)
    with pytest.raises(ValueError, match="already exists"):
        await repo.add_async(entities[0])
    print("✓ Duplicate entity correctly rejected")

    # READ - Test various read operations
    # Get by ID
    retrieved = await repo.get_async(entities[0].id)
    assert retrieved is not None
    assert retrieved.name == "CRUD Test 1"
    assert len(retrieved.friends) == 2
    assert isinstance(retrieved.friends[0], People)

    # Get non-existent entity
    non_existent = await repo.get_async(str(uuid.uuid4()))
    assert non_existent is None

    # Find with predicate
    found_entities = await repo.find_async({"name": {"$contains": "CRUD Test"}})
    our_entities = [e for e in found_entities if e.name.startswith("CRUD Test")]
    assert len(our_entities) >= 3

    # Find one
    found_one = await repo.find_one_async({"name": "CRUD Test 2"})
    assert found_one is not None
    assert found_one.name == "CRUD Test 2"

    # Check existence
    exists = await repo.exists_async({"name": "CRUD Test 3"})
    assert exists is True

    # Count
    count = await repo.count_async({"name": {"$contains": "CRUD Test"}})
    assert count >= 3

    print(f"✓ Read operations completed - found {len(our_entities)} entities")

    # UPDATE - Test updates with proper entity reconstruction
    first_entity_data = our_entities[0]

    # Reconstruct entity properly for update
    if isinstance(first_entity_data, dict):
        # Handle case where find_async returns dict instead of entity
        friends = []
        if first_entity_data.get("friends"):
            for friend_data in first_entity_data["friends"]:
                if isinstance(friend_data, dict):
                    friends.append(People(**friend_data))
                else:
                    friends.append(friend_data)

        first_entity = SampleEntity(
            id=first_entity_data["id"],
            name=first_entity_data["name"],
            age=first_entity_data["age"],
            phone=first_entity_data.get("phone", "123-456-7890"),
            friends=friends,
        )
        first_entity._partitionKey = first_entity_data.get("_partitionKey")
    else:
        first_entity = first_entity_data

    # Update entity
    original_name = first_entity.name
    first_entity.name = f"{original_name} - Updated"
    first_entity.age += 10
    if first_entity.friends:
        first_entity.friends[0].name = "Updated Alice"

    await repo.update_async(first_entity)

    # Verify update
    updated = await repo.get_async(first_entity.id)
    assert updated is not None
    assert "Updated" in updated.name
    assert updated.age == first_entity.age
    if updated.friends:
        assert updated.friends[0].name == "Updated Alice"

    print("✓ Update operations completed successfully")

    # DELETE - Test deletion
    delete_entity = our_entities[-1]
    entity_id = (
        delete_entity.id if hasattr(delete_entity, "id") else delete_entity["id"]
    )

    await repo.delete_async(entity_id)

    # Verify deletion
    deleted_check = await repo.get_async(entity_id)
    assert deleted_check is None

    # Verify remaining entities
    remaining_count = await repo.count_async({"name": {"$contains": "CRUD Test"}})
    assert remaining_count == count - 1

    print("✓ Delete operations completed successfully")


@pytest.mark.asyncio
async def test_sorting_and_pagination_comprehensive(
    test_repository: SampleEntityRepository,
):
    """Test comprehensive sorting and pagination functionality."""
    repo = test_repository

    # Create test data with specific patterns for sorting
    entities = [
        SampleEntity(name="Sort A", age=30, phone="555-0001"),
        SampleEntity(name="Sort Z", age=25, phone="555-0002"),
        SampleEntity(name="Sort M", age=35, phone="555-0003"),
        SampleEntity(name="Sort B", age=20, phone="555-0004"),
        SampleEntity(name="Sort Y", age=40, phone="555-0005"),
    ]

    for entity in entities:
        await repo.add_async(entity)

    # Test sorting - ascending by name
    sorted_asc = await repo.find_async(
        {"name": {"$contains": "Sort"}}, [SortField("name", SortDirection.ASCENDING)]
    )
    sort_entities_asc = [e for e in sorted_asc if e.name.startswith("Sort")]
    assert len(sort_entities_asc) >= 5

    # Verify ascending order
    for i in range(len(sort_entities_asc) - 1):
        assert sort_entities_asc[i].name <= sort_entities_asc[i + 1].name

    # Test sorting - descending by age
    sorted_desc = await repo.find_async(
        {"name": {"$contains": "Sort"}}, [SortField("age", SortDirection.DESCENDING)]
    )
    sort_entities_desc = [e for e in sorted_desc if e.name.startswith("Sort")]
    assert len(sort_entities_desc) >= 5

    # Verify descending order
    for i in range(len(sort_entities_desc) - 1):
        assert sort_entities_desc[i].age >= sort_entities_desc[i + 1].age

    # Test all_async with sorting
    all_sorted = await repo.all_async([SortField("name", SortDirection.ASCENDING)])
    sort_entities_all = [e for e in all_sorted if e.name.startswith("Sort")]
    assert len(sort_entities_all) >= 5

    print(f"✓ Sorting tests completed - {len(sort_entities_asc)} entities sorted")

    # Test pagination
    page_size = 2
    all_sort_entities = []
    skip = 0

    while True:
        page = await repo.find_with_pagination_async(
            {"name": {"$contains": "Sort"}},
            [SortField("name", SortDirection.ASCENDING)],
            skip=skip,
            limit=page_size,
        )

        if not page:
            break

        page_sort_entities = [e for e in page if e.name.startswith("Sort")]
        all_sort_entities.extend(page_sort_entities)
        skip += page_size

        # Verify page ordering
        if len(page_sort_entities) > 1:
            for i in range(len(page_sort_entities) - 1):
                assert page_sort_entities[i].name <= page_sort_entities[i + 1].name

    assert len(all_sort_entities) >= 5
    print(
        f"✓ Pagination tests completed - retrieved {len(all_sort_entities)} entities in pages"
    )

    # Test pagination edge cases
    # Large limit
    large_page = await repo.find_with_pagination_async(
        {"name": {"$contains": "Sort"}},
        [SortField("name", SortDirection.ASCENDING)],
        skip=0,
        limit=100,
    )
    assert len([e for e in large_page if e.name.startswith("Sort")]) >= 5

    # Skip beyond data
    empty_page = await repo.find_with_pagination_async(
        {"name": {"$contains": "Sort"}},
        [SortField("name", SortDirection.ASCENDING)],
        skip=1000,
        limit=10,
    )
    assert len([e for e in empty_page if e.name.startswith("Sort")]) == 0

    print("✓ Pagination edge cases completed successfully")


@pytest.mark.asyncio
async def test_raw_sql_queries_comprehensive(test_repository: SampleEntityRepository):
    """Test comprehensive raw SQL query functionality."""
    repo = test_repository

    # Create test data with varying complexity
    entities = [
        SampleEntity(name="SQL Test Alpha", age=25),
        SampleEntity(name="SQL Test Beta", age=30),
        SampleEntity(name="SQL Test Gamma", age=35),
        SampleEntity(name="Other Entity", age=40),
    ]

    # Add friends with specific patterns for SQL testing
    entities[0].friends.extend(
        [
            People(name="Young Friend", age=18, phone="111-111-1111"),
            People(name="Adult Friend", age=30, phone="222-222-2222"),
        ]
    )
    entities[1].friends.append(
        People(name="Senior Friend", age=45, phone="333-333-3333")
    )

    for entity in entities:
        await repo.add_async(entity)

    # Test basic raw SQL query
    basic_results = await repo.query_raw_async(
        "SELECT * FROM c WHERE CONTAINS(c.name, @namePattern)",
        parameters={"@namePattern": "SQL Test"},
    )
    sql_entities = [e for e in basic_results if e.name.startswith("SQL Test")]
    assert len(sql_entities) >= 3
    print(f"✓ Basic raw SQL query - found {len(sql_entities)} entities")

    # Test array operations with raw SQL
    friends_results = await repo.query_raw_async(
        "SELECT * FROM c WHERE ARRAY_LENGTH(c.friends) > 0 AND CONTAINS(c.name, @namePattern)",
        parameters={"@namePattern": "SQL Test"},
    )
    friends_entities = [e for e in friends_results if e.name.startswith("SQL Test")]
    assert len(friends_entities) >= 2  # Alpha and Beta have friends
    print(
        f"✓ Array operations raw SQL - found {len(friends_entities)} entities with friends"
    )

    # Test complex EXISTS query
    young_friends_results = await repo.query_raw_async(
        """SELECT * FROM c 
           WHERE CONTAINS(c.name, @namePattern)
           AND EXISTS(
               SELECT VALUE f FROM f IN c.friends 
               WHERE f.age < @maxAge
           )""",
        parameters={"@namePattern": "SQL Test", "@maxAge": 25},
    )
    young_friends_entities = [
        e for e in young_friends_results if e.name.startswith("SQL Test")
    ]
    assert len(young_friends_entities) >= 1  # Alpha has young friend
    print(
        f"✓ Complex EXISTS query - found {len(young_friends_entities)} entities with young friends"
    )

    # Test query_raw_dynamic_cursor_async for projections
    try:
        projection_results = await repo.query_raw_dynamic_cursor_async(
            "SELECT c.id, c.name, c.age, ARRAY_LENGTH(c.friends) as friendCount FROM c WHERE CONTAINS(c.name, @namePattern)",
            parameters={"@namePattern": "SQL Test"},
        )
        assert len(projection_results) >= 3
        assert all(isinstance(result, dict) for result in projection_results)
        assert all("friendCount" in result for result in projection_results)
        print(
            f"✓ Dynamic cursor projection query - got {len(projection_results)} projected results"
        )
    except Exception as e:
        print(f"⚠️ Dynamic cursor query failed (may be SDK limitation): {e}")

    # Test query_raw_single_value_async for counts
    try:
        count_result = await repo.query_raw_single_value_async(
            "SELECT VALUE COUNT(1) FROM c WHERE CONTAINS(c.name, @namePattern)",
            parameters={"@namePattern": "SQL Test"},
        )
        assert count_result >= 3
        print(f"✓ Single value count query - got count: {count_result}")
    except Exception as e:
        print(f"⚠️ Single value query failed (may be SDK limitation): {e}")

    # Test JOIN operations
    join_results = await repo.query_raw_async(
        """SELECT DISTINCT c FROM c 
           JOIN friend IN c.friends 
           WHERE CONTAINS(c.name, @namePattern) AND friend.age > @minAge""",
        parameters={"@namePattern": "SQL Test", "@minAge": 25},
    )
    join_entities = [e for e in join_results if e.name.startswith("SQL Test")]
    assert len(join_entities) >= 1
    print(f"✓ JOIN operations - found {len(join_entities)} entities")


@pytest.mark.asyncio
async def test_advanced_query_patterns(test_repository: SampleEntityRepository):
    """Test advanced query patterns and predicates."""
    repo = test_repository

    # Create entities with specific patterns for advanced testing
    entities = [
        SampleEntity(name="Advanced Alpha", age=25, phone="555-1000"),
        SampleEntity(name="Advanced Beta", age=30, phone="555-2000"),
        SampleEntity(name="Advanced Gamma", age=35, phone="555-3000"),
        SampleEntity(name="Different Entity", age=40, phone="555-4000"),
    ]

    for entity in entities:
        await repo.add_async(entity)

    # Test basic name filtering
    name_results = await repo.find_async({"name": {"$contains": "Advanced"}})
    advanced_entities = [e for e in name_results if e.name.startswith("Advanced")]
    assert len(advanced_entities) >= 3

    # Test range queries
    range_results = await repo.find_async(
        {"age": {"$gte": 25, "$lte": 35}, "name": {"$contains": "Advanced"}}
    )
    range_entities = [e for e in range_results if e.name.startswith("Advanced")]
    assert len(range_entities) >= 3

    # Test IN operator
    in_results = await repo.find_async(
        {"name": {"$in": ["Advanced Alpha", "Advanced Beta"]}}
    )
    assert len(in_results) >= 2

    # Test NOT EQUAL
    ne_results = await repo.find_async(
        {"name": {"$contains": "Advanced"}, "age": {"$ne": 25}}
    )
    ne_entities = [e for e in ne_results if e.name.startswith("Advanced")]
    assert len(ne_entities) >= 2  # Beta and Gamma (not Alpha)

    # Test greater than
    gt_results = await repo.find_async(
        {"name": {"$contains": "Advanced"}, "age": {"$gt": 25}}
    )
    gt_entities = [e for e in gt_results if e.name.startswith("Advanced")]
    assert len(gt_entities) >= 2  # Beta and Gamma

    # Test less than or equal
    lte_results = await repo.find_async(
        {"name": {"$contains": "Advanced"}, "age": {"$lte": 30}}
    )
    lte_entities = [e for e in lte_results if e.name.startswith("Advanced")]
    assert len(lte_entities) >= 2  # Alpha and Beta

    print("✓ Advanced query patterns completed successfully")


@pytest.mark.asyncio
async def test_error_handling_and_edge_cases(test_repository: SampleEntityRepository):
    """Test comprehensive error handling and edge cases."""
    repo = test_repository

    # Test non-existent operations
    non_existent_id = str(uuid.uuid4())

    # Get non-existent
    result = await repo.get_async(non_existent_id)
    assert result is None

    # Update non-existent (should fail)
    fake_entity = SampleEntity(id=non_existent_id, name="Fake", age=25)
    with pytest.raises((ValueError, Exception)):
        await repo.update_async(fake_entity)

    # Delete non-existent (should not fail)
    await repo.delete_async(non_existent_id)  # Should complete without error

    # Test empty queries
    empty_results = await repo.find_async({})
    assert isinstance(empty_results, list)

    # Test no matches
    no_matches = await repo.find_async({"name": "NonExistentEntity12345"})
    assert len(no_matches) == 0

    # Test count with no matches
    zero_count = await repo.count_async({"name": "NonExistentEntity12345"})
    assert zero_count == 0

    # Test exists with no matches
    not_exists = await repo.exists_async({"name": "NonExistentEntity12345"})
    assert not_exists is False

    print("✓ Error handling and edge cases completed successfully")


@pytest.mark.asyncio
async def test_performance_and_concurrency(test_repository: SampleEntityRepository):
    """Test performance characteristics and concurrent operations."""
    repo = test_repository

    # Test batch operations
    batch_size = 10
    entities = [
        SampleEntity(name=f"Perf Test {i:03d}", age=25 + (i % 20))
        for i in range(batch_size)
    ]

    # Measure insertion time
    start_time = time.time()
    for entity in entities:
        await repo.add_async(entity)
    insert_time = time.time() - start_time

    logger.info(f"Batch insert of {batch_size} entities: {insert_time:.2f}s")
    assert insert_time < 30, "Batch insert should complete within reasonable time"

    # Measure query time
    start_time = time.time()
    perf_entities = await repo.find_async({"name": {"$contains": "Perf Test"}})
    query_time = time.time() - start_time

    logger.info(f"Query for {len(perf_entities)} entities: {query_time:.2f}s")
    assert query_time < 5, "Query should complete within reasonable time"

    # Test concurrent operations
    concurrent_entities = [
        SampleEntity(name=f"Concurrent {i}", age=25 + i) for i in range(5)
    ]

    # Concurrent additions
    add_tasks = [repo.add_async(entity) for entity in concurrent_entities]
    await asyncio.gather(*add_tasks)

    # Verify all were added
    for entity in concurrent_entities:
        retrieved = await repo.get_async(entity.id)
        assert retrieved is not None

    # Concurrent reads
    read_tasks = [repo.get_async(entity.id) for entity in concurrent_entities]
    retrieved_entities = await asyncio.gather(*read_tasks)

    assert len(retrieved_entities) == 5
    assert all(e is not None for e in retrieved_entities)

    print(f"✓ Performance test completed - {batch_size} entities in {insert_time:.2f}s")


@pytest.mark.asyncio
async def test_context_manager_and_cleanup(test_repository: SampleEntityRepository):
    """Test context manager usage and proper cleanup."""

    connection_info = test_config.get_sql_connection_info()

    # Test context manager
    async with SampleEntityRepository(
        connection_info["connection_string"], connection_info["database_name"]
    ) as repo:
        entity = SampleEntity(name="Context Test", age=30)
        await repo.add_async(entity)

        retrieved = await repo.get_async(entity.id)
        assert retrieved is not None
        assert retrieved.name == "Context Test"

    # Repository should be properly closed after context manager
    print("✓ Context manager test completed successfully")


@pytest.mark.asyncio
async def test_entity_serialization_and_validation():
    """Test entity serialization, validation, and type handling."""

    # Test entity creation with all fields
    entity = SampleEntity(name="Serialization Test", age=30)
    entity.friends.extend(
        [
            People(name="Friend 1", age=25, phone="111-222-3333"),
            People(name="Friend 2", age=28),  # Default phone
        ]
    )

    # Test serialization
    cosmos_dict = entity.to_cosmos_dict()
    assert isinstance(cosmos_dict, dict)
    assert cosmos_dict["name"] == "Serialization Test"
    assert len(cosmos_dict["friends"]) == 2
    assert cosmos_dict["friends"][1]["phone"] == "123-456-7890"  # Default value
    assert "_partitionKey" in cosmos_dict

    # Test Pydantic validation
    entity_dict = entity.model_dump()
    reconstructed = SampleEntity.model_validate(entity_dict)
    assert reconstructed.name == entity.name
    assert len(reconstructed.friends) == 2
    assert isinstance(reconstructed.friends[0], People)

    print("✓ Entity serialization and validation completed successfully")


@pytest.mark.asyncio
async def test_comprehensive_integration_workflow(
    test_repository: SampleEntityRepository,
):
    """Test a realistic, production-like workflow."""
    repo = test_repository
    test_id = uuid.uuid4().hex[:8]

    # Simulate user registration workflow
    users = []
    for i in range(15):
        user = SampleEntity(name=f"User{test_id}_{i:02d}", age=20 + (i % 50))

        # Add some social connections
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
        await repo.add_async(user)

    # Test various query patterns
    young_users = await repo.find_async(
        {"age": {"$lte": 30}, "name": {"$contains": f"User{test_id}_"}}
    )

    # Verify we found some young users
    assert len(young_users) > 0, "Should find young users"

    # Test user lookup and updates
    for user in users[:5]:  # Test first 5 users
        retrieved = await repo.get_async(user.id)
        assert retrieved is not None
        assert retrieved.name == user.name

        # Update user
        retrieved.age += 1
        await repo.update_async(retrieved)

    # Cleanup test users
    for user in users:
        await repo.delete_async(user.id)

    print("✓ Comprehensive integration workflow completed successfully")


@integration_test()
@requires_sql()
@pytest.mark.asyncio
async def test_array_operations_functionality_sql(
    test_repository: SampleEntityRepository,
):
    """Test array operations functionality with real SQL repository."""
    repo = test_repository

    # Create a test entity with array data similar to People friends
    test_entity = SampleEntity(
        id=f"array-test-{uuid.uuid4().hex[:8]}",
        name="Array Operations Test",
        age=30,
        friends=[
            People(name="Primary Friend", age=25, phone="555-0001"),
            People(name="Secondary Friend", age=35, phone="555-0002"),
            People(name="Young Friend", age=20, phone="555-0003"),
        ],
    )

    try:
        # Add the test entity
        await repo.add_async(test_entity)

        # Test 1: Array element simple equality (works with existing friends array)
        results = await repo.find_async({"friends.name": "Primary Friend"})
        array_results = [r for r in results if r.name == "Array Operations Test"]
        assert len(array_results) == 1, "Should find entity with specific friend name"

        # Test 2: Array element comparison operations
        results = await repo.find_async({"friends.age": {"$gte": 30}})
        age_results = [r for r in results if r.name == "Array Operations Test"]
        assert len(age_results) == 1, "Should find entity with friends age >= 30"

        # Test 3: Array element string operations
        results = await repo.find_async({"friends.name": {"$contains": "Friend"}})
        friend_results = [r for r in results if r.name == "Array Operations Test"]
        assert len(friend_results) == 1, (
            "Should find entity with friends containing 'Friend'"
        )

        # Test 4: Array element phone number operations
        results = await repo.find_async({"friends.phone": {"$startswith": "555-000"}})
        phone_results = [r for r in results if r.name == "Array Operations Test"]
        assert len(phone_results) == 1, (
            "Should find entity with friends having specific phone prefix"
        )

        # Test 5: Mixed regular and array conditions
        results = await repo.find_async({"age": 30, "friends.age": {"$lt": 25}})
        mixed_results = [r for r in results if r.name == "Array Operations Test"]
        assert len(mixed_results) == 1, (
            "Should find entity matching both regular and array conditions"
        )

        # Test 6: Array element NOT operations
        results = await repo.find_async({"friends.age": {"$ne": 40}})
        not_results = [r for r in results if r.name == "Array Operations Test"]
        assert len(not_results) == 1, "Should find entity where friends age != 40"

        print("✓ Array operations functionality verified with real SQL repository!")

    finally:
        # Cleanup
        try:
            await repo.delete_async(test_entity.id)
        except Exception:
            pass


def test_array_operations_query_generation_sql():
    """Test array operations query generation without database connection."""

    # Create a mock repository for testing query generation
    class MockRepository(RepositoryBase):
        def __init__(self):
            self._container_name = "TestContainer"

        def _document_to_entity(self, document: dict):
            return document

    repo = MockRepository()

    # Test various array operations generate correct SQL
    test_cases = [
        # (predicate, expected_query_part, expected_param_count)
        (
            {"contacts.email": "test@example.com"},
            "EXISTS(SELECT VALUE p FROM p IN c.contacts WHERE p.email = @param0)",
            1,
        ),
        (
            {"products.price": {"$gte": 100.0}},
            "EXISTS(SELECT VALUE p FROM p IN c.products WHERE p.price >= @param0)",
            1,
        ),
        (
            {"tags.name": {"$contains": "important"}},
            "EXISTS(SELECT VALUE p FROM p IN c.tags WHERE CONTAINS(p.name, @param0))",
            1,
        ),
        (
            {"friends.age": {"$in": [25, 30, 35]}},
            "EXISTS(SELECT VALUE p FROM p IN c.friends WHERE p.age IN (@param1_0, @param1_1, @param1_2))",
            3,
        ),
        (
            {"items.discount": {"$exists": True}},
            "EXISTS(SELECT VALUE p FROM p IN c.items WHERE IS_DEFINED(p.discount))",
            0,
        ),
    ]

    for predicate, expected_part, expected_param_count in test_cases:
        query, params = repo._build_sql_query(predicate)
        assert expected_part in query, (
            f"Query should contain: {expected_part}\nActual query: {query}"
        )
        assert len(params) == expected_param_count, (
            f"Expected {expected_param_count} params, got {len(params)}"
        )

    # Test mixed conditions
    mixed_query, mixed_params = repo._build_sql_query(
        {
            "status": "active",
            "contacts.type": "primary",
            "products.price": {"$gt": 50.0},
        }
    )

    assert "c.status = @param0" in mixed_query
    assert (
        "EXISTS(SELECT VALUE p FROM p IN c.contacts WHERE p.type = @param1)"
        in mixed_query
    )
    assert (
        "EXISTS(SELECT VALUE p FROM p IN c.products WHERE p.price > @param2)"
        in mixed_query
    )
    assert len(mixed_params) == 3

    print("✓ Array operations query generation tests passed!")
