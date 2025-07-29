"""CraftX.py Logger Module

Logging and memory management for AI assistant interactions.
"""

import logging
from typing import Any, Dict, List

class Logger:
    """Enhanced logger with memory capabilities."""
    
    def __init__(self, name: str = "craftxpy"):
        """Initialize the logger.
        
        Args:
            name: Logger name
        """
        self.name = name
        self.logger = logging.getLogger(name)
        self.memory: List[Dict[str, Any]] = []
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def log(self, level: str, message: str, **kwargs) -> None:
        """Log a message and store in memory.
        
        Args:
            level: Log level (info, warning, error, debug)
            message: Message to log
            **kwargs: Additional metadata
        """
        # Store in memory
        log_entry = {
            "level": level,
            "message": message,
            "metadata": kwargs
        }
        self.memory.append(log_entry)
        
        # Log to standard logger
        log_method = getattr(self.logger, level.lower(), self.logger.info)
        log_method(message)
    
    def info(self, message: str, **kwargs) -> None:
        """Log info message."""
        self.log("info", message, **kwargs)
    
    def warning(self, message: str, **kwargs) -> None:
        """Log warning message."""
        self.log("warning", message, **kwargs)
    
    def error(self, message: str, **kwargs) -> None:
        """Log error message."""
        self.log("error", message, **kwargs)
    
    def debug(self, message: str, **kwargs) -> None:
        """Log debug message."""
        self.log("debug", message, **kwargs)
    
    def get_memory(self) -> List[Dict[str, Any]]:
        """Get stored log memory.
        
        Returns:
            List of log entries
        """
        return self.memory.copy()
    
    def clear_memory(self) -> None:
        """Clear stored log memory."""
        self.memory.clear()
