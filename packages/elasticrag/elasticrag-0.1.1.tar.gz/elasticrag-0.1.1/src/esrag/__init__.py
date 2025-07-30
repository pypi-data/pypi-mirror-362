"""
ElasticRAG - Elasticsearch-based RAG system with ingest pipeline processing.
"""

from .client import Client
from .user import User
from .model import Model
from .collection import Collection
from .splitter import Splitter, JinaTextSegmenter
from .utils import rrf

__version__ = "0.1.0"
__all__ = [
    'Client',
    'User', 
    'Model',
    'Collection',
    'Splitter',
    'JinaTextSegmenter',
    'rrf'
]
