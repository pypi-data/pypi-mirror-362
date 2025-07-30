"""Basic usage example for LangGraph with Tablestore Checkpoint and Store."""

import os

import tablestore # type: ignore
from typing import TypedDict
from langgraph.graph import StateGraph
from langgraph.checkpoint.tablestore import TablestoreSaver
from langgraph.store.tablestore import TablestoreStore # type: ignore

# Tablestore configuration
# You can set these environment variables or replace with your values
TABLESTORE_ENDPOINT = os.getenv("TABLESTORE_ENDPOINT", "https://your-instance.cn-hangzhou.ots.aliyuncs.com")
TABLESTORE_ACCESS_KEY_ID = os.getenv("TABLESTORE_ACCESS_KEY_ID", "your-access-key-id")
TABLESTORE_ACCESS_KEY_SECRET = os.getenv("TABLESTORE_ACCESS_KEY_SECRET", "your-access-key-secret")
TABLESTORE_INSTANCE_NAME = os.getenv("TABLESTORE_INSTANCE_NAME", "your-instance-name")

def create_tablestore_client():
    """Create a Tablestore client."""
    return tablestore.OTSClient(TABLESTORE_ENDPOINT, TABLESTORE_ACCESS_KEY_ID, TABLESTORE_ACCESS_KEY_SECRET, TABLESTORE_INSTANCE_NAME)

def basic_checkpoint_example():
    """Basic example of using TablestoreSaver."""
    # Create Tablestore client
    client = create_tablestore_client()
    
    # Create checkpoint saver
    checkpoint_saver = TablestoreSaver(client)
    
    # Define a simple state using TypedDict
    class State(TypedDict):
        value: int
    
    # Define a simple node function
    def increment(state: State) -> State:
        return {"value": state["value"] + 1}
    
    # Create graph with checkpoint
    graph = StateGraph(State)
    graph.add_node("increment", increment)
    graph.set_entry_point("increment")
    graph.set_finish_point("increment")
    
    # Compile with checkpoint
    app = graph.compile(checkpointer=checkpoint_saver)
    
    # Configure thread
    config = {"configurable": {"thread_id": "example-thread-5"}}
    
    # Run the graph
    initial_state: State = {"value": 0}
    result = app.invoke(initial_state, config) # type: ignore
    
    print(f"Result: {result['value']}")
    print("Checkpoint saved successfully!")

def basic_store_example():
    """Basic example of using TablestoreStore."""
    # Create Tablestore client
    client = create_tablestore_client()
    
    # Create store
    store = TablestoreStore(client) # type: ignore
    
    # Store some data
    store.put("user_sessions", "user_123", {"name": "Alice", "age": 30})
    store.put("user_sessions", "user_456", {"name": "Bob", "age": 25})
    store.put("app_config", "theme", "dark")
    store.put("app_config", "language", "en")
    
    # Retrieve data
    user_data = store.get("user_sessions", "user_123")
    print(f"User data: {user_data}")
    
    theme = store.get("app_config", "theme")
    print(f"Theme: {theme}")
    
    # List data in namespace
    print("\nAll user sessions:")
    for key, value in store.list("user_sessions"):
        print(f"  {key}: {value}")
    
    # List all namespaces
    print("\nAll namespaces:")
    for namespace in store.list_namespaces():
        print(f"  {namespace}")

def comprehensive_example():
    """Comprehensive example using both checkpoint and store."""
    # Create Tablestore client
    client = create_tablestore_client()
    
    # Create checkpoint saver and store
    checkpoint_saver = TablestoreSaver(client, table_name="my_checkpoints")
    store = TablestoreStore(client, table_name="my_store") # type: ignore
    
    # Define a state that uses both checkpoint and store
    class ChatState:
        def __init__(self, message: str = "", history: list = None):  # type: ignore
            self.message = message
            self.history = history or []
    
    def process_message(state: ChatState) -> ChatState:
        # Simulate processing
        response = f"Response to: {state.message}"
        new_history = state.history + [state.message, response]
        return ChatState(response, new_history)
    
    def save_to_store(state: ChatState) -> ChatState:
        # Save conversation history to store
        store.put("conversations", "latest", state.history)
        return state
    
    # Create graph
    graph = StateGraph(ChatState)
    graph.add_node("process", process_message)
    graph.add_node("save", save_to_store)
    graph.set_entry_point("process")
    graph.add_edge("process", "save")
    graph.set_finish_point("save")
    
    # Compile with checkpoint
    app = graph.compile(checkpointer=checkpoint_saver)
    
    # Configure thread
    config = {"configurable": {"thread_id": "chat-thread-1"}}
    
    # Simulate conversation
    messages = ["Hello", "How are you?", "What's the weather like?"]
    
    for msg in messages:
        print(f"User: {msg}")
        state = ChatState(msg)
        result = app.invoke(state, config) # type: ignore
        print(f"Bot: {result.message}") # type: ignore
    
    # Retrieve conversation history from store
    history = store.get("conversations", "latest")
    print(f"\nConversation history: {history}")

if __name__ == "__main__":
    print("=== Basic Checkpoint Example ===")
    try:
        basic_checkpoint_example()
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n=== Basic Store Example ===")
    try:
        basic_store_example()
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n=== Comprehensive Example ===")
    try:
        comprehensive_example()
    except Exception as e:
        print(f"Error: {e}") 