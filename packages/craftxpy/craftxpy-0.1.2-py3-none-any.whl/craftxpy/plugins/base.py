"""CraftX.py Base Plugin Module

Base plugin class and plugin system for extensible AI assistants.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class BasePlugin(ABC):
    """Base class for all CraftX.py plugins."""
    
    def __init__(self, name: str, version: str = "1.0.0"):
        """Initialize the plugin.
        
        Args:
            name: Plugin name
            version: Plugin version
        """
        self.name = name
        self.version = version
        self.enabled = True
        self.config: Dict[str, Any] = {}
    
    @abstractmethod
    def execute(self, input_data: Any, **kwargs) -> Any:
        """Execute the plugin functionality.
        
        Args:
            input_data: Input data to process
            **kwargs: Additional parameters
            
        Returns:
            Processed output
        """
        pass
    
    def configure(self, config: Dict[str, Any]) -> None:
        """Configure the plugin.
        
        Args:
            config: Configuration dictionary
        """
        self.config.update(config)
    
    def enable(self) -> None:
        """Enable the plugin."""
        self.enabled = True
    
    def disable(self) -> None:
        """Disable the plugin."""
        self.enabled = False
    
    def get_info(self) -> Dict[str, Any]:
        """Get plugin information.
        
        Returns:
            Plugin information dictionary
        """
        return {
            "name": self.name,
            "version": self.version,
            "enabled": self.enabled,
            "config": self.config
        }


class DemoPlugin(BasePlugin):
    """Demo plugin for testing purposes."""
    
    def __init__(self):
        """Initialize the demo plugin."""
        super().__init__("Demo Plugin", "0.1.2")
    
    def execute(self, input_data: Any, **kwargs) -> str:
        """Execute demo functionality.
        
        Args:
            input_data: Input data
            **kwargs: Additional parameters
            
        Returns:
            Demo response
        """
        return f"Demo plugin processed: {input_data}"
