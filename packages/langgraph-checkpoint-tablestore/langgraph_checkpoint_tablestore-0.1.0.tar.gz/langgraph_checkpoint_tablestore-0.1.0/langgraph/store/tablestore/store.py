"""Tablestore-based store implementation for LangGraph."""

import logging
from collections.abc import Iterable, Iterator
from typing import Any, Dict, List, Optional, Tuple

import orjson
from langchain_core.runnables import run_in_executor
from tablestore import OTSClient, Row  # type: ignore
from tablestore.metadata import TableMeta, TableOptions, ReservedThroughput, CapacityUnit  # type: ignore
from tablestore.error import OTSServiceError  # type: ignore

from langgraph.store.base import (
    BaseStore,
    GetOp,
    Op,
    PutOp,
    Result,
    SearchOp,
)

logger = logging.getLogger(__name__)

class DeleteOp:
    """Delete operation."""
    def __init__(self, namespace: Tuple[str, ...], key: str):
        self.namespace = namespace
        self.key = key

class TablestoreStore(BaseStore):
    """Tablestore-based store implementation for LangGraph."""

    def __init__(
        self,
        client: OTSClient,
        table_name: str = "langgraph_store",
        **kwargs: Any,
    ) -> None:
        """Initialize the TablestoreStore.

        Args:
            client: The Tablestore client instance.
            table_name: Name of the table to store key-value pairs.
            **kwargs: Additional arguments.
        """
        super().__init__(**kwargs)
        self.client = client
        self.table_name = table_name
        self._setup_table()

    def _setup_table(self) -> None:
        """Create the store table if it doesn't exist."""
        try:
            self.client.describe_table(self.table_name)
            logger.info(f"Store table {self.table_name} already exists")
        except OTSServiceError as e:
            if e.get_error_code() == "OTSObjectNotExist":
                logger.info(f"Creating store table {self.table_name}")
                # Primary key schema: namespace + key
                schema_of_primary_key = [
                    ("namespace", "STRING"),
                    ("key", "STRING"),
                ]
                table_meta = TableMeta(self.table_name, schema_of_primary_key)
                table_options = TableOptions()
                reserved_throughput = ReservedThroughput(CapacityUnit(0, 0))
                self.client.create_table(table_meta, table_options, reserved_throughput)
            else:
                raise

    def _serialize_value(self, value: Any) -> str:
        """Serialize a value for storage."""
        return orjson.dumps(value).decode()

    def _deserialize_value(self, serialized_value: str) -> Any:
        """Deserialize a value from storage."""
        return orjson.loads(serialized_value)

    def _build_key(self, namespace: Tuple[str, ...], key: str) -> str:
        """Build a composite key from namespace and key."""
        namespace_str = "/".join(namespace) if namespace else ""
        return f"{namespace_str}#{key}"

    def _parse_key(self, composite_key: str) -> Tuple[Tuple[str, ...], str]:
        """Parse a composite key into namespace and key."""
        if "#" in composite_key:
            namespace_str, key = composite_key.rsplit("#", 1)
            namespace = tuple(namespace_str.split("/")) if namespace_str else ()
        else:
            namespace = ()
            key = composite_key
        return namespace, key

    def mget(self, keys: List[Tuple[Tuple[str, ...], str]]) -> List[Optional[Any]]:
        """Get multiple values for a list of (namespace, key) tuples.
        
        Args:
            keys: List of (namespace, key) tuples.
            
        Returns:
            List of values or None if key not found.
        """
        if not keys:
            return []

        results = []
        
        # Group keys by namespace for efficient querying
        key_groups = {}
        for i, (namespace, key) in enumerate(keys):
            namespace_str = "/".join(namespace) if namespace else ""
            if namespace_str not in key_groups:
                key_groups[namespace_str] = []
            key_groups[namespace_str].append((i, key))

        # Initialize results list
        results = [None] * len(keys)

        # Query each namespace group
        for namespace_str, key_list in key_groups.items():
            try:
                # Build primary keys for batch get
                primary_keys = []
                for _, key in key_list:
                    primary_keys.append([
                        ("namespace", namespace_str),
                        ("key", key),
                    ])

                # Batch get rows
                request = []
                for pk in primary_keys:
                    request.append(pk)

                # Use batch_get_row for efficiency
                if len(request) == 1:
                    # Single row get
                    consumed, return_row, next_token = self.client.get_row(
                        self.table_name, request[0]
                    )
                    if return_row and return_row.attribute_columns:
                        data = {}
                        for attr in return_row.attribute_columns:
                            data[attr[0]] = attr[1]
                        
                        # Find the index in original keys list
                        original_key = key_list[0][1]
                        original_index = key_list[0][0]
                        
                        if "value" in data:
                            results[original_index] = self._deserialize_value(data["value"])
                else:
                    # Multiple rows get - use individual get_row calls
                    for idx, pk in enumerate(request):
                        try:
                            consumed, return_row, next_token = self.client.get_row(
                                self.table_name, pk
                            )
                            if return_row and return_row.attribute_columns:
                                data = {}
                                for attr in return_row.attribute_columns:
                                    data[attr[0]] = attr[1]
                                
                                # Find the index in original keys list
                                original_index = key_list[idx][0]
                                
                                if "value" in data:
                                    results[original_index] = self._deserialize_value(data["value"])
                        except Exception as e:
                            logger.error(f"Failed to get row: {e}")
                            continue

            except Exception as e:
                logger.error(f"Failed to get keys for namespace {namespace_str}: {e}")
                continue

        return results

    def mset(self, key_value_pairs: List[Tuple[Tuple[str, ...], str, Any]]) -> None:
        """Set multiple key-value pairs.
        
        Args:
            key_value_pairs: List of (namespace, key, value) tuples.
        """
        if not key_value_pairs:
            return

        for namespace, key, value in key_value_pairs:
            try:
                namespace_str = "/".join(namespace) if namespace else ""
                serialized_value = self._serialize_value(value)

                # Create row
                primary_key = [
                    ("namespace", namespace_str),
                    ("key", key),
                ]
                
                attribute_columns = [
                    ("value", serialized_value),
                ]

                row = Row(primary_key, attribute_columns)

                # Put row to table
                self.client.put_row(self.table_name, row)
                logger.debug(f"Set key {key} in namespace {namespace_str}")

            except Exception as e:
                logger.error(f"Failed to set key {key} in namespace {namespace}: {e}")
                raise

    def mdelete(self, keys: List[Tuple[Tuple[str, ...], str]]) -> None:
        """Delete multiple keys.
        
        Args:
            keys: List of (namespace, key) tuples to delete.
        """
        if not keys:
            return

        for namespace, key in keys:
            try:
                namespace_str = "/".join(namespace) if namespace else ""
                
                primary_key = [
                    ("namespace", namespace_str),
                    ("key", key),
                ]

                # Delete row
                consumed, return_row = self.client.delete_row(self.table_name, primary_key)
                logger.debug(f"Deleted key {key} in namespace {namespace_str}")

            except Exception as e:
                logger.error(f"Failed to delete key {key} in namespace {namespace}: {e}")
                raise

    def yield_keys(self, prefix: Tuple[str, ...]) -> Iterator[Tuple[Tuple[str, ...], str]]:
        """Yield keys that match the given prefix.
        
        Args:
            prefix: Namespace prefix to match.
            
        Yields:
            Tuples of (namespace, key) that match the prefix.
        """
        prefix_str = "/".join(prefix) if prefix else ""
        
        try:
            # Build range query to find all keys with this prefix
            inclusive_start_primary_key = [
                ("namespace", prefix_str),
                ("key", ""),
            ]
            
            if prefix_str:
                # For non-empty prefix, we want to find all keys that start with prefix
                # We use prefix + "\x00" as the exclusive end to get all keys starting with prefix
                exclusive_end_primary_key = [
                    ("namespace", prefix_str + "\x00"),
                    ("key", ""),
                ]
            else:
                # For empty prefix, we want all keys
                exclusive_end_primary_key = [
                    ("namespace", "\xFF"),
                    ("key", ""),
                ]

            next_start_primary_key = inclusive_start_primary_key
            
            while True:
                consumed, next_start_primary_key, row_list, next_token = self.client.get_range(
                    self.table_name,
                    "FORWARD",
                    next_start_primary_key,
                    exclusive_end_primary_key,
                    limit=100,
                )

                for row in row_list:
                    pk_dict = {pk[0]: pk[1] for pk in row.primary_key}
                    namespace_str = pk_dict.get("namespace", "")
                    key = pk_dict.get("key", "")
                    
                    # Parse namespace back to tuple
                    namespace = tuple(namespace_str.split("/")) if namespace_str else ()
                    
                    # Check if this key matches our prefix
                    if len(namespace) >= len(prefix) and namespace[:len(prefix)] == prefix:
                        yield (namespace, key)

                # Check if there are more results
                if next_start_primary_key is None:
                    break
                    
        except Exception as e:
            logger.error(f"Failed to yield keys with prefix {prefix}: {e}")
            return

    def batch(self, ops: Iterable[Op]) -> list[Result]:
        """Execute a batch of operations.
        
        Args:
            ops: Iterable of operations to execute.
            
        Returns:
            List of results corresponding to the operations.
        """
        ops_list = list(ops)
        if not ops_list:
            return []

        results: list[Result] = []
        
        # Group operations by type for efficiency
        get_ops = []
        put_ops = []
        delete_ops = []
        search_ops = []
        
        for i, op in enumerate(ops_list):
            if isinstance(op, GetOp):
                get_ops.append((i, op))
            elif isinstance(op, PutOp):
                put_ops.append((i, op))
            elif isinstance(op, DeleteOp):
                delete_ops.append((i, op))
            elif isinstance(op, SearchOp):
                search_ops.append((i, op))
            else:
                logger.warning(f"Unknown operation type: {type(op)}")
                
        # Initialize results list
        results = [None] * len(ops_list)
        
        # Process GET operations
        if get_ops:
            get_keys = [(op.namespace, op.key) for _, op in get_ops]
            get_results = self.mget(get_keys)
            
            for (i, op), result in zip(get_ops, get_results):
                results[i] = result
        
        # Process PUT operations
        if put_ops:
            put_data = [(op.namespace, op.key, op.value) for _, op in put_ops]
            self.mset(put_data)
            
            for i, op in put_ops:
                results[i] = None  # PUT operations typically return None
        
        # Process DELETE operations  
        if delete_ops:
            delete_keys = [(op.namespace, op.key) for _, op in delete_ops]
            self.mdelete(delete_keys)
            
            for i, op in delete_ops:
                results[i] = None  # DELETE operations typically return None
        
        # Process SEARCH operations
        for i, op in search_ops:
            try:
                search_results = list(self._search(op))
                results[i] = search_results
            except Exception as e:
                logger.error(f"Search operation failed: {e}")
                results[i] = []
        
        return results

    async def abatch(self, ops: Iterable[Op]) -> list[Result]:
        """Execute a batch of operations asynchronously.
        
        Args:
            ops: Iterable of operations to execute.
            
        Returns:
            List of results corresponding to the operations.
        """
        # Run the synchronous batch operation in a thread pool
        return await run_in_executor(None, self.batch, ops)

    def _search(self, op: SearchOp) -> Iterator[Any]:
        """Execute a search operation.
        
        Args:
            op: Search operation to execute.
            
        Yields:
            Search results.
        """
        try:
            # Build namespace prefix for search
            namespace_prefix = "/".join(op.namespace_prefix) if op.namespace_prefix else ""
            
            # Build range query
            inclusive_start_primary_key = [
                ("namespace", namespace_prefix),
                ("key", ""),
            ]
            
            if namespace_prefix:
                exclusive_end_primary_key = [
                    ("namespace", namespace_prefix + "\x00"),
                    ("key", ""),
                ]
            else:
                exclusive_end_primary_key = [
                    ("namespace", "\xFF"),
                    ("key", ""),
                ]

            next_start_primary_key = inclusive_start_primary_key
            count = 0
            
            # Apply offset by skipping records
            skipped = 0
            
            while True:
                consumed, next_start_primary_key, row_list, next_token = self.client.get_range(
                    self.table_name,
                    "FORWARD", 
                    next_start_primary_key,
                    exclusive_end_primary_key,
                    limit=100,
                )

                for row in row_list:
                    # Apply offset
                    if op.offset and skipped < op.offset:
                        skipped += 1
                        continue
                    
                    # Apply limit
                    if op.limit and count >= op.limit:
                        return
                    
                    pk_dict = {pk[0]: pk[1] for pk in row.primary_key}
                    attr_dict = {attr[0]: attr[1] for attr in row.attribute_columns}
                    
                    namespace_str = pk_dict.get("namespace", "")
                    key = pk_dict.get("key", "")
                    
                    # Parse namespace back to tuple
                    namespace = tuple(namespace_str.split("/")) if namespace_str else ()
                    
                    # Check if this key matches our prefix
                    if len(namespace) >= len(op.namespace_prefix) and namespace[:len(op.namespace_prefix)] == op.namespace_prefix:
                        if "value" in attr_dict:
                            try:
                                value = self._deserialize_value(attr_dict["value"])
                                
                                # Apply filter if provided
                                if op.filter is None or self._apply_filter(value, op.filter):
                                    yield value
                                    count += 1
                                    
                            except Exception as e:
                                logger.error(f"Failed to deserialize value: {e}")
                                continue

                # Check if there are more results
                if next_start_primary_key is None:
                    break
                    
        except Exception as e:
            logger.error(f"Search operation failed: {e}")
            return

    def _apply_filter(self, value: Any, filter_dict: Dict[str, Any]) -> bool:
        """Apply a filter to a value.
        
        Args:
            value: The value to filter.
            filter_dict: Filter criteria.
            
        Returns:
            True if the value matches the filter, False otherwise.
        """
        # Simple filter implementation - can be extended as needed
        if not isinstance(value, dict):
            return False
            
        for key, expected_value in filter_dict.items():
            if key not in value or value[key] != expected_value:
                return False
                
        return True
    
    def list(
        self,
        namespace: str,
        *,
        prefix: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> Iterator[Tuple[str, Any]]:
        """List key-value pairs in the specified namespace."""
        # Build range query
        if prefix:
            inclusive_start_primary_key = [
                ("namespace", namespace),
                ("key", prefix),
            ]
            exclusive_end_primary_key = [
                ("namespace", namespace),
                ("key", prefix + "\xff"),
            ]
        else:
            inclusive_start_primary_key = [
                ("namespace", namespace),
                ("key", ""),
            ]
            exclusive_end_primary_key = [
                ("namespace", namespace + "\x00"),
                ("key", ""),
            ]

        try:
            consumed, next_start_primary_key, row_list, next_token = self.client.get_range(
                self.table_name,
                "FORWARD",
                inclusive_start_primary_key,
                exclusive_end_primary_key,
                limit=limit or 1000,
            )

            for row in row_list:
                # Extract primary key values
                pk_dict = {pk[0]: pk[1] for pk in row.primary_key}
                
                # Convert attributes to dict
                attr_dict = {}
                for attr in row.attribute_columns:
                    attr_dict[attr[0]] = attr[1]

                key = pk_dict["key"]
                value = self._deserialize_value(attr_dict.get("value", "null"))
                
                yield (key, value)

        except Exception as e:
            logger.error(f"Failed to list key-value pairs: {e}")
            return

    def clear(self, namespace: str) -> None:
        """Clear all key-value pairs in the specified namespace."""
        # List all keys in the namespace and delete them
        keys_to_delete = []
        for key, _ in self.list(namespace):
            keys_to_delete.append(key)

        for key in keys_to_delete:
            self.delete(namespace, key)

    def list_namespaces(self) -> Iterator[str]:
        """List all namespaces."""
        seen_namespaces = set()
        
        # Build range query to get all rows
        inclusive_start_primary_key = [
            ("namespace", ""),
            ("key", ""),
        ]
        exclusive_end_primary_key = [
            ("namespace", "\xff"),
            ("key", ""),
        ]

        try:
            consumed, next_start_primary_key, row_list, next_token = self.client.get_range(
                self.table_name,
                "FORWARD",
                inclusive_start_primary_key,
                exclusive_end_primary_key,
                limit=10000,
            )

            for row in row_list:
                # Extract primary key values
                pk_dict = {pk[0]: pk[1] for pk in row.primary_key}
                namespace = pk_dict["namespace"]
                
                if namespace not in seen_namespaces:
                    seen_namespaces.add(namespace)
                    yield namespace

        except Exception as e:
            logger.error(f"Failed to list namespaces: {e}")
            return
