"""
Prompt Gear - YAML-powered prompt manager with multi-backend support.
"""

__version__ = "0.1.0"

from .schema import PromptTemplate
from .manager import PromptManager
from .core import BackendBase, PromptNotFoundError, PromptAlreadyExistsError
from .config import get_config, reload_config

# Import backends with optional dependencies
from .filesystem_backend import FilesystemBackend
from .sqlite_backend import SQLiteBackend

try:
    from .postgres_backend import PostgresBackend
except ImportError:
    PostgresBackend = None

__all__ = [
    "PromptTemplate",
    "PromptManager", 
    "BackendBase",
    "PromptNotFoundError",
    "PromptAlreadyExistsError",
    "get_config",
    "reload_config",
    "FilesystemBackend",
    "SQLiteBackend",
]

if PostgresBackend:
    __all__.append("PostgresBackend")
