# 🌀 Eidosian seed of the package – minimal, universal, ever-evolving! 🌱

"""
Ollama Forge - Python client library and CLI for Ollama

This package provides a comprehensive set of helpers for interacting with Ollama,
following all ten Eidosian principles for elegant, efficient, and effective code.

Key Features:
- Complete API coverage
- Synchronous and asynchronous interfaces
- Smart model fallbacks
- CLI helpers
- Embedding utilities
"""

import os
import warnings
from typing import Dict, Any, TypeVar, Type, cast

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📦 Version and Configuration - Adaptive Loading
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Use variables for constants to avoid redefinition issues
_version = "0.1.9"  # Fallback version
_author = "Lloyd Handyside, Eidos"
_email = "ace1928@gmail.com, syntheticeidos@gmail.com"
_ollama_api_url = "http://localhost:11434"
_chat_model = "deepseek-r1:1.5b"      # Best small model for chat
_backup_chat_model = "qwen2.5:0.5b-Instruct"  # Excellent fallback
_embedding_model = _chat_model  # Using chat model for embeddings improves context
_backup_embedding_model = _backup_chat_model  # Same fallback for embeddings

# First attempt to import from centralized config
try:
    from .config import (
        VERSION as __version__, 
        get_version_string,
        get_author_string,
        get_email_string,
        DEFAULT_OLLAMA_API_URL,
        DEFAULT_CHAT_MODEL,
        BACKUP_CHAT_MODEL,
        DEFAULT_EMBEDDING_MODEL,
        BACKUP_EMBEDDING_MODEL
    )
    __author__ = get_author_string()
    __email__ = get_email_string()
    
    # Update our variables with imported values
    _version = __version__
    _author = __author__
    _email = __email__
    _ollama_api_url = DEFAULT_OLLAMA_API_URL
    _chat_model = DEFAULT_CHAT_MODEL
    _backup_chat_model = BACKUP_CHAT_MODEL
    _embedding_model = DEFAULT_EMBEDDING_MODEL
    _backup_embedding_model = BACKUP_EMBEDDING_MODEL
    
except ImportError:
    # Fallback to direct imports if config not available
    try:
        import importlib.util
        
        # Try to find and import version.py from the main package directory
        spec = importlib.util.find_spec('version')
        if spec and spec.loader:  # Ensure loader is not None before accessing exec_module
            version_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(version_module)
            __version__ = version_module.__version__
            get_version_string = version_module.get_version_string
            _version = __version__
        else:
            # Last resort fallback for standalone use
            __version__ = _version
            get_version_string = lambda: _version
    except ImportError:
        # Last resort fallback if all else fails
        __version__ = _version
        get_version_string = lambda: _version
        
    # Package metadata fallbacks
    __author__ = _author
    __email__ = _email

# License and URL information
__license__ = "MIT"
__url__ = "https://github.com/Ace1928/ollama_forge"
__description__ = "Python client library and CLI for Ollama"

# Functions to access constants instead of exposing them directly
# This prevents constant redefinition while keeping the API consistent
def get_default_api_url() -> str: return _ollama_api_url
def get_default_chat_model() -> str: return _chat_model
def get_backup_chat_model() -> str: return _backup_chat_model
def get_default_embedding_model() -> str: return _embedding_model
def get_backup_embedding_model() -> str: return _backup_embedding_model

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🧰 Core Components - Elegant Import Strategy
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Type definition for client classes
T = TypeVar('T')
ClientType = Type[T]  # Represents a client class type

# Define placeholders for components that might fail to import
class ComponentNotAvailable:
    """Placeholder for components that could not be loaded."""
    def __init__(self, name: str, error: Exception):
        self.name = name
        self.error = error
        
    def __call__(self, *args: Any, **kwargs: Any) -> None:
        raise ImportError(f"'{self.name}' is not available: {self.error}")

# Core components with smart import handling
try:
    from .client import OllamaClient
except ImportError as e:
    OllamaClient = cast(Any, ComponentNotAvailable("OllamaClient", e))

# Use placeholder for missing AsyncOllamaClient to avoid import error
try:
    # Import commented out until module is implemented
    # from .async_client import AsyncOllamaClient
    # Use placeholder until real implementation is available
    AsyncOllamaClient = cast(Any, ComponentNotAvailable(
        "AsyncOllamaClient", 
        ImportError("Async client not yet implemented")
    ))
except ImportError as e:
    AsyncOllamaClient = cast(Any, ComponentNotAvailable("AsyncOllamaClient", e))

# Dictionary to hold exception classes for proper typing and direct access
error_classes: Dict[str, Type[Exception]] = {}

# Load exception classes individually to avoid unused import warnings
try:
    # Import each exception class individually and store in our dictionary
    from .exceptions import OllamaAPIError
    error_classes["OllamaAPIError"] = OllamaAPIError
    
    from .exceptions import OllamaConnectionError
    error_classes["OllamaConnectionError"] = OllamaConnectionError
    
    from .exceptions import OllamaModelNotFoundError
    error_classes["OllamaModelNotFoundError"] = OllamaModelNotFoundError
    
    from .exceptions import OllamaServerError
    error_classes["OllamaServerError"] = OllamaServerError
    
    from .exceptions import ConnectionError
    error_classes["ConnectionError"] = ConnectionError
    
    from .exceptions import TimeoutError
    error_classes["TimeoutError"] = TimeoutError
    
    from .exceptions import ModelNotFoundError
    error_classes["ModelNotFoundError"] = ModelNotFoundError
    
    from .exceptions import ServerError
    error_classes["ServerError"] = ServerError
    
    from .exceptions import InvalidRequestError
    error_classes["InvalidRequestError"] = InvalidRequestError
    
    from .exceptions import StreamingError
    error_classes["StreamingError"] = StreamingError
    
    from .exceptions import ParseError
    error_classes["ParseError"] = ParseError
except ImportError as e:
    warnings.warn(f"Exception classes could not be imported: {e}")

# Re-export exceptions at module level for backwards compatibility
for name, cls in error_classes.items():
    globals()[name] = cls

# Define what's available when importing * from this package
# Explicitly list all exported symbols to avoid reportUnsupportedDunderAll
__all__ = [
    'OllamaClient', 'AsyncOllamaClient', '__version__', 'get_version_string',
    'get_default_api_url', 'get_default_chat_model', 'get_backup_chat_model',
    'get_default_embedding_model', 'get_backup_embedding_model',
    
    # Explicitly list all error classes
    'OllamaAPIError', 'OllamaConnectionError', 'OllamaModelNotFoundError', 
    'OllamaServerError', 'ConnectionError', 'TimeoutError', 'ModelNotFoundError',
    'ServerError', 'InvalidRequestError', 'StreamingError', 'ParseError'
]

# Debug mode detection
if os.environ.get('OLLAMA_FORGE_DEBUG') == '1':
    print(f"🔍 Ollama Forge v{__version__} loaded and ready")
    print(f"  - Client available: {'✅' if not isinstance(OllamaClient, ComponentNotAvailable) else '❌'}")
    print(f"  - Async client available: {'✅' if not isinstance(AsyncOllamaClient, ComponentNotAvailable) else '❌'}")
    print(f"  - Default model: {get_default_chat_model()}")

