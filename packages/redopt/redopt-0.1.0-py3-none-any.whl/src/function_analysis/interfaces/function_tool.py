"""
Function tool for AI agent integration.
"""

import hashlib
from typing import Any, Dict, List, Optional

import networkx as nx
from agents import function_tool

from ..config.settings import FunctionAnalysisConfig
from ..core.clang_parser import ClangParser
from ..core.graph2vec import Graph2VecEncoder
from ..core.graph_converter import GraphConverter
from ..core.models import FunctionAnalysis, GraphData, SimilarityResult
from ..storage.redis_client import RedisClient
from ..storage.vector_search import VectorSearch


class FunctionAnalysisService:
    """Main service class for function analysis."""

    def __init__(self, config: Optional[FunctionAnalysisConfig] = None):
        """Initialize the function analysis service."""
        self.config = config or FunctionAnalysisConfig.from_env()

        # Initialize components
        self.parser = ClangParser()
        self.graph_converter = GraphConverter()
        self.encoder = Graph2VecEncoder(embedding_dim=self.config.embedding_dimension)

        # Initialize storage
        self.redis_client = RedisClient(
            host=self.config.redis_host,
            port=self.config.redis_port,
            db=self.config.redis_db,
            password=self.config.redis_password,
        )
        self.vector_search = VectorSearch(self.redis_client)

        # Try to fit encoder with existing data
        self._initialize_encoder()

    def _initialize_encoder(self):
        """Initialize the encoder with existing data if available."""
        try:
            # Get some existing functions to fit the encoder
            function_ids = self.redis_client.get_all_function_ids()
            if len(function_ids) > 5:  # Need some data to fit
                graphs: List[nx.DiGraph] = []
                for fid in function_ids[:20]:  # Use first 20 for fitting
                    analysis = self.redis_client.get_function_analysis(fid)
                    if analysis and analysis.ast_graph:
                        # Convert back to networkx graph for fitting
                        graph = self._graph_data_to_networkx(analysis.ast_graph)
                        graphs.append(graph)

                if graphs:
                    self.encoder.fit(graphs)
        except Exception as e:
            print(f"Warning: Could not initialize encoder with existing data: {e}")

    def analyze_function(
        self, code: str, function_name: Optional[str] = None, store: bool = True
    ) -> FunctionAnalysis:
        """
        Analyze a function and optionally store it.

        Args:
            code: C/C++ function code
            function_name: Optional function name
            store: Whether to store the analysis in Redis

        Returns:
            FunctionAnalysis object
        """
        # Validate code length
        if len(code) > self.config.max_code_length:
            raise ValueError(
                f"Code too long: {len(code)} > {self.config.max_code_length}"
            )

        # Parse with Clang
        parse_result = self.parser.parse_function(code, function_name)

        # Convert AST to graph
        ast_graph = self.graph_converter.ast_to_graph(parse_result["ast"])
        ast_graph_data = self.graph_converter.graph_to_data(ast_graph)
        ast_graph_data.graph_type = "ast"

        # Generate embedding
        embedding = self.encoder.encode(ast_graph)

        # Calculate complexity
        complexity = self.parser.calculate_complexity(parse_result["ast"])
        parse_result["metadata"].complexity_score = complexity

        # Create analysis object
        function_id = self._generate_function_id(code)
        analysis = FunctionAnalysis(
            id=function_id,
            code=code,
            metadata=parse_result["metadata"],
            ast_graph=ast_graph_data,
            embedding=embedding,
        )

        # Store if requested
        if store:
            self.redis_client.store_function_analysis(analysis)

        return analysis

    def find_similar_functions(
        self,
        code: Optional[str] = None,
        function_id: Optional[str] = None,
        top_k: int = None,
        threshold: float = None,
    ) -> List[SimilarityResult]:
        """
        Find functions similar to the given code or function ID.

        Args:
            code: C/C++ function code to find similarities for
            function_id: Existing function ID to find similarities for
            top_k: Number of results to return
            threshold: Similarity threshold

        Returns:
            List of SimilarityResult objects
        """
        top_k = top_k or self.config.default_top_k
        threshold = threshold or self.config.default_similarity_threshold

        if function_id:
            return self.vector_search.find_similar_by_function_id(
                function_id=function_id, top_k=top_k, threshold=threshold
            )
        elif code:
            # Analyze the code to get embedding
            analysis = self.analyze_function(code, store=False)
            return self.vector_search.find_similar_functions(
                query_embedding=analysis.embedding, top_k=top_k, threshold=threshold
            )
        else:
            raise ValueError("Either code or function_id must be provided")

    def _generate_function_id(self, code: str) -> str:
        """Generate a unique ID for a function based on its code."""
        # Use hash of code for deterministic ID
        code_hash = hashlib.sha256(code.encode()).hexdigest()[:16]
        return f"func_{code_hash}"

    def _graph_data_to_networkx(self, graph_data: GraphData):
        """Convert GraphData back to NetworkX graph."""
        import networkx as nx

        graph = nx.DiGraph()

        # Add nodes
        for node in graph_data.nodes:
            node_id = node.pop("id")
            graph.add_node(node_id, **node)

        # Add edges
        for edge in graph_data.edges:
            source = edge.pop("source")
            target = edge.pop("target")
            graph.add_edge(source, target, **edge)

        return graph


