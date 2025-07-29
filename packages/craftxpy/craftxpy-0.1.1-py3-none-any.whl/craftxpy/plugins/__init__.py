"""CraftX.py Plugins Module

This module contains the plugin system and base plugin functionality.
"""

from .base import BasePlugin
from .codegeex4 import CodeGeeX4Plugin
from .commandr7b import CommandR7BPlugin
from .qwen25coder import Qwen25CoderPlugin
from .wizardcoder import WizardCoderPlugin

__all__ = [
    'BasePlugin',
    'CodeGeeX4Plugin', 
    'CommandR7BPlugin',
    'Qwen25CoderPlugin',
    'WizardCoderPlugin'
]