# RedOpt

AI tool to connect source code, benchmarks, and profiling data. Includes a GitHub PR performance analyzer, Function Analysis Service, and Profiling Analysis System.

## Features

- 🤖 **OpenAI Agent Integration**: Built using OpenAI's Agent framework
- 📊 **Performance Analysis**: Analyzes GitHub PRs for performance improvements and regressions
- 🔍 **Redis Focus**: Specifically designed for Redis performance analysis
- ⚙️ **Simple Configuration**: Easy setup with environment variables
- 🧠 **Function Analysis Service**: Complete C/C++ function analysis with LLVM/Clang AST parsing, graph embeddings, call tree analysis, and semantic similarity search
- 🔥 **Real pprof Profiling Analysis**: Parse binary pprof files with precise CPU percentages, function-level performance data, and command impact analysis
- 💬 **Single Question Mode**: Ask performance questions directly via CLI: `redopt chat "question"`
- 🗄️ **SQLite Performance Database**: Lightweight, efficient storage for profiling data with flat/cumulative CPU percentages
- 🔗 **Multiple Interfaces**: AI agent tools, REST API, and interactive chat interface
- 📢 **Slack Notifications**: Automatic alerts for significant performance impacts via webhook integration

## Architecture Overview

```
                    Redis Code Analyzer Architecture

    Input Sources              Processing Pipeline           User Interfaces
    ┌─────────────┐           ┌─────────────────────┐       ┌─────────────┐
    │ Project     │──index───▶│                     │       │ 🤖 AI Chat  │
    │ Source Code │           │   LLVM/Clang        │◀──────│ Agent       │
    └─────────────┘           │   Parser            │       └─────────────┘
                              │         │           │
    ┌─────────────┐           │         ▼           │       ┌─────────────┐
    │ C/C++       │─analyze──▶│   Graph Converter   │◀──────│ 🌐 REST API │
    │ Functions   │           │         │           │       │ Server      │
    └─────────────┘           │         ▼           │       └─────────────┘
                              │   Graph2Vec         │
    ┌─────────────┐           │   Encoder           │       ┌─────────────┐
    │ GitHub      │──PR──────▶│         │           │◀──────│ 📊 GitHub   │
    │ PR URLs     │           │         ▼           │       │ PR Analyzer │
    └─────────────┘           └─────────────────────┘       └─────────────┘
                                        │
    ┌─────────────┐           ┌─────────▼─────────┐         ┌─────────────┐
    │ Benchmark   │──parse───▶│                   │◀────────│ 🔥 Profiling│
    │ YAML Files  │           │  Perf Script      │         │ Analysis    │
    └─────────────┘           │  Parser           │         └─────────────┘
                              │         │         │
    ┌─────────────┐           │         ▼         │         ┌─────────────┐
    │ Perf Script │─profile──▶│  Hotspot Analysis │◀────────│ 📈 Command  │
    │ Data        │           │  & Command        │         │ Group       │
    └─────────────┘           │  Group Mapping    │         │ Mapping     │
                              │         │         │
                              │         ▼         │
                              └─────────────────────┘
                                        │
                                        ▼
                              ┌─────────────────────┐
                              │   Redis Database    │
                              │   ┌─────────────┐   │
                              │   │ Functions   │   │
                              │   │ Embeddings  │   │
                              │   │ Metadata    │   │
                              │   │ Profiles    │   │
                              │   │ Hotspots    │   │
                              │   └─────────────┘   │
                              │         │           │
                              │         ▼           │
                              │   Vector Search     │
                              │   (Similarity)      │
                              │   RediSearch        │
                              │   (Profiling)       │
                              └─────────────────────┘

    Flow 1: Source Code → Clang AST → Graphs → Embeddings → Redis → Search
    Flow 2: GitHub PR → Analysis → Performance Impact → Results
    Flow 3: Benchmark YAML + Perf Data → Hotspots → Command Mapping → Redis
```

