"""
Parser for perf script collapsed format data.
"""

import re
from pathlib import Path
from typing import Dict, List, Set

from ..models import FunctionHotspot


class PerfScriptParser:
    """Parser for perf script collapsed stack format."""

    def __init__(self):
        self.function_pattern = re.compile(r"^([^;]+);.*\s+(\d+)$")

    def parse_collapsed_file(
        self, file_path: str
    ) -> tuple[List[FunctionHotspot], dict]:
        """
        Parse a collapsed stack format file and extract function hotspots and metadata.

        Format:
        # comment lines with metadata
        stack_trace sample_count
        Example:
        # benchmark_name=memtier_benchmark-100Kkeys-hash-hgetall
        # redis_git_sha1=75cdc51f
        main;redis_main;serverCron;dictScan 1234

        Args:
            file_path: Path to collapsed stack file

        Returns:
            Tuple of (List of FunctionHotspot objects sorted by percentage, metadata dict)
        """
        function_samples = {}
        total_samples = 0
        metadata = {}

        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                # Parse comment lines for metadata
                if line.startswith("#"):
                    self._parse_metadata_line(line, metadata)
                    continue

                # Split stack trace and sample count
                parts = line.rsplit(" ", 1)
                if len(parts) != 2:
                    continue

                stack_trace, sample_count_str = parts
                try:
                    sample_count = int(sample_count_str)
                except ValueError:
                    continue

                total_samples += sample_count

                # Extract functions from stack trace
                functions = stack_trace.split(";")
                for func in functions:
                    func = func.strip()
                    if func:
                        # Clean up function names (remove addresses, etc.)
                        func = self._clean_function_name(func)
                        if func:
                            function_samples[func] = (
                                function_samples.get(func, 0) + sample_count
                            )

        # Convert to hotspots
        hotspots = []
        for func_name, samples in function_samples.items():
            percentage = (samples / total_samples * 100) if total_samples > 0 else 0

            hotspot = FunctionHotspot(
                function_name=func_name,
                file_path="unknown",  # TODO: Extract from debug info if available
                percentage=percentage,
                total_samples=samples,
                benchmarks=[],  # Will be set by caller
                commands=[],  # Will be mapped later
                command_groups=[],  # Will be mapped later
            )
            hotspots.append(hotspot)

        # Sort by percentage descending
        hotspots.sort(key=lambda h: h.percentage, reverse=True)

        return hotspots, metadata

    def _parse_metadata_line(self, line: str, metadata: dict):
        """Parse metadata from comment lines in the format # key=value"""
        line = line.lstrip("#").strip()
        if "=" in line:
            key, value = line.split("=", 1)
            metadata[key.strip()] = value.strip()

    def _clean_function_name(self, func_name: str) -> str:
        """Clean up function name by removing addresses and other noise."""
        # Remove hex addresses
        func_name = re.sub(r"\+0x[0-9a-fA-F]+", "", func_name)
        func_name = re.sub(r"0x[0-9a-fA-F]+", "", func_name)

        # Remove file paths and line numbers
        func_name = re.sub(r"\s+\([^)]+\)", "", func_name)

        # Extract just the function name if it contains module info
        if "!" in func_name:
            func_name = func_name.split("!")[-1]

        # Remove leading/trailing whitespace and special chars
        func_name = func_name.strip("[]() \t")

        # Skip if it's just noise
        if not func_name or func_name in ["[unknown]", "??", "[kernel]"]:
            return ""

        return func_name
