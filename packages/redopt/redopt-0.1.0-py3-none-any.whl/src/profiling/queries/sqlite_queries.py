"""
Advanced SQLite queries for pprof profiling data analysis.
Demonstrates the power of SQL for function performance analysis.
"""

import sqlite3
from typing import Dict, List, Optional

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
