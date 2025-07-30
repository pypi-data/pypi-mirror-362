"""
Interactive chat interface for function analysis service.
"""

import re
import sys
from typing import Optional

from .function_tool import FunctionAnalysisService


class FunctionAnalysisChat:
    """Interactive chat interface for function analysis."""

    def __init__(self):
        """Initialize the chat interface."""
        self.service = FunctionAnalysisService()
        self.current_function_id: Optional[str] = None

    def start(self):
        """Start the interactive chat session."""
        print("🔍 Function Analysis Chat Interface")
        print("=" * 50)
        print("Welcome! I can help you analyze C/C++ functions and find similar code.")
        print("\nCommands:")
        print("  analyze <code>     - Analyze function code")
        print("  similar <id>       - Find similar functions by ID")
        print("  get <id>          - Get function details by ID")
        print("  stats             - Show database statistics")
        print("  list              - List recent functions")
        print("  help              - Show this help")
        print("  quit/exit         - Exit the chat")
        print("\nYou can also paste multi-line C/C++ code directly!")
        print("-" * 50)

        while True:
            try:
                user_input = self._get_user_input()

                if not user_input.strip():
                    continue

                # Check for exit commands
                if user_input.lower() in ["quit", "exit", "q"]:
                    print("👋 Goodbye!")
                    break

                # Process the input
                self._process_input(user_input)

            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

    def _get_user_input(self) -> str:
        """Get user input, handling multi-line code."""
        print("\n> ", end="")
        first_line = input().strip()

        # Check if this looks like the start of C/C++ code
        if self._looks_like_code_start(first_line):
            print(
                "📝 Multi-line code detected. Continue typing (empty line to finish):"
            )
            lines = [first_line]

            while True:
                try:
                    line = input()
                    if not line.strip():  # Empty line ends input
                        break
                    lines.append(line)
                except EOFError:
                    break

            return "\n".join(lines)

        return first_line

    def _looks_like_code_start(self, line: str) -> bool:
        """Check if a line looks like the start of C/C++ code."""
        code_patterns = [
            r"^\s*(int|void|char|float|double|long|short|unsigned)\s+\w+\s*\(",
            r"^\s*static\s+",
            r"^\s*inline\s+",
            r"^\s*#include\s*<",
            r"^\s*typedef\s+",
            r"^\s*struct\s+\w+",
            r"^\s*/\*",  # Comment start
            r"^\s*//",  # Single line comment
        ]

        return any(re.match(pattern, line) for pattern in code_patterns)

    def _process_input(self, user_input: str):
        """Process user input and execute appropriate command."""
        user_input = user_input.strip()

        # Check for specific commands
        if user_input.lower() == "help":
            self._show_help()
        elif user_input.lower() == "stats":
            self._show_stats()
        elif user_input.lower() == "list":
            self._list_functions()
        elif user_input.lower().startswith("similar "):
            function_id = user_input[8:].strip()
            self._find_similar(function_id)
        elif user_input.lower().startswith("get "):
            function_id = user_input[4:].strip()
            self._get_function(function_id)
        elif user_input.lower().startswith("analyze "):
            code = user_input[8:].strip()
            self._analyze_code(code)
        else:
            # Assume it's code to analyze
            if self._looks_like_code(user_input):
                self._analyze_code(user_input)
            else:
                print(
                    "❓ I didn't understand that. Type 'help' for available commands."
                )

    def _looks_like_code(self, text: str) -> bool:
        """Check if text looks like C/C++ code."""
        # Simple heuristics
        code_indicators = [
            "{",
            "}",
            ";",
            "(",
            ")",
            "int ",
            "void ",
            "char ",
            "float ",
            "double ",
            "if (",
            "for (",
            "while (",
            "return ",
            "#include",
            "printf",
            "malloc",
            "free",
        ]

        return any(indicator in text for indicator in code_indicators)

    def _analyze_code(self, code: str):
        """Analyze the provided code."""
        print("🔍 Analyzing function...")

        try:
            analysis = self.service.analyze_function(code)
            self.current_function_id = analysis.id

            print(f"✅ Analysis complete!")
            print(f"📋 Function: {analysis.metadata.name}")
            print(f"🔄 Return type: {analysis.metadata.return_type}")
            print(f"📊 Parameters: {len(analysis.metadata.parameters)}")
            print(f"📏 Lines: {analysis.metadata.line_count}")
            print(f"🧮 Complexity: {analysis.metadata.complexity_score:.1f}")
            print(f"🆔 Function ID: {analysis.id}")

            # Show parameters if any
            if analysis.metadata.parameters:
                print("📝 Parameters:")
                for param in analysis.metadata.parameters:
                    print(f"   - {param['name']}: {param['type']}")

            # Find similar functions
            print("\n🔍 Finding similar functions...")
            similar = self.service.find_similar_functions(function_id=analysis.id)

            if similar:
                print(f"📊 Found {len(similar)} similar functions:")
                for i, sim in enumerate(similar[:5], 1):  # Show top 5
                    print(
                        f"   {i}. {sim.function_name} (similarity: {sim.similarity_score:.3f})"
                    )
                    print(f"      ID: {sim.function_id}")
                    print(f"      Code: {sim.code_snippet[:100]}...")
                    print()
            else:
                print("📭 No similar functions found.")

        except Exception as e:
            print(f"❌ Analysis failed: {e}")

    def _find_similar(self, function_id: str):
        """Find functions similar to the given function ID."""
        print(f"🔍 Finding functions similar to {function_id}...")

        try:
            similar = self.service.find_similar_functions(function_id=function_id)

            if similar:
                print(f"📊 Found {len(similar)} similar functions:")
                for i, sim in enumerate(similar, 1):
                    print(
                        f"   {i}. {sim.function_name} (similarity: {sim.similarity_score:.3f})"
                    )
                    print(f"      ID: {sim.function_id}")
                    print(f"      Code: {sim.code_snippet[:100]}...")
                    print()
            else:
                print("📭 No similar functions found.")

        except Exception as e:
            print(f"❌ Search failed: {e}")

    def _get_function(self, function_id: str):
        """Get details of a specific function."""
        print(f"📋 Getting function {function_id}...")

        try:
            analysis = self.service.redis_client.get_function_analysis(function_id)

            if analysis:
                print(f"✅ Function found!")
                print(f"📋 Name: {analysis.metadata.name}")
                print(f"🔄 Return type: {analysis.metadata.return_type}")
                print(f"📊 Parameters: {len(analysis.metadata.parameters)}")
                print(f"📏 Lines: {analysis.metadata.line_count}")
                print(f"🧮 Complexity: {analysis.metadata.complexity_score:.1f}")
                print(f"📅 Created: {analysis.created_at}")
                print(f"\n💻 Code:")
                print("-" * 40)
                print(analysis.code)
                print("-" * 40)
            else:
                print("❌ Function not found.")

        except Exception as e:
            print(f"❌ Failed to get function: {e}")

    def _show_stats(self):
        """Show database statistics."""
        print("📊 Database Statistics:")

        try:
            redis_stats = self.service.redis_client.get_stats()
            embedding_stats = self.service.vector_search.get_embedding_statistics()

            print(f"   📦 Total functions: {redis_stats.get('total_functions', 0)}")
            print(f"   🏷️  Unique names: {redis_stats.get('unique_function_names', 0)}")
            print(f"   💾 Memory usage: {redis_stats.get('memory_usage', 'unknown')}")
            print(f"   🔗 Redis connected: {redis_stats.get('redis_connected', False)}")
            print(
                f"   📐 Embedding dimension: {embedding_stats.get('embedding_dimension', 0)}"
            )
            print(
                f"   📊 Total embeddings: {embedding_stats.get('total_embeddings', 0)}"
            )

        except Exception as e:
            print(f"❌ Failed to get stats: {e}")

    def _list_functions(self):
        """List recent functions."""
        print("📋 Recent Functions:")

        try:
            function_ids = self.service.redis_client.get_all_function_ids()

            if function_ids:
                # Show first 10
                for i, function_id in enumerate(function_ids[:10], 1):
                    analysis = self.service.redis_client.get_function_analysis(
                        function_id
                    )
                    if analysis:
                        print(f"   {i}. {analysis.metadata.name} ({function_id})")
                        print(
                            f"      Type: {analysis.metadata.return_type}, Lines: {analysis.metadata.line_count}"
                        )

                if len(function_ids) > 10:
                    print(f"   ... and {len(function_ids) - 10} more")
            else:
                print("   📭 No functions found.")

        except Exception as e:
            print(f"❌ Failed to list functions: {e}")

    def _show_help(self):
        """Show help information."""
        print("📚 Help - Function Analysis Chat")
        print("=" * 40)
        print("Commands:")
        print("  analyze <code>     - Analyze function code")
        print("  similar <id>       - Find similar functions by ID")
        print("  get <id>          - Get function details by ID")
        print("  stats             - Show database statistics")
        print("  list              - List recent functions")
        print("  help              - Show this help")
        print("  quit/exit         - Exit the chat")
        print("\nTips:")
        print("• You can paste multi-line C/C++ code directly")
        print("• Function IDs are shown after analysis")
        print("• Use 'similar <id>' to find functions like a specific one")
        print("• The system works best with complete C/C++ functions")


def main():
    """Main entry point for the chat interface."""
    try:
        chat = FunctionAnalysisChat()
        chat.start()
    except Exception as e:
        print(f"Failed to start chat interface: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
