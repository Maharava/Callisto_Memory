# API Documentation for Callisto

## Overview
This document provides documentation for the Callisto memory management system API. It includes method signatures, descriptions, parameters, return values, and examples for all available methods that Jupiter can use.

## Initialization

```python
from src.callisto import Callisto

# Initialize with default data directory ("data")
callisto = Callisto()

# Or specify a custom data directory
callisto = Callisto(data_dir="custom_data_path")
```

## User Data Management

### `get_user_data(uuid: str) -> Optional[Dict[str, Any]]`
- **Description**: Gets a user's data.
- **Parameters**:
  - `uuid`: String UUID of the user.
- **Returns**: Dictionary containing user data or None if user doesn't exist.
- **Example**:
  ```python
  user_data = callisto.get_user_data("a1b2c3d4-e5f6-7890-abcd-ef1234567890")
  ```

### `user_exists(uuid: str) -> bool`
- **Description**: Checks if a user exists.
- **Parameters**:
  - `uuid`: String UUID of the user.
- **Returns**: True if user exists, False otherwise.
- **Example**:
  ```python
  if callisto.user_exists("a1b2c3d4-e5f6-7890-abcd-ef1234567890"):
      print("User exists!")
  ```

### `create_user(uuid: str, initial_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]`
- **Description**: Creates a new user with optional initial data.
- **Parameters**:
  - `uuid`: String UUID for the new user.
  - `initial_data`: Optional dictionary of initial user data.
- **Returns**: Dictionary containing the created user data.
- **Example**:
  ```python
  initial_data = {
      "profile": {
          "name": "Alex",
          "preferred_name": "Alex"
      }
  }
  user_data = callisto.create_user("a1b2c3d4-e5f6-7890-abcd-ef1234567890", initial_data)
  ```

### `update_user(uuid: str, data: Dict[str, Any]) -> Dict[str, Any]`
- **Description**: Updates a user's data.
- **Parameters**:
  - `uuid`: String UUID of the user.
  - `data`: Dictionary of data to update.
- **Returns**: Dictionary containing the updated user data.
- **Example**:
  ```python
  updated_data = {
      "preferences": {
          "theme": "dark"
      }
  }
  user_data = callisto.update_user("a1b2c3d4-e5f6-7890-abcd-ef1234567890", updated_data)
  ```

### `update_user_field(uuid: str, category: str, field: str, value: Any) -> Dict[str, Any]`
- **Description**: Updates a specific field within a category in a user's data.
- **Parameters**:
  - `uuid`: String UUID of the user.
  - `category`: Category name to update.
  - `field`: Field name within the category.
  - `value`: New value for the field.
- **Returns**: Dictionary containing the updated user data.
- **Example**:
  ```python
  user_data = callisto.update_user_field(
      "a1b2c3d4-e5f6-7890-abcd-ef1234567890", 
      "profile", 
      "birthday", 
      "1988-06-22"
  )
  ```

### `add_to_user_list(uuid: str, list_name: str, value: Any) -> Dict[str, Any]`
- **Description**: Adds an item to a list in the user's data.
- **Parameters**:
  - `uuid`: String UUID of the user.
  - `list_name`: Name of the list to add to.
  - `value`: Value to add to the list.
- **Returns**: Dictionary containing the updated user data.
- **Example**:
  ```python
  user_data = callisto.add_to_user_list(
      "a1b2c3d4-e5f6-7890-abcd-ef1234567890", 
      "likes", 
      "python programming"
  )
  ```

### `delete_user(uuid: str) -> bool`
- **Description**: Deletes a user's data.
- **Parameters**:
  - `uuid`: String UUID of the user to delete.
- **Returns**: True if deletion was successful, False otherwise.
- **Example**:
  ```python
  success = callisto.delete_user("a1b2c3d4-e5f6-7890-abcd-ef1234567890")
  ```

### `list_users() -> List[str]`
- **Description**: Lists all user UUIDs.
- **Returns**: List of string UUIDs.
- **Example**:
  ```python
  users = callisto.list_users()
  for user_id in users:
      print(user_id)
  ```

### `merge_users(source_uuid: str, target_uuid: str) -> Dict[str, Any]`
- **Description**: Merges data from source user into target user.
- **Parameters**:
  - `source_uuid`: UUID of the source user.
  - `target_uuid`: UUID of the target user.
- **Returns**: Dictionary containing the merged user data.
- **Example**:
  ```python
  merged_data = callisto.merge_users(
      "old-uuid-a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "new-uuid-f9e8d7c6-b5a4-3210-fedc-ba9876543210"
  )
  ```

