import os
import re
import shutil
from datetime import datetime
from typing import List, Optional, Set

from .file_utils import (
    ensure_directory_exists,
    read_text_file,
    write_text_file,
    list_files,
    delete_file
)

class ConversationStore:
    """Class for managing conversation log storage."""
    
    def __init__(self, data_dir: str = "data"):
        """Initialize the ConversationStore with the data directory."""
        self.logs_dir = f"{data_dir}/logs"
        ensure_directory_exists(self.logs_dir)
    
    def _is_valid_uuid(self, uuid_string: str) -> bool:
        """Check if the given string is a valid UUID."""
        uuid_pattern = re.compile(
            r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', 
            re.IGNORECASE
        )
        return bool(uuid_pattern.match(uuid_string))
    
    def get_user_logs_dir(self, uuid_string: str) -> str:
        """Get the directory for a user's logs."""
        if not self._is_valid_uuid(uuid_string):
            raise ValueError(f"Invalid UUID: {uuid_string}")
        
        user_logs_dir = f"{self.logs_dir}/{uuid_string}"
        ensure_directory_exists(user_logs_dir)
        return user_logs_dir
    
    def get_log_file_path(self, uuid_string: str, log_name: str) -> str:
        """Get the file path for a specific log."""
        user_logs_dir = self.get_user_logs_dir(uuid_string)
        
        # Ensure log_name has .txt extension
        if not log_name.endswith(".txt"):
            log_name = f"{log_name}.txt"
        
        return f"{user_logs_dir}/{log_name}"
    
    def log_exists(self, uuid_string: str, log_name: str) -> bool:
        """Check if a log file exists."""
        if not self._is_valid_uuid(uuid_string):
            return False
            
        log_path = self.get_log_file_path(uuid_string, log_name)
        return os.path.exists(log_path)
    
    def store_conversation(self, uuid_string: str, log_name: str, content: str) -> str:
        """Store a conversation log for a user."""
        if not self._is_valid_uuid(uuid_string):
            raise ValueError(f"Invalid UUID: {uuid_string}")
        
        log_path = self.get_log_file_path(uuid_string, log_name)
        
        # Add timestamp header if it doesn't already have one
        if not content.strip().startswith("==="):
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            header = f"=== Conversation started on {now} ===\n\n"
            content = f"{header}{content}"
        
        write_text_file(log_path, content)
        return log_path
    
    def append_to_conversation(self, uuid_string: str, log_name: str, 
                              message: str, with_timestamp: bool = True) -> str:
        """Append a message to a conversation log."""
        if not self._is_valid_uuid(uuid_string):
            raise ValueError(f"Invalid UUID: {uuid_string}")
        
        log_path = self.get_log_file_path(uuid_string, log_name)
        
        # Create log if it doesn't exist
        if not os.path.exists(log_path):
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            header = f"=== Conversation started on {now} ===\n\n"
            write_text_file(log_path, header)
        
        # Format message with timestamp if needed
        if with_timestamp:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            formatted_message = f"[{now}] {message}\n"
        else:
            formatted_message = f"{message}\n"
        
        # Append to the file
        with open(log_path, 'a', encoding='utf-8') as file:
            file.write(formatted_message)
        
        return log_path
    
    def get_conversation(self, uuid_string: str, log_name: str) -> Optional[str]:
        """Get the content of a conversation log."""
        if not self._is_valid_uuid(uuid_string):
            raise ValueError(f"Invalid UUID: {uuid_string}")
        
        log_path = self.get_log_file_path(uuid_string, log_name)
        return read_text_file(log_path)
    
    def list_conversations(self, uuid_string: str) -> List[str]:
        """List all conversation logs for a user."""
        if not self._is_valid_uuid(uuid_string):
            raise ValueError(f"Invalid UUID: {uuid_string}")
        
        user_logs_dir = self.get_user_logs_dir(uuid_string)
        files = list_files(user_logs_dir, ".txt")
        return [file.replace(".txt", "") for file in files]
    
    def delete_conversation(self, uuid_string: str, log_name: str) -> bool:
        """Delete a conversation log."""
        if not self._is_valid_uuid(uuid_string):
            raise ValueError(f"Invalid UUID: {uuid_string}")
        
        log_path = self.get_log_file_path(uuid_string, log_name)
        return delete_file(log_path)
    
    def store_multi_user_conversation(self, uuids: List[str], log_name: str, content: str) -> List[str]:
        """Store a conversation log for multiple users."""
        if not uuids:
            raise ValueError("At least one UUID is required")
        
        # Validate UUIDs
        for uuid_string in uuids:
            if not self._is_valid_uuid(uuid_string):
                raise ValueError(f"Invalid UUID: {uuid_string}")
        
        paths = []
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Add multi-user header if it doesn't already have one
        if not content.strip().startswith("==="):
            header = f"=== Multi-user conversation started on {now} ===\n"
            header += f"=== Participants: {', '.join(uuids)} ===\n\n"
            content = f"{header}{content}"
        
        # Store in each user's directory
        for uuid_string in uuids:
            log_path = self.get_log_file_path(uuid_string, log_name)
            write_text_file(log_path, content)
            paths.append(log_path)
        
        return paths
    
    def move_conversations(self, source_uuid: str, target_uuid: str) -> List[str]:
        """
        Move all conversations from source user to target user.
        Used when merging users.
        """
        if not self._is_valid_uuid(source_uuid) or not self._is_valid_uuid(target_uuid):
            raise ValueError(f"Invalid UUID provided")
        
        if source_uuid == target_uuid:
            raise ValueError("Source and target UUIDs must be different")
        
        source_dir = self.get_user_logs_dir(source_uuid)
        target_dir = self.get_user_logs_dir(target_uuid)
        
        moved_logs = []
        
        # List all logs in source directory
        logs = list_files(source_dir, ".txt")
        
        for log_name in logs:
            source_path = f"{source_dir}/{log_name}"
            target_path = f"{target_dir}/{log_name}"
            
            # If target already has a log with same name, rename the source log
            if os.path.exists(target_path):
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                base_name = log_name.replace(".txt", "")
                new_log_name = f"{base_name}_merged_{timestamp}.txt"
                target_path = f"{target_dir}/{new_log_name}"
            
            # Copy source to target
            shutil.copy2(source_path, target_path)
            moved_logs.append(target_path)
            
            # Delete the source log
            os.remove(source_path)
        
        return moved_logs
    
    def prune_conversation(self, uuid_string: str, log_name: str, 
                         keep_lines: Optional[int] = None, 
                         start_date: Optional[str] = None,
                         end_date: Optional[str] = None) -> bool:
        """
        Prune a conversation log by keeping only a certain number of lines
        or entries between specific dates.
        """
        if not self._is_valid_uuid(uuid_string):
            raise ValueError(f"Invalid UUID: {uuid_string}")
        
        if not self.log_exists(uuid_string, log_name):
            return False
        
        log_path = self.get_log_file_path(uuid_string, log_name)
        content = read_text_file(log_path)
        
        if not content:
            return False
        
        lines = content.split('\n')
        header_lines = []
        conversation_lines = []
        
        # Separate header from conversation
        in_header = True
        for line in lines:
            if in_header:
                header_lines.append(line)
                if line.strip() == "":
                    in_header = False
            else:
                conversation_lines.append(line)
        
        # Apply pruning filters
        if keep_lines is not None:
            conversation_lines = conversation_lines[-keep_lines:]
        
        if start_date or end_date:
            filtered_lines = []
            for line in conversation_lines:
                # Check if line has a timestamp
                timestamp_match = re.match(r'\[([\d-]+ [\d:]+)\]', line)
                if timestamp_match:
                    line_date = timestamp_match.group(1)
                    if start_date and line_date < start_date:
                        continue
                    if end_date and line_date > end_date:
                        continue
                filtered_lines.append(line)
            conversation_lines = filtered_lines
        
        # Combine header and pruned conversation
        pruned_content = '\n'.join(header_lines + conversation_lines)
        write_text_file(log_path, pruned_content)
        
        return True