"""Tablestore-based checkpoint implementation for LangGraph."""

import logging
from typing import Any, Dict, Iterator, List, Optional, Tuple

import orjson
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.base import BaseCheckpointSaver, Checkpoint, CheckpointMetadata
from tablestore import OTSClient, Row # type: ignore
from tablestore.metadata import TableMeta, TableOptions, ReservedThroughput, CapacityUnit # type: ignore
from tablestore.error import OTSServiceError # type: ignore

logger = logging.getLogger(__name__)


class TablestoreSaver(BaseCheckpointSaver):
    """Tablestore-based checkpoint saver for LangGraph."""

    def __init__(
        self,
        client: OTSClient,
        table_name: str = "langgraph_checkpoints",
        store_table_name: str = "langgraph_store",
        **kwargs: Any,
    ) -> None:
        """Initialize the TablestoreSaver.

        Args:
            client: The Tablestore client instance.
            table_name: Name of the table to store checkpoints.
            store_table_name: Name of the table to store key-value pairs.
            **kwargs: Additional arguments.
        """
        super().__init__(**kwargs)
        self.client = client
        self.table_name = table_name
        self.store_table_name = store_table_name
        self._setup_tables()

    def _setup_tables(self) -> None:
        """Setup the required tables for checkpoints and store."""
        self._setup_checkpoint_table()
        self._setup_store_table()

    def _setup_checkpoint_table(self) -> None:
        """Create the checkpoint table if it doesn't exist."""
        try:
            self.client.describe_table(self.table_name)
            logger.info(f"Checkpoint table {self.table_name} already exists")
        except OTSServiceError as e:
            if e.get_error_code() == "OTSObjectNotExist":
                logger.info(f"Creating checkpoint table {self.table_name}")
                # Primary key schema for checkpoint table
                schema_of_primary_key = [
                    ("thread_id", "STRING"),
                    ("checkpoint_ns", "STRING"),
                    ("checkpoint_id", "STRING"),
                ]
                table_meta = TableMeta(self.table_name, schema_of_primary_key)
                table_options = TableOptions()
                reserved_throughput = ReservedThroughput(CapacityUnit(0, 0))
                self.client.create_table(table_meta, table_options, reserved_throughput)
            else:
                raise

    def _setup_store_table(self) -> None:
        """Create the store table if it doesn't exist."""
        try:
            self.client.describe_table(self.store_table_name)
            logger.info(f"Store table {self.store_table_name} already exists")
        except OTSServiceError as e:
            if e.get_error_code() == "OTSObjectNotExist":
                logger.info(f"Creating store table {self.store_table_name}")
                # Primary key schema for store table
                schema_of_primary_key = [
                    ("namespace", "STRING"),
                    ("key", "STRING"),
                ]
                table_meta = TableMeta(self.store_table_name, schema_of_primary_key)
                table_options = TableOptions()
                reserved_throughput = ReservedThroughput(CapacityUnit(0, 0))
                self.client.create_table(table_meta, table_options, reserved_throughput)
            else:
                raise

    def _serialize_checkpoint(self, checkpoint: Checkpoint) -> Dict[str, Any]:
        """Serialize a checkpoint to a dictionary suitable for Tablestore."""
        return {
            "v": checkpoint.get("v"),
            "ts": checkpoint.get("ts"),
            "id": checkpoint.get("id"),
            "channel_values": orjson.dumps(checkpoint.get("channel_values", {})).decode(),
            "channel_versions": orjson.dumps(checkpoint.get("channel_versions", {})).decode(),
            "versions_seen": orjson.dumps(checkpoint.get("versions_seen", {})).decode(),
            "pending_sends": orjson.dumps(checkpoint.get("pending_sends", [])).decode(),
        }

    def _deserialize_checkpoint(self, data: Dict[str, Any]) -> Checkpoint:
        """Deserialize a checkpoint from Tablestore data."""
        checkpoint_data = {
            "v": data.get("v"),
            "ts": data.get("ts"),
            "id": data.get("id"),
            "channel_values": orjson.loads(data.get("channel_values", "{}")),
            "channel_versions": orjson.loads(data.get("channel_versions", "{}")),
            "versions_seen": orjson.loads(data.get("versions_seen", "{}")),
            "pending_sends": orjson.loads(data.get("pending_sends", "[]")),
        }
        return checkpoint_data  # type: ignore

    def _serialize_metadata(self, metadata: CheckpointMetadata) -> Dict[str, Any]:
        """Serialize checkpoint metadata."""
        return {
            "source": metadata.get("source"),
            "step": metadata.get("step"),
            "writes": orjson.dumps(metadata.get("writes", {})).decode(),
            "parents": orjson.dumps(metadata.get("parents", {})).decode(),
        }

    def _deserialize_metadata(self, data: Dict[str, Any]) -> CheckpointMetadata:
        """Deserialize checkpoint metadata."""
        metadata_data = {
            "source": data.get("source"),
            "step": data.get("step"),
            "writes": orjson.loads(data.get("writes", "{}")),
            "parents": orjson.loads(data.get("parents", "{}")),
        }
        return metadata_data  # type: ignore

    def put(
        self,
        config: RunnableConfig,
        checkpoint: Checkpoint,
        metadata: CheckpointMetadata,
        new_versions: dict,
    ) -> RunnableConfig:
        """Store a checkpoint in Tablestore."""
        thread_id = config.get("configurable", {}).get("thread_id")
        checkpoint_ns = config.get("configurable", {}).get("checkpoint_ns", "")
        checkpoint_id = checkpoint.get("id")
        
        if not thread_id or not checkpoint_id:
            raise ValueError("thread_id and checkpoint_id are required")

        # Serialize checkpoint and metadata
        checkpoint_data = self._serialize_checkpoint(checkpoint)
        metadata_data = self._serialize_metadata(metadata)

        # Combine all data
        all_data = {**checkpoint_data, **metadata_data}

        # Create row
        primary_key = [
            ("thread_id", thread_id),
            ("checkpoint_ns", checkpoint_ns),
            ("checkpoint_id", checkpoint_id),
        ]
        
        attribute_columns = []
        for key, value in all_data.items():
            if value is not None:
                attribute_columns.append((key, value))

        row = Row(primary_key, attribute_columns)

        # Put row to table
        try:
            self.client.put_row(self.table_name, row)
            logger.debug(f"Stored checkpoint {checkpoint_id} for thread {thread_id}")
        except Exception as e:
            logger.error(f"Failed to store checkpoint: {e}")
            raise

        return config

    def get(self, config: RunnableConfig) -> Optional[Checkpoint]:
        """Retrieve a checkpoint from Tablestore."""
        thread_id = config.get("configurable", {}).get("thread_id")
        checkpoint_ns = config.get("configurable", {}).get("checkpoint_ns", "")
        checkpoint_id = config.get("configurable", {}).get("checkpoint_id")

        if not thread_id:
            return None

        if not checkpoint_id:
            # Get the latest checkpoint
            checkpoints = list(self.list(config, limit=1))
            if not checkpoints:
                return None
            return checkpoints[0].checkpoint

        # Get specific checkpoint
        primary_key = [
            ("thread_id", thread_id),
            ("checkpoint_ns", checkpoint_ns),
            ("checkpoint_id", checkpoint_id),
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

            return self._deserialize_checkpoint(data)
        except Exception as e:
            logger.error(f"Failed to retrieve checkpoint: {e}")
            return None

    def list(
        self,
        config: RunnableConfig,
        *,
        filter: Optional[Dict[str, Any]] = None,
        before: Optional[RunnableConfig] = None,
        limit: Optional[int] = None,
    ) -> Iterator["CheckpointTuple"]:
        """List checkpoints from Tablestore."""
        thread_id = config.get("configurable", {}).get("thread_id")
        checkpoint_ns = config.get("configurable", {}).get("checkpoint_ns", "")

        if not thread_id:
            return

        # Build range query
        inclusive_start_primary_key = [
            ("thread_id", thread_id),
            ("checkpoint_ns", checkpoint_ns),
            ("checkpoint_id", ""),
        ]
        exclusive_end_primary_key = [
            ("thread_id", thread_id),
            ("checkpoint_ns", checkpoint_ns + "\x00"),
            ("checkpoint_id", ""),
        ]

        try:
            consumed, next_start_primary_key, row_list, next_token = self.client.get_range(
                self.table_name,
                "FORWARD",
                inclusive_start_primary_key,
                exclusive_end_primary_key,
                limit=limit or 100,
            )

            for row in row_list:
                # Extract primary key values
                pk_dict = {pk[0]: pk[1] for pk in row.primary_key}
                
                # Convert attributes to dict
                attr_dict = {}
                for attr in row.attribute_columns:
                    attr_dict[attr[0]] = attr[1]

                # Deserialize checkpoint and metadata
                checkpoint = self._deserialize_checkpoint(attr_dict)
                metadata = self._deserialize_metadata(attr_dict)

                # Create config for this checkpoint
                checkpoint_config = {
                    "configurable": {
                        "thread_id": pk_dict["thread_id"],
                        "checkpoint_ns": pk_dict["checkpoint_ns"],
                        "checkpoint_id": pk_dict["checkpoint_id"],
                    }
                }

                yield CheckpointTuple(
                    config=checkpoint_config, # type: ignore
                    checkpoint=checkpoint,
                    metadata=metadata,
                    parent_config=None,
                )

        except Exception as e:
            logger.error(f"Failed to list checkpoints: {e}")
            return

    def put_writes(
        self,
        config: RunnableConfig,
        writes: List[Tuple[str, Any]],
        task_id: str,
    ) -> None:
        """Store writes for a checkpoint."""
        # This is typically used for streaming updates
        # For now, we'll implement a simple version
        pass

    def get_tuple(self, config: RunnableConfig) -> Optional["CheckpointTuple"]:
        """Get a checkpoint tuple (checkpoint + metadata)."""
        checkpoint = self.get(config)
        if not checkpoint:
            return None

        # TODO: Implement proper metadata retrieval
        metadata = {}  # type: ignore
        
        return CheckpointTuple(
            config=config,
            checkpoint=checkpoint,
            metadata=metadata, # type: ignore
            parent_config=None,
        )


# Import the CheckpointTuple from the correct location
try:
    from langgraph.checkpoint.base import CheckpointTuple # type: ignore
except ImportError:
    # Fallback for older versions
    from typing import NamedTuple
    
    class CheckpointTuple(NamedTuple):
        config: RunnableConfig
        checkpoint: Checkpoint
        metadata: CheckpointMetadata
        parent_config: Optional[RunnableConfig] = None 