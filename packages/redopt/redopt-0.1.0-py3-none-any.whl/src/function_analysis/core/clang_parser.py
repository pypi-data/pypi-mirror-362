"""
LLVM/Clang-based parser for C/C++ function code.
"""

import os
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

from clang.cindex import CursorKind, Index, TranslationUnit

from .models import FunctionMetadata


class ClangParser:
    """Parser using LLVM/Clang to analyze C/C++ function code."""

    def __init__(self, clang_path: Optional[str] = None):
        """Initialize the Clang parser."""
        self.index = Index.create()
        self.clang_path = clang_path

    def parse_function(
        self, code: str, function_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Parse function code using Clang and extract AST.

        Args:
            code: C/C++ function code
            function_name: Optional function name to search for

        Returns:
            Dictionary containing AST data and metadata
        """
        # Create temporary file with the code
        with tempfile.NamedTemporaryFile(mode="w", suffix=".c", delete=False) as f:
            f.write(code)
            temp_file = f.name

        try:
            # Parse with Clang
            translation_unit = self.index.parse(
                temp_file,
                args=["-std=c99"],  # Use C99 standard
                options=TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD,
            )

            if not translation_unit:
                raise ValueError("Failed to parse code with Clang")

            # Extract function information
            function_cursor = self._find_function(
                translation_unit.cursor, function_name
            )
            if not function_cursor:
                raise ValueError(
                    f"Function {function_name or 'main function'} not found"
                )

            # Extract metadata
            metadata = self._extract_metadata(function_cursor, code)

            # Extract AST
            ast_data = self._extract_ast(function_cursor)

            return {
                "metadata": metadata,
                "ast": ast_data,
                "translation_unit": translation_unit,
            }

        finally:
            # Clean up temporary file
            os.unlink(temp_file)

    def _find_function(self, cursor, function_name: Optional[str]):
        """Find the target function in the AST."""
        if cursor.kind == CursorKind.FUNCTION_DECL:
            if function_name is None or cursor.spelling == function_name:
                return cursor

        # Recursively search children
        for child in cursor.get_children():
            result = self._find_function(child, function_name)
            if result:
                return result

        return None

    def _extract_metadata(self, function_cursor, code: str) -> FunctionMetadata:
        """Extract function metadata from cursor."""
        # Get function name
        name = function_cursor.spelling

        # Get return type
        return_type = function_cursor.result_type.spelling

        # Get parameters
        parameters = []
        for arg in function_cursor.get_arguments():
            parameters.append({"name": arg.spelling, "type": arg.type.spelling})

        # Calculate line count (simple approach)
        line_count = len(code.strip().split("\n"))

        # Get location information
        location = function_cursor.location
        start_line = location.line if location.file else None

        return FunctionMetadata(
            name=name,
            return_type=return_type,
            parameters=parameters,
            line_count=line_count,
            start_line=start_line,
            end_line=start_line + line_count - 1 if start_line else None,
        )

    def _extract_ast(self, cursor) -> Dict[str, Any]:
        """Extract AST structure from cursor."""
        node = {
            "kind": cursor.kind.name,
            "spelling": cursor.spelling,
            "type": cursor.type.spelling if cursor.type else None,
            "children": [],
        }

        # Recursively process children
        for child in cursor.get_children():
            child_node = self._extract_ast(child)
            node["children"].append(child_node)

        return node

    def extract_function_calls(self, cursor) -> List[Dict[str, Any]]:
        """
        Extract all function calls from a function cursor.

        Args:
            cursor: Function cursor to analyze

        Returns:
            List of function call information
        """
        calls = []

        def visit_cursor(cursor):
            # Check for function calls
            if cursor.kind == CursorKind.CALL_EXPR:
                # Get the called function name
                called_function = cursor.spelling
                if called_function:
                    call_info = {
                        "called_function": called_function,
                        "location": {
                            "line": cursor.location.line,
                            "column": cursor.location.column,
                        },
                        "arguments": [],
                    }

                    # Extract argument information
                    for arg in cursor.get_arguments():
                        call_info["arguments"].append(
                            {
                                "type": arg.type.spelling if arg.type else None,
                                "spelling": arg.spelling,
                            }
                        )

                    calls.append(call_info)

            # Recursively visit children
            for child in cursor.get_children():
                visit_cursor(child)

        visit_cursor(cursor)
        return calls

    def calculate_complexity(self, ast_data: Dict[str, Any]) -> float:
        """
        Calculate cyclomatic complexity from AST.
        Simple implementation counting decision points.
        """
        complexity = 1  # Base complexity

        def count_decision_points(node):
            nonlocal complexity

            # Decision point node types
            decision_kinds = {
                "IF_STMT",
                "WHILE_STMT",
                "FOR_STMT",
                "DO_STMT",
                "SWITCH_STMT",
                "CASE_STMT",
                "CONDITIONAL_OPERATOR",
                "BINARY_OPERATOR",  # For && and || operators
            }

            if node.get("kind") in decision_kinds:
                complexity += 1

            # Recursively check children
            for child in node.get("children", []):
                count_decision_points(child)

        count_decision_points(ast_data)
        return float(complexity)

    def parse_source_file(
        self, file_path: str, include_dirs: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Parse an entire source file and extract all functions.

        Args:
            file_path: Path to the C/C++ source file
            include_dirs: List of include directories for compilation

        Returns:
            Dictionary containing file info and all extracted functions
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Source file not found: {file_path}")

        # Prepare compilation arguments
        args = ["-std=c99"]
        if include_dirs:
            for inc_dir in include_dirs:
                args.extend(["-I", str(inc_dir)])

        try:
            # Parse with Clang
            translation_unit = self.index.parse(
                str(file_path),
                args=args,
                options=TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD,
            )

            if not translation_unit:
                raise ValueError(f"Failed to parse file with Clang: {file_path}")

            # Extract all functions from the file
            functions = self._extract_all_functions(
                translation_unit.cursor, str(file_path)
            )

            return {
                "file_path": str(file_path),
                "file_name": file_path.name,
                "functions": functions,
                "total_functions": len(functions),
                "translation_unit": translation_unit,
            }

        except Exception as e:
            raise ValueError(f"Failed to parse file {file_path}: {e}")

    def _extract_all_functions(self, cursor, source_file: str) -> List[Dict[str, Any]]:
        """
        Extract all function definitions from a translation unit.

        Args:
            cursor: Root cursor of the translation unit
            source_file: Path to the source file being parsed

        Returns:
            List of function data dictionaries
        """
        functions = []

        def visit_cursor(cursor):
            # Only process cursors from the main source file (not includes)
            if (
                cursor.location.file
                and str(cursor.location.file) == source_file
                and cursor.kind == CursorKind.FUNCTION_DECL
            ):

                # Skip function declarations (signatures) - only process definitions
                # This ensures we only index actual function implementations, not just headers
                if not cursor.is_definition():
                    return

                try:
                    # Extract function code from source
                    function_code = self._extract_function_code(cursor, source_file)
                    if function_code:
                        # Extract metadata
                        metadata = self._extract_metadata(cursor, function_code)

                        # Extract AST
                        ast_data = self._extract_ast(cursor)

                        # Calculate complexity
                        complexity = self.calculate_complexity(ast_data)
                        metadata.complexity_score = complexity

                        functions.append(
                            {
                                "metadata": metadata,
                                "ast": ast_data,
                                "code": function_code,
                                "location": {
                                    "file": str(cursor.location.file),
                                    "line": cursor.location.line,
                                    "column": cursor.location.column,
                                },
                            }
                        )
                except Exception as e:
                    print(f"Warning: Failed to process function {cursor.spelling}: {e}")

            # Recursively visit children
            for child in cursor.get_children():
                visit_cursor(child)

        visit_cursor(cursor)
        return functions

    def _extract_function_code(self, cursor, source_file: str) -> Optional[str]:
        """
        Extract the complete function code from the source file.

        Args:
            cursor: Function cursor
            source_file: Path to the source file

        Returns:
            Function code as string or None if extraction fails
        """
        try:
            # Get function extent
            start = cursor.extent.start
            end = cursor.extent.end

            if not start.file or str(start.file) != source_file:
                return None

            # Read the source file
            with open(source_file, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()

            # Extract function lines
            start_line = start.line - 1  # Convert to 0-based
            end_line = end.line - 1

            if start_line < 0 or end_line >= len(lines):
                return None

            # Get the function code
            if start_line == end_line:
                # Single line function
                function_code = lines[start_line][start.column - 1 : end.column]
            else:
                # Multi-line function
                function_lines = []

                # First line (from start column)
                function_lines.append(lines[start_line][start.column - 1 :])

                # Middle lines (complete lines)
                for i in range(start_line + 1, end_line):
                    function_lines.append(lines[i])

                # Last line (up to end column)
                if end_line < len(lines):
                    function_lines.append(lines[end_line][: end.column])

                function_code = "".join(function_lines)

            return function_code.strip()

        except Exception as e:
            print(
                f"Warning: Failed to extract code for function {cursor.spelling}: {e}"
            )
            return None

    def parse_directory(
        self,
        directory_path: str,
        file_extensions: Optional[List[str]] = None,
        include_dirs: Optional[List[str]] = None,
        recursive: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Parse all C/C++ files in a directory.

        Args:
            directory_path: Path to the directory to parse
            file_extensions: List of file extensions to process (default: ['.c', '.cpp', '.h'])
            include_dirs: List of include directories
            recursive: Whether to search subdirectories recursively

        Returns:
            List of file parsing results
        """
        if file_extensions is None:
            file_extensions = [".c", ".cpp", ".cc", ".cxx", ".h", ".hpp"]

        directory = Path(directory_path)
        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")

        # Find all source files
        source_files = []
        if recursive:
            for ext in file_extensions:
                source_files.extend(directory.rglob(f"*{ext}"))
        else:
            for ext in file_extensions:
                source_files.extend(directory.glob(f"*{ext}"))

        # Parse each file
        results = []
        for file_path in source_files:
            try:
                result = self.parse_source_file(str(file_path), include_dirs)
                results.append(result)
            except Exception as e:
                print(f"Warning: Failed to parse {file_path}: {e}")
                # Add error result
                results.append(
                    {
                        "file_path": str(file_path),
                        "file_name": file_path.name,
                        "functions": [],
                        "total_functions": 0,
                        "error": str(e),
                    }
                )

        return results

    def build_call_tree(
        self,
        directory_path: str,
        file_extensions: Optional[List[str]] = None,
        include_dirs: Optional[List[str]] = None,
        recursive: bool = True,
    ) -> Dict[str, Any]:
        """
        Build a complete call tree for all functions in a codebase.

        Args:
            directory_path: Path to the directory to analyze
            file_extensions: List of file extensions to process
            include_dirs: List of include directories
            recursive: Whether to search subdirectories recursively

        Returns:
            Dictionary containing call tree information:
            {
                "functions": {function_name: {metadata, calls_made, called_by}},
                "call_graph": {caller: [callees]},
                "reverse_call_graph": {callee: [callers]}
            }
        """
        # Parse all files in the directory
        file_results = self.parse_directory(
            directory_path, file_extensions, include_dirs, recursive
        )

        # Build function registry and call relationships
        functions = {}
        call_graph = {}  # caller -> [callees]
        reverse_call_graph = {}  # callee -> [callers]

        # First pass: collect all functions
        for file_result in file_results:
            if "error" in file_result:
                continue

            for func_data in file_result["functions"]:
                func_name = func_data["metadata"].name
                functions[func_name] = {
                    "metadata": func_data["metadata"],
                    "location": func_data["location"],
                    "calls_made": [],
                    "called_by": [],
                }
                call_graph[func_name] = []
                if func_name not in reverse_call_graph:
                    reverse_call_graph[func_name] = []

        # Second pass: extract function calls and build relationships
        for file_result in file_results:
            if "error" in file_result:
                continue

            # Re-parse file to get cursors for call extraction
            try:
                file_path = file_result["file_path"]
                translation_unit = self.index.parse(
                    file_path,
                    args=["-std=c99"]
                    + ([f"-I{d}" for d in include_dirs] if include_dirs else []),
                    options=TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD,
                )

                if translation_unit:
                    self._extract_calls_from_file(
                        translation_unit.cursor,
                        file_path,
                        functions,
                        call_graph,
                        reverse_call_graph,
                    )

            except Exception as e:
                print(
                    f"Warning: Failed to extract calls from {file_result['file_path']}: {e}"
                )

        return {
            "functions": functions,
            "call_graph": call_graph,
            "reverse_call_graph": reverse_call_graph,
            "statistics": {
                "total_functions": len(functions),
                "total_call_relationships": sum(
                    len(callees) for callees in call_graph.values()
                ),
            },
        }

    def _extract_calls_from_file(
        self,
        cursor,
        source_file: str,
        functions: Dict[str, Any],
        call_graph: Dict[str, List[str]],
        reverse_call_graph: Dict[str, List[str]],
    ):
        """Extract function calls from a file and update call graphs."""

        def visit_cursor(cursor):
            # Process function definitions
            if (
                cursor.kind == CursorKind.FUNCTION_DECL
                and cursor.location.file
                and str(cursor.location.file) == source_file
                and cursor.is_definition()
            ):

                caller_name = cursor.spelling
                if caller_name in functions:
                    # Extract calls made by this function
                    calls = self.extract_function_calls(cursor)

                    for call in calls:
                        callee_name = call["called_function"]

                        # Update call relationships
                        if callee_name not in call_graph[caller_name]:
                            call_graph[caller_name].append(callee_name)
                            functions[caller_name]["calls_made"].append(call)

                        # Update reverse call graph
                        if callee_name not in reverse_call_graph:
                            reverse_call_graph[callee_name] = []
                        if caller_name not in reverse_call_graph[callee_name]:
                            reverse_call_graph[callee_name].append(caller_name)

                        # Update called_by for the callee if it exists
                        if callee_name in functions:
                            if caller_name not in [
                                c["caller"] for c in functions[callee_name]["called_by"]
                            ]:
                                functions[callee_name]["called_by"].append(
                                    {"caller": caller_name, "call_info": call}
                                )

            # Recursively visit children
            for child in cursor.get_children():
                visit_cursor(child)

        visit_cursor(cursor)
