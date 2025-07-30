"""
Codebase indexing tool for function analysis.
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from tqdm import tqdm

from ..core.clang_parser import ClangParser
from ..core.graph2vec import Graph2VecEncoder
from ..core.graph_converter import GraphConverter
from ..core.models import FunctionAnalysis
from ..storage.redis_client import RedisClient


class CodebaseIndexer:
    """Tool for indexing entire codebases and extracting function analyses."""

    def __init__(
        self,
        output_dir: Optional[str] = None,
        clang_path: Optional[str] = None,
        redis_config: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the codebase indexer.

        Args:
            output_dir: Directory to save JSON files
            clang_path: Path to clang executable
            redis_config: Redis configuration dictionary
        """
        self.output_dir = Path(output_dir) if output_dir else None
        self.clang_path = clang_path

        # Initialize components
        self.parser = ClangParser(clang_path=clang_path)
        self.graph_converter = GraphConverter()
        self.encoder = Graph2VecEncoder(embedding_dim=128)

        # Initialize Redis client if config provided
        self.redis_client = None
        if redis_config:
            self.redis_client = RedisClient(**redis_config)

        # Statistics
        self.stats = {
            "files_processed": 0,
            "files_with_errors": 0,
            "functions_found": 0,
            "functions_unique": 0,
            "functions_duplicates_skipped": 0,
            "functions_analyzed": 0,
            "functions_stored_redis": 0,
            "functions_stored_json": 0,
            "call_tree_built": False,
            "call_tree_functions": 0,
            "call_tree_relationships": 0,
            "call_tree_stored_redis": False,
            "call_tree_stored_json": False,
            "errors": 0,
            "start_time": None,
            "end_time": None,
        }

    def index_codebase(
        self,
        source_dir: str,
        include_dirs: Optional[List[str]] = None,
        file_extensions: Optional[List[str]] = None,
        recursive: bool = True,
        store_redis: bool = True,
        store_json: bool = True,
        build_call_tree: bool = True,
        store_call_tree_redis: bool = True,
        store_call_tree_json: bool = True,
    ) -> Dict[str, Any]:
        """
        Index an entire codebase and optionally build call tree.

        Args:
            source_dir: Directory containing source code
            include_dirs: List of include directories
            file_extensions: File extensions to process
            recursive: Whether to search recursively
            store_redis: Whether to store function analysis results in Redis
            store_json: Whether to store function analysis results as JSON files
            build_call_tree: Whether to build call tree during indexing
            store_call_tree_redis: Whether to store call tree in Redis
            store_call_tree_json: Whether to store call tree as JSON file

        Returns:
            Dictionary with indexing results and statistics
        """
        print(f"🔍 Starting codebase indexing...")
        print(f"📁 Source directory: {source_dir}")
        print(f"📤 Output directory: {self.output_dir}")
        print(f"🔧 Clang path: {self.clang_path or 'default'}")
        print(
            f"🗄️ Redis storage: {'enabled' if store_redis and self.redis_client else 'disabled'}"
        )
        print(
            f"📄 JSON storage: {'enabled' if store_json and self.output_dir else 'disabled'}"
        )
        print(f"🔗 Call tree building: {'enabled' if build_call_tree else 'disabled'}")
        if build_call_tree:
            print(
                f"🗄️ Call tree Redis storage: {'enabled' if store_call_tree_redis and self.redis_client else 'disabled'}"
            )
            print(
                f"📄 Call tree JSON storage: {'enabled' if store_call_tree_json and self.output_dir else 'disabled'}"
            )

        self.stats["start_time"] = datetime.now(timezone.utc)

        # Create output directory if needed
        if store_json and self.output_dir:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            print(f"📁 Created output directory: {self.output_dir}")

        try:
            # Parse all files in the directory
            print(f"\n🔍 Parsing source files...")
            file_results = self.parser.parse_directory(
                directory_path=source_dir,
                file_extensions=file_extensions,
                include_dirs=include_dirs,
                recursive=recursive,
            )

            self.stats["files_processed"] = len(file_results)
            self.stats["files_with_errors"] = sum(
                1 for r in file_results if "error" in r
            )
            print(
                f"📊 Processed {len(file_results)} files ({self.stats['files_with_errors']} with errors)"
            )

            # Collect all functions for encoder fitting
            all_graphs = []
            all_functions = []
            function_signatures = set()  # Track function signatures to avoid duplicates

            print(f"\n🔄 Processing functions from files...")
            for file_result in tqdm(file_results, desc="Processing files"):
                if "error" in file_result:
                    self.stats["errors"] += 1
                    continue

                self.stats["functions_found"] += len(file_result["functions"])

                for func_data in file_result["functions"]:
                    try:
                        # Create a signature for deduplication (name + parameters)
                        func_name = func_data["metadata"].name
                        func_params = tuple(
                            p["type"] for p in func_data["metadata"].parameters
                        )
                        func_signature = (func_name, func_params)

                        # Skip if we've already seen this function signature
                        if func_signature in function_signatures:
                            tqdm.write(f"⚠️  Skipping duplicate function: {func_name}")
                            continue

                        function_signatures.add(func_signature)

                        # Convert AST to graph
                        ast_graph = self.graph_converter.ast_to_graph(func_data["ast"])
                        all_graphs.append(ast_graph)
                        all_functions.append((file_result, func_data, ast_graph))

                    except Exception as e:
                        tqdm.write(
                            f"❌ Error processing function {func_data['metadata'].name}: {e}"
                        )
                        self.stats["errors"] += 1

            self.stats["functions_unique"] = len(all_functions)
            self.stats["functions_duplicates_skipped"] = self.stats[
                "functions_found"
            ] - len(all_functions)

            print(f"📊 Found {len(all_functions)} unique functions to analyze")
            if self.stats["functions_duplicates_skipped"] > 0:
                print(
                    f"⚠️  Skipped {self.stats['functions_duplicates_skipped']} duplicate function signatures"
                )

            # Fit the encoder with all graphs
            if all_graphs:
                print(
                    f"🧠 Training Graph2Vec encoder on {len(all_graphs)} functions..."
                )
                self.encoder.fit(all_graphs)
                print(f"✅ Encoder training complete")

            # Process each function
            print(f"\n🔄 Analyzing functions...")
            analyzed_functions = []

            for file_result, func_data, ast_graph in tqdm(
                all_functions, desc="Analyzing functions"
            ):
                try:
                    # Create analysis
                    analysis = self._create_function_analysis(
                        file_result, func_data, ast_graph
                    )
                    analyzed_functions.append(analysis)

                    # Store in Redis if enabled
                    if store_redis and self.redis_client:
                        success = self.redis_client.store_function_analysis(analysis)
                        if success:
                            self.stats["functions_stored_redis"] += 1

                    # Store as JSON if enabled
                    if store_json and self.output_dir:
                        self._save_function_json(analysis, file_result)
                        self.stats["functions_stored_json"] += 1

                    self.stats["functions_analyzed"] += 1

                except Exception as e:
                    tqdm.write(
                        f"❌ Error analyzing function {func_data['metadata'].name}: {e}"
                    )
                    self.stats["errors"] += 1

            # Build call tree if requested
            call_tree_data = None
            if build_call_tree:
                print(f"\n🔗 Building call tree...")
                try:
                    call_tree_data = self.parser.build_call_tree(
                        directory_path=source_dir,
                        file_extensions=file_extensions,
                        include_dirs=include_dirs,
                        recursive=recursive,
                    )

                    self.stats["call_tree_built"] = True
                    self.stats["call_tree_functions"] = call_tree_data.get(
                        "statistics", {}
                    ).get("total_functions", 0)
                    self.stats["call_tree_relationships"] = call_tree_data.get(
                        "statistics", {}
                    ).get("total_call_relationships", 0)

                    print(
                        f"✅ Call tree built with {self.stats['call_tree_functions']} functions and {self.stats['call_tree_relationships']} relationships"
                    )

                    # Store call tree in Redis if requested
                    if store_call_tree_redis and self.redis_client:
                        success = self.redis_client.store_call_tree(call_tree_data)
                        if success:
                            self.stats["call_tree_stored_redis"] = True
                            print("✅ Call tree stored in Redis successfully")
                        else:
                            print("❌ Failed to store call tree in Redis")

                    # Store call tree as JSON if requested
                    if store_call_tree_json and self.output_dir:
                        self._save_call_tree_json(call_tree_data)
                        self.stats["call_tree_stored_json"] = True

                except Exception as e:
                    print(f"❌ Error building call tree: {e}")
                    self.stats["errors"] += 1

            self.stats["end_time"] = datetime.now(timezone.utc)

            # Save summary
            summary = self._create_summary(analyzed_functions, call_tree_data)
            if store_json and self.output_dir:
                self._save_summary(summary)

            print(f"\n✅ Indexing complete!")
            self._print_statistics()

            return summary

        except Exception as e:
            print(f"❌ Indexing failed: {e}")
            self.stats["end_time"] = datetime.now(timezone.utc)
            raise

    def _create_function_analysis(
        self, file_result: Dict[str, Any], func_data: Dict[str, Any], ast_graph
    ) -> FunctionAnalysis:
        """Create a FunctionAnalysis object from parsed data."""
        # Convert graph to data
        ast_graph_data = self.graph_converter.graph_to_data(ast_graph)
        ast_graph_data.graph_type = "ast"

        # Generate embedding
        embedding = self.encoder.encode(ast_graph)

        # Update metadata with file information
        metadata = func_data["metadata"]
        metadata.source_file = file_result["file_path"]
        metadata.start_line = func_data["location"]["line"]

        # Generate function ID
        function_id = self._generate_function_id(
            func_data["code"], file_result["file_path"], metadata.name
        )

        return FunctionAnalysis(
            id=function_id,
            code=func_data["code"],
            metadata=metadata,
            ast_graph=ast_graph_data,
            embedding=embedding,
        )

    def _generate_function_id(
        self, code: str, file_path: str, function_name: str
    ) -> str:
        """Generate a unique ID for a function."""
        # Use combination of file path, function name, and code hash
        content = f"{file_path}:{function_name}:{code}"
        code_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
        return f"func_{code_hash}"

    def _save_function_json(
        self, analysis: FunctionAnalysis, file_result: Dict[str, Any]
    ):
        """Save function analysis as JSON file."""
        # Create subdirectory structure matching source
        rel_path = Path(file_result["file_path"]).relative_to(
            Path(file_result["file_path"]).anchor
        )
        output_subdir = self.output_dir / rel_path.parent
        output_subdir.mkdir(parents=True, exist_ok=True)

        # Save function JSON
        json_file = output_subdir / f"{analysis.metadata.name}_{analysis.id}.json"
        with open(json_file, "w") as f:
            json.dump(analysis.model_dump(), f, indent=2, default=str)

    def _save_call_tree_json(self, call_tree_data: Dict[str, Any]):
        """Save call tree data as JSON file."""
        # Make call tree serializable for JSON
        serializable_call_tree = self._make_call_tree_serializable(call_tree_data)

        call_tree_file = self.output_dir / "call_tree.json"
        with open(call_tree_file, "w") as f:
            json.dump(serializable_call_tree, f, indent=2, default=str)
        print(f"📄 Saved call tree to: {call_tree_file}")

    def _make_call_tree_serializable(
        self, call_tree_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Convert call tree data to be JSON serializable by converting Pydantic models to dicts.

        Args:
            call_tree_data: Raw call tree data with Pydantic models

        Returns:
            JSON-serializable dictionary
        """
        from ..core.models import FunctionMetadata

        def convert_value(obj):
            """Recursively convert objects to JSON-serializable format."""
            if isinstance(obj, FunctionMetadata):
                return obj.model_dump()
            elif isinstance(obj, dict):
                return {k: convert_value(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_value(item) for item in obj]
            else:
                return obj

        return convert_value(call_tree_data)

    def _create_summary(
        self,
        analyzed_functions: List[FunctionAnalysis],
        call_tree_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create indexing summary."""
        summary = {
            "indexing_info": {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "total_functions": len(analyzed_functions),
                "statistics": self.stats,
            },
            "functions": [
                {
                    "id": func.id,
                    "name": func.metadata.name,
                    "file": func.metadata.source_file,
                    "line": func.metadata.start_line,
                    "complexity": func.metadata.complexity_score,
                    "parameters": len(func.metadata.parameters),
                }
                for func in analyzed_functions
            ],
        }

        # Add call tree information if available
        if call_tree_data:
            summary["call_tree_info"] = {
                "total_functions": call_tree_data.get("statistics", {}).get(
                    "total_functions", 0
                ),
                "total_relationships": call_tree_data.get("statistics", {}).get(
                    "total_call_relationships", 0
                ),
                "sample_relationships": dict(
                    list(call_tree_data.get("call_graph", {}).items())[:5]
                ),
            }

        return summary

    def _save_summary(self, summary: Dict[str, Any]):
        """Save indexing summary."""
        summary_file = self.output_dir / "indexing_summary.json"
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2, default=str)
        print(f"📄 Saved summary to: {summary_file}")

    def _print_statistics(self):
        """Print indexing statistics."""
        duration = (self.stats["end_time"] - self.stats["start_time"]).total_seconds()

        print(f"\n📊 Indexing Statistics:")
        print(f"   ⏱️  Duration: {duration:.1f} seconds")
        print(f"   📁 Files processed: {self.stats['files_processed']}")
        print(f"   ❌ Files with errors: {self.stats['files_with_errors']}")
        print(f"   🔍 Functions found: {self.stats['functions_found']}")
        print(f"   🎯 Unique functions: {self.stats['functions_unique']}")
        print(f"   ⚠️  Duplicates skipped: {self.stats['functions_duplicates_skipped']}")
        print(f"   ✅ Functions analyzed: {self.stats['functions_analyzed']}")
        print(f"   🗄️ Functions stored in Redis: {self.stats['functions_stored_redis']}")
        print(f"   📄 Functions stored as JSON: {self.stats['functions_stored_json']}")

        # Call tree statistics
        if self.stats["call_tree_built"]:
            print(f"   🔗 Call tree built: ✅")
            print(f"   🔗 Call tree functions: {self.stats['call_tree_functions']}")
            print(
                f"   🔗 Call tree relationships: {self.stats['call_tree_relationships']}"
            )
            print(
                f"   🗄️ Call tree stored in Redis: {'✅' if self.stats['call_tree_stored_redis'] else '❌'}"
            )
            print(
                f"   📄 Call tree stored as JSON: {'✅' if self.stats['call_tree_stored_json'] else '❌'}"
            )
        else:
            print(f"   🔗 Call tree built: ❌")

        print(f"   ❌ Total errors: {self.stats['errors']}")

        if self.stats["functions_analyzed"] > 0:
            rate = self.stats["functions_analyzed"] / duration
            print(f"   📈 Analysis rate: {rate:.1f} functions/second")

        success_rate = (
            (self.stats["functions_analyzed"] / self.stats["functions_unique"] * 100)
            if self.stats["functions_unique"] > 0
            else 0
        )
        print(f"   📊 Success rate: {success_rate:.1f}%")


