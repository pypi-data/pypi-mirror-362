"""
Configuration settings for function analysis service.
"""

from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class FunctionAnalysisConfig(BaseSettings):
    """Configuration for function analysis service."""

    # Redis Configuration
    redis_host: str = Field(default="localhost", env="REDIS_HOST")
    redis_port: int = Field(default=6379, env="REDIS_PORT")
    redis_db: int = Field(default=0, env="REDIS_DB")
    redis_password: Optional[str] = Field(default=None, env="REDIS_PASSWORD")
    redis_json_enabled: bool = Field(default=True, env="REDIS_JSON_ENABLED")

    # Graph2Vec Configuration
    embedding_dimension: int = Field(default=128, env="EMBEDDING_DIMENSION")

    # API Configuration
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    api_title: str = Field(default="Function Analysis API", env="API_TITLE")
    api_version: str = Field(default="0.1.0", env="API_VERSION")

    # Analysis Configuration
    max_code_length: int = Field(default=10000, env="MAX_CODE_LENGTH")
    default_similarity_threshold: float = Field(
        default=0.7, env="DEFAULT_SIMILARITY_THRESHOLD"
    )
    default_top_k: int = Field(default=10, env="DEFAULT_TOP_K")

    # Clang Configuration
    clang_args: list = Field(default=["-std=c99"], env="CLANG_ARGS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Ignore extra environment variables

    @classmethod
    def from_env(cls) -> "FunctionAnalysisConfig":
        """Create configuration from environment variables."""
        return cls()
