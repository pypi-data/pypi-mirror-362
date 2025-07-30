#!/usr/bin/env python3
"""
Script to run the Function Analysis API server.
"""

import uvicorn

from .config.settings import FunctionAnalysisConfig
from .interfaces.api import create_app


def main():
    """Run the API server."""
    config = FunctionAnalysisConfig.from_env()
    app = create_app(config)

    print(f"🚀 Starting Function Analysis API server...")
    print(f"📡 Host: {config.api_host}")
    print(f"🔌 Port: {config.api_port}")
    print(f"📊 Redis: {config.redis_host}:{config.redis_port}")
    print(
        f"🔗 API docs will be available at: http://{config.api_host}:{config.api_port}/docs"
    )

    uvicorn.run(app, host=config.api_host, port=config.api_port, reload=False)


if __name__ == "__main__":
    main()
