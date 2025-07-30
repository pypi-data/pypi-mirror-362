"""Tablestore-based checkpoint implementation for LangGraph."""

import logging
from datetime import datetime
from typing import Any, Dict, Iterator, List, Optional, Tuple, Sequence

import orjson
from langgraph.checkpoint.base import ChannelVersions
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.base import BaseCheckpointSaver, Checkpoint, CheckpointMetadata
from tablestore import OTSClient, Row # type: ignore
from tablestore.metadata import TableMeta, TableOptions, ReservedThroughput, CapacityUnit, Condition, PutRowItem, BatchWriteRowRequest, TableInBatchWriteRowItem # type: ignore
from tablestore.error import OTSServiceError # type: ignore

logger = logging.getLogger(__name__)


class TablestoreSaver(BaseCheckpointSaver):
    """Tablestore-based checkpoint saver for LangGraph."""

    def __init__(
        self,
        client: OTSClient,
        table_name: str = "checkpoints",
        **kwargs: Any,
    ) -> None:
        """Initialize the TablestoreSaver.

        Args:
            client: The Tablestore client instance.
            table_name: Name of the table to store checkpoints.
            **kwargs: Additional arguments.
        """
        super().__init__(**kwargs)
        self.client = client
        self.table_name = table_name
        self._setup_tables()

    def _setup_tables(self) -> None:
        """Setup the required tables for checkpoints and store."""
        self._setup_checkpoint_table()

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
                # Construct the schema information of the table.
                table_meta = TableMeta(self.table_name, schema_of_primary_key)
                # Construct the configuration information of the table.
                table_options = TableOptions(time_to_live=-1, max_version=1, max_time_deviation=86400, allow_update=True)
                # Reserved read and write throughput, with a default value of 0.
                # (Only high-performance instances in CU mode support setting non-zero reserved throughput for a table.)
                reserved_throughput = ReservedThroughput(CapacityUnit(0, 0))
                self.client.create_table(table_meta, table_options, reserved_throughput)
                logger.info(f"Created checkpoint table {self.table_name}")

                # logger.info(f"Creating checkpoint table checkpoint_writes")
                # # Construct the schema information of the table.
                # checkpoint_writes_table_meta = TableMeta("checkpoint_writes", schema_of_primary_key)
                # self.client.create_table(checkpoint_writes_table_meta, table_options, reserved_throughput)
                # logger.info(f"Created checkpoint table checkpoint_writes")
            else:
                logger.error(f"Failed to create checkpoint table {self.table_name}")
                raise

    # def _serialize_checkpoint(self, checkpoint: Checkpoint) -> Dict[str, Any]:
    #     """Serialize a checkpoint to a dictionary suitable for Tablestore."""
    #     return {
    #         "v": checkpoint.get("v"),
    #         "ts": checkpoint.get("ts"),
    #         "id": checkpoint.get("id"),
    #         "channel_values": orjson.dumps(checkpoint.get("channel_values", {})).decode(),
    #         "channel_versions": orjson.dumps(checkpoint.get("channel_versions", {})).decode(),
    #         "versions_seen": orjson.dumps(checkpoint.get("versions_seen", {})).decode(),
    #         "pending_sends": orjson.dumps(checkpoint.get("pending_sends", [])).decode(),
    #     }

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

    # def _serialize_metadata(self, metadata: CheckpointMetadata) -> Dict[str, Any]:
    #     """Serialize checkpoint metadata."""
    #     return {
    #         "source": metadata.get("source"),
    #         "step": metadata.get("step"),
    #         "writes": orjson.dumps(metadata.get("writes", {})).decode(),
    #         "parents": orjson.dumps(metadata.get("parents", {})).decode(),
    #     }

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
        new_versions: ChannelVersions,
    ) -> RunnableConfig:
        """Save a checkpoint to the database.

        This method saves a checkpoint to the Tablestore database. The checkpoint is associated
        with the provided config and its parent config (if any).

        Args:
            config: The config to associate with the checkpoint.
            checkpoint: The checkpoint to save.
            metadata: Additional metadata to save with the checkpoint.
            new_versions: New channel versions as of this write.

        Returns:
            RunnableConfig: Updated configuration after storing the checkpoint.
        """
        thread_id = config.get("configurable", {}).get("thread_id")
        checkpoint_ns = config.get("configurable", {}).get("checkpoint_ns", "")
        checkpoint_id = checkpoint.get("id")

        if not thread_id or not checkpoint_id:
            raise ValueError("thread_id and checkpoint_id are required")

        # Serialize checkpoint and metadata
        type1, serialized_checkpoint = self.serde.dumps_typed(checkpoint)
        type2, serialized_metadata = self.serde.dumps_typed(metadata)
        print(f"serialized_checkpoint: {serialized_checkpoint}")
        if type1 != type2:
            raise ValueError(
                "Failed to serialize checkpoint and metadata to the same type."
            )

        # Create row
        primary_key = [
            ("thread_id", thread_id),
            ("checkpoint_ns", checkpoint_ns),
            ("checkpoint_id", checkpoint_id),
        ]

        attribute_columns = [
            ("parent_checkpoint_id", config.get("configurable", {}).get("checkpoint_id")),
            ("type", type1),
            ("checkpoint", serialized_checkpoint),
            ("metadata", serialized_metadata),
            ("created_at", datetime.now()),
        ]

        row = Row(primary_key, attribute_columns)

        # Put row to table
        try:
            # Check row existence
            condition = Condition("IGNORE")
            self.client.put_row(self.table_name, row, condition)
            logger.debug(f"Stored checkpoint {checkpoint_id} for thread {thread_id}")
        except Exception as e:
            logger.error(f"Failed to store checkpoint: {e}")
            raise

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
        writes: Sequence[tuple[str, Any]],
        task_id: str,
        task_path: str = "",
    ) -> None:
        """Store intermediate writes linked to a checkpoint.

        This method saves intermediate writes associated with a checkpoint to the Tablestore database.

        Args:
            config: Configuration of the related checkpoint.
            writes: List of writes to store.
            task_id: Identifier for the task creating the writes.
        """
        thread_id = config.get("configurable", {}).get("thread_id")
        checkpoint_ns = config.get("configurable", {}).get("checkpoint_ns", "")
        checkpoint_id = config.get("configurable", {}).get("checkpoint_id", "")

        if not thread_id or not checkpoint_id:
            raise ValueError("thread_id and checkpoint_id are required")

        put_row_items = []

        for idx, (channel, value) in enumerate(writes):
            type_, value_data = self.serde.dumps_typed(value)

            primary_key = [
                ("thread_id", thread_id),
                ("checkpoint_ns", checkpoint_ns),
                ("checkpoint_id", checkpoint_id),
            ]

            attribute_columns = [
                ("task_id", task_id),
                ("idx", idx),
                ("channel", channel),
                ("type", type_),
                ("value_data", value_data),
                ("task_path", task_path),
                ("created_at", datetime.now()),
            ]

            row = Row(primary_key, attribute_columns)
            condition = Condition("IGNORE")
            item = PutRowItem(row, condition)
            put_row_items.append(item)
        
        request = BatchWriteRowRequest()
        request.add(TableInBatchWriteRowItem("checkpoint_writes", put_row_items))

        try:
            result = self.client.batch_write_row(request)
            logger.debug(f"Result status: {result.is_all_succeed()}")    
        except Exception as e:
            logger.error(f"Failed to store checkpoint writes: {e}")
            raise


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
