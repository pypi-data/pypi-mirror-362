"""CraftX.py Large Storage Manager

Utilities for managing large storage operations.
"""

from typing import Any, Dict, List, Optional
import os

class LargeStorageManager:
    """Manager for large storage operations."""
    
    def __init__(self, storage_path: str = "./storage"):
        """Initialize the storage manager.
        
        Args:
            storage_path: Base storage path
        """
        self.storage_path = storage_path
        self.name = "LargeStorageManager"
        self.version = "0.1.2"
        
        # Ensure storage directory exists
        os.makedirs(storage_path, exist_ok=True)
    
    def store_data(self, key: str, data: Any) -> bool:
        """Store data with a key.
        
        Args:
            key: Storage key
            data: Data to store
            
        Returns:
            Success status
        """
        try:
            filepath = os.path.join(self.storage_path, f"{key}.data")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(data))
            return True
        except Exception:
            return False
    
    def retrieve_data(self, key: str) -> Optional[str]:
        """Retrieve data by key.
        
        Args:
            key: Storage key
            
        Returns:
            Stored data or None if not found
        """
        try:
            filepath = os.path.join(self.storage_path, f"{key}.data")
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            return None
    
    def list_keys(self) -> List[str]:
        """List all storage keys.
        
        Returns:
            List of available keys
        """
        try:
            files = os.listdir(self.storage_path)
            return [f.replace('.data', '') for f in files if f.endswith('.data')]
        except Exception:
            return []