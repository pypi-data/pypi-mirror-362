"""
Unified search module for tool filtering and vector storage
"""

import os
import logging
from typing import Optional

from .base import BaseToolFilter, Tool
from .bm25_filter import BM25Filter
from .local_embedding_filter import LocalEmbeddingFilter
from .cloud_filter import CloudFilter
from .cloud_infrastructure import VectorStoreManager

logger = logging.getLogger(__name__)


def create_filter(
    filter_type: str = None,
    vector_store_manager: Optional[VectorStoreManager] = None,
    sync_tools: bool = False,
    **kwargs
) -> BaseToolFilter:
    """
    Create a tool filter instance
    
    Args:
        filter_type: Type of filter to create. Options:
            - "bm25": Fast BM25 keyword search (default, no dependencies)
            - "local_embedding": Local semantic search using fastembed
            - "cloud": Cloud hybrid search using Pinecone (semantic + BM25)
        vector_store_manager: Optional vector store manager for cloud filters
        sync_tools: Whether to clear local caches and force recreation
        **kwargs: Additional arguments for the filter
        
    Returns:
        Tool filter instance
    """
    # Get filter type from environment if not specified
    if not filter_type:
        filter_type = os.getenv("MCP_FILTER_TYPE", "bm25")
    
    filter_type = filter_type.lower()
    
    # Map of available filters
    filter_types = {
        "bm25": BM25Filter,
        "local_embedding": LocalEmbeddingFilter,
        "cloud": CloudFilter,
    }
    
    if filter_type not in filter_types:
        logger.warning(f"Unknown filter type: {filter_type}. Using default: bm25")
        filter_type = "bm25"
    
    logger.info(f"Creating {filter_type} filter")
    
    # Get filter class
    filter_class = filter_types[filter_type]
    
    # Add vector store manager for cloud filter
    if filter_type == "cloud" and vector_store_manager:
        kwargs['vector_store_manager'] = vector_store_manager
    
    # Pass sync_tools to all filter types
    kwargs['sync_tools'] = sync_tools
    
    return filter_class(**kwargs)


__all__ = [
    'BaseToolFilter',
    'Tool',
    'BM25Filter',
    'LocalEmbeddingFilter',
    'CloudFilter',
    'create_filter'
]