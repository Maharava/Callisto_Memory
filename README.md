# Callisto

A memory management system for the Jupiter AI home companion that provides structured storage for user data and conversation history.

## Features

- **User Management**: Create, read, update, and delete user profiles with structured data
- **Conversation Storage**: Save and retrieve conversation logs with timestamps
- **Multi-user Support**: Store shared conversations across multiple user profiles
- **Data Organization**: Categorize and structure user information systematically
- **Minimal Dependencies**: Simple file-based storage with no external database requirements

## Installation

```bash
# Install directly from source
pip install .

# For development
pip install -e .
```

## Usage

Import Callisto in your Python code:

```python
from src.callisto import Callisto

# Initialize with default data directory
memory = Callisto()

# Create a user
user_id = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
memory.create_user(user_id, {"name": "Alex", "preferences": {"theme": "dark"}})

# Store a conversation
memory.store_conversation(user_id, "daily_check_in", 
    "User: How are things today?\nJupiter: Everything is running smoothly.")

# Retrieve user data
user_data = memory.get_user_data(user_id)
```

See the API documentation for a complete reference of available methods.

Data Storage
All data is stored in the configured data directory (default: ./data):

User data: ./data/users/<uuid>.json
Conversation logs: ./data/logs/<uuid>/<conversation_name>.txt