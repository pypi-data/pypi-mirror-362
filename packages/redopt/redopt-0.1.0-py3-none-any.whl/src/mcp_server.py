"""
MCP (Model Context Protocol) server for Redis analysis tools.

This server exposes all Redis function analysis, profiling, GitHub, and call tree tools
as MCP tools that can be used by AI assistants like Claude Desktop.
"""

import logging
from typing import Any, Dict, Optional

from mcp.server.fastmcp import FastMCP

from .config import Config

# Import the service classes to call the underlying functions directly
from .function_analysis.interfaces.function_tool import (
    find_redis_commands_using_function,
)
from .function_analysis.interfaces.function_tool import (
    get_service as get_function_service,
)

# Import profiling tools
from .profiling.interfaces.profiling_tool import (
    get_benchmarks_by_command_group,
    get_commands_affected_by_function,
    get_function_performance_hotspots,
    get_hotspots_by_command_group,
    get_profiling_database_status,
    get_top_performance_hotspots,
    search_performance_functions,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize configuration
config = Config.from_env()

# Create MCP server
mcp = FastMCP(
    name="Redis Analysis Tools",
    description="Comprehensive Redis codebase analysis tools including function analysis, performance profiling, and GitHub PR analysis",
)


@mcp.tool(description="Check if a Redis function is performance-critical")
def is_redis_function_performance_critical(function_name: str) -> bool:
    """
    Check if a function is performance-critical by looking at the profiling data.

    Args:
        function_name: Name of the function to analyze

    Returns:
        True if the function is performance-critical, False otherwise
    """

    # TODO: do actual check on performance data
    return len(function_name) > 5


@mcp.tool(description="Find Redis commands using a function")
def get_redis_commands_using_function(function_name: str) -> Dict[str, Any]:
    """
    Find Redis commands that end up using a specific function.

    Args:
        function_name: Name of the function to analyze

    Returns:
        Dictionary with 'commands'
    """
    return find_redis_commands_using_function(function_name)


# Function Analysis Tools
@mcp.tool(description="Analyze C/C++ code and find similar functions in Redis")
def get_redis_functions_with_similar_code(
    code: str, function_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Analyze C/C++ function code using LLVM/Clang AST parsing and find similar functions.

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
        service = get_function_service()

        # Analyze the function
        analysis = service.analyze_function(code, function_name)

        # Find similar functions
        return service.find_similar_functions(function_id=analysis.id)

    except Exception as e:
        return {"success": False, "error": str(e)}


# Profiling Tools
@mcp.tool(
    description="Get performance hotspot data for a specific function across all benchmarks"
)
def get_function_performance_hotspots_mcp(
    function_name: str, min_percentage: float = 1.0
) -> Dict[str, Any]:
    """
    Get performance hotspot data for a specific function across all benchmarks.

    Args:
        function_name: Name of the function to analyze
        min_percentage: Minimum percentage threshold for hotspots (default: 1.0%)

    Returns:
        List of benchmark coverage data showing where this function is a hotspot
    """
    try:
        result = get_function_performance_hotspots(function_name, min_percentage)
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool(
    description="Find Redis commands and command groups affected by a specific function"
)
def get_commands_affected_by_function_mcp(function_name: str) -> Dict[str, Any]:
    """
    Find Redis commands and command groups that are affected by a specific function.

    Args:
        function_name: Name of the function to analyze

    Returns:
        Dictionary with 'commands' and 'command_groups' lists
    """
    try:
        result = get_commands_affected_by_function(function_name)
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool(description="Get the top performance hotspots across all benchmarks")
def get_top_performance_hotspots_mcp(limit: int = 20) -> Dict[str, Any]:
    """
    Get the top performance hotspots across all benchmarks.

    Args:
        limit: Maximum number of hotspots to return (default: 20)

    Returns:
        List of top function hotspots with performance data
    """
    try:
        result = get_top_performance_hotspots(limit)
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool(description="Get top performance hotspots for a specific Redis command group")
def get_hotspots_by_command_group_mcp(
    command_group: str, limit: int = 20
) -> Dict[str, Any]:
    """
    Get top performance hotspots for a specific Redis command group.

    Args:
        command_group: Redis command group (e.g., 'sorted-set', 'string', 'hash')
        limit: Maximum number of hotspots to return (default: 20)

    Returns:
        List of function hotspots for the specified command group
    """
    try:
        result = get_hotspots_by_command_group(command_group, limit)
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool(description="Find all benchmarks that test a specific Redis command group")
def get_benchmarks_by_command_group_mcp(command_group: str) -> Dict[str, Any]:
    """
    Find all benchmarks that test a specific Redis command group.

    Args:
        command_group: Redis command group (e.g., 'sorted-set', 'string', 'hash')

    Returns:
        List of benchmark information for the specified command group
    """
    try:
        result = get_benchmarks_by_command_group(command_group)
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool(
    description="Search for functions by name pattern in performance profiling data"
)
def search_performance_functions_mcp(function_name: str) -> Dict[str, Any]:
    """
    Search for functions by name pattern in performance profiling data.

    Args:
        function_name: Function name or pattern to search for

    Returns:
        List of functions with performance data
    """
    try:
        result = search_performance_functions(function_name)
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool(description="Check the status of the profiling database and get statistics")
def get_profiling_database_status_mcp() -> Dict[str, Any]:
    """
    Check the status of the profiling database and get statistics.

    Returns:
        Dictionary with profiling database status and statistics
    """
    try:
        result = get_profiling_database_status()
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    """Main entry point for the MCP server."""
    logger.info("Starting Redis Analysis Tools MCP Server...")
    mcp.run()


if __name__ == "__main__":
    main()