### Data Flow Explanation

1. **📥 Input Processing**:

   - **Codebase Indexing**: Redis source code → LLVM/Clang parser
   - **Interactive Analysis**: User provides C/C++ functions → Direct analysis
   - **PR Analysis**: GitHub URLs → Performance-focused analysis
   - **Profiling Analysis**: Benchmark YAML + Perf script data → Hotspot analysis
   - **Chat Queries**: Natural language → AI agent processing

2. **⚙️ Core Analysis Pipelines**:

   **Function Analysis Pipeline**:

   - **AST Generation**: LLVM/Clang extracts Abstract Syntax Trees
   - **Graph Conversion**: ASTs transformed to NetworkX graph structures
   - **Vector Encoding**: Graph2Vec generates semantic embeddings
   - **Complexity Analysis**: Cyclomatic complexity calculation

   **Profiling Analysis Pipeline**:

   - **Benchmark Parsing**: YAML benchmark definitions → structured metadata
   - **Perf Script Parsing**: Collapsed stack format → call stacks and hotspots
   - **Command Mapping**: Functions → Redis commands → command groups
   - **Hotspot Analysis**: Sample counts → percentage coverage → performance impact

3. **🗄️ Storage & Retrieval**:

   - **Redis Database**: Stores function metadata, graphs, embeddings, profiles, and hotspots
   - **Vector Search**: Cosine similarity for semantic function matching
   - **RediSearch**: Full-text and structured search for profiling data
   - **JSON Backup**: File-based storage for offline analysis

4. **🔌 User Interfaces**:
   - **AI Chat Agent**: Conversational interface with function analysis and profiling tools
   - **REST API**: Programmatic access for integration
   - **PR Analyzer**: Specialized GitHub PR performance analysis
   - **Profiling Dashboard**: Command group performance analysis

## Key Components

### 🔧 **Function Analysis Tools**

- `analyze_function_code()`: Parse and analyze C/C++ functions using LLVM/Clang
- `find_similar_functions_by_id()`: Semantic similarity search using Graph2Vec embeddings
- `search_functions_by_name()`: Name-based function lookup in the pre-indexed Redis database
- `find_function_callers()` / `find_function_callees()`: Call tree analysis for function relationships
- `find_redis_commands_using_function()`: Map functions to Redis commands
- `check_function_database_status()`: System health and statistics

### 🔥 **Profiling Analysis Tools**

- `get_function_performance_hotspots()`: Find performance hotspots for specific functions
- `get_commands_affected_by_function()`: See which Redis commands use a function
- `get_top_performance_hotspots()`: Get overall performance hotspots across all benchmarks
- `get_hotspots_by_command_group()`: Get hotspots for specific command groups (sorted-set, string, etc.)
- `search_performance_functions()`: Search functions in performance profiling data
- `get_profiling_database_status()`: Check profiling database status and statistics

### 📊 **Processing Pipeline**

- **LLVM/Clang Parser**: Industry-standard AST extraction from C/C++ code
- **Graph Converter**: Transforms ASTs into NetworkX graph structures
- **Graph2Vec Encoder**: Generates vector embeddings for semantic similarity
- **Perf Script Parser**: Parses collapsed stack format from perf tools
- **Hotspot Analyzer**: Maps call stacks to function performance metrics
- **Command Group Mapper**: Links functions to Redis commands and command groups
- **Deduplication**: Filters function declarations, keeps only implementations

### 🗄️ **Storage Layer**

- **Redis Database**: High-performance storage for functions, embeddings, and profiling data
- **Vector Search**: Cosine similarity search on function embeddings
- **RediSearch**: Full-text search on profiling data with command group indexing
- **JSON Files**: Backup storage and offline analysis capability

### 🤖 **AI Integration**

- **Conversational Agent**: Natural language interface for code and performance analysis
- **Function Tools**: Automated function analysis and similarity search
- **Profiling Tools**: Performance hotspot analysis and command group insights
- **Context Awareness**: Maintains conversation history and context

