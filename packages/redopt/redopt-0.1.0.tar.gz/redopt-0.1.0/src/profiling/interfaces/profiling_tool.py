"""
Profiling analysis tools for AI agents.
"""

from typing import Any, Dict, List

from ..queries.sqlite_queries import SQLiteProfileQueries
from ..storage.sqlite_storage import SQLiteProfileStorage

# Global service instance
_profiling_service = None


def _print_benchmark_summary(storage: SQLiteProfileStorage):
    """Print a comprehensive summary of benchmark data."""
    import json
    from collections import Counter

    cursor = storage.conn.cursor()

    # Get all benchmark data
    cursor.execute("SELECT * FROM benchmarks")
    benchmarks = cursor.fetchall()

    if not benchmarks:
        print("   📋 No benchmark data found")
        return

    all_commands = []
    all_command_groups = []
    all_topologies = []
    all_build_variants = []
    total_samples = 0
    benchmark_names = []

    for benchmark in benchmarks:
        try:
            # Parse JSON fields
            tested_commands = (
                json.loads(benchmark["tested_commands"])
                if benchmark["tested_commands"]
                else []
            )
            tested_groups = (
                json.loads(benchmark["tested_groups"])
                if benchmark["tested_groups"]
                else []
            )
            redis_topologies = (
                json.loads(benchmark["redis_topologies"])
                if benchmark["redis_topologies"]
                else []
            )
            build_variants = (
                json.loads(benchmark["build_variants"])
                if benchmark["build_variants"]
                else []
            )

            # Collect data
            benchmark_names.append(benchmark["name"])
            all_commands.extend(tested_commands)
            all_command_groups.extend(tested_groups)
            all_topologies.extend(redis_topologies)
            all_build_variants.extend(build_variants)
            total_samples += benchmark["total_samples"] or 0

        except Exception as e:
            print(f"   ⚠️  Error reading benchmark {benchmark['name']}: {e}")

    # Count occurrences
    command_counts = Counter(all_commands)
    command_group_counts = Counter(all_command_groups)
    topology_counts = Counter(all_topologies)
    build_variant_counts = Counter(all_build_variants)

    # Print summary
    print(f"   📈 Total samples across all benchmarks: {total_samples:,}")

    if command_counts:
        print(f"   🎯 Commands tested ({len(command_counts)} unique):")
        for cmd, count in command_counts.most_common():
            print(f"      • {cmd}: {count} benchmark(s)")

    if command_group_counts:
        print(f"   🏷️  Command groups ({len(command_group_counts)} unique):")
        for group, count in command_group_counts.most_common():
            print(f"      • {group}: {count} benchmark(s)")

    if topology_counts:
        print(f"   🏗️  Redis topologies ({len(topology_counts)} unique):")
        for topology, count in topology_counts.most_common():
            print(f"      • {topology}: {count} benchmark(s)")

    if build_variant_counts:
        print(f"   🔧 Build variants ({len(build_variant_counts)} unique):")
        for variant, count in build_variant_counts.most_common():
            print(f"      • {variant}: {count} benchmark(s)")

    # Show sample benchmark names
    if benchmark_names:
        print(f"   📋 Benchmark(s):")
        for name in benchmark_names[:3]:  # Show first 3
            print(f"      • {name}")
        if len(benchmark_names) > 3:
            print(f"      ... and {len(benchmark_names) - 3} more")

    # Check database indexes
    cursor.execute("SELECT COUNT(*) FROM benchmarks")
    benchmark_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM function_hotspots")
    hotspot_count = cursor.fetchone()[0]
    print(
        f"   🔍 Search indexes: {benchmark_count} benchmarks, {hotspot_count} hotspots indexed"
    )


def get_profiling_service():
    """Get or create the profiling service instance."""
    global _profiling_service
    if _profiling_service is None:
        try:
            storage = SQLiteProfileStorage("profiling.db")
            _profiling_service = SQLiteProfileQueries(storage)

            # Get and display profiling statistics
            stats = storage.get_storage_stats()
            print("✅ Profiling service connected to SQLite")
            print(f"   📊 Total benchmarks: {stats.get('total_benchmarks', 0)}")
            print(f"   🔥 Total hotspots: {stats.get('total_hotspots', 0)}")

            # Get comprehensive benchmark summary
            try:
                _print_benchmark_summary(storage)
            except Exception as e:
                print(f"   ⚠️  Could not get detailed stats: {e}")

        except Exception as e:
            print(f"⚠️  Profiling service unavailable: {e}")
            _profiling_service = None
    return _profiling_service


