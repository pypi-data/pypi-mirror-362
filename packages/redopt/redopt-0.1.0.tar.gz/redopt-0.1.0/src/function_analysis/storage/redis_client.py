"""
Redis client for storing function analysis data.
"""

import json
import logging
from typing import Any, Dict, List, Optional

import redis

from ..core.models import FunctionAnalysis

logger = logging.getLogger(__name__)


class RedisClient:
    """Redis client for function analysis storage."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
    ):
        """
        Initialize Redis client.

        Args:
            host: Redis host
            port: Redis port
            db: Redis database number
            password: Redis password
        """
        self.redis = redis.Redis(
            host=host, port=port, db=db, password=password, decode_responses=True
        )

        # Test connection
        try:
            self.redis.ping()
        except redis.ConnectionError as e:
            raise ConnectionError(f"Failed to connect to Redis: {e}")

    def store_function_analysis(self, analysis: FunctionAnalysis) -> bool:
        """
        Store function analysis in Redis.

        Args:
            analysis: FunctionAnalysis object to store

        Returns:
            True if successful, False otherwise
        """
        try:
            # Convert to dictionary for JSON storage
            analysis_dict = analysis.model_dump()

            # Store main analysis data
            key = f"function:{analysis.id}"
            self.redis.json().set(key, "$", analysis_dict)

            # Store in function name index
            name_key = f"function_name:{analysis.metadata.name}"
            self.redis.sadd(name_key, analysis.id)

            # Store embedding for vector search
            embedding_key = f"embedding:{analysis.id}"
            created_at_str = (
                analysis.created_at.isoformat()
                if hasattr(analysis.created_at, "isoformat")
                else str(analysis.created_at)
            )
            self.redis.hset(
                embedding_key,
                mapping={
                    "vector": json.dumps(analysis.embedding),
                    "function_id": analysis.id,
                    "function_name": analysis.metadata.name,
                    "created_at": created_at_str,
                },
            )

            # Add to global function list
            self.redis.sadd("all_functions", analysis.id)

            return True

        except Exception as e:
            logger.error(f"Error storing function analysis: {e}")
            return False

    def get_function_analysis(self, function_id: str) -> Optional[FunctionAnalysis]:
        """
        Retrieve function analysis by ID.

        Args:
            function_id: Function ID to retrieve

        Returns:
            FunctionAnalysis object or None if not found
        """
        try:
            key = f"function:{function_id}"
            data = self.redis.json().get(key)

            if data:
                # Parse datetime string back to datetime object
                if "created_at" in data and isinstance(data["created_at"], str):
                    from datetime import datetime

                    try:
                        data["created_at"] = datetime.fromisoformat(data["created_at"])
                    except:
                        # Fallback for older datetime formats
                        data["created_at"] = datetime.now()

                return FunctionAnalysis(**data)
            return None

        except Exception as e:
            print(f"Error retrieving function analysis: {e}")
            return None

    def get_functions_by_name(self, function_name: str) -> List[FunctionAnalysis]:
        """
        Get all functions with a specific name.

        Args:
            function_name: Name of the function to search for

        Returns:
            List of FunctionAnalysis objects
        """
        try:
            name_key = f"function_name:{function_name}"
            function_ids = self.redis.smembers(name_key)

            functions = []
            for function_id in function_ids:
                analysis = self.get_function_analysis(function_id)
                if analysis:
                    functions.append(analysis)

            return functions

        except Exception as e:
            print(f"Error retrieving functions by name: {e}")
            return []

    def get_all_function_ids(self) -> List[str]:
        """
        Get all function IDs.

        Returns:
            List of function IDs
        """
        try:
            return list(self.redis.smembers("all_functions"))
        except Exception as e:
            print(f"Error retrieving function IDs: {e}")
            return []

    def get_function_embeddings(
        self, function_ids: Optional[List[str]] = None
    ) -> Dict[str, List[float]]:
        """
        Get embeddings for specified functions or all functions.

        Args:
            function_ids: Optional list of function IDs. If None, get all.

        Returns:
            Dictionary mapping function_id to embedding vector
        """
        try:
            if function_ids is None:
                function_ids = self.get_all_function_ids()

            embeddings = {}
            for function_id in function_ids:
                embedding_key = f"embedding:{function_id}"
                embedding_data = self.redis.hget(embedding_key, "vector")
                if embedding_data:
                    embeddings[function_id] = json.loads(embedding_data)

            return embeddings

        except Exception as e:
            print(f"Error retrieving embeddings: {e}")
            return {}

    def delete_function(self, function_id: str) -> bool:
        """
        Delete a function and all its associated data.

        Args:
            function_id: Function ID to delete

        Returns:
            True if successful, False otherwise
        """
        try:
            # Get function data first to clean up indexes
            analysis = self.get_function_analysis(function_id)
            if not analysis:
                return False

            # Remove from name index
            name_key = f"function_name:{analysis.metadata.name}"
            self.redis.srem(name_key, function_id)

            # Remove main data
            function_key = f"function:{function_id}"
            self.redis.delete(function_key)

            # Remove embedding
            embedding_key = f"embedding:{function_id}"
            self.redis.delete(embedding_key)

            # Remove from global list
            self.redis.srem("all_functions", function_id)

            return True

        except Exception as e:
            print(f"Error deleting function: {e}")
            return False

    def search_functions(self, query: str, limit: int = 10) -> List[FunctionAnalysis]:
        """
        Simple text search for functions.

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of matching FunctionAnalysis objects
        """
        try:
            # Simple implementation: search in function names and code
            all_ids = self.get_all_function_ids()
            matches = []

            for function_id in all_ids:
                if len(matches) >= limit:
                    break

                analysis = self.get_function_analysis(function_id)
                if analysis:
                    # Check if query matches name or is in code
                    if (
                        query.lower() in analysis.metadata.name.lower()
                        or query.lower() in analysis.code.lower()
                    ):
                        matches.append(analysis)

            return matches

        except Exception as e:
            print(f"Error searching functions: {e}")
            return []

    def get_stats(self) -> Dict[str, Any]:
        """
        Get storage statistics.

        Returns:
            Dictionary with storage statistics
        """
        try:
            total_functions = self.redis.scard("all_functions")

            # Get memory usage (approximate)
            memory_info = self.redis.info("memory")
            used_memory = memory_info.get("used_memory_human", "unknown")

            # Count function names
            name_keys = self.redis.keys("function_name:*")
            unique_names = len(name_keys)

            return {
                "total_functions": total_functions,
                "unique_function_names": unique_names,
                "memory_usage": used_memory,
                "redis_connected": True,
            }

        except Exception as e:
            print(f"Error getting stats: {e}")
            return {
                "total_functions": 0,
                "unique_function_names": 0,
                "memory_usage": "unknown",
                "redis_connected": False,
                "error": str(e),
            }

    def store_call_tree(self, call_tree_data: Dict[str, Any]) -> bool:
        """
        Store call tree data in Redis.

        Args:
            call_tree_data: Call tree data from ClangParser.build_call_tree()

        Returns:
            True if successful, False otherwise
        """
        try:
            # Convert FunctionMetadata objects to dictionaries for JSON serialization
            serializable_data = self._make_call_tree_serializable(call_tree_data)

            # Store the complete call tree
            self.redis.json().set("call_tree", "$", serializable_data)

            # Store reverse lookup indexes for fast queries
            reverse_graph = call_tree_data.get("reverse_call_graph", {})
            for function_name, callers in reverse_graph.items():
                key = f"callers:{function_name}"
                self.redis.delete(key)  # Clear existing
                if callers:
                    self.redis.sadd(key, *callers)

            # Store forward lookup indexes
            call_graph = call_tree_data.get("call_graph", {})
            for function_name, callees in call_graph.items():
                key = f"callees:{function_name}"
                self.redis.delete(key)  # Clear existing
                if callees:
                    self.redis.sadd(key, *callees)

            return True

        except Exception as e:
            print(f"Error storing call tree: {e}")
            return False

    def get_function_callers(self, function_name: str) -> List[str]:
        """
        Get all functions that call the specified function.

        Args:
            function_name: Name of the function to find callers for

        Returns:
            List of function names that call the specified function
        """
        try:
            key = f"callers:{function_name}"
            callers = self.redis.smembers(key)
            return [
                caller.decode() if isinstance(caller, bytes) else caller
                for caller in callers
            ]
        except Exception as e:
            print(f"Error getting callers for {function_name}: {e}")
            return []

    def get_function_callees(self, function_name: str) -> List[str]:
        """
        Get all functions called by the specified function.

        Args:
            function_name: Name of the function to find callees for

        Returns:
            List of function names called by the specified function
        """
        try:
            key = f"callees:{function_name}"
            callees = self.redis.smembers(key)
            return [
                callee.decode() if isinstance(callee, bytes) else callee
                for callee in callees
            ]
        except Exception as e:
            print(f"Error getting callees for {function_name}: {e}")
            return []

    def get_call_tree_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the stored call tree.

        Returns:
            Dictionary with call tree statistics
        """
        try:
            call_tree = self.redis.json().get("call_tree")
            if call_tree:
                return call_tree.get("statistics", {})
            return {}
        except Exception as e:
            print(f"Error getting call tree stats: {e}")
            return {}

    def search_call_paths(
        self, from_function: str, to_function: str, max_depth: int = 5
    ) -> List[List[str]]:
        """
        Find call paths from one function to another.

        Args:
            from_function: Starting function name
            to_function: Target function name
            max_depth: Maximum search depth

        Returns:
            List of call paths (each path is a list of function names)
        """
        try:
            call_tree = self.redis.json().get("call_tree")
            if not call_tree:
                return []

            call_graph = call_tree.get("call_graph", {})
            paths = []

            def dfs(current: str, target: str, path: List[str], depth: int):
                if depth > max_depth:
                    return

                if current == target:
                    paths.append(path + [current])
                    return

                if current in call_graph:
                    for callee in call_graph[current]:
                        if callee not in path:  # Avoid cycles
                            dfs(callee, target, path + [current], depth + 1)

            dfs(from_function, to_function, [], 0)
            return paths

        except Exception as e:
            print(f"Error searching call paths: {e}")
            return []

    def _make_call_tree_serializable(
        self, call_tree_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Convert call tree data to be JSON serializable by converting Pydantic models to dicts.

        Args:
            call_tree_data: Raw call tree data with Pydantic models

        Returns:
            JSON-serializable dictionary
        """
        import json

        from ..core.models import FunctionMetadata

        def convert_value(obj):
            """Recursively convert objects to JSON-serializable format."""
            if isinstance(obj, FunctionMetadata):
                return obj.model_dump()
            elif isinstance(obj, dict):
                return {k: convert_value(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_value(item) for item in obj]
            else:
                return obj

        return convert_value(call_tree_data)
