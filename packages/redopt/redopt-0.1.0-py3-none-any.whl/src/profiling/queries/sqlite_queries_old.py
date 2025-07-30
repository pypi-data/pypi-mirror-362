"""
Advanced SQLite queries for pprof profiling data analysis.
Demonstrates the power of SQL for function performance analysis.
"""

import sqlite3
from typing import Dict, List, Optional, Tuple

from ..storage.sqlite_storage import SQLiteProfileStorage


class SQLiteProfileQueries:
    """Advanced query interface for SQLite pprof profiling data"""

    def __init__(self, storage: SQLiteProfileStorage):
        self.storage = storage
        self.conn = storage.conn
    
    def get_top_functions_for_command_group(self, command_group: str, top_n: int = 10) -> List[Dict]:
        """
        Returns top N functions by average cumulative % across all benchmarks in the group.
        """
        cursor = self.conn.cursor()

        query = """
            SELECT
                function,
                AVG(flat_percent) AS avg_flat,
                AVG(cum_percent) AS avg_cum,
                COUNT(*) as benchmark_count
            FROM profile_entries
            JOIN benchmarks USING (benchmark_id)
            WHERE command_group = ?
            GROUP BY function
            ORDER BY avg_cum DESC
            LIMIT ?
        """

        cursor.execute(query, (command_group, top_n))
        return [
            {
                "function": row[0],
                "avg_flat_percent": round(row[1], 2),
                "avg_cum_percent": round(row[2], 2),
                "benchmark_count": row[3]
            }
            for row in cursor.fetchall()
        ]
    
    def get_commands_affected_by_function(self, function: str, min_cum_percent: float = 1.0) -> List[Dict]:
        """
        For a given function, return all commands where it appears with cum_percent >= min_cum_percent.
        """
        cursor = self.conn.cursor()

        query = """
            SELECT
                command,
                AVG(cum_percent) AS avg_cum,
                AVG(flat_percent) AS avg_flat,
                COUNT(*) as benchmark_count
            FROM profile_entries
            JOIN benchmarks USING (benchmark_id)
            WHERE function = ?
            GROUP BY command
            HAVING avg_cum >= ?
            ORDER BY avg_cum DESC
        """

        cursor.execute(query, (function, min_cum_percent))
        return [
            {
                "command": row[0],
                "avg_cum_percent": round(row[1], 2),
                "avg_flat_percent": round(row[2], 2),
                "benchmark_count": row[3]
            }
            for row in cursor.fetchall()
        ]
    
    def get_function_performance_summary(self, function: str) -> Dict:
        """
        Get comprehensive performance summary for a function across all benchmarks.
        """
        cursor = self.conn.cursor()

        # Get performance stats for this function
        query = """
            SELECT
                AVG(flat_percent) as avg_flat,
                AVG(cum_percent) as avg_cum,
                MAX(flat_percent) as max_flat,
                MAX(cum_percent) as max_cum,
                COUNT(*) as benchmark_count,
                COUNT(DISTINCT command) as command_count,
                COUNT(DISTINCT command_group) as command_group_count
            FROM profile_entries
            JOIN benchmarks USING (benchmark_id)
            WHERE function = ?
        """

        cursor.execute(query, (function,))
        stats = dict(cursor.fetchone())

        # Get commands affected
        commands_data = self.get_commands_affected_by_function(function, min_cum_percent=0.1)

        return {
            "function": function,
            "performance_stats": {
                "avg_flat_percent": round(stats['avg_flat'], 2),
                "avg_cum_percent": round(stats['avg_cum'], 2),
                "max_flat_percent": round(stats['max_flat'], 2),
                "max_cum_percent": round(stats['max_cum'], 2)
            },
            "coverage": {
                "benchmark_count": stats['benchmark_count'],
                "command_count": stats['command_count'],
                "command_group_count": stats['command_group_count']
            },
            "commands_affected": commands_data
        }

    # Compatibility methods for existing function tools
    def function_coverage_in_benchmarks(self, function_name: str, min_cum_percent: float = 1.0) -> List[Dict]:
        """Find benchmarks that cover a function above threshold"""
        cursor = self.conn.cursor()

        query = """
            SELECT
                pe.benchmark_id,
                b.command,
                b.command_group,
                pe.function,
                pe.flat_percent,
                pe.cum_percent
            FROM profile_entries pe
            JOIN benchmarks b USING (benchmark_id)
            WHERE pe.function LIKE ? AND pe.cum_percent >= ?
            ORDER BY pe.cum_percent DESC
        """

        cursor.execute(query, (f"%{function_name}%", min_cum_percent))
        return [dict(row) for row in cursor.fetchall()]

    def commands_affected_by_function(self, function_name: str) -> Dict[str, List[str]]:
        """Find Redis commands and command groups affected by a function"""
        commands_data = self.get_commands_affected_by_function(function_name, min_cum_percent=0.1)

        commands = set()
        command_groups = set()

        for entry in commands_data:
            commands.add(entry['command'])
            command_groups.add(entry['command_group'])

        return {
            "commands": list(commands),
            "command_groups": list(command_groups)
        }

    def top_hotspots_all_benchmarks(self, limit: int = 20) -> List[Dict]:
        """Get top hotspots across all benchmarks"""
        cursor = self.conn.cursor()

        query = """
            SELECT
                function,
                AVG(flat_percent) as avg_flat,
                AVG(cum_percent) as avg_cum,
                COUNT(DISTINCT benchmark_id) as benchmark_count
            FROM profile_entries
            GROUP BY function
            ORDER BY avg_cum DESC
            LIMIT ?
        """

        cursor.execute(query, (limit,))
        return [
            {
                "function_name": row[0],
                "avg_flat_percent": round(row[1], 2),
                "avg_cum_percent": round(row[2], 2),
                "benchmark_count": row[3]
            }
            for row in cursor.fetchall()
        ]

    def top_hotspots_by_command_group(self, command_group: str, limit: int = 20) -> List[Dict]:
        """Get top hotspots for a specific command group"""
        return self.get_top_functions_for_command_group(command_group, limit)

    def benchmarks_by_command_group(self, command_group: str) -> List[Dict]:
        """Find benchmarks that test a specific command group"""
        cursor = self.conn.cursor()

        query = """
            SELECT
                benchmark_id,
                command,
                command_group,
                profile_source
            FROM benchmarks
            WHERE command_group = ?
            ORDER BY run_time DESC
        """

        cursor.execute(query, (command_group,))
        return [dict(row) for row in cursor.fetchall()]

    def search_functions_by_name(self, function_name: str) -> List[Dict]:
        """Search functions by name pattern"""
        cursor = self.conn.cursor()

        query = """
            SELECT
                pe.function,
                AVG(pe.flat_percent) as avg_flat,
                AVG(pe.cum_percent) as avg_cum,
                COUNT(DISTINCT pe.benchmark_id) as benchmark_count
            FROM profile_entries pe
            WHERE pe.function LIKE ?
            GROUP BY pe.function
            ORDER BY avg_cum DESC
        """

        cursor.execute(query, (f"%{function_name}%",))
        return [
            {
                "function_name": row[0],
                "avg_flat_percent": round(row[1], 2),
                "avg_cum_percent": round(row[2], 2),
                "benchmark_count": row[3]
            }
            for row in cursor.fetchall()
        ]
            ORDER BY samples DESC
        """, (f"%{function_name}%",))
        callees = [dict(row) for row in cursor.fetchall()]
        
        # Stack position analysis
        cursor.execute("""
            SELECT 
                sf.position,
                COUNT(*) as occurrences,
                SUM(st.sample_count) as total_samples,
                AVG(st.stack_depth) as avg_stack_depth
            FROM stack_frames sf
            JOIN stack_traces st ON sf.stack_trace_id = st.id
            WHERE sf.function_name LIKE ?
            GROUP BY sf.position
            ORDER BY total_samples DESC
        """, (f"%{function_name}%",))
        positions = [dict(row) for row in cursor.fetchall()]
        
        # Interaction with unknowns
        cursor.execute("""
            SELECT 
                COUNT(CASE WHEN st.has_unknowns THEN 1 END) as stacks_with_unknowns,
                COUNT(*) as total_stacks,
                SUM(CASE WHEN st.has_unknowns THEN st.sample_count ELSE 0 END) as samples_with_unknowns,
                SUM(st.sample_count) as total_samples
            FROM stack_frames sf
            JOIN stack_traces st ON sf.stack_trace_id = st.id
            WHERE sf.function_name LIKE ?
        """, (f"%{function_name}%",))
        unknown_stats = dict(cursor.fetchone())
        
        return {
            "function_name": function_name,
            "callers": callers,
            "callees": callees,
            "position_analysis": positions,
            "unknown_interaction": unknown_stats
        }
    
    def search_functions_by_pattern(self, pattern: str, include_unknowns: bool = True) -> List[Dict]:
        """
        Search functions using FTS with option to include/exclude unknowns.
        """
        cursor = self.conn.cursor()
        
        query = """
            SELECT 
                fh.function_name,
                fh.cleaned_name,
                fh.total_samples,
                fh.percentage,
                fh.is_unknown,
                b.name as benchmark_name
            FROM function_hotspots fh
            JOIN benchmarks b ON fh.benchmark_id = b.id
            WHERE (fh.function_name LIKE ? OR fh.cleaned_name LIKE ?)
        """
        
        params = [f"%{pattern}%", f"%{pattern}%"]
        
        if not include_unknowns:
            query += " AND fh.is_unknown = FALSE"
        
        query += " ORDER BY fh.total_samples DESC"
        
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def get_benchmark_hotspots_with_context(self, benchmark_id: str, limit: int = 20) -> List[Dict]:
        """
        Get top hotspots for a benchmark with stack context information.
        """
        cursor = self.conn.cursor()
        
        query = """
            SELECT 
                fh.function_name,
                fh.total_samples,
                fh.percentage,
                fh.is_unknown,
                -- Count how many different stack traces hit this function
                COUNT(DISTINCT sf.stack_trace_id) as unique_stacks,
                -- Count stacks with unknowns
                COUNT(CASE WHEN st.has_unknowns THEN 1 END) as stacks_with_unknowns,
                -- Average stack position
                AVG(sf.position) as avg_position,
                -- Sample stack trace
                (SELECT st2.full_stack 
                 FROM stack_traces st2 
                 JOIN stack_frames sf2 ON st2.id = sf2.stack_trace_id
                 WHERE sf2.function_name = fh.function_name 
                   AND st2.benchmark_id = fh.benchmark_id
                 ORDER BY st2.sample_count DESC 
                 LIMIT 1) as sample_stack
            FROM function_hotspots fh
            JOIN stack_frames sf ON sf.function_name = fh.function_name
            JOIN stack_traces st ON sf.stack_trace_id = st.id AND st.benchmark_id = fh.benchmark_id
            WHERE fh.benchmark_id = ?
            GROUP BY fh.function_name, fh.total_samples, fh.percentage, fh.is_unknown
            ORDER BY fh.total_samples DESC
            LIMIT ?
        """
        
        cursor.execute(query, (benchmark_id, limit))
        return [dict(row) for row in cursor.fetchall()]
    
    def compare_benchmarks_by_function(self, function_name: str) -> List[Dict]:
        """
        Compare how a function performs across different benchmarks.
        """
        cursor = self.conn.cursor()
        
        query = """
            SELECT 
                b.name as benchmark_name,
                b.tested_commands,
                b.tested_groups,
                fh.total_samples,
                fh.percentage,
                fh.is_unknown,
                COUNT(DISTINCT sf.stack_trace_id) as unique_stacks,
                AVG(sf.position) as avg_stack_position
            FROM function_hotspots fh
            JOIN benchmarks b ON fh.benchmark_id = b.id
            LEFT JOIN stack_frames sf ON sf.function_name = fh.function_name
            LEFT JOIN stack_traces st ON sf.stack_trace_id = st.id AND st.benchmark_id = fh.benchmark_id
            WHERE fh.function_name LIKE ?
            GROUP BY b.id, b.name, b.tested_commands, b.tested_groups, fh.total_samples, fh.percentage, fh.is_unknown
            ORDER BY fh.total_samples DESC
        """
        
        cursor.execute(query, (f"%{function_name}%",))
        return [dict(row) for row in cursor.fetchall()]

    # Compatibility methods for existing function tools
    def function_coverage_in_benchmarks(self, function_name: str, min_percentage: float = 1.0) -> List[Dict]:
        """Find benchmarks that cover a function above threshold"""
        cursor = self.conn.cursor()

        query = """
            SELECT
                fh.benchmark_id,
                b.name as benchmark_name,
                fh.function_name,
                fh.total_samples,
                fh.percentage,
                fh.is_unknown,
                b.tested_commands,
                b.tested_groups
            FROM function_hotspots fh
            JOIN benchmarks b ON fh.benchmark_id = b.id
            WHERE fh.function_name LIKE ? AND fh.percentage >= ?
            ORDER BY fh.percentage DESC
        """

        cursor.execute(query, (f"%{function_name}%", min_percentage))
        return [dict(row) for row in cursor.fetchall()]

    def commands_affected_by_function(self, function_name: str) -> Dict[str, List[str]]:
        """Find Redis commands and command groups affected by a function"""
        cursor = self.conn.cursor()

        query = """
            SELECT DISTINCT b.tested_commands, b.tested_groups
            FROM function_hotspots fh
            JOIN benchmarks b ON fh.benchmark_id = b.id
            WHERE fh.function_name LIKE ?
        """

        cursor.execute(query, (f"%{function_name}%",))
        rows = cursor.fetchall()

        import json
        all_commands = set()
        all_groups = set()

        for row in rows:
            if row['tested_commands']:
                commands = json.loads(row['tested_commands'])
                all_commands.update(commands)
            if row['tested_groups']:
                groups = json.loads(row['tested_groups'])
                all_groups.update(groups)

        return {
            "commands": list(all_commands),
            "command_groups": list(all_groups)
        }

    def top_hotspots_all_benchmarks(self, limit: int = 20) -> List[Dict]:
        """Get top hotspots across all benchmarks"""
        cursor = self.conn.cursor()

        query = """
            SELECT
                fh.function_name,
                SUM(fh.total_samples) as total_samples,
                AVG(fh.percentage) as avg_percentage,
                COUNT(DISTINCT fh.benchmark_id) as benchmark_count,
                COUNT(CASE WHEN fh.is_unknown THEN 1 END) as unknown_instances
            FROM function_hotspots fh
            GROUP BY fh.function_name
            ORDER BY total_samples DESC
            LIMIT ?
        """

        cursor.execute(query, (limit,))
        return [dict(row) for row in cursor.fetchall()]

    def top_hotspots_by_command_group(self, command_group: str, limit: int = 20) -> List[Dict]:
        """Get top hotspots for a specific command group"""
        cursor = self.conn.cursor()

        query = """
            SELECT
                fh.function_name,
                fh.total_samples,
                fh.percentage,
                fh.is_unknown,
                b.name as benchmark_name
            FROM function_hotspots fh
            JOIN benchmarks b ON fh.benchmark_id = b.id
            WHERE b.tested_groups LIKE ?
            ORDER BY fh.total_samples DESC
            LIMIT ?
        """

        cursor.execute(query, (f"%{command_group}%", limit))
        return [dict(row) for row in cursor.fetchall()]

    def benchmarks_by_command_group(self, command_group: str) -> List[Dict]:
        """Find benchmarks that test a specific command group"""
        cursor = self.conn.cursor()

        query = """
            SELECT
                b.id,
                b.name,
                b.description,
                b.tested_commands,
                b.tested_groups,
                b.total_samples
            FROM benchmarks b
            WHERE b.tested_groups LIKE ?
            ORDER BY b.total_samples DESC
        """

        cursor.execute(query, (f"%{command_group}%",))
        return [dict(row) for row in cursor.fetchall()]

    def search_functions_by_name(self, function_name: str) -> List[Dict]:
        """Search functions by name pattern"""
        cursor = self.conn.cursor()

        query = """
            SELECT
                fh.function_name,
                fh.total_samples,
                fh.percentage,
                fh.is_unknown,
                b.name as benchmark_name
            FROM function_hotspots fh
            JOIN benchmarks b ON fh.benchmark_id = b.id
            WHERE fh.function_name LIKE ?
            ORDER BY fh.total_samples DESC
        """

        cursor.execute(query, (f"%{function_name}%",))
        return [dict(row) for row in cursor.fetchall()]
