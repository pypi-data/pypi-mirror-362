"""
Azure Cosmos DB SQL API Repository Implementation

This module provides a repository pattern implementation for Azure Cosmos DB SQL API,
supporting asynchronous operations, partition key handling, and type-safe CRUD operations.

Key Features:
- Async/await support for all operations
- Partition key handling for optimal performance
- Type-safe operations using generics
- Connection pooling and resource management
- Automatic container and indexing policy setup
- Comprehensive error handling with retries
- Query optimization and pagination support
- Cross-partition query support by omitting partition_key parameter
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional, TypeVar, get_args, get_origin

from azure.cosmos.aio import CosmosClient as AsyncCosmosClient
from azure.cosmos.exceptions import CosmosHttpResponseError, CosmosResourceNotFoundError
from azure.identity.aio import DefaultAzureCredential

from ..base.repository_base import RepositoryBase as Repository_Base
from ..base.repository_base import SortDirection, SortField
from .model import RootEntityBase

TEntity = TypeVar("TEntity", bound=RootEntityBase)
TKey = TypeVar("TKey", bound=str)

logger = logging.getLogger(__name__)


class RepositoryBase(Repository_Base[TEntity, TKey]):
    """
    Base repository class for Azure Cosmos DB SQL API operations.

    This class provides a generic interface for Cosmos DB containers, allowing
    type-safe CRUD operations on entities that inherit from RootEntityBase.

    Features:
    - Async/await support with proper resource management
    - Partition key optimization for performance
    - Automatic container creation and indexing
    - Connection pooling and retry logic
    - Type-safe entity conversion
    - Comprehensive error handling
    - Cross-partition queries when partition_key is None

    Examples:
        Basic usage with connection string:

        ```python
        from sas.cosmosdb.sql import RootEntityBase, RepositoryBase

        class Customer(RootEntityBase):
            name: str
            email: str
            age: int

        class CustomerRepository(RepositoryBase[Customer, str]):
            def __init__(self, connection_string: str):
                super().__init__(
                    connection_string=connection_string,
                    database_name="MyDatabase",
                    container_name="Customers"
                )

        # Usage
        async def main():
            repo = CustomerRepository("AccountEndpoint=https://...")
            await repo.initialize()

            # CRUD operations
            customer = Customer(id="123", name="John Doe", email="john@example.com", age=30)
            await repo.add_async(customer)

            found = await repo.get_async("123")
            customers = await repo.find_async({"age": {"$gte": 25}})

            await repo.close()
        ```

        Advanced usage with managed identity:

        ```python
        class ProductRepository(RepositoryBase[Product, str]):
            def __init__(self):
                super().__init__(
                    account_url="https://myaccount.documents.azure.com:443/",
                    database_name="ProductCatalog",
                    container_name="Products",
                    use_managed_identity=True,
                    throughput=1000  # Provisioned RU/s
                )

        # Usage in Azure environment
        async def azure_function_main():
            async with ProductRepository() as repo:
                # Managed identity authentication automatically handled
                products = await repo.find_async({"category": "electronics"})
                return products
        ```

        Serverless configuration:

        ```python
        # For serverless accounts, omit throughput parameter
        class OrderRepository(RepositoryBase[Order, str]):
            def __init__(self, connection_string: str):
                super().__init__(
                    connection_string=connection_string,
                    database_name="OrderDB",
                    container_name="Orders",
                    throughput=None  # Serverless mode
                )
        ```
    """

    def __init__(
        self,
        connection_string: Optional[str] = None,
        account_url: Optional[str] = None,
        database_name: str = None,
        container_name: str = None,
        partition_key_path: str = "/_partitionKey",
        throughput: Optional[int] = None,
        use_managed_identity: bool = True,
        max_retry_attempts: int = 5,
        max_retry_wait_time: int = 30,
    ):
        """
        Initialize the Cosmos DB SQL repository.

        Args:
            connection_string: Cosmos DB connection string (if not using managed identity)
            account_url: Cosmos DB account URL (required for managed identity)
            database_name: Name of the database
            container_name: Name of the container
            partition_key_path: Path to the partition key field (default: "/_partitionKey")
            throughput: Container throughput (RU/s) for provisioned accounts.
                       Leave as None for serverless accounts (default: None for serverless)
            use_managed_identity: Whether to use managed identity for authentication
            max_retry_attempts: Maximum retry attempts for operations
            max_retry_wait_time: Maximum wait time for retries

        Raises:
            ValueError: If required parameters are missing or invalid

        Examples:
            Connection string authentication:

            ```python
            repo = CustomerRepository(
                connection_string="AccountEndpoint=https://myaccount.documents.azure.com:443/;AccountKey=...",
                database_name="RetailDB",
                container_name="Customers"
            )
            ```

            Managed identity authentication (recommended for production):

            ```python
            repo = CustomerRepository(
                account_url="https://myaccount.documents.azure.com:443/",
                database_name="RetailDB",
                container_name="Customers",
                use_managed_identity=True
            )
            ```

            Provisioned throughput configuration:

            ```python
            repo = CustomerRepository(
                connection_string=conn_str,
                database_name="HighVolumeDB",
                container_name="Orders",
                throughput=4000,  # 4000 RU/s provisioned
                max_retry_attempts=10
            )
            ```

            Serverless configuration:

            ```python
            repo = CustomerRepository(
                connection_string=conn_str,
                database_name="ServerlessDB",
                container_name="Events",
                throughput=None  # Serverless mode
            )
            ```

            Custom partition key path:

            ```python
            repo = CustomerRepository(
                connection_string=conn_str,
                database_name="CustomDB",
                container_name="Items",
                partition_key_path="/customPartitionKey"
            )
            ```
        """

        # at least one of connection_string or account_url must be provided
        if not connection_string and not account_url:
            raise ValueError(
                "Either connection_string or account_url must be provided for Cosmos DB connection"
            )

        if not database_name or not container_name:
            raise ValueError("database_name and container_name are required")

        if container_name is None or container_name == "":
            entity_type = self.__orig_bases__[0].__args__[0]
            container_name = (
                f"{entity_type.__name__}Container"  # Results in "SampleEntityContainer"
            )

        self.database_name = database_name
        self.container_name = container_name
        self.partition_key_path = partition_key_path
        self.throughput = throughput
        self.use_managed_identity = True if account_url else False
        self.connection_string = connection_string
        self.account_url = account_url
        self.max_retry_attempts = max_retry_attempts
        self.max_retry_wait_time = max_retry_wait_time

        # Async initialization tracking
        self._is_initialized = asyncio.Event()
        self._initialization_lock = asyncio.Lock()

        # Client instances (will be initialized async)
        self._client: Optional[AsyncCosmosClient] = None
        self._database = None
        self._container = None

    async def _ensure_initialized(self):
        """Ensure the repository is initialized with proper connection and container setup."""
        if not self._is_initialized.is_set():
            async with self._initialization_lock:
                await self._initialize_client()
                self._client.logging_enable = True
                await self._ensure_database_and_container_exist()
                self._is_initialized.set()

    async def _initialize_client(self):
        """Initialize the async Cosmos DB client."""
        try:
            if self.use_managed_identity:
                # Use managed identity for authentication with simple configuration
                azure_credential = DefaultAzureCredential()
                self._client = AsyncCosmosClient(
                    url=self.account_url,
                    credential=azure_credential,
                    connection_retry_policy={
                        "retry_total": self.max_retry_attempts,
                        "retry_backoff_max": self.max_retry_wait_time,
                    },
                )
            else:
                # Use connection string
                self._client = AsyncCosmosClient.from_connection_string(
                    conn_str=self.connection_string,
                    connection_retry_policy={
                        "retry_total": self.max_retry_attempts,
                        "retry_backoff_max": self.max_retry_wait_time,
                    },
                )

            logger.info(
                f"Initialized Cosmos DB client for database: {self.database_name}"
            )
        except Exception as e:
            logger.error(f"Failed to initialize Cosmos DB client: {e}")
            raise

    async def _ensure_database_and_container_exist(self):
        """
        Ensure the database and container exist, with graceful handling of permission issues.

        This method attempts to create the database and container if they don't exist,
        but gracefully handles cases where the user only has data plane permissions.

        For production scenarios, it's recommended to pre-create databases and containers
        via Azure CLI, Portal, or Infrastructure as Code (Bicep/ARM templates).
        """
        try:
            # First, try to create database if not exists (this handles both cases)
            try:
                logger.info(f"Ensuring database '{self.database_name}' exists...")

                # Can't create a CosmosDB database using Python SDK 4.9.0
                # https://github.com/Azure/azure-sdk-for-python/issues/40120
                # We need to presume the database already exists at this moment.
                self._database = await self._client.create_database_if_not_exists(
                    id=self.database_name
                )

                logger.info(f"Database '{self.database_name}' is ready")
            except CosmosHttpResponseError as e:
                if e.status_code == 403:
                    # Permission denied for management operations - try to just get the database
                    logger.warning(
                        f"Cannot create database due to RBAC restrictions. Attempting to access existing database '{self.database_name}'..."
                    )
                    try:
                        self._database = self._client.get_database_client(
                            self.database_name
                        )
                        # Test if we can actually access it with a read operation
                        await self._database.read()
                        logger.info(
                            f"Successfully connected to existing database '{self.database_name}'"
                        )
                    except (
                        CosmosResourceNotFoundError,
                        CosmosHttpResponseError,
                    ) as read_error:
                        logger.error(
                            f"Cannot access database '{self.database_name}'. "
                            f"Database may not exist or you lack sufficient permissions."
                        )
                        # Provide helpful guidance for resolving the issue
                        if isinstance(read_error, CosmosResourceNotFoundError):
                            error_message = (
                                f"Database '{self.database_name}' does not exist. "
                                f"Please create it using one of these methods:\n"
                                f"1. Azure CLI: az cosmosdb sql database create --account-name <account> --resource-group <rg> --name {self.database_name}\n"
                                f"2. Azure Portal: Navigate to your Cosmos DB account and create the database\n"
                                f"3. Assign 'DocumentDB Account Contributor' role for programmatic creation"
                            )
                        else:
                            error_message = (
                                f"Cannot access database '{self.database_name}'. "
                                f"Please ensure you have the required RBAC permissions:\n"
                                f"1. For data operations: 'Cosmos DB Built-in Data Contributor' role\n"
                                f"2. For management operations: 'DocumentDB Account Contributor' role"
                            )
                        raise RuntimeError(error_message) from read_error
                else:
                    raise

            # Now handle container creation/access
            try:
                logger.info(f"Ensuring container '{self.container_name}' exists...")

                # Create container with proper partition key if it doesn't exist
                container_definition = {
                    "id": self.container_name,
                    "partitionKey": {
                        "paths": [self.partition_key_path],
                        "kind": "Hash",
                    },
                }

                # Add throughput if specified (for provisioned accounts)
                if self.throughput:
                    self._container = (
                        await self._database.create_container_if_not_exists(
                            id=container_definition["id"],
                            partition_key=container_definition["partitionKey"],
                            offer_throughput=self.throughput,
                        )
                    )
                else:
                    # For serverless accounts, don't specify throughput
                    self._container = (
                        await self._database.create_container_if_not_exists(
                            id=container_definition["id"],
                            partition_key=container_definition["partitionKey"],
                        )
                    )

                logger.info(f"Container '{self.container_name}' is ready")
            except CosmosHttpResponseError as e:
                if e.status_code == 403:
                    # Permission denied for management operations - try to just get the container
                    logger.warning(
                        f"Cannot create container due to RBAC restrictions. Attempting to access existing container '{self.container_name}'..."
                    )
                    try:
                        self._container = self._database.get_container_client(
                            self.container_name
                        )
                        # Test if we can actually access it with a read operation
                        await self._container.read()
                        logger.info(
                            f"Successfully connected to existing container '{self.container_name}'"
                        )
                    except (
                        CosmosResourceNotFoundError,
                        CosmosHttpResponseError,
                    ) as read_error:
                        logger.error(
                            f"Cannot access container '{self.container_name}'. "
                            f"Container may not exist or you lack sufficient permissions."
                        )
                        # Provide helpful guidance for resolving the issue
                        if isinstance(read_error, CosmosResourceNotFoundError):
                            error_message = (
                                f"Container '{self.container_name}' does not exist in database '{self.database_name}'. "
                                f"Please create it using one of these methods:\n"
                                f"1. Azure CLI: az cosmosdb sql container create --account-name <account> --resource-group <rg> --database-name {self.database_name} --name {self.container_name} --partition-key-path {self.partition_key_path}\n"
                                f"2. Azure Portal: Navigate to your database and create the container\n"
                                f"3. Assign 'DocumentDB Account Contributor' role for programmatic creation"
                            )
                        else:
                            error_message = (
                                f"Cannot access container '{self.container_name}' in database '{self.database_name}'. "
                                f"Please ensure you have the required RBAC permissions:\n"
                                f"1. For data operations: 'Cosmos DB Built-in Data Contributor' role\n"
                                f"2. For management operations: 'DocumentDB Account Contributor' role\n"
                                f"3. Or ensure the container exists and you have data access permissions"
                            )
                        raise RuntimeError(error_message) from read_error
                else:
                    raise

        except CosmosHttpResponseError as e:
            if e.status_code == 403:
                # General permission error
                logger.error(
                    f"RBAC Permission Error: {e.message}. "
                    f"Please ensure you have the appropriate roles assigned."
                )
                raise RuntimeError(
                    f"Insufficient RBAC permissions for Cosmos DB operations.\n"
                    f"Required roles:\n"
                    f"1. For data operations: 'Cosmos DB Built-in Data Contributor'\n"
                    f"2. For management operations: 'DocumentDB Account Contributor'\n"
                    f"Current error: {e.message}"
                ) from e
            else:
                logger.error(f"Failed to initialize database and container: {e}")
                raise
        except Exception as e:
            logger.error(
                f"Unexpected error during database/container initialization: {e}"
            )
            raise

    async def _execute_with_retry(self, operation, *args, **kwargs):
        """Execute an operation with retry logic for transient failures."""
        for attempt in range(self.max_retry_attempts):
            try:
                return await operation(*args, **kwargs)
            except CosmosHttpResponseError as e:
                if attempt == self.max_retry_attempts - 1:
                    raise

                # Check if error is retryable (rate limiting, timeouts, etc.)
                if e.status_code in [
                    429,
                    503,
                    408,
                ]:  # Too Many Requests, Service Unavailable, Timeout
                    wait_time = min(2**attempt, self.max_retry_wait_time)
                    logger.warning(
                        f"Retrying operation after {wait_time}s (attempt {attempt + 1}/{self.max_retry_attempts}): {e}"
                    )
                    await asyncio.sleep(wait_time)
                else:
                    raise
            except Exception as e:
                logger.error(f"Unexpected error in operation: {e}")
                raise

    def _build_sql_query(
        self,
        predicate: Dict[str, Any],
        sort_fields: Optional[List[SortField]] = None,
        select_clause: str = "SELECT *",
    ) -> tuple[str, Dict[str, Any]]:
        """
        Build a SQL query from predicate conditions with customizable SELECT clause.

        This is a unified query builder that handles all query types.
        For complex array operations, use query_raw_async instead.

        Args:
            predicate: Query conditions as key-value pairs
            sort_fields: Optional sorting fields
            select_clause: The SELECT clause (default: "SELECT *")
                          Examples:
                          - "SELECT *" (default for find operations)
                          - "SELECT c.id, c._partitionKey" (for delete operations)
                          - "SELECT VALUE COUNT(1)" (for count operations)

        Returns:
            Tuple of (query_string, parameters)

        Examples:
            Basic equality queries:

            ```python
            # Simple field equality
            query, params = self._build_sql_query({"status": "active"})
            # Result: "SELECT * FROM c WHERE c.status = @param0"
            # Params: {"@param0": "active"}

            # Multiple conditions (implicit AND)
            query, params = self._build_sql_query({
                "status": "active",
                "age": {"$gte": 18}
            })
            # Result: "SELECT * FROM c WHERE c.status = @param0 AND c.age >= @param1"
            ```

            Range and comparison queries:

            ```python
            # Age range
            query, params = self._build_sql_query({
                "age": {"$gte": 18, "$lt": 65}
            })
            # Result: "SELECT * FROM c WHERE c.age >= @param0 AND c.age < @param1"

            # Date comparison
            query, params = self._build_sql_query({
                "createdDate": {"$gt": "2024-01-01"}
            })
            ```

            List operations:

            ```python
            # IN operation
            query, params = self._build_sql_query({
                "city": {"$in": ["Seattle", "Portland", "Vancouver"]}
            })
            # Result: "SELECT * FROM c WHERE c.city IN (@param0_0, @param0_1, @param0_2)"

            # NOT IN operation
            query, params = self._build_sql_query({
                "status": {"$nin": ["deleted", "banned"]}
            })
            ```

            Text operations:

            ```python
            # Contains text
            query, params = self._build_sql_query({
                "description": {"$contains": "urgent"}
            })
            # Result: "SELECT * FROM c WHERE CONTAINS(c.description, @param0)"

            # String prefix
            query, params = self._build_sql_query({
                "username": {"$startswith": "admin_"}
            })
            # Result: "SELECT * FROM c WHERE STARTSWITH(c.username, @param0)"

            # String suffix
            query, params = self._build_sql_query({
                "email": {"$endswith": "@company.com"}
            })
            ```

            Logical operations:

            ```python
            # AND conditions
            query, params = self._build_sql_query({
                "$and": [
                    {"status": "active"},
                    {"age": {"$gte": 18}},
                    {"balance": {"$gt": 0}}
                ]
            })

            # OR conditions
            query, params = self._build_sql_query({
                "$or": [
                    {"tier": "premium"},
                    {"balance": {"$gte": 10000}}
                ]
            })
            ```

            Field existence:

            ```python
            # Field exists
            query, params = self._build_sql_query({
                "verifiedDate": {"$exists": True}
            })
            # Result: "SELECT * FROM c WHERE IS_DEFINED(c.verifiedDate)"

            # Field doesn't exist
            query, params = self._build_sql_query({
                "tempField": {"$exists": False}
            })
            # Result: "SELECT * FROM c WHERE NOT IS_DEFINED(c.tempField)"
            ```

            Array and nested field operations:

            ```python
            # Array field access with dot notation (generates EXISTS subquery)
            query, params = self._build_sql_query({
                "children.grade": {"$gte": 5}  # children: list[Child]
            })
            # Result: "SELECT * FROM c WHERE EXISTS(
            #   SELECT VALUE p FROM p IN c.children WHERE p.grade >= @param0
            # )"

            # Single object field access with dot notation (direct access)
            query, params = self._build_sql_query({
                "address.city": "Seattle"  # address: Address
            })
            # Result: "SELECT * FROM c WHERE c.address.city = @param0"

            # Array element containment with dot notation
            query, params = self._build_sql_query({
                "friends.name": {"$contains": "John"}  # friends: list[Friend]
            })
            # Result: "SELECT * FROM c WHERE EXISTS(
            #   SELECT VALUE p FROM p IN c.friends WHERE CONTAINS(p.name, @param0)
            # )"

            # Single object text operations
            query, params = self._build_sql_query({
                "profile.bio": {"$startswith": "Software"}  # profile: UserProfile
            })
            # Result: "SELECT * FROM c WHERE STARTSWITH(c.profile.bio, @param0)"

            # Array element comparisons
            query, params = self._build_sql_query({
                "scores.value": {"$gte": 90}  # scores: list[Score]
            })
            # Result: "SELECT * FROM c WHERE EXISTS(
            #   SELECT VALUE p FROM p IN c.scores WHERE p.value >= @param0
            # )"

            # Array element IN operations
            query, params = self._build_sql_query({
                "tags.category": {"$in": ["urgent", "important"]}  # tags: list[Tag]
            })
            # Result: "SELECT * FROM c WHERE EXISTS(
            #   SELECT VALUE p FROM p IN c.tags WHERE p.category IN (@param0_0, @param0_1)
            # )"

            # Single object field existence
            query, params = self._build_sql_query({
                "settings.theme": {"$exists": True}  # settings: UserSettings
            })
            # Result: "SELECT * FROM c WHERE IS_DEFINED(c.settings.theme)"

            # Array element field existence
            query, params = self._build_sql_query({
                "contacts.verified": {"$exists": True}  # contacts: list[Contact]
            })
            # Result: "SELECT * FROM c WHERE EXISTS(
            #   SELECT VALUE p FROM p IN c.contacts WHERE IS_DEFINED(p.verified)
            # )"
            ```

            Custom SELECT clauses:

            ```python
            # For deletion (only get ID and partition key)
            query, params = self._build_sql_query(
                {"status": "inactive"},
                select_clause="SELECT c.id, c._partitionKey"
            )

            # For counting
            query, params = self._build_sql_query(
                {"tier": "premium"},
                select_clause="SELECT VALUE COUNT(1)"
            )

            # For specific fields
            query, params = self._build_sql_query(
                {"status": "active"},
                select_clause="SELECT c.name, c.email, c.tier"
            )
            ```

            Sorting:

            ```python
            from sas.cosmosdb.sql import SortField, SortDirection

            query, params = self._build_sql_query(
                {"status": "active"},
                sort_fields=[
                    SortField("tier", SortDirection.ASCENDING),
                    SortField("joinDate", SortDirection.DESCENDING)
                ]
            )
            # Result: "SELECT * FROM c WHERE c.status = @param0
            #          ORDER BY c.tier ASC, c.joinDate DESC"
            ```

        Supported operators:
            - Basic: $eq, $ne, $gt, $gte, $lt, $lte (all support array element operations)
            - Lists: $in, $nin (not in) (both support array element operations)
            - Text: $contains, $startswith, $endswith (all support array element operations)
            - Logical: $and, $or
            - Existence: $exists (supports array element field existence)
            - Arrays: dot notation for nested fields - ALL operators support this

        Array Operations with Dot Notation:
            The query builder now intelligently determines whether dot notation refers to
            arrays or single objects by analyzing Pydantic type hints:

            For array fields (e.g., friends: list[Friend], children: list[Child]):
            - "friends.age": 25 → EXISTS(SELECT VALUE p FROM p IN c.friends WHERE p.age = 25)
            - "children.grade": {"$gte": 5} → EXISTS(SELECT VALUE p FROM p IN c.children WHERE p.grade >= 5)

            For single object fields (e.g., address: Address, profile: UserProfile):
            - "address.city": "Seattle" → c.address.city = "Seattle"
            - "profile.name": {"$contains": "John"} → CONTAINS(c.profile.name, "John")

            This smart detection prevents unnecessary EXISTS subqueries for single object fields,
            improving query performance and correctness.

        Note:
            For complex array operations like ARRAY_LENGTH(), use query_raw_async() instead:
            ```python
            results = await repo.query_raw_async(
                "SELECT * FROM c WHERE ARRAY_LENGTH(c.items) > 5"
            )
            ```
        """
        conditions = []
        parameters = {}
        param_counter = 0

        def process_condition(field, condition, is_nested=False):
            nonlocal param_counter

            if isinstance(condition, dict):
                for operator, value in condition.items():
                    param_name = f"param{param_counter}"
                    param_counter += 1

                    # Check if this is a nested field operation (dot notation)
                    is_nested_operation = "." in field
                    is_array_operation = False

                    if is_nested_operation:
                        # Split field path for nested access
                        field_parts = field.split(".", 1)
                        root_field = field_parts[0]
                        nested_field = field_parts[1]

                        # Use smart detection to determine if this is an array operation
                        is_array_operation = self._is_array_field(field)

                    if operator == "$contains":
                        if is_array_operation:
                            # Generate EXISTS query for array element matching
                            conditions.append(
                                f"EXISTS(SELECT VALUE p FROM p IN c.{root_field} WHERE CONTAINS(p.{nested_field}, @{param_name}))"
                            )
                            parameters[f"@{param_name}"] = value
                        elif is_nested_operation:
                            # Direct nested field access for single object
                            conditions.append(f"CONTAINS(c.{field}, @{param_name})")
                            parameters[f"@{param_name}"] = value
                        else:
                            # Simple field containment
                            conditions.append(f"CONTAINS(c.{field}, @{param_name})")
                            parameters[f"@{param_name}"] = value

                    elif operator == "$startswith":
                        if is_array_operation:
                            # Array element startswith operation
                            conditions.append(
                                f"EXISTS(SELECT VALUE p FROM p IN c.{root_field} WHERE STARTSWITH(p.{nested_field}, @{param_name}))"
                            )
                            parameters[f"@{param_name}"] = value
                        elif is_nested_operation:
                            # Direct nested field access for single object
                            conditions.append(f"STARTSWITH(c.{field}, @{param_name})")
                            parameters[f"@{param_name}"] = value
                        else:
                            conditions.append(f"STARTSWITH(c.{field}, @{param_name})")
                            parameters[f"@{param_name}"] = value

                    elif operator == "$endswith":
                        if is_array_operation:
                            # Array element endswith operation
                            conditions.append(
                                f"EXISTS(SELECT VALUE p FROM p IN c.{root_field} WHERE ENDSWITH(p.{nested_field}, @{param_name}))"
                            )
                            parameters[f"@{param_name}"] = value
                        elif is_nested_operation:
                            # Direct nested field access for single object
                            conditions.append(f"ENDSWITH(c.{field}, @{param_name})")
                            parameters[f"@{param_name}"] = value
                        else:
                            conditions.append(f"ENDSWITH(c.{field}, @{param_name})")
                            parameters[f"@{param_name}"] = value

                    elif operator == "$eq" or operator == "=":
                        if is_array_operation:
                            # Array element equality operation
                            conditions.append(
                                f"EXISTS(SELECT VALUE p FROM p IN c.{root_field} WHERE p.{nested_field} = @{param_name})"
                            )
                            parameters[f"@{param_name}"] = value
                        elif is_nested_operation:
                            # Direct nested field access for single object
                            conditions.append(f"c.{field} = @{param_name}")
                            parameters[f"@{param_name}"] = value
                        else:
                            conditions.append(f"c.{field} = @{param_name}")
                            parameters[f"@{param_name}"] = value

                    elif operator == "$ne" or operator == "!=":
                        if is_array_operation:
                            # Array element not equal operation
                            conditions.append(
                                f"EXISTS(SELECT VALUE p FROM p IN c.{root_field} WHERE p.{nested_field} != @{param_name})"
                            )
                            parameters[f"@{param_name}"] = value
                        elif is_nested_operation:
                            # Direct nested field access for single object
                            conditions.append(f"c.{field} != @{param_name}")
                            parameters[f"@{param_name}"] = value
                        else:
                            conditions.append(f"c.{field} != @{param_name}")
                            parameters[f"@{param_name}"] = value

                    elif operator == "$gt":
                        if is_array_operation:
                            # Array element greater than operation
                            conditions.append(
                                f"EXISTS(SELECT VALUE p FROM p IN c.{root_field} WHERE p.{nested_field} > @{param_name})"
                            )
                            parameters[f"@{param_name}"] = value
                        elif is_nested_operation:
                            # Direct nested field access for single object
                            conditions.append(f"c.{field} > @{param_name}")
                            parameters[f"@{param_name}"] = value
                        else:
                            conditions.append(f"c.{field} > @{param_name}")
                            parameters[f"@{param_name}"] = value

                    elif operator == "$gte":
                        if is_array_operation:
                            # Array element greater than or equal operation
                            conditions.append(
                                f"EXISTS(SELECT VALUE p FROM p IN c.{root_field} WHERE p.{nested_field} >= @{param_name})"
                            )
                            parameters[f"@{param_name}"] = value
                        elif is_nested_operation:
                            # Direct nested field access for single object
                            conditions.append(f"c.{field} >= @{param_name}")
                            parameters[f"@{param_name}"] = value
                        else:
                            conditions.append(f"c.{field} >= @{param_name}")
                            parameters[f"@{param_name}"] = value

                    elif operator == "$lt":
                        if is_array_operation:
                            # Array element less than operation
                            conditions.append(
                                f"EXISTS(SELECT VALUE p FROM p IN c.{root_field} WHERE p.{nested_field} < @{param_name})"
                            )
                            parameters[f"@{param_name}"] = value
                        elif is_nested_operation:
                            # Direct nested field access for single object
                            conditions.append(f"c.{field} < @{param_name}")
                            parameters[f"@{param_name}"] = value
                        else:
                            conditions.append(f"c.{field} < @{param_name}")
                            parameters[f"@{param_name}"] = value

                    elif operator == "$lte":
                        if is_array_operation:
                            # Array element less than or equal operation
                            conditions.append(
                                f"EXISTS(SELECT VALUE p FROM p IN c.{root_field} WHERE p.{nested_field} <= @{param_name})"
                            )
                            parameters[f"@{param_name}"] = value
                        elif is_nested_operation:
                            # Direct nested field access for single object
                            conditions.append(f"c.{field} <= @{param_name}")
                            parameters[f"@{param_name}"] = value
                        else:
                            conditions.append(f"c.{field} <= @{param_name}")
                            parameters[f"@{param_name}"] = value

                    elif operator == "$in":
                        # Handle $in operator with list of values
                        if not isinstance(value, (list, tuple)):
                            raise ValueError(
                                f"$in operator requires a list or tuple of values, got {type(value)}"
                            )
                        if not value:
                            raise ValueError("$in operator requires at least one value")

                        if is_array_operation:
                            # Array element IN operation
                            param_names = []
                            for i, val in enumerate(value):
                                in_param_name = f"param{param_counter}_{i}"
                                param_names.append(f"@{in_param_name}")
                                parameters[f"@{in_param_name}"] = val

                            # Create SQL EXISTS clause with IN condition for array elements
                            conditions.append(
                                f"EXISTS(SELECT VALUE p FROM p IN c.{root_field} WHERE p.{nested_field} IN ({', '.join(param_names)}))"
                            )
                            param_counter += 1
                        else:
                            # Create parameters for each value in the list
                            param_names = []
                            for i, val in enumerate(value):
                                in_param_name = f"param{param_counter}_{i}"
                                param_names.append(f"@{in_param_name}")
                                parameters[f"@{in_param_name}"] = val

                            # Create SQL IN clause
                            conditions.append(
                                f"c.{field} IN ({', '.join(param_names)})"
                            )
                            # Don't increment param_counter here since we used it for the base name
                            param_counter += 1

                    elif operator == "$nin":
                        # Handle $nin (not in) operator
                        if not isinstance(value, (list, tuple)):
                            raise ValueError(
                                f"$nin operator requires a list or tuple of values, got {type(value)}"
                            )
                        if not value:
                            raise ValueError(
                                "$nin operator requires at least one value"
                            )

                        if is_array_operation:
                            # Array element NOT IN operation
                            param_names = []
                            for i, val in enumerate(value):
                                nin_param_name = f"param{param_counter}_{i}"
                                param_names.append(f"@{nin_param_name}")
                                parameters[f"@{nin_param_name}"] = val

                            # Create SQL EXISTS clause with NOT IN condition for array elements
                            conditions.append(
                                f"EXISTS(SELECT VALUE p FROM p IN c.{root_field} WHERE p.{nested_field} NOT IN ({', '.join(param_names)}))"
                            )
                            param_counter += 1
                        else:
                            param_names = []
                            for i, val in enumerate(value):
                                nin_param_name = f"param{param_counter}_{i}"
                                param_names.append(f"@{nin_param_name}")
                                parameters[f"@{nin_param_name}"] = val

                            conditions.append(
                                f"c.{field} NOT IN ({', '.join(param_names)})"
                            )
                            param_counter += 1

                    elif operator == "$exists":
                        # Check if field exists
                        if is_array_operation:
                            # Array element field existence operation
                            if value:
                                conditions.append(
                                    f"EXISTS(SELECT VALUE p FROM p IN c.{root_field} WHERE IS_DEFINED(p.{nested_field}))"
                                )
                            else:
                                conditions.append(
                                    f"EXISTS(SELECT VALUE p FROM p IN c.{root_field} WHERE NOT IS_DEFINED(p.{nested_field}))"
                                )
                        elif is_nested_operation:
                            # Direct nested field existence for single object
                            if value:
                                conditions.append(f"IS_DEFINED(c.{field})")
                            else:
                                conditions.append(f"NOT IS_DEFINED(c.{field})")
                        else:
                            if value:
                                conditions.append(f"IS_DEFINED(c.{field})")
                            else:
                                conditions.append(f"NOT IS_DEFINED(c.{field})")

                    else:
                        # For complex conditions, recommend using query_raw_async
                        logger.warning(
                            f"Operator {operator} not supported in simple query builder. Use query_raw_async for complex queries."
                        )
                        raise ValueError(
                            f"Unsupported operator: {operator}. Use query_raw_async for complex array operations."
                        )
            else:
                # Simple equality condition
                param_name = f"param{param_counter}"
                param_counter += 1

                # Check if this is a nested field operation (dot notation)
                if "." in field:
                    # Split field path for nested access
                    field_parts = field.split(".", 1)
                    root_field = field_parts[0]
                    nested_field = field_parts[1]

                    # Use smart detection to determine if this is an array operation
                    if self._is_array_field(field):
                        # Array element equality operation
                        conditions.append(
                            f"EXISTS(SELECT VALUE p FROM p IN c.{root_field} WHERE p.{nested_field} = @{param_name})"
                        )
                        parameters[f"@{param_name}"] = condition
                    else:
                        # Direct nested field access for single object
                        conditions.append(f"c.{field} = @{param_name}")
                        parameters[f"@{param_name}"] = condition
                else:
                    conditions.append(f"c.{field} = @{param_name}")
                    parameters[f"@{param_name}"] = condition

        if predicate:
            for field, condition in predicate.items():
                if field == "$and":
                    # Handle $and operator
                    if not isinstance(condition, list):
                        raise ValueError("$and operator requires a list of conditions")

                    and_conditions = []
                    for sub_condition in condition:
                        sub_conditions = []
                        for sub_field, sub_value in sub_condition.items():
                            temp_conditions = conditions.copy()
                            process_condition(sub_field, sub_value, True)
                            # Get the new conditions added
                            new_conditions = conditions[len(temp_conditions) :]
                            sub_conditions.extend(new_conditions)
                            # Remove them from main conditions as we'll group them
                            conditions = conditions[: len(temp_conditions)]

                        if sub_conditions:
                            and_conditions.append(f"({' AND '.join(sub_conditions)})")

                    if and_conditions:
                        conditions.append(f"({' AND '.join(and_conditions)})")

                elif field == "$or":
                    # Handle $or operator
                    if not isinstance(condition, list):
                        raise ValueError("$or operator requires a list of conditions")

                    or_conditions = []
                    for sub_condition in condition:
                        sub_conditions = []
                        for sub_field, sub_value in sub_condition.items():
                            temp_conditions = conditions.copy()
                            process_condition(sub_field, sub_value, True)
                            # Get the new conditions added
                            new_conditions = conditions[len(temp_conditions) :]
                            sub_conditions.extend(new_conditions)
                            # Remove them from main conditions as we'll group them
                            conditions = conditions[: len(temp_conditions)]

                        if sub_conditions:
                            or_conditions.append(f"({' AND '.join(sub_conditions)})")

                    if or_conditions:
                        conditions.append(f"({' OR '.join(or_conditions)})")
                else:
                    process_condition(field, condition)

        # Build WHERE clause
        where_clause = " AND ".join(conditions) if conditions else "1=1"

        # Build ORDER BY clause
        order_clause = ""
        if sort_fields:
            order_parts = []
            for sort_field in sort_fields:
                direction = (
                    "ASC" if sort_field.order == SortDirection.ASCENDING else "DESC"
                )
                order_parts.append(f"c.{sort_field.field_name} {direction}")
            order_clause = f" ORDER BY {', '.join(order_parts)}"

        query = f"{select_clause} FROM c WHERE {where_clause}{order_clause}"

        return query, parameters

    # Implementation of abstract methods from RepositoryBase

    async def get_async(
        self, key: TKey, partition_key: Optional[str] = None
    ) -> Optional[TEntity]:
        """
        Retrieve an entity by its key and partition key.

        Args:
            key: The document ID
            partition_key: The partition key value (if not provided, will be derived from key)

        Returns:
            The entity if found, None otherwise

        Examples:
            Basic retrieval (partition key auto-derived):

            ```python
            # Partition key automatically derived from ID
            customer = await repo.get_async("customer-123")
            if customer:
                print(f"Found customer: {customer.name}")
            else:
                print("Customer not found")
            ```

            Explicit partition key for performance:

            ```python
            # Provide partition key for optimal performance
            order = await repo.get_async("order-456", partition_key="customer-123")
            ```

            Handling missing entities:

            ```python
            async def get_customer_safely(customer_id: str):
                try:
                    customer = await repo.get_async(customer_id)
                    return customer
                except Exception as e:
                    logger.error(f"Error retrieving customer {customer_id}: {e}")
                    return None
            ```

            Batch retrieval pattern:

            ```python
            async def get_multiple_customers(customer_ids: List[str]):
                customers = []
                for customer_id in customer_ids:
                    customer = await repo.get_async(customer_id)
                    if customer:
                        customers.append(customer)
                return customers
            ```
        """
        await self._ensure_initialized()

        try:
            # If partition key is not provided, derive it from the key using RootEntityBase logic
            if partition_key is None:
                partition_key = RootEntityBase.get_partition_key_from_id(key)

            response = await self._execute_with_retry(
                self._container.read_item, item=key, partition_key=partition_key
            )

            return self._document_to_entity(response)
        except CosmosResourceNotFoundError:
            return None
        except Exception as e:
            logger.error(f"Error retrieving entity with key '{key}': {e}")
            raise

    async def find_async(
        self,
        predicate: Dict[str, Any] | None = None,
        sort_fields: List[SortField] = None,
        partition_key: Optional[str] = None,
    ) -> List[TEntity]:
        """
        Find entities matching a predicate with optional sorting.

        This method supports basic query operations. For complex queries involving arrays,
        aggregations, or advanced Cosmos DB SQL features, use query_raw_async() instead.

        Args:
            predicate: Query conditions as key-value pairs (basic operators only)
            sort_fields: Fields to sort by
            partition_key: Specific partition key to query (for performance).
                          If None, performs cross-partition query.

        Returns:
            List of entities matching the criteria

        Examples:
            Simple equality queries:

            ```python
            # Find by exact match
            active_customers = await repo.find_async({"status": "active"})

            # Find by multiple conditions (implicit AND)
            premium_adults = await repo.find_async({
                "tier": "premium",
                "age": {"$gte": 18}
            })
            ```

            Range and comparison queries:

            ```python
            # Age ranges
            young_adults = await repo.find_async({
                "age": {"$gte": 18, "$lt": 30}
            })

            # Date ranges
            recent_orders = await repo.find_async({
                "orderDate": {"$gte": "2024-01-01"}
            })
            ```

            List membership and text operations:

            ```python
            # Find customers in specific cities
            city_customers = await repo.find_async({
                "city": {"$in": ["Seattle", "Portland", "Vancouver"]}
            })

            # Text operations
            temp_users = await repo.find_async({
                "username": {"$startswith": "temp_"}
            })

            # Contains operation
            tagged_items = await repo.find_async({
                "description": {"$contains": "urgent"}
            })
            ```

            Complex logical conditions:

            ```python
            # AND conditions
            qualified_customers = await repo.find_async({
                "$and": [
                    {"age": {"$gte": 21}},
                    {"status": "verified"},
                    {"balance": {"$gt": 1000}}
                ]
            })

            # OR conditions
            priority_customers = await repo.find_async({
                "$or": [
                    {"tier": "premium"},
                    {"balance": {"$gte": 10000}}
                ]
            })
            ```

            Sorting and partition optimization:

            ```python
            from sas.cosmosdb.sql import SortField, SortDirection

            # Sort by multiple fields
            sorted_customers = await repo.find_async(
                {"status": "active"},
                sort_fields=[
                    SortField("tier", SortDirection.ASCENDING),
                    SortField("joinDate", SortDirection.DESCENDING)
                ]
            )

            # Partition-specific query for performance
            partition_customers = await repo.find_async(
                {"status": "active"},
                partition_key="premium-tier"
            )
            ```

            Field existence and enhanced array operations:

            ```python
            # Check field existence
            verified_profiles = await repo.find_async({
                "verificationDate": {"$exists": True}
            })

            # Enhanced array operations with dot notation (all operators supported)
            customers_with_company_emails = await repo.find_async({
                "contacts.email": {"$contains": "@company.com"}
            })

            # Array element comparisons
            customers_with_young_friends = await repo.find_async({
                "friends.age": {"$lt": 25}
            })

            # Array element IN operations
            customers_with_priority_tags = await repo.find_async({
                "tags.category": {"$in": ["urgent", "vip", "priority"]}
            })

            # Array element string operations
            customers_with_admin_contacts = await repo.find_async({
                "contacts.email": {"$startswith": "admin@"}
            })

            # Array element field existence
            orders_with_discounts = await repo.find_async({
                "items.discountPrice": {"$exists": True}
            })

            # Complex array queries with multiple conditions
            high_value_orders = await repo.find_async({
                "items.price": {"$gte": 1000},
                "items.category": {"$in": ["electronics", "jewelry"]}
            })
            ```

        Note:
            For array operations like ARRAY_LENGTH(), use query_raw_async() with proper SQL:
            ```python
            # Complex array operations require raw SQL
            results = await repo.query_raw_async(
                "SELECT * FROM c WHERE ARRAY_LENGTH(c.friends) > 0"
            )
            ```

        Cross-partition queries:
            When partition_key is None, the query will scan all partitions.
            This is more expensive but sometimes necessary for global queries.

            ```python
            # Cross-partition search (expensive but comprehensive)
            all_premium = await repo.find_async(
                {"tier": "premium"},
                partition_key=None  # Searches all partitions
            )
            ```
        """
        await self._ensure_initialized()

        try:
            # Build SQL query with parameters
            query, parameters = self._build_sql_query(predicate, sort_fields)

            # Configure query options
            query_options = {}

            # Only set partition_key if provided - omitting it enables cross-partition queries
            if partition_key is not None:
                query_options["partition_key"] = partition_key

            # Add parameters to query options
            if parameters:
                query_options["parameters"] = [
                    {"name": name, "value": value} for name, value in parameters.items()
                ]

            # Execute query
            items = []
            async for item in self._container.query_items(query=query, **query_options):
                items.append(self._document_to_entity(item))

            return items
        except Exception as e:
            logger.error(f"Error finding entities: {e}")
            raise

    async def add_async(self, entity: TEntity) -> None:
        """
        Add a new entity to the container.

        Args:
            entity: The entity to add

        Raises:
            ValueError: If entity with the same ID already exists
            Exception: For other database errors

        Examples:
            Basic entity creation:

            ```python
            customer = Customer(
                id="customer-123",
                name="John Doe",
                email="john@example.com",
                age=30
            )
            await repo.add_async(customer)
            print(f"Added customer: {customer.id}")
            ```

            Batch creation:

            ```python
            customers = [
                Customer(id="cust-1", name="Alice", email="alice@example.com"),
                Customer(id="cust-2", name="Bob", email="bob@example.com"),
                Customer(id="cust-3", name="Carol", email="carol@example.com")
            ]

            for customer in customers:
                try:
                    await repo.add_async(customer)
                    print(f"✅ Added {customer.name}")
                except ValueError as e:
                    print(f"❌ Duplicate: {e}")
                except Exception as e:
                    print(f"❌ Error: {e}")
            ```

            Handling duplicates gracefully:

            ```python
            async def add_customer_if_new(customer: Customer):
                try:
                    await repo.add_async(customer)
                    return True
                except ValueError:
                    # Customer already exists
                    logger.info(f"Customer {customer.id} already exists")
                    return False
            ```

            Entity with auto-generated partition key:

            ```python
            # Partition key automatically derived from ID
            order = Order(
                id="order-456-customer-123",  # ID format: order-{orderId}-{customerId}
                customerId="customer-123",
                amount=99.99,
                items=["item1", "item2"]
            )
            # Partition key will be auto-set to "customer-123"
            await repo.add_async(order)
            ```

            Entity with explicit partition key:

            ```python
            product = Product(
                id="product-789",
                name="Laptop",
                category="electronics",
                price=1299.99
            )
            # Manually set partition key if needed
            product._partitionKey = "electronics"
            await repo.add_async(product)
            ```
        """
        await self._ensure_initialized()

        try:
            # Ensure partition key is set using RootEntityBase logic
            if not entity._partitionKey:
                entity._partitionKey = RootEntityBase.get_partition_key_from_id(
                    entity.id
                )

            document = self._entity_to_document(entity)

            await self._execute_with_retry(self._container.create_item, body=document)

            logger.debug(f"Added entity with ID: {entity.id}")
        except CosmosHttpResponseError as e:
            if e.status_code == 409:  # Conflict - item already exists
                raise ValueError(f"Entity with ID '{entity.id}' already exists")
            raise
        except Exception as e:
            logger.error(f"Error adding entity: {e}")
            raise

    async def update_async(self, entity: TEntity) -> None:
        """
        Update an existing entity.

        Args:
            entity: The entity to update
            predicate: Optional predicate (for compatibility with base class)
        """
        await self._ensure_initialized()

        try:
            # Ensure partition key is set using RootEntityBase logic
            # if not entity._partitionKey:
            #     entity._partitionKey = RootEntityBase.get_partition_key_from_id(
            #         entity.id
            #     )

            document = self._entity_to_document(entity)

            await self._execute_with_retry(
                self._container.replace_item, item=entity.id, body=document
            )

            logger.debug(f"Updated entity with ID: {entity.id}")
        except CosmosResourceNotFoundError:
            raise ValueError(f"Entity with ID '{entity.id}' not found")
        except Exception as e:
            logger.error(f"Error updating entity: {e}")
            raise

    async def delete_async(
        self,
        key: TKey,
        partition_key: Optional[str] = None,
    ) -> None:
        """
        Delete an entity by its key.

        Args:
            key: The document ID
            partition_key: The partition key value (if not provided, will be derived from key)
            predicate: Optional predicate (for compatibility with base class)
        """
        await self._ensure_initialized()

        try:
            if partition_key is None:
                partition_key = RootEntityBase.get_partition_key_from_id(key)

            await self._execute_with_retry(
                self._container.delete_item, item=key, partition_key=partition_key
            )

            logger.debug(f"Deleted entity with ID: {key}")
        except CosmosResourceNotFoundError:
            logger.warning(f"Entity with ID '{key}' not found for deletion")
        except Exception as e:
            logger.error(f"Error deleting entity: {e}")
            raise

    async def delete_items_async(self, predicate):
        """
        Delete multiple entities matching the specified predicate.

        This method uses a simple, efficient approach:
        1. Build a SELECT query to find items to delete
        2. Stream through results and delete each item individually
        3. Handle errors gracefully and continue processing

        Args:
            predicate: Query conditions as key-value pairs

        Returns:
            int: Number of entities deleted

        Examples:
            Simple deletion by field value:

            ```python
            # Delete inactive customers
            deleted_count = await repo.delete_items_async({"status": "inactive"})
            print(f"Deleted {deleted_count} inactive customers")

            # Delete old orders
            deleted_count = await repo.delete_items_async({
                "orderDate": {"$lt": "2023-01-01"}
            })
            ```

            Range-based deletion:

            ```python
            # Delete customers in age range
            deleted_count = await repo.delete_items_async({
                "age": {"$gte": 65, "$lt": 100}
            })

            # Delete low-value orders
            deleted_count = await repo.delete_items_async({
                "amount": {"$lt": 10.0}
            })
            ```

            List-based deletion:

            ```python
            # Delete customers from specific cities
            deleted_count = await repo.delete_items_async({
                "city": {"$in": ["TestCity1", "TestCity2", "TempLocation"]}
            })

            # Delete products not in active categories
            deleted_count = await repo.delete_items_async({
                "category": {"$nin": ["electronics", "books", "clothing"]}
            })
            ```

            Complex logical conditions:

            ```python
            # Delete with AND conditions
            deleted_count = await repo.delete_items_async({
                "$and": [
                    {"status": "inactive"},
                    {"lastLogin": {"$lt": "2024-01-01"}},
                    {"balance": {"$eq": 0}}
                ]
            })

            # Delete with OR conditions
            deleted_count = await repo.delete_items_async({
                "$or": [
                    {"status": "deleted"},
                    {"markedForDeletion": True}
                ]
            })
            ```

            Text-based deletion:

            ```python
            # Delete temporary records
            deleted_count = await repo.delete_items_async({
                "name": {"$startswith": "temp_"}
            })

            # Delete test data
            deleted_count = await repo.delete_items_async({
                "description": {"$contains": "test"}
            })
            ```

            Field existence-based deletion:

            ```python
            # Delete records with deprecated fields
            deleted_count = await repo.delete_items_async({
                "deprecatedField": {"$exists": True}
            })

            # Delete incomplete records
            deleted_count = await repo.delete_items_async({
                "requiredField": {"$exists": False}
            })
            ```

            Safe deletion with verification:

            ```python
            async def safe_bulk_delete(predicate: dict):
                # First, count what will be deleted
                count = await repo.count_async(predicate)

                if count == 0:
                    print("No records match the deletion criteria")
                    return 0

                print(f"About to delete {count} records")

                # Confirm before deletion (in production, add user confirmation)
                if count > 100:
                    print("⚠️ Large deletion detected - verify predicate")
                    return 0

                # Perform deletion
                deleted_count = await repo.delete_items_async(predicate)
                print(f"✅ Successfully deleted {deleted_count} records")
                return deleted_count
            ```

            Emergency cleanup:

            ```python
            # ⚠️ DANGER: Delete all documents (use with extreme caution!)
            async def emergency_cleanup():
                # Count first
                total = await repo.count_async({})
                print(f"About to delete ALL {total} documents")

                # Uncomment only if you're absolutely sure!
                # deleted_count = await repo.delete_items_async({})
                # print(f"Deleted {deleted_count} documents")
            ```

        Note:
            - Uses streaming deletion to minimize memory usage and provide
              consistent performance across different dataset sizes.
            - This operation is IRREVERSIBLE - always test with count_async() first
            - Individual item deletion failures are logged but don't stop the process
            - For large datasets, monitor Request Unit (RU) consumption
        """
        await self._ensure_initialized()

        try:
            # Build the delete query using the consolidated _build_sql_query method
            delete_query, parameters = self._build_sql_query(
                predicate, select_clause="SELECT c.id, c._partitionKey"
            )

            # Configure query options
            query_options = {}
            if parameters:
                query_options["parameters"] = [
                    {"name": name, "value": value} for name, value in parameters.items()
                ]

            # Execute deletion using streaming approach
            deleted_count = 0
            async for item in self._container.query_items(
                query=delete_query, **query_options
            ):
                try:
                    # Get partition key, fallback to id if not available
                    partition_key = item.get("_partitionKey", item["id"])

                    # Delete the item
                    await self._execute_with_retry(
                        self._container.delete_item,
                        item=item["id"],
                        partition_key=partition_key,
                    )
                    deleted_count += 1

                except CosmosResourceNotFoundError:
                    # Item was already deleted, continue
                    logger.warning(
                        f"Entity with ID '{item['id']}' not found during deletion"
                    )
                except Exception as delete_error:
                    # Log error but continue with other deletions
                    logger.error(f"Error deleting entity {item['id']}: {delete_error}")
                    continue

            logger.info(f"Successfully deleted {deleted_count} entities")
            return deleted_count

        except Exception as e:
            logger.error(f"Error deleting items: {e}")
            raise

    async def all_async(
        self,
        sort_fields: Optional[List[SortField]] = None,
        partition_key: Optional[str] = None,
    ) -> List[TEntity]:
        """
        Retrieve all entities with optional sorting.

        Args:
            sort_fields: Optional sorting fields
            partition_key: Optional partition key to limit query scope.
                          If None, performs cross-partition query.

        Returns:
            List of all entities matching the criteria
        """
        await self._ensure_initialized()

        try:
            # Build query for all items
            query = "SELECT * FROM c"
            if sort_fields:
                order_clauses = []
                for field in sort_fields:
                    direction = (
                        "ASC" if field.order == SortDirection.ASCENDING else "DESC"
                    )
                    order_clauses.append(f"c.{field.field_name} {direction}")
                query += f" ORDER BY {', '.join(order_clauses)}"

            # Configure query options
            query_options = {}
            # Only set partition_key if provided - omitting it enables cross-partition queries
            if partition_key is not None:
                query_options["partition_key"] = partition_key

            # Execute query
            items = []
            async for item in self._container.query_items(query=query, **query_options):
                items.append(self._document_to_entity(item))

            return items
        except Exception as e:
            logger.error(f"Error retrieving all entities: {e}")
            raise

    async def find_with_pagination_async(
        self,
        predicate: Dict[str, Any],
        sort_fields: List[SortField] = None,
        skip: int = 0,
        limit: int = 100,
        partition_key: Optional[str] = None,
    ) -> List[TEntity]:
        """
        Find entities with pagination support.

        Args:
            predicate: Query conditions as key-value pairs
            sort_fields: Fields to sort by
            skip: Number of items to skip
            limit: Maximum number of items to return
            partition_key: Specific partition key to query (for performance).
                          If None, performs cross-partition query.

        Returns:
            List of entities matching the criteria
        """
        await self._ensure_initialized()

        try:
            # Build SQL query with pagination
            query, parameters = self._build_sql_query(predicate, sort_fields)
            query += f" OFFSET {skip} LIMIT {limit}"

            # Configure query options
            query_options = {}
            # Only set partition_key if provided - omitting it enables cross-partition queries
            if partition_key is not None:
                query_options["partition_key"] = partition_key

            # Add parameters to query options
            if parameters:
                query_options["parameters"] = [
                    {"name": name, "value": value} for name, value in parameters.items()
                ]

            # Execute query
            items = []
            async for item in self._container.query_items(query=query, **query_options):
                items.append(self._document_to_entity(item))

            return items
        except Exception as e:
            logger.error(f"Error finding entities with pagination: {e}")
            raise

    async def count_async(
        self, predicate: Dict[str, Any] = None, partition_key: Optional[str] = None
    ) -> int:
        """
        Count entities matching a predicate.

        Args:
            predicate: Query conditions as key-value pairs (optional)
            partition_key: Specific partition key to query (for performance).
                          If None, performs cross-partition query.

        Returns:
            Number of entities matching the criteria
        """
        await self._ensure_initialized()

        try:
            # Build count query using unified query builder
            if predicate:
                query, parameters = self._build_sql_query(
                    predicate, select_clause="SELECT VALUE COUNT(1)"
                )
            else:
                query = "SELECT VALUE COUNT(1) FROM c"
                parameters = {}

            # Configure query options
            query_options = {}
            # Only set partition_key if provided - omitting it enables cross-partition queries
            if partition_key is not None:
                query_options["partition_key"] = partition_key

            # Add parameters to query options
            if parameters:
                query_options["parameters"] = [
                    {"name": name, "value": value} for name, value in parameters.items()
                ]

            # Execute query
            result = []
            async for item in self._container.query_items(query=query, **query_options):
                result.append(item)

            return result[0] if result else 0
        except Exception as e:
            logger.error(f"Error counting entities: {e}")
            raise

    async def find_one_async(
        self, predicate: Dict[str, Any], partition_key: Optional[str] = None
    ) -> Optional[TEntity]:
        """
        Find a single entity matching a predicate.

        Args:
            predicate: Query conditions as key-value pairs
            partition_key: Specific partition key to query (for performance).
                          If None, performs cross-partition query.

        Returns:
            The first entity matching the criteria, or None if not found
        """
        await self._ensure_initialized()

        try:
            # Build SQL query with parameters and add LIMIT
            query, parameters = self._build_sql_query(predicate)
            query += " OFFSET 0 LIMIT 1"

            # Configure query options
            query_options = {}
            # Only set partition_key if provided - omitting it enables cross-partition queries
            if partition_key is not None:
                query_options["partition_key"] = partition_key

            # Add parameters to query options
            if parameters:
                query_options["parameters"] = [
                    {"name": name, "value": value} for name, value in parameters.items()
                ]

            # Execute query
            async for item in self._container.query_items(query=query, **query_options):
                return self._document_to_entity(item)

            return None
        except Exception as e:
            logger.error(f"Error finding single entity: {e}")
            raise

    async def exists_async(
        self, predicate: Dict[str, Any], partition_key: Optional[str] = None
    ) -> bool:
        """
        Check if any entity exists matching a predicate.

        Args:
            predicate: Query conditions as key-value pairs
            partition_key: Specific partition key to query (for performance).
                          If None, performs cross-partition query.

        Returns:
            True if at least one entity matches the criteria, False otherwise
        """
        entity = await self.find_one_async(predicate, partition_key)
        return entity is not None

    async def query_raw_async(
        self,
        sql_query: str,
        parameters: Optional[Dict[str, Any]] = None,
        partition_key: Optional[str] = None,
    ) -> List[TEntity]:
        """
        Execute a raw SQL query against the container.

        This method allows for complex queries that aren't supported by the predicate-based methods,
        such as array operations, joins, aggregations, etc.

        Args:
            sql_query: Raw SQL query string using Cosmos DB SQL syntax
            parameters: Optional parameters for the query (use @param1, @param2, etc. in query)
            partition_key: Optional partition key to limit query scope.
                          If None, performs cross-partition query.

        Returns:
            List of entities matching the query

        Example:
            # Find entities with non-empty friends array
            entities = await repo.query_raw_async(
                "SELECT * FROM c WHERE ARRAY_LENGTH(c.friends) > 0"
            )

            # Find entities with friends older than a certain age
            entities = await repo.query_raw_async(
                "SELECT * FROM c WHERE EXISTS(SELECT VALUE f FROM f IN c.friends WHERE f.age > @minAge)",
                parameters={"@minAge": 25}
            )
        """
        await self._ensure_initialized()

        try:
            # Configure query options
            query_options = {}
            # Only set partition_key if provided - omitting it enables cross-partition queries
            if partition_key is not None:
                query_options["partition_key"] = partition_key

            # Add parameters to query options
            if parameters:
                query_options["parameters"] = [
                    {"name": name, "value": value} for name, value in parameters.items()
                ]

            # Execute query
            items = []
            async for item in self._container.query_items(
                query=sql_query, **query_options
            ):
                items.append(self._document_to_entity(item))

            return items
        except Exception as e:
            logger.error(f"Error executing raw query: {e}")
            raise

    async def query_raw_dynamic_cursor_async(
        self,
        sql_query: str,
        parameters: Optional[Dict[str, Any]] = None,
        partition_key: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Execute a raw SQL query against the container and return dynamic results.

        This method is ideal for aggregation queries, projections, and other queries
        that don't return complete entity objects.

        Args:
            sql_query: Raw SQL query string using Cosmos DB SQL syntax
            parameters: Optional parameters for the query (use @param1, @param2, etc. in query)
            partition_key: Optional partition key to limit query scope.
                          If None, performs cross-partition query.

        Returns:
            List of dictionaries containing the query results

        Example:
            # Aggregation query
            results = await repo.query_raw_dynamic_cursor_async(
                "SELECT c.address.city, COUNT(1) as family_count FROM c GROUP BY c.address.city"
            )

            # Projection query
            results = await repo.query_raw_dynamic_cursor_async(
                "SELECT c.id, c.parents[0].given_name as first_parent FROM c"
            )
        """
        await self._ensure_initialized()

        try:
            # Configure query options
            query_options = {}
            # Only set partition_key if provided - omitting it enables cross-partition queries
            if partition_key is not None:
                query_options["partition_key"] = partition_key

            # Add parameters to query options
            if parameters:
                query_options["parameters"] = [
                    {"name": name, "value": value} for name, value in parameters.items()
                ]

            # Execute query
            items = []
            async for item in self._container.query_items(
                query=sql_query, **query_options
            ):
                items.append(dict(item))  # Convert to dict for dynamic typing

            return items

        except Exception as e:
            logger.error(f"Error executing raw dynamic query: {e}")
            raise

    async def query_raw_single_value_async(
        self,
        sql_query: str,
        parameters: Optional[Dict[str, Any]] = None,
        partition_key: Optional[str] = None,
    ) -> int:
        """
        Execute a raw SQL query that returns a single numeric value.

        This method is optimized for queries that return a single value like counts,
        sums, averages, etc.

        Args:
            sql_query: Raw SQL query that returns a single numeric value
            parameters: Optional parameters for the query
            partition_key: Optional partition key to limit query scope.
                          If None, performs cross-partition query.

        Returns:
            The single numeric value returned by the query

        Example:
            # Count with complex conditions
            count = await repo.query_raw_single_value_async(
                "SELECT VALUE COUNT(1) FROM c WHERE ARRAY_LENGTH(c.friends) > 0"
            )

            # Sum aggregation
            total = await repo.query_raw_single_value_async(
                "SELECT VALUE SUM(c.children_count) FROM c"
            )
        """
        await self._ensure_initialized()

        try:
            # Configure query options
            query_options = {}
            # Only set partition_key if provided - omitting it enables cross-partition queries
            if partition_key is not None:
                query_options["partition_key"] = partition_key

            # Add parameters to query options
            if parameters:
                query_options["parameters"] = [
                    {"name": name, "value": value} for name, value in parameters.items()
                ]

            # Execute query
            result = []
            async for item in self._container.query_items(
                query=sql_query, **query_options
            ):
                result.append(item)

            return result[0] if result else 0
        except Exception as e:
            logger.error(f"Error executing raw single value query: {e}")
            raise

    async def close(self):
        """Close the Cosmos DB client and clean up resources."""
        if self._client:
            await self._client.close()
            logger.info("Cosmos DB client closed")

    async def __aenter__(self):
        """Async context manager entry."""
        await self._ensure_initialized()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()

    def _get_field_type_info(self, field_path: str) -> Dict[str, Any]:
        """
        Get type information for a field path using Pydantic model annotations.

        Args:
            field_path: The field path (e.g., "address.city" or "children.name")

        Returns:
            Dict with keys: 'is_array', 'element_type', 'field_exists'
        """
        try:
            # Get the entity type from the generic type parameter
            entity_type = self.__orig_bases__[0].__args__[0]
            field_parts = field_path.split(".", 1)
            root_field = field_parts[0]

            # Check if the root field exists in the model
            if (
                not hasattr(entity_type, "__annotations__")
                or root_field not in entity_type.__annotations__
            ):
                return {"is_array": False, "element_type": None, "field_exists": False}

            field_type = entity_type.__annotations__[root_field]

            # First check if it's directly a list type
            origin = get_origin(field_type)
            if origin is list:
                # It's a list type like List[SomeType]
                args = get_args(field_type)
                element_type = args[0] if args else None
                return {
                    "is_array": True,
                    "element_type": element_type,
                    "field_exists": True,
                }

            # Handle Union types (e.g., Optional[Address] = Union[Address, None])
            # Check for Union which includes Optional types
            from typing import Union

            if hasattr(field_type, "__origin__") and field_type.__origin__ is Union:
                args = get_args(field_type)
                # Filter out None types for Optional fields
                non_none_args = [arg for arg in args if arg is not type(None)]
                if len(non_none_args) == 1:
                    # It's an Optional type, check the actual type
                    actual_type = non_none_args[0]
                    actual_origin = get_origin(actual_type)
                    if actual_origin is list:
                        # It's Optional[List[SomeType]]
                        actual_args = get_args(actual_type)
                        element_type = actual_args[0] if actual_args else None
                        return {
                            "is_array": True,
                            "element_type": element_type,
                            "field_exists": True,
                        }
                    else:
                        # It's Optional[SomeType] where SomeType is not a list
                        return {
                            "is_array": False,
                            "element_type": actual_type,
                            "field_exists": True,
                        }

            # If we get here, it's a simple type (not Union, not List)
            return {"is_array": False, "element_type": field_type, "field_exists": True}

        except Exception as e:
            logger.debug(f"Could not determine type for field '{field_path}': {e}")
            # Default to array behavior for backward compatibility
            return {"is_array": True, "element_type": None, "field_exists": True}

    def _is_array_field(self, field_path: str) -> bool:
        """
        Determine if a field path refers to an array or a single object.

        Args:
            field_path: The field path (e.g., "address.city" or "children.name")

        Returns:
            True if the root field is an array, False if it's a single object
        """
        type_info = self._get_field_type_info(field_path)
        return type_info["is_array"]
