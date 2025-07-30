"""Tablestore-based store implementation for LangGraph."""

import logging
from typing import Any, Dict, Iterator, List, Optional, Tuple, Union

import orjson
from langgraph.store.base import BaseStore
from tablestore import OTSClient, Row
from tablestore.metadata import TableMeta, TableOptions, ReservedThroughput, CapacityUnit
from tablestore.error import OTSServiceError

logger = logging.getLogger(__name__)


class TablestoreStore(BaseStore):
    """Tablestore-based store for LangGraph."""

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
                # Primary key schema for store table
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

    def _deserialize_value(self, value: str) -> Any:
        """Deserialize a value from storage."""
        return orjson.loads(value)

    def put(
        self,
        namespace: str,
        key: str,
        value: Any,
    ) -> None:
        """Store a key-value pair in the specified namespace."""
        # Create row
        primary_key = [
            ("namespace", namespace),
            ("key", key),
        ]
        
        attribute_columns = [
            ("value", self._serialize_value(value)),
        ]

        row = Row(primary_key, attribute_columns)

        # Put row to table
        try:
            self.client.put_row(self.table_name, row)
            logger.debug(f"Stored key {key} in namespace {namespace}")
        except Exception as e:
            logger.error(f"Failed to store key-value pair: {e}")
            raise

    def get(
        self,
        namespace: str,
        key: str,
    ) -> Optional[Any]:
        """Retrieve a value by key from the specified namespace."""
        primary_key = [
            ("namespace", namespace),
            ("key", key),
        ]

        try:
            consumed, return_row, next_token = self.client.get_row(
                self.table_name, primary_key
            )
            if not return_row or not return_row.attribute_columns:
                return None

            # Convert to dict
            data = {}
            for attr in return_row.attribute_columns:
                data[attr[0]] = attr[1]

            return self._deserialize_value(data.get("value", "null"))
        except Exception as e:
            logger.error(f"Failed to retrieve value: {e}")
            return None

    def delete(
        self,
        namespace: str,
        key: str,
    ) -> None:
        """Delete a key-value pair from the specified namespace."""
        primary_key = [
            ("namespace", namespace),
            ("key", key),
        ]

        try:
            self.client.delete_row(self.table_name, primary_key)
            logger.debug(f"Deleted key {key} from namespace {namespace}")
        except Exception as e:
            logger.error(f"Failed to delete key-value pair: {e}")
            raise

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
