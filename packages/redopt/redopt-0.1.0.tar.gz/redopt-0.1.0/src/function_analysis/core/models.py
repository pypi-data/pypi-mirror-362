"""
Data models for function analysis service.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class FunctionMetadata(BaseModel):
    """Metadata extracted from function code."""

    name: str
    return_type: str
    parameters: List[Dict[str, str]]  # [{"name": "param1", "type": "int"}, ...]
    line_count: int
    complexity_score: Optional[float] = None
    source_file: Optional[str] = None
    start_line: Optional[int] = None
    end_line: Optional[int] = None


class GraphData(BaseModel):
    """Graph representation data."""

    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
    graph_type: str  # "ast" or "cfg"

    class Config:
        arbitrary_types_allowed = True


class FunctionAnalysis(BaseModel):
    """Complete analysis result for a function."""

    id: str = Field(..., description="Unique identifier for the function")
    code: str = Field(..., description="Original function code")
    metadata: FunctionMetadata
    ast_graph: GraphData
    cfg_graph: Optional[GraphData] = None
    embedding: List[float] = Field(..., description="Graph2Vec embedding vector")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}

    def model_dump(self, **kwargs):
        """Override model_dump to handle datetime serialization."""
        data = super().model_dump(**kwargs)

        # Convert datetime objects to ISO strings
        if "created_at" in data and hasattr(data["created_at"], "isoformat"):
            data["created_at"] = data["created_at"].isoformat()

        return data


class SimilarityResult(BaseModel):
    """Result from similarity search."""

    function_id: str
    function_name: str
    similarity_score: float
    code_snippet: str
    metadata: FunctionMetadata


class AnalysisRequest(BaseModel):
    """Request for function analysis."""

    code: str
    function_name: Optional[str] = None
    source_file: Optional[str] = None
    include_cfg: bool = False


class SimilaritySearchRequest(BaseModel):
    """Request for similarity search."""

    code: Optional[str] = None
    function_id: Optional[str] = None
    top_k: int = Field(default=10, ge=1, le=100)
    threshold: float = Field(default=0.7, ge=0.0, le=1.0)


class AnalysisResponse(BaseModel):
    """Response from analysis endpoint."""

    analysis: FunctionAnalysis
    similar_functions: List[SimilarityResult]


class FunctionCall(BaseModel):
    """Information about a function call."""

    called_function: str
    location: Dict[str, int]  # line, column
    arguments: List[Dict[str, Optional[str]]]  # type, spelling


class CallTreeNode(BaseModel):
    """Node in the call tree representing a function."""

    metadata: FunctionMetadata
    location: Dict[str, Any]  # file, line, column
    calls_made: List[FunctionCall]
    called_by: List[Dict[str, Any]]  # caller info


class CallTree(BaseModel):
    """Complete call tree for a codebase."""

    functions: Dict[str, CallTreeNode]
    call_graph: Dict[str, List[str]]  # caller -> [callees]
    reverse_call_graph: Dict[str, List[str]]  # callee -> [callers]
    statistics: Dict[str, int]
