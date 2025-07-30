"""
Claude Code Indexer - Code indexing tool using Ensmallen graph database
"""

__version__ = "1.0.1"
__author__ = "Claude AI Assistant"
__email__ = "noreply@anthropic.com"

from .indexer import CodeGraphIndexer
from .cli import main

__all__ = ["CodeGraphIndexer", "main"]