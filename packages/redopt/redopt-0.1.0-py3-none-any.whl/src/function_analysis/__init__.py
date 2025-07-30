"""
Function Analysis Service

A service for analyzing C/C++ function code through LLVM/Clang AST parsing,
graph-based representation, and semantic similarity search using Redis.
"""

from .core.clang_parser import ClangParser
from .core.graph2vec import Graph2VecEncoder
from .core.graph_converter import GraphConverter
from .core.models import CallTree, FunctionAnalysis, FunctionCall, SimilarityResult
from .storage.redis_client import RedisClient
from .storage.vector_search import VectorSearch

__version__ = "0.1.0"
__all__ = [
    "FunctionAnalysis",
    "SimilarityResult",
    "CallTree",
    "FunctionCall",
    "ClangParser",
    "GraphConverter",
    "Graph2VecEncoder",
    "RedisClient",
    "VectorSearch",
]