## Workflow Examples

### 📚 **Indexing a Codebase**

```bash
redopt index --source ~/redis/src --output ./functions
```

**Flow**: Redis Source → Clang Parser → Graph Converter → Graph2Vec → Redis Database

### 🔥 **Indexing Profiling Data**

Index real Redis performance profiling data from pprof files:

```bash
# Index profiling data with pprof support
redopt profile-index \
  --benchmark sample-inputs/benchmarks/memtier_benchmark-1Mkeys-generic-scan-count-500-pipeline-10.yml \
  --pprof sample-inputs/pprof/generic-scan-count-500-pipeline-10.pb.gz

# This will:
# ✅ Parse benchmark metadata (commands, command groups)
# ✅ Extract function performance data from pprof using 'pprof -top'
# ✅ Store flat and cumulative CPU percentages in SQLite
# ✅ Enable AI agent to answer performance questions
```

**Flow**: Benchmark YAML + pprof File → pprof Parser → Function Performance Data → SQLite Database

**Real Output:**
```
🔥 Starting profiling data indexing...
✅ Loaded benchmark: memtier_benchmark-1Mkeys-generic-scan-count-500-pipeline-10
✅ Parsed 50 profile entries from pprof
📊 Top function: scanGenericCommand (83.01% cum)
✅ Stored benchmark: generic-scan-count-500-pipeline-10 with 50 profile entries
🎉 Profiling data indexing completed successfully!
```

### 💬 **Interactive Analysis**

```bash
# Interactive chat mode
redopt chat
> Find functions similar to dictScan
> What are the hotspots for sorted-set commands?
> Which functions affect ZRANGE performance?

# Single question mode (NEW!)
redopt chat "What are the Redis functions that take more than 5% of CPU?"
redopt chat "What Redis commands are affected by the listDelNode function?"
```

**Flow**: Chat Query → AI Agent → Function/Profiling Tools → Vector/SQLite Search → Results

**Real Examples:**

```bash
$ redopt chat "What are the Redis functions that take more than 5% of CPU in the benchmark data?"
🤖 Redis Code Analyzer - Single Question Mode
==================================================
Question: What are the Redis functions that take more than 5% of CPU in the benchmark data?

🤖 Analyzing...
✅ SQLite database initialized
✅ Profiling service connected to SQLite

🤖 Answer:
The following Redis functions take more than 5% of CPU time based on benchmark data:

1. **dictScanDefragBucket**:
   - Flat CPU %: 11.03
   - Cumulative CPU %: 21.52

2. **_addReplyProtoToList**:
   - Flat CPU %: 6.75
   - Cumulative CPU %: 8.03

3. **[[kernel.kallsyms]_text]**:
   - Flat CPU %: 6.01
   - Cumulative CPU %: 6.67

4. **update_zmalloc_stat_alloc (inline)**:
   - Flat CPU %: 5.83
   - Cumulative CPU %: 6.24

5. **rev (inline)**:
   - Flat CPU %: 5.63
   - Cumulative CPU %: 5.66

6. **_addReplyToBufferOrList.part.0**:
   - Flat CPU %: 5.03
   - Cumulative CPU %: 5.09
```

```bash
$ redopt chat "What Redis commands are affected by the listDelNode function?"
🤖 Redis Code Analyzer - Single Question Mode
==================================================
Question: What Redis commands are affected by the listDelNode function?

🤖 Analyzing...
✅ SQLite database initialized
✅ Profiling service connected to SQLite

🤖 Answer:
The `listDelNode` function affects Redis commands in the `scan` command group, with a
performance impact estimated at about 7.53%. Specifically, it is part of the `generic`
command group.
```

### 🔍 **Function Analysis**

```bash
curl -X POST "localhost:8000/analyze" -d '{"code": "int func() {...}"}'
```

