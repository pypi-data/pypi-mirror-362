"""
Profiling data indexing tool.
"""

import argparse
import glob
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional

import yaml

from ..models import BenchmarkDefinition, BenchmarkProfile, FunctionHotspot
from ..parsers.perf_parser import PerfScriptParser
from ..storage.sqlite_storage import SQLiteProfileStorage


def _parse_pprof_top_output(pprof_file: str, top_n: int = 50) -> List[dict]:
    """
    Parse pprof file using pprof -top command and extract function data.

    Args:
        pprof_file: Path to pprof file
        top_n: Number of top functions to extract

    Returns:
        List of dicts with function, flat_percent, cum_percent
    """
    try:
        # Run pprof -top command
        result = subprocess.run(
            ['pprof', '-top', '-nodecount', str(top_n), pprof_file],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            print(f"   ⚠️  pprof command failed: {result.stderr}")
            return []

        # Parse the output
        lines = result.stdout.strip().split('\n')

        # Find the start of the data (after headers)
        data_start = None
        for i, line in enumerate(lines):
            if 'flat' in line and 'flat%' in line and 'sum%' in line:
                data_start = i + 1
                break

        if data_start is None:
            print("   ⚠️  Could not find data section in pprof output")
            return []

        entries = []
        for line in lines[data_start:]:
            line = line.strip()
            if not line or line.startswith('Dropped') or line.startswith('Showing'):
                continue

            # Parse line format: flat flat% sum% cum cum% function_name
            parts = line.split()
            if len(parts) >= 6:
                try:
                    flat_percent = float(parts[1].rstrip('%'))
                    cum_percent = float(parts[4].rstrip('%'))
                    function_name = ' '.join(parts[5:])  # Function name might have spaces

                    entries.append({
                        'function': function_name,
                        'flat_percent': flat_percent,
                        'cum_percent': cum_percent
                    })
                except (ValueError, IndexError):
                    continue

        return entries

    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"   ⚠️  Error running pprof command: {e}")
        return []
    except Exception as e:
        print(f"   ⚠️  Error parsing pprof output: {e}")
        return []


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

    # Check database indexes and stack trace stats
    cursor.execute("SELECT COUNT(*) FROM benchmarks")
    benchmark_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM function_hotspots")
    hotspot_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM stack_traces")
    stack_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM stack_traces WHERE has_unknowns = 1")
    unknown_stack_count = cursor.fetchone()[0]

    print(
        f"   🔍 Search indexes: {benchmark_count} benchmarks, {hotspot_count} hotspots indexed"
    )
    print(
        f"   📊 Stack traces: {stack_count:,} total, {unknown_stack_count:,} with unknowns ({unknown_stack_count/stack_count*100:.1f}%)"
    )


