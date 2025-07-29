"""CraftX.py - Advanced AI-Powered Assistant Framework

CraftX.py is a modular, extensible framework for building AI-powered assistants
with plugin support, memory management, and advanced routing capabilities.

Key Features:
- Multiple AI model support (Ollama integration)
- Plugin-based architecture
- Memory management and logging
- Tool integration system
- Web-based assistant UI

Example Usage:
    from craftxpy.agents import Router
    from craftxpy.plugins.base import BasePlugin
    
    router = Router()
    # Use the router to manage AI assistant interactions
"""

__version__ = "0.1.1"
__author__ = "CraftX.py Team"
__description__ = "Advanced AI-Powered Assistant Framework"

# Import key components for easy access
from .agents import Router
from .plugins.base import BasePlugin
from .memory import Logger
from .utils import PageBuilder, ShellExecutor

__all__ = [
    'Router',
    'BasePlugin', 
    'Logger',
    'PageBuilder',
    'ShellExecutor',
    '__version__',
    '__author__',
    '__description__'
]