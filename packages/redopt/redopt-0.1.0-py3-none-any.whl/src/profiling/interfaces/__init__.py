"""Profiling interfaces for AI agents."""

from .profiling_tool import (  # New SQLite-powered functions; analyze_function_context,; analyze_partial_stacks,; find_stacks_through_function,
    get_benchmarks_by_command_group,
    get_commands_affected_by_function,
    get_function_performance_hotspots,
    get_hotspots_by_command_group,
    get_profiling_database_status,
    get_profiling_service,
    get_top_performance_hotspots,
    search_performance_functions,
)

__all__ = [
    "get_function_performance_hotspots",
    "get_commands_affected_by_function",
    "get_top_performance_hotspots",
    "get_hotspots_by_command_group",
    "get_benchmarks_by_command_group",
    "search_performance_functions",
    "get_profiling_database_status",
    "get_profiling_service",
    # # New SQLite-powered functions
    # "get_stacks_with_unknowns",
    # "find_stacks_through_function",
    # "analyze_function_context",
    # "analyze_partial_stacks",
]
