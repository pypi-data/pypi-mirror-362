"""
FastAPI REST API for function analysis service.
"""

from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ..config.settings import FunctionAnalysisConfig
from ..core.models import (
    AnalysisRequest,
    AnalysisResponse,
    FunctionAnalysis,
    SimilarityResult,
    SimilaritySearchRequest,
)
from .function_tool import FunctionAnalysisService


# Response models
class AnalysisOnlyResponse(BaseModel):
    """Response containing only analysis data."""

    analysis: FunctionAnalysis


class SimilarityOnlyResponse(BaseModel):
    """Response containing only similarity results."""

    similar_functions: List[SimilarityResult]
    total_results: int


class StatsResponse(BaseModel):
    """Response containing service statistics."""

    redis_stats: dict
    embedding_stats: dict


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    version: str
    redis_connected: bool


# Global service instance
service: Optional[FunctionAnalysisService] = None


def get_service() -> FunctionAnalysisService:
    """Dependency to get the service instance."""
    global service
    if service is None:
        service = FunctionAnalysisService()
    return service


def create_app(config: Optional[FunctionAnalysisConfig] = None) -> FastAPI:
    """Create and configure the FastAPI application."""
    if config is None:
        config = FunctionAnalysisConfig.from_env()

    app = FastAPI(
        title=config.api_title,
        version=config.api_version,
        description="Function Analysis API for C/C++ code analysis and similarity search",
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health", response_model=HealthResponse)
    async def health_check(service: FunctionAnalysisService = Depends(get_service)):
        """Health check endpoint."""
        try:
            stats = service.redis_client.get_stats()
            redis_connected = stats.get("redis_connected", False)

            return HealthResponse(
                status="healthy" if redis_connected else "degraded",
                version=config.api_version,
                redis_connected=redis_connected,
            )
        except Exception as e:
            return HealthResponse(
                status="unhealthy", version=config.api_version, redis_connected=False
            )

    @app.post("/analyze", response_model=AnalysisResponse)
    async def analyze_function(
        request: AnalysisRequest,
        service: FunctionAnalysisService = Depends(get_service),
    ):
        """
        Analyze a function and return analysis results with similar functions.
        """
        try:
            # Validate code length
            if len(request.code) > config.max_code_length:
                raise HTTPException(
                    status_code=400,
                    detail=f"Code too long: {len(request.code)} > {config.max_code_length}",
                )

            # Analyze the function
            analysis = service.analyze_function(
                code=request.code, function_name=request.function_name
            )

            # Find similar functions
            similar_functions = service.find_similar_functions(function_id=analysis.id)

            return AnalysisResponse(
                analysis=analysis, similar_functions=similar_functions
            )

        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

    @app.post("/analyze-only", response_model=AnalysisOnlyResponse)
    async def analyze_function_only(
        request: AnalysisRequest,
        service: FunctionAnalysisService = Depends(get_service),
    ):
        """
        Analyze a function without finding similar functions.
        """
        try:
            if len(request.code) > config.max_code_length:
                raise HTTPException(
                    status_code=400,
                    detail=f"Code too long: {len(request.code)} > {config.max_code_length}",
                )

            analysis = service.analyze_function(
                code=request.code, function_name=request.function_name
            )

            return AnalysisOnlyResponse(analysis=analysis)

        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

    @app.post("/search", response_model=SimilarityOnlyResponse)
    async def search_similar_functions(
        request: SimilaritySearchRequest,
        service: FunctionAnalysisService = Depends(get_service),
    ):
        """
        Search for functions similar to the provided code or function ID.
        """
        try:
            if not request.code and not request.function_id:
                raise HTTPException(
                    status_code=400,
                    detail="Either 'code' or 'function_id' must be provided",
                )

            if request.code and len(request.code) > config.max_code_length:
                raise HTTPException(
                    status_code=400,
                    detail=f"Code too long: {len(request.code)} > {config.max_code_length}",
                )

            similar_functions = service.find_similar_functions(
                code=request.code,
                function_id=request.function_id,
                top_k=request.top_k,
                threshold=request.threshold,
            )

            return SimilarityOnlyResponse(
                similar_functions=similar_functions,
                total_results=len(similar_functions),
            )

        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

    @app.get("/function/{function_id}", response_model=FunctionAnalysis)
    async def get_function(
        function_id: str, service: FunctionAnalysisService = Depends(get_service)
    ):
        """
        Get a function analysis by ID.
        """
        try:
            analysis = service.redis_client.get_function_analysis(function_id)
            if not analysis:
                raise HTTPException(status_code=404, detail="Function not found")

            return analysis

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to retrieve function: {str(e)}"
            )

    @app.get("/function/{function_id}/similar", response_model=SimilarityOnlyResponse)
    async def get_similar_functions(
        function_id: str,
        top_k: int = 10,
        threshold: float = 0.7,
        service: FunctionAnalysisService = Depends(get_service),
    ):
        """
        Get functions similar to the specified function ID.
        """
        try:
            # Check if function exists
            analysis = service.redis_client.get_function_analysis(function_id)
            if not analysis:
                raise HTTPException(status_code=404, detail="Function not found")

            similar_functions = service.find_similar_functions(
                function_id=function_id, top_k=top_k, threshold=threshold
            )

            return SimilarityOnlyResponse(
                similar_functions=similar_functions,
                total_results=len(similar_functions),
            )

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

    @app.delete("/function/{function_id}")
    async def delete_function(
        function_id: str, service: FunctionAnalysisService = Depends(get_service)
    ):
        """
        Delete a function and all its associated data.
        """
        try:
            success = service.redis_client.delete_function(function_id)
            if not success:
                raise HTTPException(status_code=404, detail="Function not found")

            return {"message": "Function deleted successfully"}

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to delete function: {str(e)}"
            )

    @app.get("/stats", response_model=StatsResponse)
    async def get_stats(service: FunctionAnalysisService = Depends(get_service)):
        """
        Get service statistics.
        """
        try:
            redis_stats = service.redis_client.get_stats()
            embedding_stats = service.vector_search.get_embedding_statistics()

            return StatsResponse(
                redis_stats=redis_stats, embedding_stats=embedding_stats
            )

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to get stats: {str(e)}"
            )

    @app.get("/functions")
    async def list_functions(
        limit: int = 100,
        offset: int = 0,
        service: FunctionAnalysisService = Depends(get_service),
    ):
        """
        List all functions with pagination.
        """
        try:
            all_ids = service.redis_client.get_all_function_ids()

            # Simple pagination
            paginated_ids = all_ids[offset : offset + limit]

            functions = []
            for function_id in paginated_ids:
                analysis = service.redis_client.get_function_analysis(function_id)
                if analysis:
                    functions.append(
                        {
                            "function_id": analysis.id,
                            "function_name": analysis.metadata.name,
                            "return_type": analysis.metadata.return_type,
                            "line_count": analysis.metadata.line_count,
                            "created_at": analysis.created_at,
                        }
                    )

            return {
                "functions": functions,
                "total": len(all_ids),
                "limit": limit,
                "offset": offset,
            }

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to list functions: {str(e)}"
            )

    return app


# Create the app instance
app = create_app()
