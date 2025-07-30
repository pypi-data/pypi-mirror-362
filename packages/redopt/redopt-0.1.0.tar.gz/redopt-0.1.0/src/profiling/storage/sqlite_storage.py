"""
SQLite storage for profiling data with full stack trace support.
Preserves stack context and handles unknown functions properly.
"""

import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class SQLiteProfileStorage:
    """SQLite storage layer for benchmark profiles with stack trace support"""
    
    def __init__(self, db_path: str = "profiling.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Enable dict-like access
        self._init_database()
    
    def _init_database(self):
        """Initialize database schema for pprof-based profiling"""
        # Define schema directly to avoid parsing issues
        schema_statements = [
            """CREATE TABLE IF NOT EXISTS benchmarks (
                benchmark_id TEXT PRIMARY KEY,
                command TEXT,
                command_group TEXT,
                profile_source TEXT,
                run_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",

            """CREATE TABLE IF NOT EXISTS profile_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                benchmark_id TEXT NOT NULL,
                function TEXT NOT NULL,
                flat_percent REAL NOT NULL,
                cum_percent REAL NOT NULL,
                FOREIGN KEY (benchmark_id) REFERENCES benchmarks(benchmark_id)
            )""",

            # Indexes
            "CREATE INDEX IF NOT EXISTS idx_benchmarks_command ON benchmarks(command)",
            "CREATE INDEX IF NOT EXISTS idx_benchmarks_command_group ON benchmarks(command_group)",
            "CREATE INDEX IF NOT EXISTS idx_profile_entries_benchmark ON profile_entries(benchmark_id)",
            "CREATE INDEX IF NOT EXISTS idx_profile_entries_function ON profile_entries(function)",
            "CREATE INDEX IF NOT EXISTS idx_profile_entries_flat_percent ON profile_entries(flat_percent DESC)",
            "CREATE INDEX IF NOT EXISTS idx_profile_entries_cum_percent ON profile_entries(cum_percent DESC)"
        ]

        for statement in schema_statements:
            try:
                self.conn.execute(statement)
            except sqlite3.Error as e:
                print(f"Schema warning: {e}")

        self.conn.commit()
        print("✅ SQLite database initialized")
    
    def insert_benchmark(self, benchmark_id: str, command: str, command_group: str,
                        profile_source: str, entries: List[Dict[str, Any]]) -> None:
        """Insert a benchmark and its profile entries"""
        cursor = self.conn.cursor()

        try:
            # Store benchmark metadata
            cursor.execute("""
                INSERT OR REPLACE INTO benchmarks (
                    benchmark_id, command, command_group, profile_source, run_time
                ) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (benchmark_id, command, command_group, profile_source))

            # Store profile entries
            for entry in entries:
                cursor.execute("""
                    INSERT INTO profile_entries (
                        benchmark_id, function, flat_percent, cum_percent
                    ) VALUES (?, ?, ?, ?)
                """, (
                    benchmark_id,
                    entry['function'],
                    entry['flat_percent'],
                    entry['cum_percent']
                ))

            self.conn.commit()
            print(f"✅ Stored benchmark: {benchmark_id} with {len(entries)} profile entries")

        except Exception as e:
            self.conn.rollback()
            print(f"❌ Error storing benchmark: {e}")
            raise

    def ingest_from_pprof_top_json(self, benchmark_id: str, command: str, command_group: str,
                                  profile_source: str, json_data: List[Dict]) -> None:
        """Wrapper to insert both benchmark metadata and parsed pprof entries"""
        self.insert_benchmark(benchmark_id, command, command_group, profile_source, json_data)
    
    def get_top_functions_for_command_group(self, command_group: str, top_n: int = 10) -> List[Tuple[str, float, float]]:
        """Returns top N functions by average cumulative % across all benchmarks in the group"""
        cursor = self.conn.cursor()

        query = """
            SELECT function, AVG(flat_percent) AS avg_flat, AVG(cum_percent) AS avg_cum
            FROM profile_entries
            JOIN benchmarks USING (benchmark_id)
            WHERE command_group = ?
            GROUP BY function
            ORDER BY avg_cum DESC
            LIMIT ?
        """

        cursor.execute(query, (command_group, top_n))
        return [(row[0], round(row[1], 2), round(row[2], 2)) for row in cursor.fetchall()]

    def get_commands_affected_by_function(self, function: str, min_cum_percent: float = 1.0) -> List[Tuple[str, float]]:
        """For a given function, return all commands where it appears with cum_percent >= min_cum_percent"""
        cursor = self.conn.cursor()

        query = """
            SELECT command, AVG(cum_percent) AS avg_cum
            FROM profile_entries
            JOIN benchmarks USING (benchmark_id)
            WHERE function = ?
            GROUP BY command
            HAVING avg_cum >= ?
            ORDER BY avg_cum DESC
        """

        cursor.execute(query, (function, min_cum_percent))
        return [(row[0], round(row[1], 2)) for row in cursor.fetchall()]

    def export_command_summary_to_json(self, command: str) -> Dict[str, Any]:
        """Outputs JSON summarizing top functions for a command"""
        cursor = self.conn.cursor()

        query = """
            SELECT function, AVG(flat_percent) AS avg_flat, AVG(cum_percent) AS avg_cum
            FROM profile_entries
            JOIN benchmarks USING (benchmark_id)
            WHERE command = ?
            GROUP BY function
            ORDER BY avg_cum DESC
            LIMIT 20
        """

        cursor.execute(query, (command,))
        functions = [
            {
                "function": row[0],
                "avg_flat_percent": round(row[1], 2),
                "avg_cum_percent": round(row[2], 2)
            }
            for row in cursor.fetchall()
        ]

        return {
            "command": command,
            "top_functions": functions,
            "total_functions": len(functions)
        }
    

    
    def get_storage_stats(self) -> Dict[str, int]:
        """Get storage statistics"""
        cursor = self.conn.cursor()

        stats = {}

        # Basic counts
        cursor.execute("SELECT COUNT(*) FROM benchmarks")
        stats['total_benchmarks'] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM profile_entries")
        stats['total_profile_entries'] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(DISTINCT function) FROM profile_entries")
        stats['unique_functions'] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(DISTINCT command) FROM benchmarks")
        stats['unique_commands'] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(DISTINCT command_group) FROM benchmarks")
        stats['unique_command_groups'] = cursor.fetchone()[0]

        return stats
    
    def close(self):
        """Close database connection"""
        self.conn.close()
