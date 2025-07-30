"""
Redis storage for profiling data with RediSearch integration.
"""

import json
from typing import Dict, List, Optional

import redis
from redis.commands.search.field import NumericField, TagField, TextField

from ..models import BenchmarkDefinition, BenchmarkProfile, FunctionHotspot


class ProfileStorage:
    """Storage layer for benchmark profiles and hotspots"""

    def __init__(self, redis_client):
        self.redis = redis_client
        self._create_indexes()

    def _create_indexes(self):
        """Create RediSearch indexes for profiling data"""
        try:
            # Index for benchmark profiles
            self.redis.ft("benchmark_idx").create_index(
                [
                    TextField("name"),
                    TextField("description"),
                    TagField("tested_groups"),  # sorted-set, string, etc.
                    TagField("tested_commands"),  # zrange, set, get, etc.
                    TagField("redis_topologies"),  # oss-standalone, cluster, etc.
                    TagField("build_variants"),
                    NumericField("total_samples"),
                    NumericField("duration_ms"),
                    NumericField("priority"),
                ]
            )
            print("✅ Created benchmark_idx")
        except Exception as e:
            print(f"⚠️  Benchmark index might already exist: {e}")

        try:
            # Index for function hotspots
            self.redis.ft("hotspot_idx").create_index(
                [
                    TextField("function_name"),
                    TextField("file_path"),
                    NumericField("percentage"),
                    NumericField("total_samples"),
                    TagField("benchmarks"),  # benchmark names
                    TagField("commands"),  # Redis commands
                    TagField("command_groups"),  # sorted-set, string, etc.
                ]
            )
            print("✅ Created hotspot_idx")
        except Exception as e:
            print(f"⚠️  Hotspot index might already exist: {e}")

    def store_benchmark_profile(self, profile: BenchmarkProfile):
        """Store benchmark profile with rich metadata"""
        key = f"benchmark:{profile.id}"

        # Store full profile as JSON (use model_dump with mode='json' to handle datetime serialization)
        profile_data = profile.model_dump(mode="json")
        self.redis.json().set(key, "$", profile_data)

        # Store in search index with flattened data
        self.redis.hset(
            f"search:benchmark:{profile.id}",
            mapping={
                "name": profile.definition.name,
                "description": profile.definition.description,
                "tested_groups": ",".join(profile.definition.tested_groups),
                "tested_commands": ",".join(profile.definition.tested_commands),
                "redis_topologies": ",".join(profile.definition.redis_topologies),
                "build_variants": ",".join(profile.definition.build_variants),
                "total_samples": profile.total_samples,
                "duration_ms": profile.duration_ms,
                "priority": profile.definition.priority,
            },
        )

        # Store hotspots with command group mapping
        for hotspot in profile.hotspots:
            hotspot_key = f"hotspot:{profile.id}:{hotspot.function_name}"

            # Store full hotspot as JSON (use model_dump with mode='json' to handle datetime serialization)
            hotspot_data = hotspot.model_dump(mode="json")
            self.redis.json().set(f"hotspot_json:{hotspot_key}", "$", hotspot_data)

            # Store in search index
            self.redis.hset(
                f"search:hotspot:{hotspot_key}",
                mapping={
                    "function_name": hotspot.function_name,
                    "file_path": hotspot.file_path,
                    "percentage": hotspot.percentage,
                    "total_samples": hotspot.total_samples,
                    "benchmarks": ",".join(hotspot.benchmarks),
                    "commands": ",".join(hotspot.commands),
                    "command_groups": ",".join(hotspot.command_groups),
                },
            )

    def get_benchmark_profile(self, profile_id: str) -> Optional[BenchmarkProfile]:
        """Retrieve benchmark profile by ID"""
        key = f"benchmark:{profile_id}"
        data = self.redis.json().get(key)
        if data:
            return BenchmarkProfile(**data)
        return None

    def list_benchmark_profiles(self, limit: int = 100) -> List[str]:
        """List all benchmark profile IDs"""
        keys = self.redis.keys("benchmark:*")
        return [key.replace("benchmark:", "") for key in keys[:limit]]

    def get_storage_stats(self) -> Dict[str, int]:
        """Get storage statistics"""
        benchmark_count = len(self.redis.keys("benchmark:*"))
        hotspot_count = len(self.redis.keys("hotspot_json:*"))

        return {
            "total_benchmarks": benchmark_count,
            "total_hotspots": hotspot_count,
            "redis_memory_usage": (
                self.redis.memory_usage("benchmark:*") if benchmark_count > 0 else 0
            ),
        }
