import os
from datetime import datetime
from typing import Dict, Any, List, Optional, Union

from .user_store import UserStore
from .conversation_store import ConversationStore
from .file_utils import ensure_directory_exists

class Callisto:
    """
    Main class for the Callisto memory management system.
    This serves as the primary interface for Jupiter to interact with.
    """
    
    def __init__(self, data_dir: str = "data"):
        """Initialize Callisto with the data directory."""
        self.data_dir = data_dir
        ensure_directory_exists(data_dir)
        
        # Initialize stores
        self.user_store = UserStore(data_dir)
        self.conversation_store = ConversationStore(data_dir)
    
    #
    # User Data Management
    #
    
    def get_user_data(self, uuid: str) -> Optional[Dict[str, Any]]:
        """Get a user's data."""
        return self.user_store.get_user_data(uuid)
    
    def user_exists(self, uuid: str) -> bool:
        """Check if a user exists."""
        return self.user_store.user_exists(uuid)
    
    def create_user(self, uuid: str, initial_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a new user with optional initial data."""
        return self.user_store.create_user(uuid, initial_data)
    
    def update_user(self, uuid: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a user's data."""
        return self.user_store.update_user(uuid, data)
    
    def update_user_field(self, uuid: str, category: str, field: str, value: Any) -> Dict[str, Any]:
        """Update a specific field within a category in a user's data."""
        return self.user_store.update_category_field(uuid, category, field, value)
    
    def add_to_user_list(self, uuid: str, list_name: str, value: Any) -> Dict[str, Any]:
        """Add an item to a list in the user's data."""
        return self.user_store.add_to_list(uuid, list_name, value)
    
    def delete_user(self, uuid: str) -> bool:
        """Delete a user's data."""
        return self.user_store.delete_user(uuid)
    
    def list_users(self) -> List[str]:
        """List all user UUIDs."""
        return self.user_store.list_users()
    
    def merge_users(self, source_uuid: str, target_uuid: str) -> Dict[str, Any]:
        """
        Merge data from source user into target user.
        Also merges conversation logs.
        """
        # First, merge user data
        result = self.user_store.merge_users(source_uuid, target_uuid)
        
        # Then, move conversation logs
        self.conversation_store.move_conversations(source_uuid, target_uuid)
        
        return result
    
    #
    # Conversation Management
    #
    
    def get_conversation(self, uuid: str, log_name: str) -> Optional[str]:
        """Get a conversation log."""
        return self.conversation_store.get_conversation(uuid, log_name)
    
    def store_conversation(self, uuid: str, log_name: str, content: str) -> str:
        """Store a conversation log."""
        return self.conversation_store.store_conversation(uuid, log_name, content)
    
    def append_to_conversation(self, uuid: str, log_name: str, 
                              message: str, with_timestamp: bool = True) -> str:
        """Append a message to a conversation log."""
        return self.conversation_store.append_to_conversation(
            uuid, log_name, message, with_timestamp
        )
    
    def store_multi_user_conversation(self, uuids: List[str], log_name: str, content: str) -> List[str]:
        """Store a conversation log for multiple users."""
        # Verify all UUIDs exist, creating any that don't
        for uuid in uuids:
            if not self.user_exists(uuid):
                self.create_user(uuid)
        
        return self.conversation_store.store_multi_user_conversation(uuids, log_name, content)
    
    def list_conversations(self, uuid: str) -> List[str]:
        """List all conversation logs for a user."""
        return self.conversation_store.list_conversations(uuid)
    
    def delete_conversation(self, uuid: str, log_name: str) -> bool:
        """Delete a conversation log."""
        return self.conversation_store.delete_conversation(uuid, log_name)
    
    def prune_conversation(self, uuid: str, log_name: str, 
                         keep_lines: Optional[int] = None,
                         start_date: Optional[str] = None,
                         end_date: Optional[str] = None) -> bool:
        """Prune a conversation log."""
        return self.conversation_store.prune_conversation(
            uuid, log_name, keep_lines, start_date, end_date
        )