## Conversation Management

### `get_conversation(uuid: str, log_name: str) -> Optional[str]`
- **Description**: Gets a conversation log.
- **Parameters**:
  - `uuid`: String UUID of the user.
  - `log_name`: Name of the conversation log.
- **Returns**: String content of the conversation or None if not found.
- **Example**:
  ```python
  conversation = callisto.get_conversation(
      "a1b2c3d4-e5f6-7890-abcd-ef1234567890", 
      "daily_check_in"
  )
  ```

### `store_conversation(uuid: str, log_name: str, content: str) -> str`
- **Description**: Stores a conversation log.
- **Parameters**:
  - `uuid`: String UUID of the user.
  - `log_name`: Name for the conversation log.
  - `content`: String content of the conversation.
- **Returns**: String path to the stored log file.
- **Example**:
  ```python
  file_path = callisto.store_conversation(
      "a1b2c3d4-e5f6-7890-abcd-ef1234567890", 
      "project_discussion", 
      "User: Let's discuss the project\nJupiter: Sure, what aspects would you like to focus on?"
  )
  ```

### `append_to_conversation(uuid: str, log_name: str, message: str, with_timestamp: bool = True) -> str`
- **Description**: Appends a message to a conversation log.
- **Parameters**:
  - `uuid`: String UUID of the user.
  - `log_name`: Name of the conversation log.
  - `message`: Message to append.
  - `with_timestamp`: Whether to include timestamp (default: True).
- **Returns**: String path to the log file.
- **Example**:
  ```python
  file_path = callisto.append_to_conversation(
      "a1b2c3d4-e5f6-7890-abcd-ef1234567890", 
      "daily_check_in", 
      "User: I completed the task we discussed yesterday."
  )
  ```

### `store_multi_user_conversation(uuids: List[str], log_name: str, content: str) -> List[str]`
- **Description**: Stores a conversation log for multiple users.
- **Parameters**:
  - `uuids`: List of user UUIDs.
  - `log_name`: Name for the conversation log.
  - `content`: String content of the conversation.
- **Returns**: List of file paths where the conversation was stored.
- **Example**:
  ```python
  file_paths = callisto.store_multi_user_conversation(
      ["uuid1-a1b2c3d4", "uuid2-f9e8d7c6"], 
      "group_chat", 
      "User1: Hi everyone\nUser2: Hello\nJupiter: Good afternoon all"
  )
  ```

### `list_conversations(uuid: str) -> List[str]`
- **Description**: Lists all conversation logs for a user.
- **Parameters**:
  - `uuid`: String UUID of the user.
- **Returns**: List of conversation log names.
- **Example**:
  ```python
  logs = callisto.list_conversations("a1b2c3d4-e5f6-7890-abcd-ef1234567890")
  for log in logs:
      print(log)
  ```

### `delete_conversation(uuid: str, log_name: str) -> bool`
- **Description**: Deletes a conversation log.
- **Parameters**:
  - `uuid`: String UUID of the user.
  - `log_name`: Name of the conversation log to delete.
- **Returns**: True if deletion was successful, False otherwise.
- **Example**:
  ```python
  success = callisto.delete_conversation(
      "a1b2c3d4-e5f6-7890-abcd-ef1234567890", 
      "old_chat"
  )
  ```

### `prune_conversation(uuid: str, log_name: str, keep_lines: Optional[int] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> bool`
- **Description**: Prunes a conversation log.
- **Parameters**:
  - `uuid`: String UUID of the user.
  - `log_name`: Name of the conversation log.
  - `keep_lines`: Optional number of lines to keep from the end.
  - `start_date`: Optional start date filter (format: "YYYY-MM-DD").
  - `end_date`: Optional end date filter (format: "YYYY-MM-DD").
- **Returns**: True if pruning was successful, False otherwise.
- **Example**:
  ```python
  # Keep only the most recent 50 lines
  success = callisto.prune_conversation(
      "a1b2c3d4-e5f6-7890-abcd-ef1234567890", 
      "long_conversation", 
      keep_lines=50
  )
  
  # Keep only messages between specified dates
  success = callisto.prune_conversation(
      "a1b2c3d4-e5f6-7890-abcd-ef1234567890", 
      "project_discussion", 
      start_date="2025-03-01", 
      end_date="2025-03-15"
  )
  ```

## Error Handling
All methods will raise appropriate exceptions with descriptive error messages when invalid parameters are provided or operations cannot be completed.