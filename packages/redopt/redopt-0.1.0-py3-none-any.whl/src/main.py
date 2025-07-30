import asyncio
import logging
import sys
from typing import Any, Dict, List

from agents import Agent, Runner, function_tool, set_tracing_disabled, trace
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
from openai import AsyncOpenAI

from .config import Config
from .function_analysis.interfaces.function_tool import (  # find_call_paths,
    analyze_function_code,
    check_function_database_status,
    find_function_callees,
    find_function_callers,
    find_redis_commands_using_function,
    find_similar_functions_by_id,
    get_function_analysis_stats,
    get_service,
    search_functions_by_name,
)
from .github_client.client import GitHubClient
from .notifications.tool import (
    send_performance_alert,
    send_pr_analysis_summary,
    send_slack_notification,
)
from .profiling.interfaces.profiling_tool import (
    get_benchmarks_by_command_group,
    get_commands_affected_by_function,
    get_function_performance_hotspots,
    get_hotspots_by_command_group,
    get_profiling_database_status,
    get_profiling_service,
    get_top_performance_hotspots,
    search_performance_functions,
)

config = Config.from_env()

logging.basicConfig(
    level=config.log_level, format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# Configure tracing based on config setting
set_tracing_disabled(config.openai_tracing_disabled)


class RedisChatAgent(Agent):
    def __init__(self, config: Config):
        chat_openai_client = AsyncOpenAI(
            api_key=config.openai_api_key, base_url=config.openai_base_url
        )
        model = OpenAIChatCompletionsModel(
            model=config.openai_model, openai_client=chat_openai_client
        )
        github_client = GitHubClient(config)

        @function_tool
        def tool_find_redis_commands_using_function(
            function_name: str,
        ) -> Dict[str, Any]:
            """Finds all Redis commands that use a given function by tracing up through callers."""
            return find_redis_commands_using_function(function_name)

        @function_tool
        def tool_get_pull_request_summary(owner: str, repo: str, pr_number: int) -> str:
            """Gets a detailed summary from a GitHub Pull Request"""
            summary = github_client.get_pull_request_summary(owner, repo, pr_number)
            logger.debug(f"Pull request summary:\n%s", summary)
            return summary

        @function_tool
        def tool_get_function_performance_hotspots(
            function_name: str, min_percentage: float = 1.0
        ) -> List[Dict[str, Any]]:
            """Get performance hotspot data for a specific function across all benchmarks."""
            return get_function_performance_hotspots(function_name, min_percentage)

        @function_tool
        def tool_get_commands_affected_by_function(
            function_name: str,
        ) -> Dict[str, List[str]]:
            """Find Redis commands and command groups that are affected by a specific function."""
            return get_commands_affected_by_function(function_name)

        @function_tool
        def tool_get_top_performance_hotspots(limit: int = 20) -> List[Dict[str, Any]]:
            """Get the top performance hotspots across all benchmarks."""
            return get_top_performance_hotspots(limit)

        @function_tool
        def tool_get_hotspots_by_command_group(
            command_group: str, limit: int = 20
        ) -> List[Dict[str, Any]]:
            """Get top performance hotspots for a specific Redis command group."""
            return get_hotspots_by_command_group(command_group, limit)

        @function_tool
        def tool_get_benchmarks_by_command_group(
            command_group: str,
        ) -> List[Dict[str, Any]]:
            """Find all benchmarks that test a specific Redis command group."""
            return get_benchmarks_by_command_group(command_group)

        @function_tool
        def tool_search_performance_functions(
            function_name: str,
        ) -> List[Dict[str, Any]]:
            """Search for functions by name pattern in performance profiling data."""
            return search_performance_functions(function_name)

        @function_tool
        def tool_get_profiling_database_status() -> Dict[str, Any]:
            """Check the status of the profiling database and get statistics."""
            return get_profiling_database_status()

        super().__init__(
            name="RedisCodeAnalyzer",
            instructions="""You are a Redis code analysis expert with access to a comprehensive database of 7,000+ Redis functions and performance profiling data from pprof profiles. You can:

1. Search for specific Redis functions by name using search_functions_by_name()
2. Analyze C/C++ function code using LLVM/Clang AST parsing with analyze_function_code()
3. Find semantically similar functions using Graph2Vec embeddings with find_similar_functions_by_id()
4. Check database status and get statistics with check_function_database_status()
5. Get real performance data from pprof profiles using SQLite-based profiling tools:
   - get_function_performance_hotspots() - Find where functions are performance bottlenecks with flat/cumulative CPU %
   - get_commands_affected_by_function() - See which Redis commands use a function and their performance impact
   - get_top_performance_hotspots() - Get overall performance hotspots across all benchmarks
   - get_hotspots_by_command_group() - Get hotspots for specific command groups (scan, hash, string, etc.)
   - search_performance_functions() - Search functions in performance data
   - get_benchmarks_by_command_group() - Find benchmarks that test specific command groups
   - get_profiling_database_status() - Check profiling database status and statistics

IMPORTANT:
- When users ask about Redis functions or commands, use search_functions_by_name() to find functions in the database. if you find header and C files use the C file given it includes more detail.
- When users ask about performance, use the profiling tools to get real pprof benchmark data from SQLite
- The profiling data includes flat/cumulative CPU percentages from pprof profiles parsed with 'pprof -top' command
- Provide specific function names, file locations, complexity information, and performance metrics from the actual indexed Redis codebase
- When users reference previous conversations or ask follow-up questions, use the conversation context
- If a user says "y", "yes", "proceed", or similar, continue with the previous topic
- When users ask to analyze implementation files, use the function search tools to find the actual code
- When users ask to analyze a GitHub PR, use get_pull_request_summary() to get the PR summary and the most affected functions (performance wise). Then, use the other tools to analyze the affected functions and understand the performance implications.
- To relate a function with Redis commands calling it (directly or indirectly), use find_redis_commands_using_function(). This is useful when users need to know what commands should be affected by changes to a function.
- When you need to know what functions call a specific function, use find_function_callers()
- When you need to know what functions a specific function calls, use find_function_callees()
- When analyzing PRs with significant performance impact (>5%), use send_performance_alert() to notify the #perf-ci Slack channel with action buttons
- When analyzing any PR and sending to Slack, ALWAYS use send_pr_analysis_summary() instead of send_slack_notification() to include repository context, affected commands, changed functions, and action buttons
- Use send_slack_notification() ONLY for general messages that are not related to PR analysis
- IMPORTANT: For PR analysis summaries sent to Slack, always use send_pr_analysis_summary() which includes interactive action buttons

Always use the available tools to provide accurate, data-driven responses about the Redis codebase.
Respond in a helpful, conversational manner and maintain conversation context.""",
            model=model,
            tools=[
                analyze_function_code,
                find_similar_functions_by_id,
                get_function_analysis_stats,
                search_functions_by_name,
                check_function_database_status,
                # Github tools
                tool_get_pull_request_summary,
                # Profiling tools (pprof-based)
                tool_get_function_performance_hotspots,
                tool_get_commands_affected_by_function,
                tool_get_top_performance_hotspots,
                tool_get_hotspots_by_command_group,
                tool_get_benchmarks_by_command_group,
                tool_search_performance_functions,
                tool_get_profiling_database_status,
                # Call tree tools
                find_function_callees,
                find_function_callers,
                tool_find_redis_commands_using_function,
                # Notification tools
                send_slack_notification,
                send_performance_alert,
                send_pr_analysis_summary,
            ],
        )


redis_chat_agent = RedisChatAgent(config)


async def async_main():
    """Main async function - can run PR analysis or interactive chat."""
    # Check if we should run in interactive mode
    if len(sys.argv) > 1 and sys.argv[1] == "chat":
        # Check if a question was provided directly
        if len(sys.argv) > 2:
            question = " ".join(sys.argv[2:])
            await single_question_chat(question)
        else:
            await interactive_chat()
        return


async def single_question_chat(question: str):
    """Handle a single question via CLI and exit."""
    print("🤖 Redis Code Analyzer - Single Question Mode")
    print("=" * 50)
    print(f"Question: {question}")
    print("\n🤖 Analyzing...")

    try:
        with trace("Single question chat"):
            response = await Runner.run(
                redis_chat_agent,
                question,
            )

            # Extract the actual response from RunResult
            if hasattr(response, "final_output"):
                result = response.final_output
            else:
                result = str(response)

            print(f"\n🤖 Answer:\n{result}")

    except Exception as e:
        print(f"❌ Error: {e}")
        logger.error(f"Single question chat error: {e}")


async def interactive_chat():
    """Interactive chat mode with the Redis analyzer agent."""
    print("🤖 Redis Code Analyzer - Interactive Chat")
    print("=" * 50)
    print(
        "I can help you analyze Redis code, find similar functions, and understand performance implications."
    )
    print("\nExamples:")
    print("• Paste C/C++ function code for analysis")
    print("• Ask about Redis performance patterns and real pprof benchmark data")
    print("• Request function similarity searches")
    print("• Analyze GitHub PR URLs")
    print("• Get performance hotspots with flat/cumulative CPU percentages")
    print("• Find which Redis commands are affected by a function")
    print("• Analyze function performance across different command groups")
    print("• Search for functions in pprof performance data")
    print("\nType 'quit' or 'exit' to end the session.")
    print("-" * 50)

    # Initialize function analysis service and log status
    print("\n🔧 Initializing services...")
    try:
        get_service()  # Initialize service and trigger logging
        print("✅ Function Analysis Service ready")
    except Exception as e:
        print(f"⚠️  Function Analysis Service initialization warning: {e}")
        print("   Some features may be limited without Redis")

    try:
        print("🔧 Initializing SQLite Profiling Service...")
        get_profiling_service()  # Initialize profiling service and show stats
        print("✅ SQLite Profiling Service ready")
    except Exception as e:
        print(f"⚠️  SQLite Profiling Service initialization warning: {e}")
        print(
            "   Performance analysis features may be limited without pprof profiling data"
        )

    # Initialize conversation history
    conversation_history: List[str] = []

    while True:
        try:
            # Get user input
            print("\n> ", end="")
            user_input = input().strip()

            if not user_input:
                continue

            # Check for exit commands
            if user_input.lower() in ["quit", "exit", "q"]:
                print("👋 Goodbye!")
                break

            # Add user input to conversation history
            conversation_history.append(f"User: {user_input}")

            # Create context with conversation history
            if len(conversation_history) > 1:
                # Include recent conversation context (last 10 exchanges)
                recent_history = conversation_history[
                    -20:
                ]  # Last 10 user + 10 assistant messages
                context = "\n".join(recent_history) + f"\nUser: {user_input}"
            else:
                context = user_input

            # Process with the agent
            print("\n🤖 Analyzing...")

            with trace("Interactive chat"):
                response = await Runner.run(
                    redis_chat_agent,
                    context,
                )

                # Extract the actual response from RunResult
                if hasattr(response, "final_output"):
                    actual_response = response.final_output
                elif hasattr(response, "data"):
                    actual_response = response.data
                else:
                    actual_response = str(response)

                # Add assistant response to conversation history
                conversation_history.append(f"Assistant: {actual_response}")

                print(f"\n🤖 {actual_response}")

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            logger.error(f"Chat error: {e}")


def main():
    """Entry point for the Poetry script."""
    # Check for different commands
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "index":
            # Delegate to indexer
            from .function_analysis.cli.indexer import main as indexer_main

            indexer_main()
            return
        elif command == "profile-index":
            # Delegate to profiling indexer
            from .profiling.cli.profile_indexer import main as profile_indexer_main

            # Remove the command from sys.argv so the profiling indexer gets clean args
            sys.argv = [sys.argv[0]] + sys.argv[2:]
            profile_indexer_main()
            return
        elif command == "chat":
            # Run interactive chat mode
            asyncio.run(async_main())
            return
        elif command == "--help" or command == "-h":
            print_help()
            return

    # Default behavior - run the GitHub PR analyzer
    asyncio.run(async_main())


def print_help():
    """Print help information."""
    print("🤖 Redis Code Analyzer")
    print("=" * 30)
    print("Usage:")
    print("  poetry run redopt                    # Analyze hardcoded GitHub PR")
    print("  poetry run redopt chat               # Interactive chat mode")
    print('  poetry run redopt chat "<question>"  # Ask a single question')
    print("  poetry run redopt index [options]    # Index codebase")
    print("  poetry run redopt profile-index [options] # Index profiling data")
    print("  poetry run redopt --help             # Show this help")
    print()
    print("Interactive Chat Mode:")
    print("  • Analyze C/C++ function code")
    print("  • Find similar functions")
    print("  • Analyze GitHub PRs")
    print("  • Get Redis performance insights from real pprof benchmark data")
    print("  • Find performance hotspots with flat/cumulative CPU percentages")
    print("  • Analyze function performance across different Redis command groups")
    print("  • Search and analyze functions from SQLite profiling database")
    print()
    print("Indexing:")
    print("  poetry run redopt index --source ~/redis/src --output ./functions")
    print()
    print("Profiling (SQLite-based pprof data management):")
    print("  poetry run redopt profile-index \\")
    print(
        "    --benchmark-spec-dir ../redis-benchmarks-specification/redis_benchmarks_specification/test-suites/ \\"
    )
    print("    --pprof-dir ./sample-inputs/pprof-profiles \\")
    print("    --output ./profiles \\")
    print("    --db-path ./profiling.db")
    print()
    print("  # Single file mode:")
    print("  poetry run redopt profile-index \\")
    print("    --benchmark ./benchmark.yml \\")
    print("    --pprof ./profile.pb.gz \\")
    print("    --db-path ./profiling.db")
    print()
    print(
        "  # Profiles are pprof files (.pb.gz) parsed with 'pprof -top' into flat/cumulative CPU %"
    )
    print("  # Data is stored in SQLite with benchmarks and profile_entries tables")
    print(
        "  # Replaces old stack trace approach with cleaner function-level performance data"
    )
    print()
    print("Other Commands:")
    print("  poetry run function-analysis-api     # Start REST API server")
    print("  poetry run function-analysis-chat    # Standalone chat interface")


if __name__ == "__main__":
    main()
