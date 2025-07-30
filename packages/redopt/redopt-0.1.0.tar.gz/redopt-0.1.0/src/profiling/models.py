"""
Data models for profiling analysis service.
"""

import time
from datetime import datetime, timezone
from typing import Dict, List, Optional

import yaml
from pydantic import BaseModel, Field


class BenchmarkDefinition(BaseModel):
    """Parsed benchmark definition from YAML"""

    name: str
    description: str
    tested_groups: List[str] = Field(default_factory=list)  # e.g., ["sorted-set"]
    tested_commands: List[str] = Field(default_factory=list)  # e.g., ["zrange"]
    redis_topologies: List[str] = Field(default_factory=list)
    build_variants: List[str] = Field(default_factory=list)
    priority: int = 0

    # Client config
    tool: str = "unknown"  # e.g., "memtier_benchmark"
    arguments: str = ""
    test_time: Optional[int] = None

    # DB config
    keyspace_length: Optional[int] = None
    init_commands: List[str] = Field(default_factory=list)

    @classmethod
    def from_yaml(cls, yaml_path: str) -> "BenchmarkDefinition":
        """Load benchmark definition from YAML file"""
        with open(yaml_path, "r") as f:
            data = yaml.safe_load(f)
        return cls.from_yaml_data(data)

    @classmethod
    def from_yaml_data(cls, data: dict) -> "BenchmarkDefinition":
        """Load benchmark definition from already-loaded YAML data"""
        # Extract nested values
        clientconfig = data.get("clientconfig", {})
        dbconfig = data.get("dbconfig", {})
        check_config = dbconfig.get("check", {})

        return cls(
            name=data.get("name", "unknown"),
            description=data.get("description", ""),
            tested_groups=data.get("tested-groups", []),
            tested_commands=data.get("tested-commands", []),
            redis_topologies=data.get("redis-topologies", []),
            build_variants=data.get("build-variants", []),
            priority=data.get("priority", 0),
            tool=clientconfig.get("tool", "unknown"),
            arguments=clientconfig.get("arguments", ""),
            keyspace_length=check_config.get("keyspacelen"),
            init_commands=dbconfig.get("init_commands", []),
        )


class StackFrame(BaseModel):
    """Single frame in a call stack"""

    function_name: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    module: Optional[str] = None


class CallStack(BaseModel):
    """Complete call stack with sample count"""

    frames: List[StackFrame]
    sample_count: int
    percentage: float = 0.0


class FunctionHotspot(BaseModel):
    """Function hotspot data"""

    function_name: str
    file_path: str
    total_samples: int
    percentage: float
    benchmarks: List[str] = Field(
        default_factory=list
    )  # benchmark names that hit this function
    commands: List[str] = Field(
        default_factory=list
    )  # Redis commands that use this function
    command_groups: List[str] = Field(
        default_factory=list
    )  # e.g., ["sorted-set", "string"]


class BenchmarkProfile(BaseModel):
    """Complete benchmark profile with profiling data"""

    id: str
    definition: BenchmarkDefinition
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    total_samples: int
    duration_ms: float
    perf_script_path: str

    # Derived metrics
    function_coverage: Dict[str, float] = Field(
        default_factory=dict
    )  # function -> percentage
    command_coverage: Dict[str, float] = Field(
        default_factory=dict
    )  # command -> percentage
    hotspots: List[FunctionHotspot] = Field(default_factory=list)

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}
