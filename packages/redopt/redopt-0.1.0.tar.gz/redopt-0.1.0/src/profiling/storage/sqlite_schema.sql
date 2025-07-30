-- SQLite schema for profiling data with stack trace support
-- Optimized for stack analysis and partial stack information

-- Benchmark definitions and metadata
CREATE TABLE benchmarks (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    tested_groups TEXT, -- JSON array: ["hash", "string"]
    tested_commands TEXT, -- JSON array: ["hset", "get"]
    redis_topologies TEXT, -- JSON array: ["oss-standalone"]
    build_variants TEXT, -- JSON array: ["gcc:8.5.0"]
    tool TEXT,
    arguments TEXT,
    keyspace_length INTEGER,
    priority INTEGER DEFAULT 0,
    total_samples INTEGER,
    duration_ms REAL,
    perf_script_path TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    metadata TEXT -- JSON for additional metadata
);

-- Individual stack traces with full context preserved
CREATE TABLE stack_traces (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    benchmark_id TEXT NOT NULL REFERENCES benchmarks(id),
    full_stack TEXT NOT NULL, -- Original stack: "main;aeMain;readQuery;[unknown]"
    sample_count INTEGER NOT NULL,
    stack_depth INTEGER NOT NULL,
    has_unknowns BOOLEAN DEFAULT FALSE,
    stack_hash TEXT -- Hash for deduplication
);

-- Individual frames within each stack trace
CREATE TABLE stack_frames (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stack_trace_id INTEGER NOT NULL REFERENCES stack_traces(id),
    position INTEGER NOT NULL, -- 0=bottom (main), higher=up the stack
    function_name TEXT NOT NULL,
    is_unknown BOOLEAN DEFAULT FALSE,
    cleaned_name TEXT -- Cleaned version for analysis
);

-- Aggregated function hotspots (for fast queries)
CREATE TABLE function_hotspots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    benchmark_id TEXT NOT NULL REFERENCES benchmarks(id),
    function_name TEXT NOT NULL,
    cleaned_name TEXT,
    total_samples INTEGER NOT NULL,
    percentage REAL NOT NULL,
    stack_count INTEGER NOT NULL, -- How many different stacks hit this function
    is_unknown BOOLEAN DEFAULT FALSE,
    file_path TEXT DEFAULT 'unknown'
);

-- Call relationships (who calls whom)
CREATE TABLE call_relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    benchmark_id TEXT NOT NULL REFERENCES benchmarks(id),
    caller_function TEXT NOT NULL,
    callee_function TEXT NOT NULL,
    call_count INTEGER NOT NULL, -- How many times this call happened
    total_samples INTEGER NOT NULL -- Total samples through this call path
);

-- Indexes for performance
CREATE INDEX idx_stack_traces_benchmark ON stack_traces(benchmark_id);
CREATE INDEX idx_stack_traces_has_unknowns ON stack_traces(has_unknowns);
CREATE INDEX idx_stack_frames_stack_id ON stack_frames(stack_trace_id);
CREATE INDEX idx_stack_frames_function ON stack_frames(function_name);
CREATE INDEX idx_stack_frames_position ON stack_frames(position);
CREATE INDEX idx_stack_frames_unknown ON stack_frames(is_unknown);
CREATE INDEX idx_function_hotspots_benchmark ON function_hotspots(benchmark_id);
CREATE INDEX idx_function_hotspots_function ON function_hotspots(function_name);
CREATE INDEX idx_function_hotspots_percentage ON function_hotspots(percentage DESC);
CREATE INDEX idx_call_relationships_benchmark ON call_relationships(benchmark_id);
CREATE INDEX idx_call_relationships_caller ON call_relationships(caller_function);
CREATE INDEX idx_call_relationships_callee ON call_relationships(callee_function);

-- Note: FTS and triggers will be created programmatically if needed

-- Note: Views will be created programmatically to avoid SQL parsing issues
