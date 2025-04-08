import os
import json
import uuid
import re
from datetime import datetime
from typing import Dict, Any, List, Optional, Union

from .file_utils import (
    ensure_directory_exists,
    read_json_file,
    write_json_file,
    list_files,
    delete_file
)

class UserStore:
    """Class for managing user data storage."""
    
    def __init__(self, data_dir: str = "data"):
        """Initialize the UserStore with the data directory."""
        self.users_dir = f"{data_dir}/users"
        ensure_directory_exists(self.users_dir)
    
    def _is_valid_uuid(self, uuid_string: str) -> bool:
        """Check if the given string is a valid UUID."""
        uuid_pattern = re.compile(
            r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', 
            re.IGNORECASE
        )
        return bool(uuid_pattern.match(uuid_string))
    
    def get_user_file_path(self, uuid_string: str) -> str:
        """Get the file path for a user's data."""
        if not self._is_valid_uuid(uuid_string):
            raise ValueError(f"Invalid UUID: {uuid_string}")
        
        return f"{self.users_dir}/{uuid_string}.json"
    
    def user_exists(self, uuid_string: str) -> bool:
        """Check if a user with the given UUID exists."""
        if not self._is_valid_uuid(uuid_string):
            return False
        return os.path.exists(self.get_user_file_path(uuid_string))
    
    def get_user_data(self, uuid_string: str) -> Optional[Dict[str, Any]]:
        """Get the data for a user."""
        if not self._is_valid_uuid(uuid_string):
            raise ValueError(f"Invalid UUID: {uuid_string}")
        
        file_path = self.get_user_file_path(uuid_string)
        return read_json_file(file_path)
    
    def create_user(self, uuid_string: str, initial_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a new user with optional initial data."""
        if not self._is_valid_uuid(uuid_string):
            raise ValueError(f"Invalid UUID: {uuid_string}")
        
        if self.user_exists(uuid_string):
            raise ValueError(f"User already exists: {uuid_string}")
        
        now = datetime.now().strftime("%Y-%m-%d")
        
        user_data = {
            "uuid": uuid_string,
            "created": now,
            "last_modified": now
        }
        
        if initial_data:
            # Don't allow overriding uuid, created
            for key in ["uuid", "created"]:
                if key in initial_data:
                    del initial_data[key]
            user_data.update(initial_data)
        
        file_path = self.get_user_file_path(uuid_string)
        write_json_file(file_path, user_data)
        
        return user_data
    
    def update_user(self, uuid_string: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a user's data."""
        if not self._is_valid_uuid(uuid_string):
            raise ValueError(f"Invalid UUID: {uuid_string}")
        
        if not self.user_exists(uuid_string):
            raise ValueError(f"User does not exist: {uuid_string}")
        
        user_data = self.get_user_data(uuid_string)
        
        # Update the last_modified timestamp
        now = datetime.now().strftime("%Y-%m-%d")
        user_data["last_modified"] = now
        
        # Update the user data with the new data
        for key, value in data.items():
            if key in ["uuid", "created"]:
                continue  # Don't allow updating these fields
            user_data[key] = value
        
        file_path = self.get_user_file_path(uuid_string)
        write_json_file(file_path, user_data)
        
        return user_data
    
    def update_category_field(self, uuid_string: str, category: str, field: str, value: Any) -> Dict[str, Any]:
        """Update a field within a category in the user's data."""
        if not self._is_valid_uuid(uuid_string):
            raise ValueError(f"Invalid UUID: {uuid_string}")
        
        if not self.user_exists(uuid_string):
            raise ValueError(f"User does not exist: {uuid_string}")
        
        user_data = self.get_user_data(uuid_string)
        now = datetime.now().strftime("%Y-%m-%d")
        
        # Create category if it doesn't exist
        if category not in user_data:
            user_data[category] = {}
        
        # Ensure the category is a dictionary
        if not isinstance(user_data[category], dict):
            raise ValueError(f"{category} is not a dictionary in user data")
        
        # Format the value with date_added if needed
        if isinstance(value, dict) and "value" in value:
            if "date_added" not in value:
                value["date_added"] = now
            user_data[category][field] = value
        else:
            user_data[category][field] = {
                "value": value,
                "date_added": now
            }
        
        # Update last_modified timestamps
        user_data[category]["last_modified"] = now
        user_data["last_modified"] = now
        
        file_path = self.get_user_file_path(uuid_string)
        write_json_file(file_path, user_data)
        
        return user_data
    
    def add_to_list(self, uuid_string: str, list_name: str, value: Any) -> Dict[str, Any]:
        """Add an item to a list in the user's data."""
        if not self._is_valid_uuid(uuid_string):
            raise ValueError(f"Invalid UUID: {uuid_string}")
        
        if not self.user_exists(uuid_string):
            raise ValueError(f"User does not exist: {uuid_string}")
        
        user_data = self.get_user_data(uuid_string)
        now = datetime.now().strftime("%Y-%m-%d")
        
        # Create the list if it doesn't exist
        if list_name not in user_data:
            user_data[list_name] = []
        
        # Ensure it's a list
        if not isinstance(user_data[list_name], list):
            raise ValueError(f"{list_name} is not a list in user data")
        
        # Add the value with date_added
        if isinstance(value, dict) and "value" in value:
            if "date_added" not in value:
                value["date_added"] = now
            user_data[list_name].append(value)
        else:
            entry = {
                "value": value,
                "date_added": now
            }
            user_data[list_name].append(entry)
        
        # Update the last_modified timestamp
        user_data["last_modified"] = now
        
        file_path = self.get_user_file_path(uuid_string)
        write_json_file(file_path, user_data)
        
        return user_data
    
    def delete_user(self, uuid_string: str) -> bool:
        """Delete a user's data file."""
        if not self._is_valid_uuid(uuid_string):
            raise ValueError(f"Invalid UUID: {uuid_string}")
        
        file_path = self.get_user_file_path(uuid_string)
        return delete_file(file_path)
    
    def merge_users(self, source_uuid: str, target_uuid: str) -> Dict[str, Any]:
        """
        Merge data from the source user to the target user.
        After merging, the source user data is deleted.
        """
        if not self._is_valid_uuid(source_uuid) or not self._is_valid_uuid(target_uuid):
            raise ValueError(f"Invalid UUID provided")
        
        if source_uuid == target_uuid:
            raise ValueError("Source and target UUIDs must be different")
        
        if not self.user_exists(source_uuid):
            raise ValueError(f"Source user does not exist: {source_uuid}")
        
        # Create target user if it doesn't exist
        if not self.user_exists(target_uuid):
            self.create_user(target_uuid)
        
        source_data = self.get_user_data(source_uuid)
        target_data = self.get_user_data(target_uuid)
        
        # Merge data
        merged_data = self._merge_user_data(source_data, target_data)
        
        # Update the target user
        file_path = self.get_user_file_path(target_uuid)
        write_json_file(file_path, merged_data)
        
        # Delete the source user
        self.delete_user(source_uuid)
        
        return merged_data
    
    def _merge_user_data(self, source_data: Dict[str, Any], target_data: Dict[str, Any]) -> Dict[str, Any]:
        """Merge source user data into target user data."""
        result = target_data.copy()
        now = datetime.now().strftime("%Y-%m-%d")
        result["last_modified"] = now
        
        # Loop through each key in source_data
        for key, value in source_data.items():
            # Skip UUID and created date
            if key in ["uuid", "created"]:
                continue
            
            # Handle different data types
            if key not in result:
                # If the key doesn't exist in target, copy it directly
                result[key] = value
            elif isinstance(value, list) and isinstance(result[key], list):
                # Merge lists, avoiding duplicates by value field
                existing_values = [item.get("value") for item in result[key] 
                                  if isinstance(item, dict) and "value" in item]
                
                for item in value:
                    if isinstance(item, dict) and "value" in item and item["value"] not in existing_values:
                        result[key].append(item)
                        existing_values.append(item["value"])
            elif isinstance(value, dict) and isinstance(result[key], dict):
                # Handle nested dictionaries
                for field, field_value in value.items():
                    if field == "last_modified":
                        result[key]["last_modified"] = now
                    elif field not in result[key] or field == "total_conversations":
                        # Copy missing fields or add conversation counts
                        if field == "total_conversations":
                            result[key][field] = result[key].get(field, 0) + value.get(field, 0)
                        else:
                            result[key][field] = field_value
                    elif isinstance(field_value, dict) and "date_added" in field_value:
                        # For fields with date_added, keep the newer one
                        if "date_added" in result[key][field]:
                            if field_value["date_added"] > result[key][field]["date_added"]:
                                result[key][field] = field_value
                    elif isinstance(field_value, list) and isinstance(result[key][field], list):
                        # For nested lists (like recent_topics), merge and sort
                        combined = result[key][field] + field_value
                        if field == "recent_topics" and all("date_discussed" in item for item in combined):
                            combined.sort(key=lambda x: x["date_discussed"], reverse=True)
                            result[key][field] = combined[:10]  # Keep only 10 most recent
                        else:
                            result[key][field] = combined
        
        return result
    
    def list_users(self) -> List[str]:
        """List all user UUIDs."""
        files = list_files(self.users_dir, ".json")
        return [file.replace(".json", "") for file in files]