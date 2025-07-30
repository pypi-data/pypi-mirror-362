"""Basic tests for TablestoreCheckpoint and TablestoreStore."""

import os
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from unittest.mock import Mock, MagicMock
from tablestore import OTSClient
from langgraph_checkpoint_tablestore import TablestoreCheckpoint, TablestoreStore


class TestTablestoreCheckpoint:
    """Test TablestoreCheckpoint functionality."""

    def test_init(self):
        """Test TablestoreCheckpoint initialization."""
        mock_client = Mock(spec=OTSClient)
        mock_client.describe_table.side_effect = Exception("Table not found")
        mock_client.create_table = Mock()
        
        checkpoint = TablestoreCheckpoint(mock_client)
        
        assert checkpoint.client == mock_client
        assert checkpoint.table_name == "langgraph_checkpoints"
        assert checkpoint.store_table_name == "langgraph_store"

    def test_serialize_checkpoint(self):
        """Test checkpoint serialization."""
        mock_client = Mock(spec=OTSClient)
        mock_client.describe_table.side_effect = Exception("Table not found")
        mock_client.create_table = Mock()
        
        checkpoint = TablestoreCheckpoint(mock_client)
        
        test_checkpoint = {
            "v": 1,
            "ts": "2023-01-01T00:00:00Z",
            "id": "test-id",
            "channel_values": {"key": "value"},
            "channel_versions": {"key": 1},
            "versions_seen": {"key": 1},
            "pending_sends": [],
        }
        
        serialized = checkpoint._serialize_checkpoint(test_checkpoint)
        
        assert serialized["v"] == 1
        assert serialized["ts"] == "2023-01-01T00:00:00Z"
        assert serialized["id"] == "test-id"
        assert '"key":"value"' in serialized["channel_values"]

    def test_deserialize_checkpoint(self):
        """Test checkpoint deserialization."""
        mock_client = Mock(spec=OTSClient)
        mock_client.describe_table.side_effect = Exception("Table not found")
        mock_client.create_table = Mock()
        
        checkpoint = TablestoreCheckpoint(mock_client)
        
        test_data = {
            "v": 1,
            "ts": "2023-01-01T00:00:00Z",
            "id": "test-id",
            "channel_values": '{"key":"value"}',
            "channel_versions": '{"key":1}',
            "versions_seen": '{"key":1}',
            "pending_sends": '[]',
        }
        
        deserialized = checkpoint._deserialize_checkpoint(test_data)
        
        assert deserialized["v"] == 1
        assert deserialized["ts"] == "2023-01-01T00:00:00Z"
        assert deserialized["id"] == "test-id"
        assert deserialized["channel_values"] == {"key": "value"}


class TestTablestoreStore:
    """Test TablestoreStore functionality."""

    def test_init(self):
        """Test TablestoreStore initialization."""
        mock_client = Mock(spec=OTSClient)
        mock_client.describe_table.side_effect = Exception("Table not found")
        mock_client.create_table = Mock()
        
        store = TablestoreStore(mock_client)
        
        assert store.client == mock_client
        assert store.table_name == "langgraph_store"

    def test_serialize_value(self):
        """Test value serialization."""
        mock_client = Mock(spec=OTSClient)
        mock_client.describe_table.side_effect = Exception("Table not found")
        mock_client.create_table = Mock()
        
        store = TablestoreStore(mock_client)
        
        test_value = {"key": "value", "number": 42}
        serialized = store._serialize_value(test_value)
        
        assert isinstance(serialized, str)
        assert "key" in serialized
        assert "value" in serialized
        assert "42" in serialized

    def test_deserialize_value(self):
        """Test value deserialization."""
        mock_client = Mock(spec=OTSClient)
        mock_client.describe_table.side_effect = Exception("Table not found")
        mock_client.create_table = Mock()
        
        store = TablestoreStore(mock_client)
        
        test_data = '{"key":"value","number":42}'
        deserialized = store._deserialize_value(test_data)
        
        assert deserialized == {"key": "value", "number": 42}

    def test_put_get_delete(self):
        """Test basic put/get/delete operations."""
        mock_client = Mock(spec=OTSClient)
        mock_client.describe_table.side_effect = Exception("Table not found")
        mock_client.create_table = Mock()
        
        # Mock put_row
        mock_client.put_row = Mock()
        
        # Mock get_row
        mock_return_row = Mock()
        mock_return_row.attribute_columns = [("value", '{"test":"data"}')]
        mock_client.get_row.return_value = (None, mock_return_row, None)
        
        # Mock delete_row
        mock_client.delete_row = Mock()
        
        store = TablestoreStore(mock_client)
        
        # Test put
        store.put("namespace1", "key1", {"test": "data"})
        mock_client.put_row.assert_called_once()
        
        # Test get
        result = store.get("namespace1", "key1")
        assert result == {"test": "data"}
        
        # Test delete
        store.delete("namespace1", "key1")
        mock_client.delete_row.assert_called_once()

    def test_get_nonexistent(self):
        """Test getting non-existent key."""
        mock_client = Mock(spec=OTSClient)
        mock_client.describe_table.side_effect = Exception("Table not found")
        mock_client.create_table = Mock()
        
        # Mock get_row returning None
        mock_client.get_row.return_value = (None, None, None)
        
        store = TablestoreStore(mock_client)
        result = store.get("namespace1", "nonexistent")
        
        assert result is None


if __name__ == "__main__":
    # Run basic tests
    test_checkpoint = TestTablestoreCheckpoint()
    test_checkpoint.test_init()
    test_checkpoint.test_serialize_checkpoint()
    test_checkpoint.test_deserialize_checkpoint()
    print("TablestoreCheckpoint tests passed!")
    
    test_store = TestTablestoreStore()
    test_store.test_init()
    test_store.test_serialize_value()
    test_store.test_deserialize_value()
    test_store.test_put_get_delete()
    test_store.test_get_nonexistent()
    print("TablestoreStore tests passed!")
    
    print("All tests passed!") 