"""
Data models for GitHub PR Summarizer
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class GitHubUser(BaseModel):
    """GitHub user model"""

    login: str
    id: int
    avatar_url: str
    html_url: str


class PRFile(BaseModel):
    """Pull request file change model"""

    filename: str
    status: str  # added, modified, removed, renamed
    additions: int
    deletions: int
    changes: int
    patch: Optional[str] = None


class PRComment(BaseModel):
    """Pull request comment model"""

    id: int
    user: GitHubUser
    body: str
    created_at: datetime
    updated_at: datetime
    html_url: str


class PRReview(BaseModel):
    """Pull request review model"""

    id: int
    user: GitHubUser
    body: Optional[str]
    state: str  # APPROVED, CHANGES_REQUESTED, COMMENTED
    submitted_at: Optional[datetime]
    html_url: str


class PullRequest(BaseModel):
    """Complete pull request model"""

    number: int
    title: str
    body: Optional[str]
    state: str  # open, closed, merged
    user: GitHubUser
    created_at: datetime
    updated_at: datetime
    merged_at: Optional[datetime]
    html_url: str

    # Additional metadata
    additions: int
    deletions: int
    changed_files: int
    commits: int

    # Related data
    files: List[PRFile] = Field(default_factory=list)
    comments: List[PRComment] = Field(default_factory=list)
    reviews: List[PRReview] = Field(default_factory=list)

    # Repository info
    repo_owner: str
    repo_name: str
