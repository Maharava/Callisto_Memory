import os
import json
from pathlib import Path
from typing import Dict, Any, Optional, List

def ensure_directory_exists(directory_path: str) -> None:
    """Ensures that the specified directory exists, creating it if necessary."""
    Path(directory_path).mkdir(parents=True, exist_ok=True)

def read_json_file(file_path: str) -> Optional[Dict[str, Any]]:
    """Reads and returns the contents of a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        # If the file exists but isn't valid JSON, return None
        return None

def write_json_file(file_path: str, data: Dict[str, Any]) -> None:
    """Writes data to a JSON file."""
    ensure_directory_exists(os.path.dirname(file_path))
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2)

def read_text_file(file_path: str) -> Optional[str]:
    """Reads and returns the contents of a text file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return None

def write_text_file(file_path: str, text: str, mode: str = 'w') -> None:
    """Writes text to a file."""
    ensure_directory_exists(os.path.dirname(file_path))
    with open(file_path, mode, encoding='utf-8') as file:
        file.write(text)

def list_files(directory_path: str, extension: Optional[str] = None) -> List[str]:
    """Lists all files in a directory with an optional extension filter."""
    ensure_directory_exists(directory_path)
    files = []
    for file in os.listdir(directory_path):
        if extension and not file.endswith(extension):
            continue
        files.append(file)
    return files

def delete_file(file_path: str) -> bool:
    """Deletes a file if it exists."""
    try:
        os.remove(file_path)
        return True
    except FileNotFoundError:
        return False