# Global service instance
_service_instance = None


def get_service() -> FunctionAnalysisService:
    """Get or create the global service instance."""
    global _service_instance
    if _service_instance is None:
        _service_instance = _initialize_service_with_logging()
    return _service_instance


def _initialize_service_with_logging() -> FunctionAnalysisService:
    """Initialize the service with detailed logging."""
    print("🔧 Initializing Function Analysis Service...")

    try:
        service = FunctionAnalysisService()

        # Test Redis connection and log status
        print("🔍 Checking Redis connection...")
        stats = service.redis_client.get_stats()

        if stats.get("redis_connected", False):
            print(f"✅ Redis connected successfully!")
            print(
                f"   🗄️  Database: {service.redis_client.redis.connection_pool.connection_kwargs.get('db', 0)}"
            )
            print(f"   📊 Total functions: {stats['total_functions']}")
            print(f"   🏷️  Unique function names: {stats['unique_function_names']}")
            print(f"   💾 Memory usage: {stats['memory_usage']}")

            # Check embedding statistics
            print("🧠 Checking embeddings...")
            embedding_stats = service.vector_search.get_embedding_statistics()
            total_embeddings = embedding_stats.get("total_embeddings", 0)

            if total_embeddings > 0:
                print(f"   ✅ Found {total_embeddings} function embeddings")
                print(
                    f"   📐 Embedding dimension: {embedding_stats['embedding_dimension']}"
                )
                print(
                    f"   📊 Average norm: {embedding_stats.get('average_norm', 0):.3f}"
                )

                # Try to get some sample function names
                try:
                    function_ids = service.redis_client.get_all_function_ids()
                    if function_ids:
                        sample_functions = []
                        for fid in function_ids[:3]:  # Get first 3 as samples
                            analysis = service.redis_client.get_function_analysis(fid)
                            if analysis:
                                sample_functions.append(analysis.metadata.name)

                        if sample_functions:
                            print(
                                f"   📋 Sample functions: {', '.join(sample_functions)}"
                            )
                except:
                    pass

            else:
                print("   ⚠️  No embeddings found in database")
                print("   💡 Run indexing to populate the database:")
                print(
                    "      poetry run redopt index --source ~/redis/src --output ./functions"
                )

        else:
            print("❌ Redis connection failed!")
            print("   🔧 Redis may not be running or accessible")
            print(
                "   💡 Start Redis with: docker run -d -p 6379:6379 redis/redis-stack"
            )
            print("   ⚠️  Function analysis will work but without similarity search")

        return service

    except Exception as e:
        print(f"❌ Function Analysis Service initialization failed: {e}")
        print("   💡 Check Redis connection and try again")
        print("   🔧 Falling back to basic functionality")

        # Return a basic service that can still parse functions
        try:
            return FunctionAnalysisService()
        except:
            # Last resort - create minimal service
            from ..config.settings import FunctionAnalysisConfig

            config = FunctionAnalysisConfig.from_env()
            config.redis_host = "dummy"  # This will fail gracefully
            return FunctionAnalysisService(config)


def log_service_status():
    """Log the current service status - useful for debugging."""
    try:
        service = get_service()
        stats = service.redis_client.get_stats()
        embedding_stats = service.vector_search.get_embedding_statistics()

        print("\n📊 Function Analysis Service Status:")
        print(
            f"   Redis: {'✅ Connected' if stats.get('redis_connected') else '❌ Disconnected'}"
        )
        print(f"   Functions: {stats.get('total_functions', 0)}")
        print(f"   Embeddings: {embedding_stats.get('total_embeddings', 0)}")
        print(f"   Memory: {stats.get('memory_usage', 'unknown')}")

    except Exception as e:
        print(f"❌ Could not get service status: {e}")


