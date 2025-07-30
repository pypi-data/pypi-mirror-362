"""
GitHub API client for fetching pull request data
"""

import logging
from typing import List

from github import Auth, Github, GithubException
from github.PullRequest import PullRequest as GithubPR

from ..config import Config
from .models import GitHubUser, PRComment, PRFile, PRReview, PullRequest

logger = logging.getLogger(__name__)


class GitHubClient:
    """Client for interacting with GitHub API"""

    def __init__(self, config: Config):
        self.config = config
        auth = Auth.Token(config.github_token)
        self.github = Github(auth=auth, base_url=config.github_api_url)

    def get_pull_request(self, owner: str, repo: str, pr_number: int) -> PullRequest:
        """
        Fetch complete pull request data including files, comments, and reviews

        Args:
            owner: Repository owner
            repo: Repository name
            pr_number: Pull request number

        Returns:
            PullRequest model with all related data
        """
        logger.info(f"Fetching PR #{pr_number} from {owner}/{repo}")
        try:
            repository = self.github.get_repo(f"{owner}/{repo}")
            github_pr = repository.get_pull(pr_number)

            # Convert GitHub PR to our model
            pr = self._convert_github_pr(github_pr, owner, repo)

            # Fetch additional data
            pr.files = self._get_pr_files(github_pr)
            pr.comments = self._get_pr_comments(github_pr)
            pr.reviews = self._get_pr_reviews(github_pr)

            logger.info(f"Successfully fetched PR #{pr_number} from {owner}/{repo}")
            return pr

        except GithubException as e:
            logger.error(f"GitHub API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching PR: {e}")
            raise

    def _convert_github_pr(
        self, github_pr: GithubPR, owner: str, repo: str
    ) -> PullRequest:
        """Convert GitHub PR object to our PullRequest model"""
        user = GitHubUser(
            login=github_pr.user.login,
            id=github_pr.user.id,
            avatar_url=github_pr.user.avatar_url,
            html_url=github_pr.user.html_url,
        )

        return PullRequest(
            number=github_pr.number,
            title=github_pr.title,
            body=github_pr.body,
            state=github_pr.state,
            user=user,
            created_at=github_pr.created_at,
            updated_at=github_pr.updated_at,
            merged_at=github_pr.merged_at,
            html_url=github_pr.html_url,
            additions=github_pr.additions,
            deletions=github_pr.deletions,
            changed_files=github_pr.changed_files,
            commits=github_pr.commits,
            repo_owner=owner,
            repo_name=repo,
        )

    def _get_pr_files(self, github_pr: GithubPR) -> List[PRFile]:
        """Fetch files changed in the pull request"""
        files = []
        try:
            for file in github_pr.get_files():
                # Limit patch size to avoid overwhelming the AI
                patch = file.patch
                if (
                    patch and len(patch) > self.config.max_diff_lines * 100
                ):  # Rough estimate
                    patch = (
                        patch[: self.config.max_diff_lines * 100] + "\n... (truncated)"
                    )

                pr_file = PRFile(
                    filename=file.filename,
                    status=file.status,
                    additions=file.additions,
                    deletions=file.deletions,
                    changes=file.changes,
                    patch=patch,
                )
                files.append(pr_file)
        except Exception as e:
            logger.warning(f"Error fetching PR files: {e}")

        return files

    def _get_pr_comments(self, github_pr: GithubPR) -> List[PRComment]:
        """Fetch comments on the pull request"""
        comments = []
        if not self.config.include_comments:
            return comments

        try:
            for comment in github_pr.get_issue_comments():
                user = GitHubUser(
                    login=comment.user.login,
                    id=comment.user.id,
                    avatar_url=comment.user.avatar_url,
                    html_url=comment.user.html_url,
                )

                pr_comment = PRComment(
                    id=comment.id,
                    user=user,
                    body=comment.body,
                    created_at=comment.created_at,
                    updated_at=comment.updated_at,
                    html_url=comment.html_url,
                )
                comments.append(pr_comment)
        except Exception as e:
            logger.warning(f"Error fetching PR comments: {e}")

        return comments

    def _get_pr_reviews(self, github_pr: GithubPR) -> List[PRReview]:
        """Fetch reviews on the pull request"""
        reviews = []
        if not self.config.include_reviews:
            return reviews

        try:
            for review in github_pr.get_reviews():
                user = GitHubUser(
                    login=review.user.login,
                    id=review.user.id,
                    avatar_url=review.user.avatar_url,
                    html_url=review.user.html_url,
                )

                pr_review = PRReview(
                    id=review.id,
                    user=user,
                    body=review.body,
                    state=review.state,
                    submitted_at=review.submitted_at,
                    html_url=review.html_url,
                )
                reviews.append(pr_review)
        except Exception as e:
            logger.warning(f"Error fetching PR reviews: {e}")

        return reviews

    def get_pull_request_summary(self, owner: str, repo: str, pr_number: int) -> str:
        """
        Fetch detailed information about a GitHub pull request.

        Args:
            owner: Repository owner/organization name
            repo: Repository name
            pr_number: Pull request number

        Returns:
            String containing formatted PR data
        """

        logger.info(f"Fetching PR data for {owner}/{repo}#{pr_number}")

        try:
            pr = self.get_pull_request(owner, repo, pr_number)

            # Format as a simple string to avoid schema issues
            result = f"""Pull Request #{pr.number}: {pr.title}
Author: {pr.user.login}
State: {pr.state}
Changes: +{pr.additions} -{pr.deletions} lines across {pr.changed_files} files

Description:
{pr.body or 'No description provided'}

Files Changed ({len(pr.files)} total):"""

            for f in pr.files[:30]:  # Limit to first 10 files
                result += (
                    f"\n- {f.filename} ({f.status}): +{f.additions} -{f.deletions}"
                )
                if f.patch:
                    result += f"\n  Patch preview: {f.patch[:500]}..."

            if pr.comments:
                result += f"\n\nComments ({len(pr.comments)} total):"
                for c in pr.comments[:30]:  # Limit to first 30 comments
                    result += f"\n- {c.user.login}: {c.body[:200]}..."

            if pr.reviews:
                result += f"\n\nReviews ({len(pr.reviews)} total):"
                for r in pr.reviews[:30]:  # Limit to first 30 reviews
                    status_emoji = {
                        "APPROVED": "✅",
                        "CHANGES_REQUESTED": "❌",
                        "COMMENTED": "💬",
                    }.get(r.state, "")
                    result += f"\n- {r.user.login} {status_emoji} {r.state}"
                    if r.body:
                        result += f": {r.body[:200]}..."

            return result

        except Exception as e:
            logger.error(f"Error fetching PR data: {e}")
            return f"Error fetching PR data: {str(e)}"