**Flow**: Function Code → Clang Parser → Graph Analysis → Similarity Search → JSON Response

### 📈 **Profiling Analysis**

Query performance data directly via AI agent or programmatically:

```bash
# AI-powered performance analysis
redopt chat "What are the top 3 functions consuming the most CPU?"
redopt chat "Show me functions with more than 10% flat CPU usage"
redopt chat "Which functions are related to scanning operations?"

# Programmatic access via SQLite
sqlite3 profiling.db "SELECT function, flat_percent, cum_percent FROM profile_entries WHERE flat_percent > 5.0 ORDER BY cum_percent DESC"
```

**Flow**: Performance Query → SQLite Database → Function Data → CPU Percentages → Analysis Results

## Installation

### Prerequisites

- Python 3.12 or higher
- OpenAI API key
- GitHub Personal Access Token

### Install from PyPI

```bash
# Install redopt
pip install redopt

# Or with pipx for isolated installation
pipx install redopt
```

### Install from Source with Poetry

```bash
# Clone the repository
git clone https://github.com/redis/redopt.git
cd redopt

# Install dependencies
poetry install

# Activate the virtual environment
poetry shell
```

### Docker Setup (Recommended)

For the easiest setup, use Docker Compose to run Redis with all required modules:

```bash
# Start Redis with RedisJSON and RedisInsight
docker-compose up -d

# Check if Redis is running
docker-compose ps

# View Redis logs
docker-compose logs redis

# Stop Redis
docker-compose down
```

This will start:

- **Redis Stack** on port `6379` (with RedisJSON, RedisSearch, and other modules)
- **RedisInsight** web UI on port `8001` for database management

Access RedisInsight at: http://localhost:8001

## Configuration

Create a `.env` file in your project root:

```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here
GITHUB_TOKEN=your_github_personal_access_token_here

# Optional
OPENAI_MODEL=gpt-4o
OPENAI_BASE_URL=https://api.openai.com/v1
LOG_LEVEL=INFO
MAX_DIFF_LINES=1000
INCLUDE_COMMENTS=true
INCLUDE_REVIEWS=true
```

### GitHub Token Setup

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token with the most strict permissions

## Usage

### 1. Codebase Indexing

Index an entire C/C++ codebase (like Redis) to extract and analyze all functions:

```bash
# Index Redis source code
redopt index \
  --source ~/redislabs/redis/src \
  --output ./redis_functions \
  --clang-path /usr/bin/clang \
  --include-dirs ~/redislabs/redis/src

# Alternative command
function-analysis-index index \
  --source ~/redislabs/redis/src \
  --output ./redis_functions

# Options:
#   --source: Source directory to index
#   --output: Output directory for JSON files
#   --clang-path: Path to clang executable
#   --include-dirs: Include directories for compilation
#   --extensions: File extensions to process (.c .cpp .h)
#   --no-recursive: Don't search subdirectories
#   --no-redis: Don't store in Redis
#   --no-json: Don't save JSON files
#   --redis-host: Redis host (default: localhost)
#   --redis-port: Redis port (default: 6379)
```

This will:

- Parse all C/C++ files using LLVM/Clang
- Extract function metadata, AST, and complexity
- Generate Graph2Vec embeddings
- Store results in Redis and/or JSON files
- Create a summary with statistics

### 2. Profiling Data Indexing

Index Redis performance profiling data from pprof files:

```bash
# Index profiling data with pprof support
redopt profile-index \
  --benchmark sample-inputs/benchmarks/memtier_benchmark-1Mkeys-generic-scan-count-500-pipeline-10.yml \
  --pprof sample-inputs/pprof/generic-scan-count-500-pipeline-10.pb.gz

# Options:
#   --benchmark: YAML benchmark definition file
#   --pprof: Binary pprof file (.pb.gz format)
#   --output: Output directory (optional)
#   --db-path: SQLite database path (default: profiling.db)

# Batch processing multiple files
redopt profile-index \
  --benchmark-dir ./benchmarks \
  --pprof-dir ./pprof_files \
  --output ./profiling_results
```

