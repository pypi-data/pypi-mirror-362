# Function Analysis Service

A comprehensive service for analyzing function code through graph-based semantic similarity search and call tree analysis.

## Architecture Overview

The service consists of several key components:

### 1. Core Components

- **LLVM/Clang AST Parser**: Uses clang to parse C/C++ code and extract ASTs
- **Graph Converter**: Converts LLVM ASTs to networkx graphs for processing
- **Graph2Vec Encoder**: Converts graphs to vector embeddings
- **Redis Storage**: Stores functions, graphs, embeddings, and call tree data
- **Similarity Search**: Performs semantic similarity queries
- **Call Tree Analysis**: Tracks function call relationships and Redis command mappings

### 2. Interface Layers

- **Function Tool**: Integration with AI agents (openai-agents)
- **REST API**: FastAPI-based HTTP endpoints
- **Chat Interface**: Interactive command-line chat
- **Codebase Indexer**: Batch processing tool for entire codebases

### 3. Data Flow

```
C/C++ Function Code → Clang AST → Graph Converter → Graph2Vec → Redis Storage
                                                              ↓
Interactive Chat ← REST API ← Function Tool ← Similarity Search & Call Tree
```

## Features

- **LLVM/Clang Integration**: Uses industry-standard clang for robust AST parsing
- **C/C++ Focus**: Optimized for Redis codebase analysis (C/C++)
- **Graph Embeddings**: Graph2Vec for semantic similarity
- **Call Tree Analysis**: Build and query function call relationships
- **Redis Command Mapping**: Trace functions to Redis commands using fnToCommand.json
- **Redis Integration**: RedisJSON for storage, vector search with RediSearch
- **Multiple Interfaces**: AI agent tool, REST API, interactive chat, CLI indexer

## Quick Start

### Prerequisites

1. **Redis Server** with RedisJSON module (Redis Stack recommended)
2. **LLVM/Clang** installed on your system
3. **Python 3.10+**

### Installation

```bash
# Install dependencies
poetry install

# Start Redis (with RedisJSON support)
# Option 1: Redis Stack
docker run -d --name redis-stack -p 6379:6379 redis/redis-stack:latest

# Option 2: Redis with RedisJSON module
# Follow Redis installation instructions for your system
```

### Environment Configuration

Create a `.env` file:

```bash
# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Analysis Configuration
EMBEDDING_DIMENSION=128
DEFAULT_SIMILARITY_THRESHOLD=0.7
```

## Usage Examples

### 1. Interactive AI Chat (Recommended)

```bash
# Start the integrated AI chat
poetry run redopt chat

# The AI agent automatically uses function analysis tools
> Analyze this Redis function: int dictScan(dict *d, ...) { ... }
> Find functions similar to dictFind
> What's the complexity of this function?
> What Redis commands use the dictFind function?
> Show me database statistics
```

### 2. Codebase Indexing

```bash
# Index an entire codebase (e.g., Redis source)
poetry run redopt index --source ~/redis/src --output ./functions --redis
```

### 3. As AI Agent Function Tool

```python
from agents import function_tool
from src.function_analysis.interfaces.function_tool import (
    analyze_function_code,
    search_functions_by_name,
    find_function_callers,
    find_redis_commands_using_function
)

# The function tools are automatically available to AI agents
@function_tool
def analyze_redis_function(code: str) -> dict:
    """Analyze Redis C function code and find similar functions"""
    return analyze_function_code(code)
```

### 4. As REST API

```bash
# Start the API server
poetry run function-analysis-api

# Analyze a function
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "int dictScan(dict *d, unsigned long v, dictScanFunction *fn, void *privdata) { ... }",
    "function_name": "dictScan"
  }'

# Find similar functions
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "function_id": "func_abc123",
    "top_k": 10,
    "threshold": 0.7
  }'

# Get function details
curl "http://localhost:8000/function/func_abc123"

# View API documentation
open http://localhost:8000/docs
```

### 5. Standalone Chat Interface

```bash
poetry run function-analysis-chat

# Interactive session:
> int quicksort(int arr[], int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quicksort(arr, low, pi - 1);
        quicksort(arr, pi + 1, high);
    }
}

# Commands:
> analyze <code>     # Analyze function code
> similar <id>       # Find similar functions by ID
> get <id>          # Get function details
> stats             # Show database statistics
> list              # List recent functions
> help              # Show help
```

### 5. Programmatic Usage

