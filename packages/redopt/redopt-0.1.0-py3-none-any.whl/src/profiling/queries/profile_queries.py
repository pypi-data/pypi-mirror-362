"""
Query interface for profiling data with RediSearch.
"""

from typing import Dict, List, Optional

from redis.commands.search.query import Query

from ..models import BenchmarkProfile, FunctionHotspot
from ..storage.profile_storage import ProfileStorage


class ProfileQueries:
    """Query interface for profiling data"""

    def __init__(self, storage: ProfileStorage):
        self.storage = storage

    def function_coverage_in_benchmarks(
        self, function_name: str, min_percentage: float = 1.0
    ) -> List[Dict]:
        """Find benchmarks that cover a function above threshold"""
        query = f"@function_name:{function_name} @percentage:[{min_percentage} +inf]"

        try:
            results = self.storage.redis.ft("hotspot_idx").search(query)
        except Exception as e:
            print(f"Search error: {e}")
            return []

        coverage = []
        for doc in results.docs:
            coverage.append(
                {
                    "benchmark_name": (
                        doc.benchmarks.split(",")[0]
                        if hasattr(doc, "benchmarks") and doc.benchmarks
                        else "unknown"
                    ),
                    "percentage": (
                        float(doc.percentage) if hasattr(doc, "percentage") else 0.0
                    ),
                    "samples": (
                        int(doc.total_samples) if hasattr(doc, "total_samples") else 0
                    ),
                    "command_groups": (
                        doc.command_groups.split(",")
                        if hasattr(doc, "command_groups") and doc.command_groups
                        else []
                    ),
                    "commands": (
                        doc.commands.split(",")
                        if hasattr(doc, "commands") and doc.commands
                        else []
                    ),
                }
            )

        return coverage

    def commands_affected_by_function(self, function_name: str) -> Dict[str, List[str]]:
        """Find Redis commands and command groups affected by a function"""
        query = f"@function_name:{function_name}"

        try:
            results = self.storage.redis.ft("hotspot_idx").search(query)
        except Exception as e:
            print(f"Search error: {e}")
            return {"commands": [], "command_groups": []}

        commands = set()
        command_groups = set()

        for doc in results.docs:
            if hasattr(doc, "commands") and doc.commands:
                commands.update(
                    [cmd.strip() for cmd in doc.commands.split(",") if cmd.strip()]
                )
            if hasattr(doc, "command_groups") and doc.command_groups:
                command_groups.update(
                    [
                        grp.strip()
                        for grp in doc.command_groups.split(",")
                        if grp.strip()
                    ]
                )

        return {"commands": list(commands), "command_groups": list(command_groups)}

    def top_hotspots_all_benchmarks(self, limit: int = 20) -> List[Dict]:
        """Get top hotspots across all benchmarks"""
        try:
            query = Query("*").sort_by("percentage", asc=False).paging(0, limit)
            results = self.storage.redis.ft("hotspot_idx").search(query)
        except Exception as e:
            print(f"Search error: {e}")
            return []

        hotspots = []
        for doc in results.docs:
            hotspots.append(
                {
                    "function_name": getattr(doc, "function_name", "unknown"),
                    "file_path": getattr(doc, "file_path", "unknown"),
                    "percentage": float(getattr(doc, "percentage", 0.0)),
                    "total_samples": int(getattr(doc, "total_samples", 0)),
                    "benchmarks": (
                        getattr(doc, "benchmarks", "").split(",")
                        if getattr(doc, "benchmarks", "")
                        else []
                    ),
                    "commands": (
                        getattr(doc, "commands", "").split(",")
                        if getattr(doc, "commands", "")
                        else []
                    ),
                    "command_groups": (
                        getattr(doc, "command_groups", "").split(",")
                        if getattr(doc, "command_groups", "")
                        else []
                    ),
                }
            )

        return hotspots

    def top_hotspots_by_command_group(
        self, command_group: str, limit: int = 20
    ) -> List[Dict]:
        """Get top hotspots for specific command group (e.g., 'sorted-set')"""
        try:
            query = (
                Query(f"@command_groups:{command_group}")
                .sort_by("percentage", asc=False)
                .paging(0, limit)
            )
            results = self.storage.redis.ft("hotspot_idx").search(query)
        except Exception as e:
            print(f"Search error: {e}")
            return []

        hotspots = []
        for doc in results.docs:
            hotspots.append(
                {
                    "function_name": getattr(doc, "function_name", "unknown"),
                    "file_path": getattr(doc, "file_path", "unknown"),
                    "percentage": float(getattr(doc, "percentage", 0.0)),
                    "total_samples": int(getattr(doc, "total_samples", 0)),
                    "benchmarks": (
                        getattr(doc, "benchmarks", "").split(",")
                        if getattr(doc, "benchmarks", "")
                        else []
                    ),
                    "commands": (
                        getattr(doc, "commands", "").split(",")
                        if getattr(doc, "commands", "")
                        else []
                    ),
                    "command_groups": (
                        getattr(doc, "command_groups", "").split(",")
                        if getattr(doc, "command_groups", "")
                        else []
                    ),
                }
            )

        return hotspots

    def benchmarks_by_command_group(self, command_group: str) -> List[Dict]:
        """Find all benchmarks that test a specific command group"""
        query = f"@tested_groups:{command_group}"

        try:
            results = self.storage.redis.ft("benchmark_idx").search(query)
        except Exception as e:
            print(f"Search error: {e}")
            return []

        benchmarks = []
        for doc in results.docs:
            benchmarks.append(
                {
                    "name": getattr(doc, "name", "unknown"),
                    "description": getattr(doc, "description", ""),
                    "tested_commands": (
                        getattr(doc, "tested_commands", "").split(",")
                        if getattr(doc, "tested_commands", "")
                        else []
                    ),
                    "total_samples": int(getattr(doc, "total_samples", 0)),
                    "priority": int(getattr(doc, "priority", 0)),
                }
            )

        return benchmarks

    def search_functions_by_name(self, function_name: str) -> List[Dict]:
        """Search for functions by name pattern"""
        query = f"@function_name:*{function_name}*"

        try:
            results = self.storage.redis.ft("hotspot_idx").search(query)
        except Exception as e:
            print(f"Search error: {e}")
            return []

        functions = []
        for doc in results.docs:
            functions.append(
                {
                    "function_name": getattr(doc, "function_name", "unknown"),
                    "file_path": getattr(doc, "file_path", "unknown"),
                    "percentage": float(getattr(doc, "percentage", 0.0)),
                    "total_samples": int(getattr(doc, "total_samples", 0)),
                    "benchmarks": (
                        getattr(doc, "benchmarks", "").split(",")
                        if getattr(doc, "benchmarks", "")
                        else []
                    ),
                    "commands": (
                        getattr(doc, "commands", "").split(",")
                        if getattr(doc, "commands", "")
                        else []
                    ),
                }
            )

        return functions
