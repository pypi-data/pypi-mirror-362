"""CraftX.py Memory Storage

Storage management for memory systems.
"""

from typing import Any, Dict, List, Optional
import json
import os
from datetime import datetime

class MemoryStorage:
    """Storage manager for memory data."""
    
    def __init__(self, storage_path: str = "./memory_storage"):
        """Initialize memory storage.
        
        Args:
            storage_path: Path to storage directory
        """
        self.storage_path = storage_path
        self.memory_data: Dict[str, Any] = {}
        
        os.makedirs(storage_path, exist_ok=True)
        self.load_memory()
    
    def store(self, key: str, data: Any, metadata: Optional[Dict] = None) -> bool:
        """Store data with optional metadata.
        
        Args:
            key: Storage key
            data: Data to store
            metadata: Optional metadata
            
        Returns:
            Success status
        """
        try:
            entry = {
                "data": data,
                "metadata": metadata or {},
                "timestamp": datetime.now().isoformat()
            }
            self.memory_data[key] = entry
            return self.save_memory()
        except Exception:
            return False
    
    def retrieve(self, key: str) -> Optional[Any]:
        """Retrieve data by key.
        
        Args:
            key: Storage key
            
        Returns:
            Stored data or None if not found
        """
        entry = self.memory_data.get(key)
        return entry["data"] if entry else None
    
    def get_metadata(self, key: str) -> Optional[Dict]:
        """Get metadata for a key.
        
        Args:
            key: Storage key
            
        Returns:
            Metadata or None if not found
        """
        entry = self.memory_data.get(key)
        return entry["metadata"] if entry else None
    
    def list_keys(self) -> List[str]:
        """List all storage keys.
        
        Returns:
            List of available keys
        """
        return list(self.memory_data.keys())
    
    def delete(self, key: str) -> bool:
        """Delete data by key.
        
        Args:
            key: Storage key
            
        Returns:
            Success status
        """
        if key in self.memory_data:
            del self.memory_data[key]
            return self.save_memory()
        return False
    
    def load_memory(self) -> bool:
        """Load memory data from storage.
        
        Returns:
            Success status
        """
        try:
            memory_file = os.path.join(self.storage_path, "memory.json")
            if os.path.exists(memory_file):
                with open(memory_file, 'r', encoding='utf-8') as f:
                    self.memory_data = json.load(f)
            return True
        except Exception:
            self.memory_data = {}
            return False
    
    def save_memory(self) -> bool:
        """Save memory data to storage.
        
        Returns:
            Success status
        """
        try:
            memory_file = os.path.join(self.storage_path, "memory.json")
            with open(memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.memory_data, f, indent=2)
            return True
        except Exception:
            return False