def main():
    """Main entry point for the indexing tool."""
    parser = argparse.ArgumentParser(
        description="Index C/C++ codebase and extract function analyses"
    )

    parser.add_argument("command", choices=["index"], help="Command to execute")

    parser.add_argument("--source", required=True, help="Source directory to index")

    parser.add_argument("--output", help="Output directory for JSON files")

    parser.add_argument("--clang-path", help="Path to clang executable")

    parser.add_argument(
        "--include-dirs", nargs="*", help="Include directories for compilation"
    )

    parser.add_argument(
        "--extensions",
        nargs="*",
        default=[".c", ".cpp", ".h"],
        help="File extensions to process",
    )

    parser.add_argument(
        "--no-recursive",
        action="store_true",
        help="Don't search subdirectories recursively",
    )

    parser.add_argument(
        "--no-redis", action="store_true", help="Don't store results in Redis"
    )

    parser.add_argument("--no-json", action="store_true", help="Don't save JSON files")

    parser.add_argument(
        "--no-call-tree", action="store_true", help="Don't build call tree"
    )

    parser.add_argument(
        "--no-call-tree-redis",
        action="store_true",
        help="Don't store call tree in Redis",
    )

    parser.add_argument(
        "--no-call-tree-json",
        action="store_true",
        help="Don't save call tree as JSON",
    )

    parser.add_argument("--redis-host", default="localhost", help="Redis host")

    parser.add_argument("--redis-port", type=int, default=6379, help="Redis port")

    args = parser.parse_args()

    if args.command == "index":
        try:
            # Setup Redis config
            redis_config = None
            if not args.no_redis:
                redis_config = {"host": args.redis_host, "port": args.redis_port}

            # Create indexer
            indexer = CodebaseIndexer(
                output_dir=args.output,
                clang_path=args.clang_path,
                redis_config=redis_config,
            )

            # Run indexing
            indexer.index_codebase(
                source_dir=args.source,
                include_dirs=args.include_dirs,
                file_extensions=args.extensions,
                recursive=not args.no_recursive,
                store_redis=not args.no_redis,
                store_json=not args.no_json,
                build_call_tree=not args.no_call_tree,
                store_call_tree_redis=not args.no_call_tree_redis,
                store_call_tree_json=not args.no_call_tree_json,
            )

        except Exception as e:
            print(f"❌ Indexing failed: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