This will:

- Parse benchmark metadata (commands, command groups, descriptions)
- Extract function performance data using `pprof -top` command
- Store flat and cumulative CPU percentages in SQLite
- Enable AI agent to answer performance questions
- Create comprehensive profiling database

**Sample Questions After Indexing:**

```bash
# Performance analysis questions
redopt chat "What are the Redis functions that take more than 5% of CPU in the benchmark data?"
# Expected: "dictScanDefragBucket (11.03% flat, 21.52% cumulative), _addReplyProtoToList (6.75% flat, 8.03% cumulative)..."

redopt chat "What Redis commands are affected by the scanGenericCommand function?"
# Expected: "scanGenericCommand affects the SCAN command with 83.01% performance impact in the 'generic' command group"

redopt chat "Show me the top 3 functions consuming the most CPU"
# Expected: Ranked list of functions with their CPU percentages

redopt chat "What specific Redis command and command group are being tested in this benchmark?"
# Expected: Command and group information from benchmark metadata
```

### 3. Interactive AI Chat

Chat with the Redis Code Analyzer AI agent:

```bash
# Start interactive chat mode
redopt chat

# Single question mode (NEW!)
redopt chat "What are the Redis functions that take more than 5% of CPU?"
redopt chat "What Redis commands are affected by the scanGenericCommand function?"

# Examples of what you can do:
> Search for Redis functions by name: "find functions related to dict"
> Analyze this Redis function: int dictScan(dict *d, ...) { ... }
> Find functions similar to dictFind
> What Redis commands use the dictFind function?
> What are the performance implications of this code change?
> Show me statistics about the function database
> Analyze GitHub PR: https://github.com/redis/redis/pull/14108
> What are the top 3 functions consuming the most CPU?
> Show me the benchmark database status
```

The AI agent can:

- Search the pre-indexed Redis codebase (7,000+ functions)
- Analyze C/C++ function code automatically using LLVM/Clang
- Find semantically similar functions using Graph2Vec embeddings
- Perform call tree analysis to trace function relationships
- Map functions to Redis commands
- **Analyze real profiling data from pprof files with precise CPU percentages**
- **Identify performance hotspots and functions consuming >5% CPU**
- **Link functions to Redis commands and command groups with performance impact**
- **Query SQLite profiling database for flat and cumulative CPU usage**
- Provide Redis performance insights from real benchmark data
- Answer questions about the codebase and performance characteristics
- Analyze GitHub PRs for performance impact

### 4. GitHub PR Analysis

Run the performance analyzer on a specific PR:

```bash
redopt
```

The tool will analyze GitHub PRs for performance-related changes and can use the indexed function database for enhanced analysis.

### 5. Slack Notifications

RedOpt AI can send notifications to Slack channels for significant performance impacts:

```bash
# Set up Slack webhook token
export PERFORMANCE_WH_TOKEN=T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX

# Analyze a PR with automatic Slack alerts for significant impacts
redopt chat "Assess the impact of https://github.com/redis/redis/pull/14200. If the impact is significant warn us on slack on #perf-ci."

# Send a manual notification
redopt chat "Send a test message to slack saying 'Hello from RedOpt AI'"
```

Features:
- Automatic alerts for PRs with >5% performance impact
- Performance alerts with detailed impact analysis
- Interactive action buttons (JIRA, GitHub comments, benchmarks)
- Repository-specific functionality (Redis repos get additional features)
- Configurable via webhook token
- Supports custom channels and message formatting

See [docs/slack_notifications.md](docs/slack_notifications.md) for detailed configuration and usage.

## How It Works

The tool uses an OpenAI Agent to:

1. Fetch GitHub PR data (description, files, comments, reviews)
2. Analyze the changes for performance impact
3. Generate a structured analysis including:
   - Performance improvements and regressions
   - Affected Redis commands
   - Significance assessment
   - Summary of changes