def index_profile(
    benchmark_file: str,
    pprof_file: str,
    output_dir: Optional[str] = None,
    db_path: str = "profiling.db",
) -> bool:
    """
    Index profiling data from benchmark YAML and perf script.

    Args:
        benchmark_file: Path to benchmark YAML file
        perf_script_file: Path to perf script collapsed format file
        output_dir: Optional output directory for JSON files
        redis_host: Redis host
        redis_port: Redis port

    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"🔥 Starting profiling data indexing...")
        print(f"📄 Benchmark file: {benchmark_file}")
        print(f"📊 Pprof file: {pprof_file}")
        print(f"📁 Output directory: {output_dir or 'None'}")
        print(f"🗄️ SQLite database: {db_path}")

        # Load benchmark definition
        print("\n📋 Loading benchmark definition...")
        with open(benchmark_file, "r") as f:
            benchmark_data = yaml.safe_load(f)

        benchmark_def = BenchmarkDefinition.from_yaml_data(benchmark_data)
        print(f"✅ Loaded benchmark: {benchmark_def.name}")
        print(f"   Description: {benchmark_def.description}")
        print(f"   Tested groups: {benchmark_def.tested_groups}")
        print(f"   Tested commands: {benchmark_def.tested_commands}")

        # Parse pprof data (placeholder - would use pprof -top command)
        print("\n🔍 Parsing pprof data...")

        # Extract benchmark ID from pprof filename
        benchmark_id = (
            os.path.basename(pprof_file).replace(".pb.gz", "").replace(".pprof", "")
        )

        # Determine command and command group from benchmark definition
        command = (
            benchmark_def.tested_commands[0]
            if benchmark_def.tested_commands
            else "unknown"
        )
        command_group = (
            benchmark_def.tested_groups[0] if benchmark_def.tested_groups else "unknown"
        )

        # Parse pprof data using pprof -top command
        profile_entries = _parse_pprof_top_output(pprof_file)

        print(f"✅ Parsed {len(profile_entries)} profile entries from pprof")
        print(f"📊 Benchmark ID: {benchmark_id}")
        print(f"🎯 Command: {command}, Group: {command_group}")

        print(f"📊 Profile summary:")
        print(f"   Profile entries: {len(profile_entries)}")
        if profile_entries:
            top_entry = max(profile_entries, key=lambda x: x["cum_percent"])
            print(
                f"   Top function: {top_entry['function']} ({top_entry['cum_percent']:.2f}% cum)"
            )

        # Connect to SQLite and store
        print("\n🗄️ Storing in SQLite...")
        storage = SQLiteProfileStorage(db_path)
        storage.insert_benchmark(
            benchmark_id, command, command_group, pprof_file, profile_entries
        )
        print("✅ Stored benchmark and profile entries in SQLite")

        # Save to JSON if output directory specified
        if output_dir:
            print(f"\n💾 Saving to JSON files...")
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)

            # Save profile entries as JSON
            profile_file = output_path / f"{benchmark_id}.json"
            profile_data = {
                "benchmark_id": benchmark_id,
                "command": command,
                "command_group": command_group,
                "profile_source": pprof_file,
                "profile_entries": profile_entries,
            }
            with open(profile_file, "w") as f:
                import json

                json.dump(profile_data, f, indent=2)
            print(f"✅ Saved profile to {profile_file}")

        print(f"\n🎉 Profiling data indexing completed successfully!")

        # Print comprehensive summary
        print(f"\n📊 Profiling Database Summary:")
        try:
            _print_benchmark_summary(storage)
        except Exception as summary_error:
            print(f"   ⚠️  Could not generate summary: {summary_error}")
            print(f"   📊 Basic stats: 1 benchmark indexed with {len(profile_entries)} profile entries")

        return True

    except Exception as e:
        print(f"❌ Error indexing profiling data: {e}")
        return False


def index_profiles_from_directories(
    benchmark_spec_dir: str,
    pprof_dir: str,
    output_dir: Optional[str] = None,
    db_path: str = "profiling.db",
) -> bool:
    """
    Index profiling data from directories of benchmark specs and pprof files.

    Args:
        benchmark_spec_dir: Directory containing benchmark YAML files
        pprof_dir: Directory containing pprof files (.pb.gz format)
        output_dir: Optional output directory for JSON files
        db_path: SQLite database path

    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"🔥 Starting batch profiling data indexing...")
        print(f"📁 Benchmark specs directory: {benchmark_spec_dir}")
        print(f"📊 Pprof directory: {pprof_dir}")
        print(f"📁 Output directory: {output_dir or 'None'}")
        print(f"🗄️ SQLite database: {db_path}")

        # Find all pprof files
        pprof_path = Path(pprof_dir)
        pprof_files = list(pprof_path.glob("*.pb.gz")) + list(
            pprof_path.glob("*.pprof")
        )

        if not pprof_files:
            print(f"❌ No pprof files found in {pprof_dir}")
            return False

        print(f"\n📊 Found {len(pprof_files)} pprof files")

        # Connect to SQLite
        storage = SQLiteProfileStorage(db_path)
        parser = PerfScriptParser()

        successful_profiles = 0
        failed_profiles = 0

        for pprof_file in pprof_files:
            try:
                print(f"\n🔍 Processing {pprof_file.name}...")

                # Extract benchmark ID from pprof filename
                benchmark_id = pprof_file.stem.replace(".pb", "").replace(".pprof", "")

                # For now, derive benchmark name from filename
                # In real implementation, this would be extracted from benchmark specs
                benchmark_name = benchmark_id
                print(f"📋 Benchmark: {benchmark_name}")

                # Find corresponding benchmark spec file
                benchmark_spec_path = Path(benchmark_spec_dir)
                benchmark_file = None

                # Look for exact match first
                exact_match = benchmark_spec_path / f"{benchmark_name}.yml"
                if exact_match.exists():
                    benchmark_file = exact_match
                else:
                    # Search for files containing the benchmark name
                    for spec_file in benchmark_spec_path.glob("*.yml"):
                        if benchmark_name in spec_file.stem:
                            benchmark_file = spec_file
                            break

                if not benchmark_file:
                    print(
                        f"⚠️  No benchmark spec found for {benchmark_name}, creating minimal definition"
                    )
                    # Create a minimal benchmark definition
                    benchmark_def = BenchmarkDefinition(
                        name=benchmark_name,
                        description=f"Auto-generated from {pprof_file.name}",
                        tested_groups=["unknown"],
                        tested_commands=["unknown"],
                        redis_topologies=["oss-standalone"],
                        build_variants=["unknown"],
                        tool="pprof",
                    )
                else:
                    print(f"✅ Found benchmark spec: {benchmark_file.name}")
                    with open(benchmark_file, "r") as f:
                        benchmark_data = yaml.safe_load(f)
                    benchmark_def = BenchmarkDefinition.from_yaml_data(benchmark_data)

                # Determine command and command group from benchmark definition
                command = (
                    benchmark_def.tested_commands[0]
                    if benchmark_def.tested_commands
                    else "unknown"
                )
                command_group = (
                    benchmark_def.tested_groups[0]
                    if benchmark_def.tested_groups
                    else "unknown"
                )

                # Parse pprof data using pprof -top command
                profile_entries = _parse_pprof_top_output(pprof_file)

                # Store in SQLite
                storage.insert_benchmark(
                    benchmark_id,
                    command,
                    command_group,
                    str(pprof_file),
                    profile_entries,
                )

                # Save to JSON if output directory specified
                if output_dir:
                    output_path = Path(output_dir)
                    output_path.mkdir(parents=True, exist_ok=True)
                    profile_file = output_path / f"{benchmark_id}.json"
                    profile_data = {
                        "benchmark_id": benchmark_id,
                        "command": command,
                        "command_group": command_group,
                        "profile_source": str(pprof_file),
                        "profile_entries": profile_entries,
                    }
                    with open(profile_file, "w") as f:
                        import json

                        json.dump(profile_data, f, indent=2)

                print(
                    f"✅ Indexed profile for {benchmark_name} ({len(profile_entries)} entries)"
                )
                successful_profiles += 1

            except Exception as e:
                print(f"❌ Error processing {pprof_file.name}: {e}")
                failed_profiles += 1

        print(f"\n🎉 Batch indexing completed!")
        print(f"✅ Successfully indexed: {successful_profiles} profiles")
        if failed_profiles > 0:
            print(f"❌ Failed to index: {failed_profiles} profiles")

        # Print comprehensive summary
        print(f"\n📊 Profiling Database Summary:")
        _print_benchmark_summary(storage)

        return successful_profiles > 0

    except Exception as e:
        print(f"❌ Error in batch indexing: {e}")
        return False