# Function tools for AI agent integration
@function_tool
def analyze_function_code(code: str, function_name: str = None) -> Dict[str, Any]:
    """
    Analyze C/C++ function code using LLVM/Clang AST parsing and find similar functions using Graph2Vec embeddings.

    This tool automatically:
    - Parses the code with LLVM/Clang to extract AST
    - Calculates cyclomatic complexity
    - Generates graph embeddings for semantic similarity
    - Finds similar functions in the database
    - Stores the analysis for future reference

    Args:
        code: C/C++ function code to analyze (complete function including braces)
        function_name: Optional name of the function to analyze (auto-detected if not provided)

    Returns:
        Dictionary containing detailed analysis results and similar functions
    """
    try:
        service = get_service()

        # Analyze the function
        analysis = service.analyze_function(code, function_name)

        # Find similar functions
        similar_functions = service.find_similar_functions(function_id=analysis.id)

        return {
            "success": True,
            "function_id": analysis.id,
            "function_name": analysis.metadata.name,
            "metadata": {
                "return_type": analysis.metadata.return_type,
                "parameters": analysis.metadata.parameters,
                "line_count": analysis.metadata.line_count,
                "complexity_score": analysis.metadata.complexity_score,
            },
            "similar_functions": [
                {
                    "function_id": sim.function_id,
                    "function_name": sim.function_name,
                    "similarity_score": sim.similarity_score,
                    "code_snippet": sim.code_snippet,
                }
                for sim in similar_functions
            ],
            "total_similar": len(similar_functions),
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


@function_tool
def find_similar_functions_by_id(
    function_id: str, top_k: int = 10, threshold: float = 0.7
) -> Dict[str, Any]:
    """
    Find functions similar to an existing function by its ID.

    Args:
        function_id: ID of the function to find similarities for
        top_k: Number of similar functions to return (default: 10)
        threshold: Similarity threshold (default: 0.7)

    Returns:
        Dictionary containing similar functions
    """
    try:
        service = get_service()

        # Get the original function
        original = service.redis_client.get_function_analysis(function_id)
        if not original:
            return {
                "success": False,
                "error": f"Function with ID {function_id} not found",
            }

        # Find similar functions
        similar_functions = service.find_similar_functions(
            function_id=function_id, top_k=top_k, threshold=threshold
        )

        return {
            "success": True,
            "original_function": {
                "function_id": original.id,
                "function_name": original.metadata.name,
                "code_snippet": (
                    original.code[:200] + "..."
                    if len(original.code) > 200
                    else original.code
                ),
            },
            "similar_functions": [
                {
                    "function_id": sim.function_id,
                    "function_name": sim.function_name,
                    "similarity_score": sim.similarity_score,
                    "code_snippet": sim.code_snippet,
                }
                for sim in similar_functions
            ],
            "total_similar": len(similar_functions),
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


@function_tool
def get_function_analysis_stats() -> Dict[str, Any]:
    """
    Get statistics about the function analysis database including total functions, embeddings, and memory usage.

    Returns:
        Dictionary containing comprehensive database statistics
    """
    try:
        service = get_service()

        # Get Redis stats
        redis_stats = service.redis_client.get_stats()

        # Get embedding stats
        embedding_stats = service.vector_search.get_embedding_statistics()

        return {
            "success": True,
            "database_info": {
                "total_functions": redis_stats.get("total_functions", 0),
                "unique_function_names": redis_stats.get("unique_function_names", 0),
                "memory_usage": redis_stats.get("memory_usage", "unknown"),
                "redis_connected": redis_stats.get("redis_connected", False),
            },
            "embedding_info": {
                "total_embeddings": embedding_stats.get("total_embeddings", 0),
                "embedding_dimension": embedding_stats.get("embedding_dimension", 0),
                "average_norm": embedding_stats.get("average_norm", 0.0),
            },
            "redis_stats": redis_stats,
            "embedding_stats": embedding_stats,
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


@function_tool
def check_function_database_status() -> Dict[str, Any]:
    """
    Check the status of the function analysis database and Redis connection.

    Returns:
        Dictionary containing detailed status information
    """
    try:
        service = get_service()

        # Get comprehensive status
        redis_stats = service.redis_client.get_stats()
        embedding_stats = service.vector_search.get_embedding_statistics()

        # Get sample function names
        sample_functions = []
        try:
            function_ids = service.redis_client.get_all_function_ids()
            for fid in function_ids[:5]:  # Get first 5 as samples
                analysis = service.redis_client.get_function_analysis(fid)
                if analysis:
                    sample_functions.append(
                        {
                            "name": analysis.metadata.name,
                            "complexity": analysis.metadata.complexity_score,
                            "source_file": analysis.metadata.source_file,
                        }
                    )
        except:
            pass

        return {
            "success": True,
            "redis_connected": redis_stats.get("redis_connected", False),
            "database_stats": {
                "total_functions": redis_stats.get("total_functions", 0),
                "unique_function_names": redis_stats.get("unique_function_names", 0),
                "memory_usage": redis_stats.get("memory_usage", "unknown"),
            },
            "embedding_stats": {
                "total_embeddings": embedding_stats.get("total_embeddings", 0),
                "embedding_dimension": embedding_stats.get("embedding_dimension", 0),
                "average_norm": embedding_stats.get("average_norm", 0.0),
            },
            "sample_functions": sample_functions,
            "recommendations": _get_status_recommendations(
                redis_stats, embedding_stats
            ),
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "recommendations": [
                "Check if Redis is running: docker run -d -p 6379:6379 redis/redis-stack",
                "Verify Redis connection settings in .env file",
                "Run indexing to populate database: poetry run redopt index --source ~/redis/src",
            ],
        }


def _get_status_recommendations(redis_stats: Dict, embedding_stats: Dict) -> List[str]:
    """Generate recommendations based on current status."""
    recommendations = []

    if not redis_stats.get("redis_connected", False):
        recommendations.append(
            "Start Redis server: docker run -d -p 6379:6379 redis/redis-stack"
        )
        recommendations.append("Check Redis connection settings in .env file")

    total_functions = redis_stats.get("total_functions", 0)
    if total_functions == 0:
        recommendations.append(
            "Index a codebase: poetry run redopt index --source ~/redis/src --output ./functions"
        )
        recommendations.append(
            "The database is empty - function similarity search won't work until you index some code"
        )
    elif total_functions < 100:
        recommendations.append(
            "Consider indexing more code for better similarity search results"
        )

    total_embeddings = embedding_stats.get("total_embeddings", 0)
    if total_embeddings == 0 and total_functions > 0:
        recommendations.append(
            "Embeddings are missing - re-run indexing to generate them"
        )

    if not recommendations:
        recommendations.append(
            "System is ready for function analysis and similarity search!"
        )

    return recommendations


@function_tool
def search_functions_by_name(function_name: str) -> Dict[str, Any]:
    """
    Search for functions by name in the database.

    Args:
        function_name: Name of the function to search for

    Returns:
        Dictionary containing matching functions
    """
    try:
        service = get_service()

        # Search for functions by name
        functions = service.redis_client.get_functions_by_name(function_name)

        return {
            "success": True,
            "function_name": function_name,
            "total_matches": len(functions),
            "functions": [
                {
                    "function_id": func.id,
                    "function_name": func.metadata.name,
                    "return_type": func.metadata.return_type,
                    "parameters": len(func.metadata.parameters),
                    "complexity": func.metadata.complexity_score,
                    "source_file": func.metadata.source_file,
                    "line_count": func.metadata.line_count,
                }
                for func in functions
            ],
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


@function_tool
def find_function_callers(function_name: str) -> Dict[str, Any]:
    """
    Find all functions that call the specified function.

    Args:
        function_name: Name of the function to find callers for

    Returns:
        Dictionary with caller information
    """
    try:
        service = get_service()
        callers = service.redis_client.get_function_callers(function_name)

        return {
            "success": True,
            "function_name": function_name,
            "callers": callers,
            "caller_count": len(callers),
            "message": f"Found {len(callers)} functions that call '{function_name}'",
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to find callers for '{function_name}': {str(e)}",
            "error_type": type(e).__name__,
        }


@function_tool
def find_function_callees(function_name: str) -> Dict[str, Any]:
    """
    Find all functions called by the specified function.

    Args:
        function_name: Name of the function to find callees for

    Returns:
        Dictionary with callee information
    """
    try:
        service = get_service()
        callees = service.redis_client.get_function_callees(function_name)

        return {
            "success": True,
            "function_name": function_name,
            "callees": callees,
            "callee_count": len(callees),
            "message": f"Function '{function_name}' calls {len(callees)} other functions",
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to find callees for '{function_name}': {str(e)}",
            "error_type": type(e).__name__,
        }


@function_tool
def find_call_paths(
    from_function: str, to_function: str, max_depth: int = 15
) -> Dict[str, Any]:
    """
    Find call paths from one function to another.

    Args:
        from_function: Starting function name
        to_function: Target function name
        max_depth: Maximum search depth (default: 15)

    Returns:
        Dictionary with call path information
    """
    try:
        service = get_service()
        paths = service.redis_client.search_call_paths(
            from_function, to_function, max_depth
        )

        return {
            "success": True,
            "from_function": from_function,
            "to_function": to_function,
            "paths": paths,
            "path_count": len(paths),
            "message": f"Found {len(paths)} call paths from '{from_function}' to '{to_function}'",
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to find call paths: {str(e)}",
            "error_type": type(e).__name__,
        }


def find_redis_commands_using_function(
    function_name: str, max_depth: int = 20
) -> Dict[str, Any]:
    """
    Find all Redis commands that use a given function by tracing up through callers.

    This tool traverses the call tree upward from the given function to find all Redis
    command functions that eventually call it, either directly or indirectly.

    Args:
        function_name: Name of the function to trace callers for
        max_depth: Maximum depth to search up the call tree (default: 20)

    Returns:
        Dictionary containing Redis commands that use the function and their call paths
    """
    try:
        import json
        from pathlib import Path

        service = get_service()

        # Load the function-to-command mapping
        mapping_file = Path(__file__).parent.parent / "fnToCommand.json"
        try:
            with open(mapping_file, "r") as f:
                fn_to_command = json.load(f)
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to load function-to-command mapping: {str(e)}",
                "error_type": type(e).__name__,
            }

        # Get all command functions (keys from the mapping)
        command_functions = set(fn_to_command.keys())

        # Perform breadth-first search up the call tree
        visited = set()
        queue = [
            (function_name, [function_name])
        ]  # (current_function, path_to_current)
        redis_commands_found = {}

        while queue and len(visited) < max_depth * 100:  # Prevent infinite loops
            current_function, path = queue.pop(0)

            if current_function in visited:
                continue
            visited.add(current_function)

            # Check if current function is a Redis command
            if current_function in command_functions:
                commands = fn_to_command[current_function]
                if isinstance(commands, str):
                    commands = [commands]

                for cmd in commands:
                    if cmd not in redis_commands_found:
                        redis_commands_found[cmd] = []
                    redis_commands_found[cmd].append(
                        {
                            "path": path,
                            "depth": len(path) - 1,
                            "command_function": current_function,
                        }
                    )

            # If we haven't reached max depth, get callers and add to queue
            if len(path) < max_depth:
                try:
                    callers = service.redis_client.get_function_callers(
                        current_function
                    )
                    # Sort callers to prioritize command functions first
                    command_callers = [c for c in callers if c in command_functions]
                    other_callers = [c for c in callers if c not in command_functions]

                    # Add command functions first, then others
                    for caller in command_callers + other_callers:
                        if caller not in visited:
                            new_path = [caller] + path
                            queue.append((caller, new_path))
                except Exception:
                    # Continue if we can't get callers for this function
                    continue

        # Sort commands by name and prepare detailed results
        sorted_commands = sorted(redis_commands_found.items())
        command_details = []

        for cmd, paths in sorted_commands:
            # Get the shortest path for each command
            shortest_path = min(paths, key=lambda x: x["depth"])
            command_details.append(
                {
                    "command": cmd,
                    "command_function": shortest_path["command_function"],
                    "shortest_path": shortest_path["path"],
                    "shortest_depth": shortest_path["depth"],
                    "total_paths": len(paths),
                    "all_paths": [
                        p["path"] for p in paths[:5]
                    ],  # Limit to first 5 paths
                }
            )

        return {
            "success": True,
            "function_name": function_name,
            "redis_commands": [detail["command"] for detail in command_details],
            "total_commands": len(command_details),
            "command_details": command_details,
            "search_stats": {
                "functions_visited": len(visited),
                "max_depth_used": max_depth,
                "total_paths_found": sum(
                    len(paths) for paths in redis_commands_found.values()
                ),
            },
            "message": f"Found {len(command_details)} Redis commands that use '{function_name}'",
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to find Redis commands using '{function_name}': {str(e)}",
            "error_type": type(e).__name__,
        }