## Project Structure

```
src/
├── main.py                    # Main application entry point
├── config.py                  # Configuration management
├── github_client/             # GitHub API client
│   ├── client.py              # GitHub client implementation
│   └── models.py              # Data models
├── function_analysis/         # Function analysis service
│   ├── core/                  # Core analysis components
│   │   ├── clang_parser.py    # LLVM/Clang AST parsing
│   │   ├── graph_converter.py # Convert clang AST to networkx graphs
│   │   ├── graph2vec.py       # Graph embedding generation
│   │   └── models.py          # Data models and schemas
│   ├── storage/               # Storage layer
│   │   ├── redis_client.py    # Redis integration
│   │   └── vector_search.py   # Similarity search implementation
│   ├── interfaces/            # User interfaces
│   │   ├── function_tool.py   # AI agent function tool
│   │   ├── api.py            # FastAPI REST endpoints
│   │   └── chat.py           # Interactive chat interface
│   └── cli/                   # Command line tools
│       └── indexer.py         # Codebase indexing CLI
└── profiling/                 # Profiling analysis service
    ├── models.py              # Profiling data models
    ├── parsers/               # Data parsers
    │   └── perf_parser.py     # Perf script parser
    ├── storage/               # Storage layer
    │   └── profile_storage.py # Redis storage for profiling data
    ├── queries/               # Query interface
    │   └── profile_queries.py # Profiling data queries
    └── cli/                   # Command line tools
        └── profile_indexer.py # Profiling data indexing CLI
```

## Publishing to PyPI

### Prerequisites for Publishing

1. **PyPI Account**: Create accounts on [PyPI](https://pypi.org/account/register/) and [TestPyPI](https://test.pypi.org/account/register/)
2. **API Tokens**: Generate API tokens for both PyPI and TestPyPI
3. **Poetry Configuration**: Configure Poetry with your credentials

### Configure Poetry for Publishing

```bash
# Configure PyPI credentials
poetry config pypi-token.pypi your-pypi-api-token

# Configure TestPyPI for testing (optional)
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry config pypi-token.testpypi your-testpypi-api-token
```

### Publishing Process

```bash
# 1. Update version in pyproject.toml
poetry version patch  # or minor, major

# 2. Build the package
poetry build

# 3. Test publish to TestPyPI (optional but recommended)
poetry publish -r testpypi

# 4. Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ redopt

# 5. Publish to PyPI
poetry publish

# 6. Verify installation
pip install redopt
redopt --help
```

### Version Management

```bash
# Patch version (0.1.0 -> 0.1.1)
poetry version patch

# Minor version (0.1.0 -> 0.2.0)
poetry version minor

# Major version (0.1.0 -> 1.0.0)
poetry version major

# Pre-release versions
poetry version prerelease  # 0.1.0 -> 0.1.1a0
poetry version prepatch    # 0.1.0 -> 0.1.1a0
poetry version preminor    # 0.1.0 -> 0.2.0a0
poetry version premajor    # 0.1.0 -> 1.0.0a0
```

## Development

This is a Redis AI Week project focused on performance analysis of Redis-related pull requests, combining:

1. **Static Code Analysis**: Function-level semantic analysis using LLVM/Clang and Graph2Vec
2. **Runtime Profiling**: Performance hotspot analysis from perf script data
3. **Benchmark Integration**: Mapping between functions, Redis commands, and performance characteristics
4. **AI-Powered Insights**: Conversational interface for exploring code and performance relationships

The system enables developers to:

- Understand which functions are performance-critical for specific Redis operations
- Find semantically similar functions that might have similar performance characteristics
- Analyze the performance impact of code changes through both static analysis and profiling data
- Get AI-powered insights about Redis performance optimization opportunities

## Authors

- Filipe Oliveira <filipe@redis.com>
- Paulo Sousa <paulo.sousa@redis.com>