def main():
    """Main entry point for the profiling indexing tool."""
    parser = argparse.ArgumentParser(
        description="Index profiling data from benchmark YAML and pprof files"
    )

    # Create mutually exclusive group for single file vs directory processing
    input_group = parser.add_mutually_exclusive_group(required=True)

    # Single file mode (legacy)
    input_group.add_argument(
        "--benchmark", help="Path to single benchmark YAML file (use with --pprof)"
    )

    # Directory mode (new)
    input_group.add_argument(
        "--benchmark-spec-dir",
        help="Directory containing benchmark YAML specification files",
    )

    parser.add_argument(
        "--pprof",
        help="Path to single pprof file (.pb.gz format) (use with --benchmark)",
    )

    parser.add_argument(
        "--pprof-dir",
        help="Directory containing pprof files (.pb.gz format) (use with --benchmark-spec-dir)",
    )

    parser.add_argument(
        "--redis-host", default="localhost", help="Redis host (default: localhost)"
    )

    parser.add_argument(
        "--output",
        help="Output directory for results (optional)",
    )

    parser.add_argument(
        "--db-path",
        default="profiling.db",
        help="SQLite database path (default: profiling.db)",
    )

    args = parser.parse_args()

    # Validate argument combinations
    if args.benchmark and not args.pprof:
        parser.error("--benchmark requires --pprof")

    if args.benchmark_spec_dir and not args.pprof_dir:
        parser.error("--benchmark-spec-dir requires --pprof-dir")

    if args.pprof and not args.benchmark:
        parser.error("--pprof requires --benchmark")

    if args.pprof_dir and not args.benchmark_spec_dir:
        parser.error("--pprof-dir requires --benchmark-spec-dir")

    # Execute appropriate indexing mode
    if args.benchmark:
        # Single file mode
        success = index_profile(
            benchmark_file=args.benchmark,
            pprof_file=args.pprof,
            output_dir=args.output,
            db_path=args.db_path,
        )
    else:
        # Directory mode
        success = index_profiles_from_directories(
            benchmark_spec_dir=args.benchmark_spec_dir,
            pprof_dir=args.pprof_dir,
            output_dir=args.output,
            db_path=args.db_path,
        )

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
