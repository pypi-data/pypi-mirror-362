"""
Configuration management for GitHub PR Summarizer
"""

from typing import Optional

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()


class Config(BaseSettings):
    """Configuration settings for the PR Summarizer agent"""

    # OpenAI Configuration
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o", env="OPENAI_MODEL")
    openai_base_url: Optional[str] = Field(default=None, env="OPENAI_BASE_URL")
    openai_tracing_disabled: bool = Field(default=False, env="OPENAI_TRACING_DISABLED")

    # GitHub Configuration
    github_token: str = Field(..., env="GITHUB_TOKEN")
    github_api_url: str = Field(default="https://api.github.com", env="GITHUB_API_URL")

    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")

    # Summary Configuration
    max_diff_lines: int = Field(default=1000, env="MAX_DIFF_LINES")
    include_comments: bool = Field(default=True, env="INCLUDE_COMMENTS")
    include_reviews: bool = Field(default=True, env="INCLUDE_REVIEWS")

    # Slack Configuration
    slack_webhook_token: Optional[str] = Field(default=None, env="PERFORMANCE_WH_TOKEN")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Ignore extra environment variables

    def validate_config(self) -> None:
        """Validate that all required configuration is present"""
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required")
        if not self.github_token:
            raise ValueError("GITHUB_TOKEN is required")

    @classmethod
    def from_env(cls) -> "Config":
        """Create configuration from environment variables"""
        config = cls()
        config.validate_config()
        return config