```python
from src.function_analysis.interfaces.function_tool import FunctionAnalysisService

# Initialize service
service = FunctionAnalysisService()

# Analyze a function
code = """
int binary_search(int arr[], int n, int target) {
    int left = 0, right = n - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] == target) return mid;
        if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}
"""

analysis = service.analyze_function(code)
print(f"Function: {analysis.metadata.name}")
print(f"Complexity: {analysis.metadata.complexity_score}")

# Find similar functions
similar = service.find_similar_functions(function_id=analysis.id)
for sim in similar:
    print(f"Similar: {sim.function_name} (score: {sim.similarity_score:.3f})")
```

## Directory Structure

```
src/function_analysis/
├── __init__.py
├── README.md
├── fnToCommand.json       # Maps C functions to Redis commands
├── run_api.py            # API server entry point
├── cli/
│   ├── __init__.py
│   └── indexer.py        # Codebase indexing tool
├── core/
│   ├── __init__.py
│   ├── clang_parser.py    # LLVM/Clang AST parsing
│   ├── graph_converter.py # Convert clang AST to networkx graphs
│   ├── graph2vec.py       # Graph embedding generation
│   └── models.py          # Data models and schemas
├── storage/
│   ├── __init__.py
│   ├── redis_client.py    # Redis integration
│   └── vector_search.py   # Similarity search implementation
├── interfaces/
│   ├── __init__.py
│   ├── function_tool.py   # AI agent function tool with call tree support
│   ├── api.py            # FastAPI REST endpoints
│   └── chat.py           # Standalone chat interface
├── config/
│   ├── __init__.py
│   └── settings.py       # Configuration management
└── tests/
    ├── __init__.py
    └── test_clang_parser.py
```

## API Endpoints

### Analysis Endpoints

- `POST /analyze` - Analyze function and find similar functions
- `POST /analyze-only` - Analyze function without similarity search
- `POST /search` - Search for similar functions

### Function Management

- `GET /function/{id}` - Get function details by ID
- `GET /function/{id}/similar` - Get similar functions by ID
- `DELETE /function/{id}` - Delete function
- `GET /functions` - List all functions (paginated)

### System Endpoints

- `GET /health` - Health check
- `GET /stats` - Database statistics
- `GET /docs` - API documentation (Swagger UI)

## Testing

```bash
# Run tests
python -m pytest src/function_analysis/tests/

# Run specific test
python -m pytest src/function_analysis/tests/test_clang_parser.py

# Run with coverage
python -m pytest --cov=src/function_analysis src/function_analysis/tests/
```

## Demo

```bash
# Run the demo script
python examples/function_analysis_demo.py
```

## Integration with AI Agents

The service provides comprehensive function tools for AI agents, including call tree analysis:

1. **`analyze_function_code(code, function_name=None)`**

   - Analyzes C/C++ function code using LLVM/Clang AST
   - Returns analysis results and similar functions
   - Stores the function in the database

2. **`search_functions_by_name(query, limit=10)`**

   - Searches for functions by name in the pre-indexed Redis codebase
   - Returns function details including file locations and complexity

3. **`find_similar_functions_by_id(function_id, top_k=10, threshold=0.7)`**

   - Finds functions similar to an existing function using Graph2Vec embeddings
   - Returns similarity scores and code snippets

4. **`find_function_callers(function_name)`**

   - Finds all functions that call the specified function
   - Uses call tree analysis for accurate results

5. **`find_function_callees(function_name)`**

   - Finds all functions called by the specified function
   - Provides call tree traversal capabilities

6. **`find_redis_commands_using_function(function_name)`**

   - Maps functions to Redis commands using fnToCommand.json
   - Traces function usage up to Redis command level

7. **`check_function_database_status()`**

   - Returns database connection status and statistics
   - Useful for monitoring and debugging

8. **`get_function_analysis_stats()`**
   - Returns detailed database statistics
   - Includes function counts, embedding status, and performance metrics

These tools are automatically available when the function analysis module is imported in your AI agent setup and provide comprehensive Redis codebase analysis capabilities.

## Performance Considerations

- **Graph2Vec Encoding**: Initial encoding may be slow for the first few functions until the encoder is fitted
- **Redis Memory**: Function code and graphs are stored in Redis; monitor memory usage
- **Clang Parsing**: AST parsing is CPU-intensive; consider caching for repeated analyses
- **Similarity Search**: O(n) complexity; performance degrades with large function databases

## Troubleshooting

### Common Issues

1. **Clang not found**: Ensure LLVM/Clang is installed and in PATH
2. **Redis connection failed**: Check Redis server is running and accessible
3. **RedisJSON not available**: Use Redis Stack or install RedisJSON module
4. **Memory issues**: Monitor Redis memory usage, consider data cleanup
5. **Parsing errors**: Ensure C/C++ code is syntactically correct

### Debug Mode

Set environment variables for debugging:

```bash
export LOG_LEVEL=DEBUG
export REDIS_HOST=localhost
export REDIS_PORT=6379
```
