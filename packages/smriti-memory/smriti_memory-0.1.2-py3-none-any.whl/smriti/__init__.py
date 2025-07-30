"""
Smriti Memory - An intelligent memory layer for AI applications with RAG capabilities.

This package provides a sophisticated memory system that can store, retrieve, and update
contextual information for AI applications using vector databases and LLM-powered decision making.
"""

__version__ = "0.1.2"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .memory_manager import MemoryManager
from .config import (
    MemoryConfig, 
    EmbeddingProviderConfig, 
    VectorStoreConfig, 
    LLMProviderConfig,
    create_openai_config,
    create_local_config,
    create_cloud_config
)
from .exceptions import SmritiError, MemoryError, ConfigurationError, EmbeddingError, VectorDBError, LLMError
from .embeddings import EmbeddingManager, EmbeddingConfig
from .vector_stores import VectorStoreManager, VectorDBConfig, MemoryRecord

# Import framework adapters with graceful fallback
try:
    from .framework_adapters import (
        SmritiLangChainMemory,
        SmritiLlamaIndexMemory, 
        SmritiMemoryBuffer,
        create_langchain_memory,
        create_llamaindex_memory,
        create_universal_memory
    )
    FRAMEWORK_ADAPTERS_AVAILABLE = True
except ImportError:
    FRAMEWORK_ADAPTERS_AVAILABLE = False

__all__ = [
    "MemoryManager",
    "MemoryConfig",
    "EmbeddingProviderConfig",
    "VectorStoreConfig", 
    "LLMProviderConfig",
    "EmbeddingManager",
    "EmbeddingConfig",
    "VectorStoreManager",
    "VectorDBConfig",
    "MemoryRecord",
    "SmritiError",
    "MemoryError",
    "ConfigurationError",
    "EmbeddingError",
    "VectorDBError", 
    "LLMError",
    "create_openai_config",
    "create_local_config",
    "create_cloud_config",
    "__version__",
]

# Add framework adapters to exports if available
if FRAMEWORK_ADAPTERS_AVAILABLE:
    __all__.extend([
        "SmritiLangChainMemory",
        "SmritiLlamaIndexMemory",
        "SmritiMemoryBuffer", 
        "create_langchain_memory",
        "create_llamaindex_memory",
        "create_universal_memory"
    ]) 