def get_function_performance_hotspots(
    function_name: str, min_percentage: float = 1.0
) -> List[Dict[str, Any]]:
    """
    Get performance hotspot data for a specific function across all benchmarks.

    Args:
        function_name: Name of the function to analyze
        min_percentage: Minimum percentage threshold for hotspots (default: 1.0%)

    Returns:
        List of benchmark coverage data showing where this function is a hotspot
    """
    service = get_profiling_service()
    if not service:
        return [{"error": "Profiling service unavailable - SQLite connection failed"}]

    try:
        coverage = service.function_coverage_in_benchmarks(
            function_name, min_percentage
        )
        if not coverage:
            return [
                {
                    "message": f"No performance hotspots found for function '{function_name}' above {min_percentage}%"
                }
            ]

        return coverage
    except Exception as e:
        return [{"error": f"Error querying function hotspots: {e}"}]


def get_commands_affected_by_function(function_name: str) -> Dict[str, List[str]]:
    """
    Find Redis commands and command groups that are affected by a specific function.

    Args:
        function_name: Name of the function to analyze

    Returns:
        Dictionary with 'commands' and 'command_groups' lists
    """
    service = get_profiling_service()
    if not service:
        return {"error": "Profiling service unavailable - SQLite connection failed"}

    try:
        result = service.commands_affected_by_function(function_name)
        if not result["commands"] and not result["command_groups"]:
            return {
                "message": f"No Redis commands found affected by function '{function_name}'"
            }

        return result
    except Exception as e:
        return {"error": f"Error querying affected commands: {e}"}


def get_top_performance_hotspots(limit: int = 20) -> List[Dict[str, Any]]:
    """
    Get the top performance hotspots across all benchmarks.

    Args:
        limit: Maximum number of hotspots to return (default: 20)

    Returns:
        List of top function hotspots with performance data
    """
    service = get_profiling_service()
    if not service:
        return [{"error": "Profiling service unavailable - SQLite connection failed"}]

    try:
        hotspots = service.top_hotspots_all_benchmarks(limit)
        if not hotspots:
            return [{"message": "No performance hotspots found"}]

        return hotspots
    except Exception as e:
        return [{"error": f"Error querying top hotspots: {e}"}]


def get_hotspots_by_command_group(
    command_group: str, limit: int = 20
) -> List[Dict[str, Any]]:
    """
    Get top performance hotspots for a specific Redis command group.

    Args:
        command_group: Redis command group (e.g., 'sorted-set', 'string', 'hash')
        limit: Maximum number of hotspots to return (default: 20)

    Returns:
        List of function hotspots for the specified command group
    """
    service = get_profiling_service()
    if not service:
        return [{"error": "Profiling service unavailable - SQLite connection failed"}]

    try:
        hotspots = service.top_hotspots_by_command_group(command_group, limit)
        if not hotspots:
            return [
                {
                    "message": f"No performance hotspots found for command group '{command_group}'"
                }
            ]

        return hotspots
    except Exception as e:
        return [{"error": f"Error querying hotspots for command group: {e}"}]


def get_benchmarks_by_command_group(command_group: str) -> List[Dict[str, Any]]:
    """
    Find all benchmarks that test a specific Redis command group.

    Args:
        command_group: Redis command group (e.g., 'sorted-set', 'string', 'hash')

    Returns:
        List of benchmark information for the specified command group
    """
    service = get_profiling_service()
    if not service:
        return [{"error": "Profiling service unavailable - SQLite connection failed"}]

    try:
        benchmarks = service.benchmarks_by_command_group(command_group)
        if not benchmarks:
            return [
                {"message": f"No benchmarks found for command group '{command_group}'"}
            ]

        return benchmarks
    except Exception as e:
        return [{"error": f"Error querying benchmarks: {e}"}]


def search_performance_functions(function_name: str) -> List[Dict[str, Any]]:
    """
    Search for functions by name pattern in performance profiling data.

    Args:
        function_name: Function name or pattern to search for

    Returns:
        List of functions with performance data
    """
    service = get_profiling_service()
    if not service:
        return [{"error": "Profiling service unavailable - SQLite connection failed"}]

    try:
        functions = service.search_functions_by_name(function_name)
        if not functions:
            return [
                {
                    "message": f"No functions found matching '{function_name}' in performance data"
                }
            ]

        return functions
    except Exception as e:
        return [{"error": f"Error searching functions: {e}"}]


def get_profiling_database_status() -> Dict[str, Any]:
    """
    Check the status of the profiling database and get statistics.

    Returns:
        Dictionary with profiling database status and statistics
    """
    service = get_profiling_service()
    if not service:
        return {
            "connected": False,
            "error": "Profiling service unavailable - SQLite connection failed",
        }

    try:
        stats = service.storage.get_storage_stats()
        return {
            "connected": True,
            "total_benchmarks": stats.get("total_benchmarks", 0),
            "total_profile_entries": stats.get("total_profile_entries", 0),
            "unique_functions": stats.get("unique_functions", 0),
            "unique_commands": stats.get("unique_commands", 0),
            "unique_command_groups": stats.get("unique_command_groups", 0),
        }
    except Exception as e:
        return {"connected": False, "error": f"Error getting profiling stats: {e}"}
